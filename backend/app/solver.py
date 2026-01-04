import calendar
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Tuple

from ortools.sat.python import cp_model
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .constants import DEFAULT_PENALTIES, MINUTES_PER_DAY
from .models import (
    ConstraintEntry,
    MonthConfig,
    MonthlyRequirement,
    Nurse,
    NurseMonthAdjustment,
    NurseMonthStat,
    ProfessionalCategory,
    ScheduleEntry,
    Service,
    Shift,
)
from .utils import sort_nurses_by_category


@dataclass
class Slot:
    index: int
    day: int
    service_code: str
    shift_code: str
    minutes: int
    week_id: int


BASIC_BLOCKING_CODES = {"FERIAS", "DISPENSA", "FERIADO"}
SHIFT_LETTER_MAP = {}
MAX_CONSECUTIVE_WORK_DAYS = 6
MINIMUM_DAILY_REST_MINUTES = 11 * 60
FERIADO_REDUCTION_MINUTES = 8 * 60
PARTIAL_CATEGORIES = {"RV_TEMPO_PARCIAL", "CONTRATADO_TEMPO_PARCIAL"}


def _role_from_group(session: Session, group: str | None) -> str | None:
    if not group:
        return None
    normalized = group.strip().lower()
    if normalized in {"ao", "assistente_operacional", "assistente operacional"}:
        return "ASSISTENTE_OPERACIONAL"
    if normalized in {"enf", "enfermagem"}:
        return "ENFERMEIRO"
    for role in session.scalars(select(ProfessionalCategory.role)).all():
        if role and role.lower() == normalized:
            return role
    return None


def _categories_for_role(session: Session, role: str) -> List[str]:
    return list(
        session.scalars(
            select(ProfessionalCategory.name).where(
                ProfessionalCategory.role == role,
                ProfessionalCategory.is_active.is_(True),
            )
        )
    )
@dataclass(frozen=True)
class ShiftMeta:
    code: str
    shift_type: str
    start_minute: int
    end_minute: int
    minutes: int


SHIFT_LOOKUP: Dict[str, ShiftMeta] = {}


def _days_in_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def _week_id(year: int, month: int, day: int) -> int:
    return date(year, month, day).isocalendar()[1]


def _business_days(year: int, month: int) -> int:
    days = _days_in_month(year, month)
    count = 0
    for day in range(1, days + 1):
        if date(year, month, day).weekday() < 5:
            count += 1
    return count


def get_or_create_month_config(session: Session, year: int, month: int) -> MonthConfig:
    config = session.scalar(
        select(MonthConfig).where(
            MonthConfig.year == year,
            MonthConfig.month == month,
        )
    )
    if config:
        # Ensure penalties default keys exist
        penalties = {**DEFAULT_PENALTIES, **config.penalty_weights}
        config.penalty_weights = penalties
        return config
    config = MonthConfig(
        year=year,
        month=month,
        penalty_weights=DEFAULT_PENALTIES,
    )
    session.add(config)
    session.flush()
    return config


def _default_penalty(config: MonthConfig, key: str, fallback: int) -> int:
    return int(config.penalty_weights.get(key, fallback))


def _normalize_shift_letter(shift_type: str) -> str:
    if not shift_type:
        return ""
    letter = shift_type[0].upper()
    return SHIFT_LETTER_MAP.get(letter, letter)


def _shift_letters_from_code(code: str) -> str:
    if "_" not in code:
        return ""
    return code.split("_", 1)[1].upper()


def _allows_shift(constraint: str, shift_letter: str) -> bool:
    if not constraint:
        return False
    if constraint.startswith("DISPONIVEL_"):
        letters = _shift_letters_from_code(constraint)
        return shift_letter in letters
    if constraint == "DISPONIVEL":
        return True
    if constraint == "FERIADO_TRAB":
        return True
    return False


def _blocks_shift(constraint: str, shift_letter: str) -> bool:
    if not constraint:
        return False
    if constraint == "INDISPONIVEL":
        return True
    if constraint.startswith("INDISPONIVEL_"):
        letters = _shift_letters_from_code(constraint)
        return shift_letter in letters
    return False


def _resolve_constraint(nurse: Nurse, constraint: str) -> str:
    if constraint:
        return constraint
    if nurse.category in PARTIAL_CATEGORIES:
        return "INDISPONIVEL_MTLN"
    if nurse.category == "COORDENADOR":
        return "INDISPONIVEL"
    return "DISPONIVEL_MTLN"


def _rest_interval_minutes(prev_code: str, next_code: str) -> int:
    prev = SHIFT_LOOKUP.get(prev_code)
    nxt = SHIFT_LOOKUP.get(next_code)
    if not prev or not nxt:
        return MINUTES_PER_DAY
    prev_end_mod = prev.end_minute % MINUTES_PER_DAY
    minutes_to_midnight = (MINUTES_PER_DAY - prev_end_mod) % MINUTES_PER_DAY
    interval = minutes_to_midnight + (nxt.start_minute % MINUTES_PER_DAY)
    return interval


def refresh_shift_lookup(session: Session) -> None:
    global SHIFT_LOOKUP
    shift_map: Dict[str, ShiftMeta] = {}
    for shift in session.scalars(select(Shift)):
        end = shift.end_minute
        start = shift.start_minute
        minutes = end - start if end > start else MINUTES_PER_DAY - start + end
        shift_map[shift.code] = ShiftMeta(
            code=shift.code,
            shift_type=shift.shift_type,
            start_minute=start,
            end_minute=end,
            minutes=minutes,
        )
    SHIFT_LOOKUP = shift_map


def _has_minimum_rest(prev_code: str, next_code: str, minimum: int) -> bool:
    if not prev_code or not next_code:
        return True
    return _rest_interval_minutes(prev_code, next_code) >= minimum


def _contracted_target_minutes(
    nurse: Nurse,
    year: int,
    month: int,
    constraint_map: Dict[Tuple[int, int], str],
    adjustment: Optional[NurseMonthAdjustment],
) -> Optional[int]:
    if not nurse.weekly_hours:
        return None
    weekly_hours = nurse.weekly_hours
    daily_minutes = (weekly_hours / 5) * 60
    base_minutes = int(_business_days(year, month) * daily_minutes)
    vacation_days = sum(
        1
        for (nurse_id, day), code in constraint_map.items()
        if nurse_id == nurse.id and code == "FERIAS"
    )
    vacation_minutes = int(vacation_days * daily_minutes)
    legacy_holiday_days = sum(
        1
        for (nurse_id, day), code in constraint_map.items()
        if nurse_id == nurse.id and code == "FERIADO_TRAB"
    )
    holiday_worked_minutes = int(legacy_holiday_days * daily_minutes)
    if adjustment:
        holiday_worked_minutes += adjustment.feriados_trabalhados * FERIADO_REDUCTION_MINUTES
    target = max(0, base_minutes - vacation_minutes - holiday_worked_minutes)
    return target


def _static_eligibility(
    nurse: Nurse,
    slot: Slot,
    constraint: str,
    locked_days: Dict[Tuple[int, int], bool],
    pedidos_hard: bool,
) -> Tuple[bool, str, bool]:
    """
    Returns tuple (eligible, reason_when_false, pedido_penalty).
    pedido_penalty -> True if assignment violates pedido (soft).
    """
    if nurse.category == "COORDENADOR":
        return False, "Coordenador fora do solver", False
    if locked_days.get((nurse.id, slot.day)):
        return False, "Célula bloqueada/lock", False
    if nurse.services_permitted and slot.shift_code not in nurse.services_permitted:
        return False, "Serviço/turno não permitido", False

    constraint = _resolve_constraint(nurse, constraint)

    if constraint in BASIC_BLOCKING_CODES:
        return False, f"Restrição {constraint}", False

    if slot.shift_code not in SHIFT_LOOKUP:
        return False, "Turno desconhecido", False

    shift_meta = SHIFT_LOOKUP[slot.shift_code]
    shift_letter = _normalize_shift_letter(shift_meta.shift_type)
    if shift_meta.shift_type == "N" and not nurse.can_work_night:
        return False, "Não autorizado para noites", False

    if _blocks_shift(constraint, shift_letter):
        return False, "Indisponível para este turno", False

    if constraint.startswith("DISPONIVEL_") and not _allows_shift(
        constraint, shift_letter
    ):
        return False, "Disponível para outro turno", False

    if nurse.category in PARTIAL_CATEGORIES:
        if not _allows_shift(constraint, shift_letter):
            return False, "Parcial sem disponibilidade", False
    elif nurse.category == "RV_TEMPO_INTEIRO":
        if _blocks_shift(constraint, shift_letter):
            return False, "Indisponível", False

    if constraint in {"PEDIDO_FOLGA", "PEDIDO_DESCANSO", "PEDIDO_DESCANSO_FOLGA"}:
        return False, "Pedido (hard)", False

    return True, "", False


def _allows_double_shift(nurse: Nurse, first_type: str, second_type: str) -> bool:
    if not first_type or not second_type:
        return False
    if first_type == second_type:
        return False
    pair = {first_type, second_type}
    if nurse.category in {"ASSISTENTE_OPERACIONAL", "CONTRATADO"} or (
        nurse.category and nurse.category.startswith("CONTRATADO")
    ):
        return pair == {"M", "T"}
    return True


def _shift_intervals(meta: ShiftMeta) -> List[Tuple[int, int]]:
    if meta.end_minute > meta.start_minute:
        return [(meta.start_minute, meta.end_minute)]
    return [(meta.start_minute, MINUTES_PER_DAY), (0, meta.end_minute)]


def _shifts_overlap(first: ShiftMeta, second: ShiftMeta) -> bool:
    for start_a, end_a in _shift_intervals(first):
        for start_b, end_b in _shift_intervals(second):
            if start_a < end_b and start_b < end_a:
                return True
    return False


def _insert_rest_entries(
    session: Session, assignments: List[ScheduleEntry], year: int, month: int
) -> None:
    days = _days_in_month(year, month)
    for entry in assignments:
        shift_meta = SHIFT_LOOKUP.get(entry.shift_code)
        if not shift_meta or shift_meta.shift_type != "N":
            continue
        next_day = entry.day + 1
        if next_day > days:
            continue
        existing = session.scalar(
            select(ScheduleEntry).where(
                ScheduleEntry.year == year,
                ScheduleEntry.month == month,
                ScheduleEntry.day == next_day,
                ScheduleEntry.nurse_id == entry.nurse_id,
            )
        )
        if existing:
            continue
        rest_entry = ScheduleEntry(
            nurse_id=entry.nurse_id,
            year=year,
            month=month,
            day=next_day,
            service_code="REST",
            shift_code="D",
            locked=False,
            source="auto_rest",
        )
        session.add(rest_entry)


def _folga_after_nd_violations(
    assignments: List[ScheduleEntry],
    nurses: List[Nurse],
    year: int,
    month: int,
) -> List[str]:
    days_in_month = _days_in_month(year, month)
    by_nurse_day: Dict[Tuple[int, int], ScheduleEntry] = {
        (entry.nurse_id, entry.day): entry for entry in assignments
    }
    nurse_names = {nurse.id: nurse.name for nurse in nurses}
    warnings: List[str] = []
    for entry in assignments:
        shift_meta = SHIFT_LOOKUP.get(entry.shift_code)
        if not shift_meta or shift_meta.shift_type != "N":
            continue
        check_day = entry.day + 2
        if check_day > days_in_month:
            continue
        next_entry = by_nurse_day.get((entry.nurse_id, check_day))
        if next_entry and next_entry.service_code != "REST":
            nurse_name = nurse_names.get(entry.nurse_id, f"ID {entry.nurse_id}")
            warnings.append(
                f"Sem folga após sequência N+D (dia {entry.day}): {nurse_name}"
            )
    return warnings


def generate_schedule(session: Session, year: int, month: int, group: str | None = None):
    refresh_shift_lookup(session)
    config = get_or_create_month_config(session, year, month)
    service_roles = {
        service.code: service.role for service in session.scalars(select(Service))
    }
    nurse_query = select(Nurse)
    role = _role_from_group(session, group)
    if role:
        categories = _categories_for_role(session, role)
        if categories:
            nurse_query = nurse_query.where(Nurse.category.in_(categories))
        else:
            nurse_query = nurse_query.where(Nurse.category == role)
    nurses: List[Nurse] = sort_nurses_by_category(list(session.scalars(nurse_query)))
    nurse_ids = [nurse.id for nurse in nurses]
    service_codes = []
    if role:
        service_codes = list(
            session.scalars(select(Service.code).where(Service.role == role))
        )
    requirements_query = select(MonthlyRequirement).where(
        MonthlyRequirement.year == year,
        MonthlyRequirement.month == month,
    )
    if service_codes:
        requirements_query = requirements_query.where(
            MonthlyRequirement.service_code.in_(service_codes)
        )
    requirements_query = requirements_query.order_by(
        MonthlyRequirement.day,
        MonthlyRequirement.service_code,
        MonthlyRequirement.shift_code,
    )
    requirements: List[MonthlyRequirement] = list(session.scalars(requirements_query))
    constraints_query = select(ConstraintEntry).where(
        ConstraintEntry.year == year,
        ConstraintEntry.month == month,
    )
    if nurse_ids:
        constraints_query = constraints_query.where(
            ConstraintEntry.nurse_id.in_(nurse_ids)
        )
    constraints: List[ConstraintEntry] = list(session.scalars(constraints_query))
    constraint_map: Dict[Tuple[int, int], str] = {
        (item.nurse_id, item.day): item.code for item in constraints
    }

    adjustments_query = select(NurseMonthAdjustment).where(
        NurseMonthAdjustment.year == year,
        NurseMonthAdjustment.month == month,
    )
    if nurse_ids:
        adjustments_query = adjustments_query.where(
            NurseMonthAdjustment.nurse_id.in_(nurse_ids)
        )
    adjustments: List[NurseMonthAdjustment] = list(session.scalars(adjustments_query))
    adjustment_map: Dict[int, NurseMonthAdjustment] = {
        item.nurse_id: item for item in adjustments
    }

    locked_query = select(ScheduleEntry).where(
        ScheduleEntry.year == year,
        ScheduleEntry.month == month,
        ScheduleEntry.locked.is_(True),
    )
    if nurse_ids:
        locked_query = locked_query.where(ScheduleEntry.nurse_id.in_(nurse_ids))
    locked_entries: List[ScheduleEntry] = list(session.scalars(locked_query))
    locked_violations: List[str] = []
    if locked_entries:
        grouped_locked: Dict[Tuple[int, int], List[ScheduleEntry]] = defaultdict(list)
        for entry in locked_entries:
            grouped_locked[(entry.nurse_id, entry.day)].append(entry)
        invalid_locked_keys: set[Tuple[int, int]] = set()
        for (nurse_id, day), entries in grouped_locked.items():
            if len(entries) < 2:
                continue
            nurse = next((item for item in nurses if item.id == nurse_id), None)
            if not nurse:
                continue
            codes = [item.shift_code for item in entries]
            metas = [SHIFT_LOOKUP.get(code) for code in codes]
            invalid = False
            for idx, first_meta in enumerate(metas):
                for jdx in range(idx + 1, len(metas)):
                    second_meta = metas[jdx]
                    if not first_meta or not second_meta:
                        invalid = True
                        continue
                    if first_meta.shift_type == second_meta.shift_type:
                        invalid = True
                        continue
                    if _shifts_overlap(first_meta, second_meta):
                        invalid = True
                        continue
                    if not _allows_double_shift(
                        nurse, first_meta.shift_type, second_meta.shift_type
                    ):
                        invalid = True
            if invalid:
                invalid_locked_keys.add((nurse_id, day))
                locked_violations.append(
                    f"Dia {day} {nurse.name}: turnos bloqueados removidos"
                )
        if invalid_locked_keys:
            for nurse_id, day in invalid_locked_keys:
                session.execute(
                    delete(ScheduleEntry).where(
                        ScheduleEntry.year == year,
                        ScheduleEntry.month == month,
                        ScheduleEntry.day == day,
                        ScheduleEntry.nurse_id == nurse_id,
                        ScheduleEntry.locked.is_(True),
                    )
                )
            locked_entries = [
                entry
                for entry in locked_entries
                if (entry.nurse_id, entry.day) not in invalid_locked_keys
            ]

    # Remove previous auto assignments (including rest placeholders).
    delete_query = delete(ScheduleEntry).where(
        ScheduleEntry.year == year,
        ScheduleEntry.month == month,
        ScheduleEntry.locked.is_(False),
    )
    if nurse_ids:
        delete_query = delete_query.where(ScheduleEntry.nurse_id.in_(nurse_ids))
    session.execute(delete_query)

    locked_counts: Dict[Tuple[int, str, str], int] = defaultdict(int)
    locked_days: Dict[Tuple[int, int], bool] = {}
    locked_shift_map: Dict[Tuple[int, int], str] = {}
    locked_week_minutes: Dict[Tuple[int, int], int] = defaultdict(int)
    locked_month_minutes: Dict[int, int] = defaultdict(int)
    locked_type_counts: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    days = _days_in_month(year, month)

    for entry in locked_entries:
        locked_counts[(entry.day, entry.service_code, entry.shift_code)] += 1
        locked_days[(entry.nurse_id, entry.day)] = True
        locked_shift_map[(entry.nurse_id, entry.day)] = entry.shift_code
        shift_meta = SHIFT_LOOKUP.get(entry.shift_code)
        minutes = shift_meta.minutes if shift_meta else 0
        week_id = _week_id(year, month, entry.day)
        locked_week_minutes[(entry.nurse_id, week_id)] += minutes
        locked_month_minutes[entry.nurse_id] += minutes
        if shift_meta and shift_meta.shift_type:
            locked_type_counts[entry.nurse_id][shift_meta.shift_type] += 1

    slots: List[Slot] = []
    slots_by_day: Dict[int, List[Slot]] = defaultdict(list)
    slot_idx = 0
    sap_long_days = {
        req.day
        for req in requirements
        if req.service_code == "TLs" and req.required_count > 0
    }
    for req in requirements:
        shift_meta = SHIFT_LOOKUP.get(req.shift_code)
        if not shift_meta:
            continue
        if req.service_code in {"Ts", "Ls"} and req.day in sap_long_days:
            continue
        remaining = req.required_count - locked_counts[
            (req.day, req.service_code, req.shift_code)
        ]
        if remaining <= 0:
            continue
        for _ in range(remaining):
            slot = Slot(
                index=slot_idx,
                day=req.day,
                service_code=req.service_code,
                shift_code=req.shift_code,
                minutes=shift_meta.minutes,
                week_id=_week_id(year, month, req.day),
            )
            slots.append(slot)
            slots_by_day[req.day].append(slot)
            slot_idx += 1

    slot_candidate_vars: Dict[int, List[Tuple[int, cp_model.IntVar]]] = defaultdict(list)
    candidate_lookup: Dict[Tuple[int, int], cp_model.IntVar] = {}
    slot_candidate_meta: Dict[Tuple[int, int], Dict[str, int]] = {}
    slot_unfilled_vars: Dict[int, cp_model.IntVar] = {}
    slot_reason_counts: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    unfilled_report: List[Dict[str, str]] = []

    model = cp_model.CpModel()
    pedido_penalty_vars: List[cp_model.IntVar] = []
    objective_terms: List[cp_model.LinearExpr] = []

    days_range = range(1, days + 1)

    # Build decision variables for each slot/nurse pair.
    for slot in slots:
        slot_candidates = []
        for nurse in nurses:
            constraint = constraint_map.get((nurse.id, slot.day), "")
            eligible, reason, pedido_flag = _static_eligibility(
                nurse,
                slot,
                constraint,
                locked_days,
                config.pedidos_folga_hard,
            )
            if not eligible:
                if reason:
                    slot_reason_counts[slot.index][reason] += 1
                continue
            var = model.NewBoolVar(f"x_{slot.index}_{nurse.id}")
            slot_candidates.append((nurse.id, var))
            candidate_lookup[(slot.index, nurse.id)] = var
            slot_candidate_meta[(slot.index, nurse.id)] = {
                "category_penalty": 0 if nurse.category == "RV_TEMPO_PARCIAL" else 1,
            }
            if pedido_flag:
                pedido_penalty_vars.append(var)

        if not slot_candidates:
            unfilled_report.append(
                {
                    "day": slot.day,
                    "service_code": slot.service_code,
                    "shift_code": slot.shift_code,
                    "reason": "Sem enfermeiros elegíveis (restrições hard)",
                }
            )
            continue

        assignment_sum = sum(var for _, var in slot_candidates)
        unfilled_var = model.NewBoolVar(f"slot_{slot.index}_unfilled")
        slot_unfilled_vars[slot.index] = unfilled_var
        model.Add(assignment_sum + unfilled_var == 1)
        slot_candidate_vars[slot.index] = slot_candidates

    # No slots to process -> return early (only locked entries exist)
    if not slot_candidate_vars and not unfilled_report:
        assignments = locked_entries
        _update_hour_balances(
            session,
            nurses,
            assignments,
            year,
            month,
            constraint_map,
            adjustment_map,
        )
        stats = collect_nurse_stats(session, nurses, year, month)
        return assignments, [], [], stats

    min_rest_minutes = (config.min_rest_hours or 11) * 60

    # Enforce minimum rest between consecutive days.
    double_mismatch_penalty = _default_penalty(
        config, "double_service_mismatch", 40
    )

    for nurse in nurses:
        for day in range(1, days):
            slots_today = slots_by_day.get(day, [])
            slots_next = slots_by_day.get(day + 1, [])
            if not slots_today or not slots_next:
                continue
            for slot_today in slots_today:
                var_today = candidate_lookup.get((slot_today.index, nurse.id))
                if var_today is None:
                    continue
                for slot_next in slots_next:
                    if _has_minimum_rest(
                        slot_today.shift_code,
                        slot_next.shift_code,
                        min_rest_minutes,
                    ):
                        continue
                    var_next = candidate_lookup.get((slot_next.index, nurse.id))
                    if var_next is None:
                        continue
                    model.Add(var_today + var_next <= 1)

    # Ensure per-day assignments limit.
    day_assign_vars: Dict[Tuple[int, int], cp_model.IntVar] = {}
    night_assign_vars: Dict[Tuple[int, int], cp_model.IntVar] = {}
    locked_night_count: Dict[int, int] = defaultdict(int)
    for entry in locked_entries:
        shift_meta = SHIFT_LOOKUP.get(entry.shift_code)
        if shift_meta and shift_meta.shift_type == "N":
            locked_night_count[entry.nurse_id] += 1

    for nurse in nurses:
        for day in days_range:
            if locked_days.get((nurse.id, day)):
                day_assign_vars[(nurse.id, day)] = None
                night_assign_vars[(nurse.id, day)] = None
                continue
            vars_for_day: List[Tuple[cp_model.IntVar, Slot, ShiftMeta]] = []
            night_vars_for_day: List[cp_model.IntVar] = []
            for slot in slots_by_day.get(day, []):
                var = candidate_lookup.get((slot.index, nurse.id))
                if var is None:
                    continue
                shift_meta = SHIFT_LOOKUP.get(slot.shift_code)
                if not shift_meta:
                    continue
                vars_for_day.append((var, slot, shift_meta))
                if shift_meta.shift_type == "N":
                    night_vars_for_day.append(var)

            if vars_for_day:
                assign_var = model.NewBoolVar(f"assign_{nurse.id}_{day}")
                day_expr = sum(var for var, _, _ in vars_for_day)
                max_per_day = 2
                model.Add(day_expr <= max_per_day)
                model.Add(day_expr >= assign_var)
                model.Add(day_expr <= assign_var * max_per_day)
                day_assign_vars[(nurse.id, day)] = assign_var

                # Block invalid double-shift combos per nurse.
                for idx, (first_var, first_slot, first_meta) in enumerate(
                    vars_for_day
                ):
                    for jdx in range(idx + 1, len(vars_for_day)):
                        second_var, second_slot, second_meta = vars_for_day[jdx]
                        if _shifts_overlap(first_meta, second_meta):
                            model.Add(first_var + second_var <= 1)
                            continue
                        if not _allows_double_shift(
                            nurse, first_meta.shift_type, second_meta.shift_type
                        ):
                            model.Add(first_var + second_var <= 1)
                        elif (
                            double_mismatch_penalty > 0
                            and first_slot.service_code != second_slot.service_code
                        ):
                            mismatch_var = model.NewBoolVar(
                                f"double_mismatch_{nurse.id}_{day}_{idx}_{jdx}"
                            )
                            model.Add(mismatch_var >= first_var + second_var - 1)
                            model.Add(mismatch_var <= first_var)
                            model.Add(mismatch_var <= second_var)
                            objective_terms.append(
                                mismatch_var * double_mismatch_penalty
                            )
            else:
                day_assign_vars[(nurse.id, day)] = None

            if night_vars_for_day:
                night_var = model.NewBoolVar(f"night_{nurse.id}_{day}")
                night_expr = sum(night_vars_for_day)
                model.Add(night_var == night_expr)
                night_assign_vars[(nurse.id, day)] = night_var
            else:
                night_assign_vars[(nurse.id, day)] = None

    rest_penalty = _default_penalty(config, "rest_followup", 80)
    if not config.prefer_folga_after_nd:
        rest_penalty = 0
    night_seq_penalty = _default_penalty(config, "night_sequence", 120)

    # Max consecutive work days (6)
    window_length = MAX_CONSECUTIVE_WORK_DAYS + 1
    weekend_pairs = []
    for week in calendar.monthcalendar(year, month):
        saturday = week[calendar.SATURDAY]
        sunday = week[calendar.SUNDAY]
        if saturday and sunday:
            weekend_pairs.append((saturday, sunday))

    for nurse in nurses:
        for day in range(1, days):
            night_today = night_assign_vars.get((nurse.id, day))
            next_day_assign = day_assign_vars.get((nurse.id, day + 1))
            if night_today is not None or next_day_assign is not None:
                expr = 0
                if night_today is not None:
                    expr += night_today
                if next_day_assign is not None:
                    expr += next_day_assign
                model.Add(expr <= 1)

            next_night = night_assign_vars.get((nurse.id, day + 1))
            if (
                night_seq_penalty > 0
                and night_today is not None
                and next_night is not None
            ):
                seq_var = model.NewBoolVar(f"night_seq_{nurse.id}_{day}")
                model.Add(seq_var >= night_today + next_night - 1)
                model.Add(seq_var <= night_today)
                model.Add(seq_var <= next_night)
                objective_terms.append(seq_var * night_seq_penalty)

            if day + 2 <= days:
                next_day_assign = day_assign_vars.get((nurse.id, day + 1))
                next_night = night_assign_vars.get((nurse.id, day + 1))
                folga_day = day_assign_vars.get((nurse.id, day + 2))
                if (
                    night_today is not None
                    and next_day_assign is not None
                    and folga_day is not None
                ):
                    non_night_next = model.NewBoolVar(
                        f"non_night_{nurse.id}_{day + 1}"
                    )
                    if next_night is None:
                        model.Add(non_night_next == next_day_assign)
                    else:
                        model.Add(non_night_next <= next_day_assign)
                        model.Add(non_night_next <= 1 - next_night)
                        model.Add(non_night_next >= next_day_assign - next_night)
                    model.Add(folga_day == 0).OnlyEnforceIf(
                        [night_today, non_night_next]
                    )
                    if rest_penalty > 0:
                        rest_var = model.NewBoolVar(
                            f"rest_followup_{nurse.id}_{day}"
                        )
                        model.Add(
                            rest_var >= night_today + non_night_next + folga_day - 2
                        )
                        model.Add(rest_var <= night_today)
                        model.Add(rest_var <= non_night_next)
                        model.Add(rest_var <= folga_day)
                        objective_terms.append(rest_var * rest_penalty)

        if nurse.max_noites_mes:
            night_vars = []
            for day in days_range:
                var = night_assign_vars.get((nurse.id, day))
                if var is not None:
                    night_vars.append(var)
            if night_vars:
                model.Add(
                    sum(night_vars) + locked_night_count.get(nurse.id, 0)
                    <= nurse.max_noites_mes
                )

        for start_day in range(1, max(1, days - window_length + 2)):
            vars_window: List[cp_model.IntVar] = []
            locked_count = 0
            for offset in range(window_length):
                day = start_day + offset
                if day > days:
                    continue
                var = day_assign_vars.get((nurse.id, day))
                if var is not None:
                    vars_window.append(var)
                elif locked_shift_map.get((nurse.id, day)) and locked_shift_map[
                    (nurse.id, day)
                ] != "REST":
                    locked_count += 1
            if not vars_window and locked_count == 0:
                continue
            rhs = MAX_CONSECUTIVE_WORK_DAYS - locked_count
            if rhs < 0:
                rhs = 0
            if vars_window:
                model.Add(sum(vars_window) <= rhs)

        if weekend_pairs:
            weekend_off_vars = []
            for saturday, sunday in weekend_pairs:
                sat_assign = day_assign_vars.get((nurse.id, saturday))
                sun_assign = day_assign_vars.get((nurse.id, sunday))
                if sat_assign is None or sun_assign is None:
                    continue
                off_var = model.NewBoolVar(
                    f"weekend_off_{nurse.id}_{saturday}_{sunday}"
                )
                model.Add(off_var <= 1 - sat_assign)
                model.Add(off_var <= 1 - sun_assign)
                model.Add(off_var >= 1 - sat_assign - sun_assign)
                weekend_off_vars.append(off_var)
            if weekend_off_vars:
                model.Add(sum(weekend_off_vars) >= 1)

    # Weekly hours / fairness constraints.
    week_ids = sorted({slot.week_id for slot in slots})
    for nurse in nurses:
        for week_id in week_ids:
            week_terms = []
            for slot in slots:
                if slot.week_id != week_id:
                    continue
                var = candidate_lookup.get((slot.index, nurse.id))
                if var is None:
                    continue
                week_terms.append(var * slot.minutes)
            if not week_terms and locked_week_minutes.get((nurse.id, week_id), 0) == 0:
                continue
            week_expr = sum(week_terms) if week_terms else 0
            locked_minutes = locked_week_minutes.get((nurse.id, week_id), 0)
            if locked_minutes:
                week_expr = week_expr + locked_minutes
            weekly_target = nurse.weekly_hours or config.target_hours_week
            target_minutes = weekly_target * 60
            diff = model.NewIntVar(0, 24000, f"weekdiff_{nurse.id}_{week_id}")
            model.Add(diff >= week_expr - target_minutes)
            model.Add(diff >= target_minutes - week_expr)
            objective_terms.append(diff * _default_penalty(config, "hours_target", 5))
            if nurse.category == "CONTRATADO":
                max_minutes = max(config.max_hours_week_contratado, weekly_target) * 60
                model.Add(week_expr <= max_minutes)

    bank_balance_weight = _default_penalty(config, "bank_balance", 2)
    if bank_balance_weight:
        average_bank = (
            int(
                sum((nurse.hour_balance_minutes or 0) for nurse in nurses)
                / len(nurses)
            )
            if nurses
            else 0
        )
        for nurse in nurses:
            desired_delta = average_bank - (nurse.hour_balance_minutes or 0)
            target = _contracted_target_minutes(
                nurse,
                year,
                month,
                constraint_map,
                adjustment_map.get(nurse.id),
            )
            if target is None:
                target = 0
            adjustment = adjustment_map.get(nurse.id)
            adjustment_minutes = 0
            if adjustment:
                adjustment_minutes += adjustment.extra_minutes
                adjustment_minutes -= adjustment.reduced_minutes
            month_terms = []
            for slot in slots:
                var = candidate_lookup.get((slot.index, nurse.id))
                if var is None:
                    continue
                month_terms.append(var * slot.minutes)
            month_expr = sum(month_terms) if month_terms else 0
            locked_minutes = locked_month_minutes.get(nurse.id, 0)
            if locked_minutes:
                month_expr = month_expr + locked_minutes
            if adjustment_minutes:
                month_expr = month_expr + adjustment_minutes
            delta_expr = month_expr - target
            diff = model.NewIntVar(0, 100000, f"bankdiff_{nurse.id}")
            model.Add(diff >= delta_expr - desired_delta)
            model.Add(diff >= desired_delta - delta_expr)
            objective_terms.append(diff * bank_balance_weight)

    pedido_penalty_weight = _default_penalty(config, "pedido", 300)
    unfilled_penalty_weight = _default_penalty(config, "unfilled", 5000)

    for var in pedido_penalty_vars:
        objective_terms.append(var * pedido_penalty_weight)

    for slot_idx, var in slot_unfilled_vars.items():
        objective_terms.append(var * unfilled_penalty_weight)

    for (slot_idx, nurse_id), meta in slot_candidate_meta.items():
        penalty = meta.get("category_penalty", 0)
        if not penalty:
            continue
        var = candidate_lookup.get((slot_idx, nurse_id))
        if var is not None:
            objective_terms.append(var * penalty)

    shift_balance_weight = _default_penalty(config, "shift_balance", 4)
    if shift_balance_weight and nurses:
        normalized_group = (group or "").strip().lower()
        role_hint = None
        if normalized_group in {"ao", "assistente_operacional"}:
            role_hint = "ASSISTENTE_OPERACIONAL"
        elif normalized_group in {"enf", "enfermagem"}:
            role_hint = "ENFERMEIRO"

        slot_roles: Dict[int, str] = {}
        totals_by_role: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        slots_by_role_type: Dict[str, Dict[str, List[int]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for slot in slots:
            shift_meta = SHIFT_LOOKUP.get(slot.shift_code)
            if not shift_meta or not shift_meta.shift_type:
                continue
            slot_role = (
                role_hint
                or service_roles.get(slot.service_code)
                or "ENFERMEIRO"
            )
            slot_roles[slot.index] = slot_role
            totals_by_role[slot_role][shift_meta.shift_type] += 1
            slots_by_role_type[slot_role][shift_meta.shift_type].append(slot.index)

        for slot_role, total_by_type in totals_by_role.items():
            group_nurses = [
                nurse
                for nurse in nurses
                if (slot_role == "ASSISTENTE_OPERACIONAL")
                == (nurse.category == "ASSISTENTE_OPERACIONAL")
            ]
            if not group_nurses:
                continue
            nurse_count = len(group_nurses)
            for shift_type in ("M", "T", "N"):
                total = total_by_type.get(shift_type, 0)
                if total == 0:
                    continue
                target = int(round(total / nurse_count))
                slot_indexes = slots_by_role_type[slot_role][shift_type]
                for nurse in group_nurses:
                    terms = []
                    for slot_idx in slot_indexes:
                        var = candidate_lookup.get((slot_idx, nurse.id))
                        if var is None:
                            continue
                        terms.append(var)
                    count_expr = sum(terms) if terms else 0
                    locked_count = locked_type_counts.get(nurse.id, {}).get(
                        shift_type, 0
                    )
                    if locked_count:
                        count_expr = count_expr + locked_count
                    diff = model.NewIntVar(
                        0, 1000, f"typebal_{slot_role}_{shift_type}_{nurse.id}"
                    )
                    model.Add(diff >= count_expr - target)
                    model.Add(diff >= target - count_expr)
                    objective_terms.append(diff * shift_balance_weight)

    if objective_terms:
        model.Minimize(sum(objective_terms))
    else:
        model.Minimize(0)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 20
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _fallback_greedy(
            session,
            nurses,
            requirements,
            constraint_map,
            locked_entries,
            year,
            month,
            config,
            adjustment_map,
        )

    created_entries: List[ScheduleEntry] = []
    for slot in slots:
        pair_list = slot_candidate_vars.get(slot.index)
        if not pair_list:
            continue
        assigned_nurse = None
        for nurse_id, var in pair_list:
            if solver.Value(var) == 1:
                assigned_nurse = nurse_id
                break
        if assigned_nurse is None:
            unfilled_var = slot_unfilled_vars.get(slot.index)
            if unfilled_var is not None and solver.Value(unfilled_var) == 1:
                reason_counts = slot_reason_counts.get(slot.index, {})
                reason = "Limitações globais"
                if reason_counts:
                    reason = f"Elegíveis insuficientes ({max(reason_counts.items(), key=lambda item: item[1])[0]})"
                unfilled_report.append(
                    {
                        "day": slot.day,
                        "service_code": slot.service_code,
                        "shift_code": slot.shift_code,
                        "reason": reason,
                    }
                )
            continue
        entry = ScheduleEntry(
            nurse_id=assigned_nurse,
            year=year,
            month=month,
            day=slot.day,
            service_code=slot.service_code,
            shift_code=slot.shift_code,
            locked=False,
            source="auto",
        )
        session.add(entry)
        created_entries.append(entry)

    session.flush()
    _insert_rest_entries(session, created_entries, year, month)
    session.flush()

    assignments: List[ScheduleEntry] = list(
        session.scalars(
            select(ScheduleEntry).where(
                ScheduleEntry.year == year,
                ScheduleEntry.month == month,
            )
        )
    )

    violations = [
        f"Dia {item['day']} {item['service_code']}/{item['shift_code']}: {item['reason']}"
        for item in unfilled_report
    ]
    if config.prefer_folga_after_nd:
        violations.extend(_folga_after_nd_violations(assignments, nurses, year, month))
    if locked_violations:
        violations.extend(locked_violations)

    _update_hour_balances(
        session,
        nurses,
        assignments,
        year,
        month,
        constraint_map,
        adjustment_map,
    )

    stats = collect_nurse_stats(session, nurses, year, month)

    return assignments, unfilled_report, violations, stats


def _fallback_greedy(
    session: Session,
    nurses: List[Nurse],
    requirements: List[MonthlyRequirement],
    constraint_map: Dict[Tuple[int, int], str],
    locked_entries: List[ScheduleEntry],
    year: int,
    month: int,
    config: MonthConfig,
    adjustment_map: Dict[int, NurseMonthAdjustment],
):
    locked_counts: Dict[Tuple[int, str, str], int] = defaultdict(int)
    locked_days = {(entry.nurse_id, entry.day): True for entry in locked_entries}

    for entry in locked_entries:
        locked_counts[(entry.day, entry.service_code, entry.shift_code)] += 1

    assignments_total: Dict[int, int] = defaultdict(int)
    for entry in locked_entries:
        assignments_total[entry.nurse_id] += 1

    assigned_days: Dict[Tuple[int, int], bool] = dict(locked_days)
    created_entries: List[ScheduleEntry] = []
    unfilled: List[Dict[str, str]] = []

    for req in requirements:
        remaining = req.required_count - locked_counts[
            (req.day, req.service_code, req.shift_code)
        ]
        if remaining <= 0:
            continue
        shift_meta = SHIFT_LOOKUP.get(req.shift_code)
        if not shift_meta:
            continue

        for _ in range(remaining):
            best = None
            for nurse in nurses:
                constraint = constraint_map.get((nurse.id, req.day), "")
                eligible, _, pedido_flag = _static_eligibility(
                    nurse, Slot(0, req.day, req.service_code, req.shift_code, 0, 0), constraint, locked_days, config.pedidos_folga_hard
                )
                if not eligible:
                    continue
                if assigned_days.get((nurse.id, req.day)):
                    continue
                weight = 1 if pedido_flag else 0
                score = (weight, assignments_total[nurse.id], nurse.id)
                if best is None or score < best[0]:
                    best = (score, nurse)

            if not best:
                unfilled.append(
                    {
                        "day": req.day,
                        "service_code": req.service_code,
                        "shift_code": req.shift_code,
                        "reason": "Sem enfermeiros elegíveis (fallback)",
                    }
                )
                continue

            selected = best[1]
            entry = ScheduleEntry(
                nurse_id=selected.id,
                year=year,
                month=month,
                day=req.day,
                service_code=req.service_code,
                shift_code=req.shift_code,
                locked=False,
                source="auto",
            )
            session.add(entry)
            created_entries.append(entry)
            assignments_total[selected.id] += 1
            assigned_days[(selected.id, req.day)] = True

    session.flush()
    _insert_rest_entries(session, created_entries, year, month)
    session.flush()

    assignments: List[ScheduleEntry] = list(
        session.scalars(
            select(ScheduleEntry).where(
                ScheduleEntry.year == year,
                ScheduleEntry.month == month,
            )
        )
    )

    violations = [
        f"Dia {item['day']} {item['service_code']}/{item['shift_code']}: {item['reason']}"
        for item in unfilled
    ]
    if config.prefer_folga_after_nd:
        violations.extend(_folga_after_nd_violations(assignments, nurses, year, month))

    _update_hour_balances(
        session,
        nurses,
        assignments,
        year,
        month,
        constraint_map,
        adjustment_map,
    )

    stats = collect_nurse_stats(session, nurses, year, month)

    return assignments, unfilled, violations, stats


def _update_hour_balances(
    session: Session,
    nurses: List[Nurse],
    assignments: List[ScheduleEntry],
    year: int,
    month: int,
    constraint_map: Dict[Tuple[int, int], str],
    adjustment_map: Dict[int, NurseMonthAdjustment],
):
    actual_minutes: Dict[int, int] = defaultdict(int)
    for entry in assignments:
        if entry.service_code == "REST":
            continue
        shift_meta = SHIFT_LOOKUP.get(entry.shift_code)
        if not shift_meta:
            continue
        actual_minutes[entry.nurse_id] += shift_meta.minutes

    for nurse in nurses:
        target = _contracted_target_minutes(
            nurse,
            year,
            month,
            constraint_map,
            adjustment_map.get(nurse.id),
        )
        if target is None:
            target = 0
        actual = actual_minutes.get(nurse.id, 0)
        adjustment = adjustment_map.get(nurse.id)
        if adjustment:
            actual += adjustment.extra_minutes
            actual -= adjustment.reduced_minutes
        delta = actual - target
        stat = session.scalar(
            select(NurseMonthStat).where(
                NurseMonthStat.nurse_id == nurse.id,
                NurseMonthStat.year == year,
                NurseMonthStat.month == month,
            )
        )
        if stat:
            nurse.hour_balance_minutes -= stat.delta_minutes
            stat.target_minutes = target
            stat.actual_minutes = actual
            stat.delta_minutes = delta
        else:
            stat = NurseMonthStat(
                nurse_id=nurse.id,
                year=year,
                month=month,
                target_minutes=target,
                actual_minutes=actual,
                delta_minutes=delta,
            )
        nurse.hour_balance_minutes += delta
        session.add(stat)
        session.add(nurse)


def collect_nurse_stats(
    session: Session,
    nurses: List[Nurse],
    year: int,
    month: int,
) -> List[Dict[str, int]]:
    stat_map: Dict[int, NurseMonthStat] = {
        stat.nurse_id: stat
        for stat in session.scalars(
            select(NurseMonthStat).where(
                NurseMonthStat.year == year,
                NurseMonthStat.month == month,
            )
        )
    }
    results: List[Dict[str, int]] = []
    for nurse in nurses:
        stat = stat_map.get(nurse.id)
        target = stat.target_minutes if stat else 0
        actual = stat.actual_minutes if stat else 0
        delta = stat.delta_minutes if stat else 0
        bank = nurse.hour_balance_minutes or 0
        previous_bank = bank - delta
        results.append(
            {
                "nurse_id": nurse.id,
                "target_minutes": target,
                "actual_minutes": actual,
                "delta_minutes": delta,
                "bank_minutes": bank,
                "previous_bank_minutes": previous_bank,
            }
        )
    return results
