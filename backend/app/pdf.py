import io
import calendar
import re
from datetime import datetime
from typing import Dict, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import APP_NAME, ORG_NAME
from .excel import _constraint_display, _constraint_text
from .holidays import month_holidays
from .models import (
    ConstraintEntry,
    ManualHoliday,
    MonthlyRequirement,
    Nurse,
    NurseMonthAdjustment,
    NurseMonthStat,
    ProfessionalCategory,
    ScheduleEntry,
    Service,
    ServiceShift,
    Shift,
    SwapDecision,
    SwapParticipant,
    SwapRequest,
    User,
)


APP_LOGO_SIZE = (60 * mm, 22 * mm)
ORG_LOGO_SIZE = (20 * mm, 20 * mm)
HOLIDAY_COLOR = colors.Color(1, 0.9, 0.9)
WEEKEND_COLOR = colors.Color(0.93, 0.95, 1)
GREEN_OK = colors.Color(0.86, 0.97, 0.9)
RED_BAD = colors.Color(0.99, 0.88, 0.88)


PDF_LABELS = {
    "pt": {
        "legend_code": "Código",
        "legend_service": "Serviço",
        "legend_start": "Entrada",
        "legend_end": "Saída",
        "header_service_shift": "Serviço/Turno",
        "header_professional": "Profissional",
        "header_balance": "Saldo (h)",
        "header_total_hours": "Total Horas",
        "header_current_balance": "Saldo atual",
        "header_monthly_hours": "Horas Mensais",
        "title_schedule": "Escala",
        "title_constraints": "Disponibilidades",
        "signature_coordinator": "Enf. Coordenador",
        "signature_director": "Enf. Diretor",
        "title_swap": "Comprovativo de troca",
        "label_request_id": "Pedido",
        "label_date": "Data",
        "label_status": "Estado",
        "label_created_at": "Criado em",
        "label_requester": "Pedido por",
        "label_current": "Atual",
        "label_desired": "Pretendido",
        "label_service_shift": "Serviço/Turno",
        "label_reason": "Motivo",
        "label_observations": "Observações",
        "label_participants": "Participantes",
        "label_decision": "Decisão",
        "label_exported_for": "Exportado para",
        "label_exported_at": "Exportado em",
    },
    "en": {
        "legend_code": "Code",
        "legend_service": "Service",
        "legend_start": "Start",
        "legend_end": "End",
        "header_service_shift": "Service/Shift",
        "header_professional": "Professional",
        "header_balance": "Balance (h)",
        "header_total_hours": "Total Hours",
        "header_current_balance": "Current balance",
        "header_monthly_hours": "Monthly Hours",
        "title_schedule": "Schedule",
        "title_constraints": "Availability",
        "signature_coordinator": "Nurse Coordinator",
        "signature_director": "Nurse Director",
        "title_swap": "Swap proof",
        "label_request_id": "Request",
        "label_date": "Date",
        "label_status": "Status",
        "label_created_at": "Created at",
        "label_requester": "Requested by",
        "label_current": "Current",
        "label_desired": "Desired",
        "label_service_shift": "Service/Shift",
        "label_reason": "Reason",
        "label_observations": "Observations",
        "label_participants": "Participants",
        "label_decision": "Decision",
        "label_exported_for": "Exported for",
        "label_exported_at": "Exported at",
    },
}


def _lang_key(lang: str | None) -> str:
    return "en" if lang and lang.lower().startswith("en") else "pt"


def _label(lang: str | None, key: str, fallback: str | None = None) -> str:
    return PDF_LABELS[_lang_key(lang)].get(key, fallback or key)


def _logo_reader(path: str | None):
    if not path:
        return None
    try:
        return ImageReader(path)
    except Exception:
        return None


def _build_header(app_logo: str | None, org_logo: str | None, title: str):
    styles = getSampleStyleSheet()
    title_el = Paragraph(title, styles["Title"])
    app_img = (
        Image(app_logo, width=APP_LOGO_SIZE[0], height=APP_LOGO_SIZE[1])
        if app_logo
        else ""
    )
    org_img = (
        Image(org_logo, width=ORG_LOGO_SIZE[0], height=ORG_LOGO_SIZE[1])
        if org_logo
        else ""
    )
    table = Table(
        [[app_img, title_el, org_img]],
        colWidths=[APP_LOGO_SIZE[0], None, ORG_LOGO_SIZE[0]],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _day_headers(year: int, month: int):
    _, days_in_month = calendar.monthrange(year, month)
    return list(range(1, days_in_month + 1))


def _weekend_set(year: int, month: int) -> set[int]:
    _, days_in_month = calendar.monthrange(year, month)
    weekends = set()
    for day in range(1, days_in_month + 1):
        weekday = calendar.weekday(year, month, day)
        if weekday in (5, 6):
            weekends.add(day)
    return weekends


def _holiday_set(session: Session, year: int, month: int) -> set[int]:
    manual_entries = [
        {"day": item.day, "label": item.label, "action": item.action}
        for item in session.scalars(
            select(ManualHoliday).where(
                ManualHoliday.year == year,
                ManualHoliday.month == month,
            )
        )
    ]
    return {record["day"] for record in month_holidays(year, month, manual_entries)}


def _hex_to_color(value: str | None):
    if not value:
        return None
    cleaned = value.lstrip("#")
    if len(cleaned) != 6:
        return None
    try:
        r = int(cleaned[0:2], 16) / 255
        g = int(cleaned[2:4], 16) / 255
        b = int(cleaned[4:6], 16) / 255
        return colors.Color(r, g, b)
    except ValueError:
        return None


def _minute_label(value: int) -> str:
    hours = (value // 60) % 24
    minutes = value % 60
    return f"{hours:02d}:{minutes:02d}"


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


def _categories_for_role(session: Session, role: str) -> list[str]:
    return list(
        session.scalars(
            select(ProfessionalCategory.name).where(
                ProfessionalCategory.role == role,
                ProfessionalCategory.is_active.is_(True),
            )
        )
    )


def _shift_legend_rows(session: Session, group: str | None):
    query = (
        select(ServiceShift, Service, Shift)
        .join(Service, Service.code == ServiceShift.service_code)
        .join(Shift, Shift.code == ServiceShift.shift_code)
        .where(Service.is_active.is_(True))
    )
    role = _role_from_group(session, group)
    if role:
        query = query.where(Service.role == role)
    rows = list(session.exec(query).all())
    type_order = {"M": 0, "T": 1, "L": 2, "N": 3}
    rows.sort(
        key=lambda row: (
            row[1].name,
            type_order.get(row[2].shift_type, 9),
            row[2].code,
        )
    )
    legend_rows = []
    for _, service, shift in rows:
        legend_rows.append(
            [
                shift.code,
                service.name,
                _minute_label(shift.start_minute),
                _minute_label(shift.end_minute),
            ]
        )
    return legend_rows


def _legend_table(rows: list[list[str]], width: float, lang: str | None):
    if not rows:
        return None
    header = [
        _label(lang, "legend_code", "Código"),
        _label(lang, "legend_service", "Serviço"),
        _label(lang, "legend_start", "Entrada"),
        _label(lang, "legend_end", "Saída"),
    ]
    blocks = 4
    block_width = width / blocks
    combined = []
    for idx in range(0, len(rows), blocks):
        row = []
        for offset in range(blocks):
            block = rows[idx + offset] if idx + offset < len(rows) else ["", "", "", ""]
            row.extend(block)
        combined.append(row)
    col_widths = []
    for _ in range(blocks):
        col_widths.extend(
            [
                block_width * 0.2,
                block_width * 0.4,
                block_width * 0.2,
                block_width * 0.2,
            ]
        )
    table = Table(
        [header * blocks] + combined,
        colWidths=col_widths,
    )
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 5),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
            ]
        )
    )
    return table


def _tiny_text_block(info_text: str | None):
    if not info_text:
        return ""
    safe_text = info_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "<br/>".join(line.strip() for line in safe_text.splitlines())


def _signature_table(width: float, lang: str | None):
    gap = 16 * mm
    col_width = (width - gap) / 2
    table = Table(
        [
            ["", "", ""],
            [
                _label(lang, "signature_coordinator", "Enf. Coordenador"),
                "",
                _label(lang, "signature_director", "Enf. Diretor"),
            ],
        ],
        colWidths=[col_width, gap, col_width],
        rowHeights=[28 * mm, 6 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (0, 0), 0.6, colors.black),
                ("LINEBELOW", (2, 0), (2, 0), 0.6, colors.black),
                ("ALIGN", (0, 1), (0, 1), "CENTER"),
                ("ALIGN", (2, 1), (2, 1), "CENTER"),
                ("TOPPADDING", (0, 1), (0, 1), 6),
                ("BOTTOMPADDING", (0, 1), (0, 1), 2),
                ("TOPPADDING", (2, 1), (2, 1), 6),
                ("BOTTOMPADDING", (2, 1), (2, 1), 2),
                ("FONT", (0, 1), (2, 1), "Helvetica", 7),
            ]
        )
    )
    return table


def _swap_status_label(status: str, lang: str | None) -> str:
    labels = {
        "pt": {
            "PENDING_PARTICIPANTS": "A aguardar participantes",
            "PENDING_COORDINATOR": "A aguardar coordenador",
            "APPROVED": "Aprovado",
            "REJECTED": "Rejeitado",
            "REJECTED_BY_PARTICIPANT": "Recusado por participante",
        },
        "en": {
            "PENDING_PARTICIPANTS": "Waiting for participants",
            "PENDING_COORDINATOR": "Waiting for coordinator",
            "APPROVED": "Approved",
            "REJECTED": "Rejected",
            "REJECTED_BY_PARTICIPANT": "Rejected by participant",
        },
    }
    return labels[_lang_key(lang)].get(status, status)


def _swap_participant_label(status: str, lang: str | None) -> str:
    labels = {
        "pt": {
            "PENDING": "A aguardar",
            "ACCEPTED": "Aceite",
            "REJECTED": "Recusado",
        },
        "en": {
            "PENDING": "Pending",
            "ACCEPTED": "Accepted",
            "REJECTED": "Rejected",
        },
    }
    return labels[_lang_key(lang)].get(status, status)


def _format_user(user: User | None) -> str:
    if not user:
        return "-"
    return f"{user.full_name} ({user.username}) · {user.role}"


def export_swap_pdf(
    session: Session,
    request_id: int,
    app_logo_path: str | None,
    org_logo_path: str | None,
    app_name: str | None = None,
    org_name: str | None = None,
    info_text: str | None = None,
    exported_for: User | None = None,
    lang: str | None = None,
) -> io.BytesIO:
    req = session.get(SwapRequest, request_id)
    if not req:
        raise ValueError("Swap request not found")
    requester = session.get(User, req.requester_id)
    participants = list(
        session.scalars(
            select(SwapParticipant).where(SwapParticipant.request_id == request_id)
        )
    )
    participant_ids = [item.user_id for item in participants]
    users = (
        list(session.scalars(select(User).where(User.id.in_(participant_ids))))
        if participant_ids
        else []
    )
    user_map = {user.id: user for user in users}
    decision = session.scalar(
        select(SwapDecision).where(SwapDecision.request_id == request_id)
    )
    coordinator = (
        session.get(User, decision.coordinator_id) if decision else None
    )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )
    resolved_app_name = app_name or APP_NAME
    resolved_org_name = org_name or ORG_NAME
    title = f"{resolved_app_name} · {resolved_org_name} · {_label(lang, 'title_swap', 'Comprovativo de troca')} #{req.id}"
    header_table = _build_header(app_logo_path, org_logo_path, title)

    status_label = _swap_status_label(req.status, lang)
    created_at = req.created_at.strftime("%d/%m/%Y %H:%M")
    decision_text = "-"
    if decision:
        decision_status = _swap_status_label(decision.status, lang)
        reason = f" ({decision.reason})" if decision.reason else ""
        decided_at = decision.decided_at.strftime("%d/%m/%Y %H:%M")
        decision_text = (
            f"{decision_status}{reason} · {_format_user(coordinator)} · {decided_at}"
        )

    participant_lines = []
    for participant in participants:
        user = user_map.get(participant.user_id)
        status = _swap_participant_label(participant.status, lang)
        responded_at = (
            participant.responded_at.strftime("%d/%m/%Y %H:%M")
            if participant.responded_at
            else "-"
        )
        participant_lines.append(
            f"{_format_user(user)} · {status} · {responded_at}"
        )
    participants_text = "<br/>".join(participant_lines) if participant_lines else "-"

    current_service_shift = f"{req.service_code or '-'} / {req.shift_code or '-'}"
    desired_service_shift = (
        f"{req.desired_service_code or '-'} / {req.desired_shift_code or '-'}"
    )

    exported_at = datetime.now().strftime("%d/%m/%Y %H:%M")
    exported_for_text = _format_user(exported_for)

    data = [
        [_label(lang, "label_request_id", "Pedido"), f"#{req.id}"],
        [
            _label(lang, "label_date", "Data"),
            f"{req.day:02d}/{req.month:02d}/{req.year}",
        ],
        [_label(lang, "label_status", "Estado"), status_label],
        [_label(lang, "label_created_at", "Criado em"), created_at],
        [_label(lang, "label_requester", "Pedido por"), _format_user(requester)],
        [
            _label(lang, "label_current", "Atual"),
            f"{_label(lang, 'label_service_shift', 'Serviço/Turno')}: {current_service_shift}",
        ],
        [
            _label(lang, "label_desired", "Pretendido"),
            f"{_label(lang, 'label_service_shift', 'Serviço/Turno')}: {desired_service_shift}",
        ],
        [_label(lang, "label_reason", "Motivo"), req.reason or "-"],
        [_label(lang, "label_observations", "Observações"), req.observations or "-"],
        [_label(lang, "label_participants", "Participantes"), participants_text],
        [_label(lang, "label_decision", "Decisão"), decision_text],
        [_label(lang, "label_exported_for", "Exportado para"), exported_for_text],
        [_label(lang, "label_exported_at", "Exportado em"), exported_at],
    ]

    style = getSampleStyleSheet()["Normal"]
    style.fontSize = 9
    style.leading = 11
    table_data = []
    for label, value in data:
        value_text = _tiny_text_block(str(value)) if isinstance(value, str) else str(value)
        table_data.append([label, Paragraph(value_text, style)])
    table = Table(table_data, colWidths=[110, doc.width - 110])
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 9),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    small_style = getSampleStyleSheet()["Normal"]
    small_style.fontSize = 6
    small_style.leading = 7
    info_block = Paragraph(_tiny_text_block(info_text), small_style) if info_text else None
    elements = [header_table, table]
    if info_block:
        elements.extend([Spacer(1, 6), info_block])
    doc.build(elements)
    buffer.seek(0)
    return buffer


def _requirements_summary_table(
    session: Session,
    year: int,
    month: int,
    group: str | None,
    day_width: float,
    leading_widths: list[float],
    trailing_widths: list[float],
    lang: str | None,
):
    service_codes = None
    role = _role_from_group(session, group)
    if role:
        service_codes = list(
            session.scalars(select(Service.code).where(Service.role == role))
        )
    req_query = select(MonthlyRequirement).where(
        MonthlyRequirement.year == year,
        MonthlyRequirement.month == month,
    )
    if service_codes:
        req_query = req_query.where(MonthlyRequirement.service_code.in_(service_codes))
    requirements = list(session.scalars(req_query))
    if not requirements:
        return None
    service_names = {
        service.code: service.name for service in session.scalars(select(Service))
    }
    shifts = {shift.code: shift for shift in session.scalars(select(Shift))}
    required_map: Dict[Tuple[str, str, int], int] = {}
    rows_set = []
    for req in requirements:
        key = (req.service_code, req.shift_code, req.day)
        required_map[key] = req.required_count
        row_key = (req.service_code, req.shift_code)
        if row_key not in rows_set:
            rows_set.append(row_key)
    entries_query = select(ScheduleEntry).where(
        ScheduleEntry.year == year,
        ScheduleEntry.month == month,
    )
    if service_codes:
        entries_query = entries_query.where(ScheduleEntry.service_code.in_(service_codes))
    entries = list(session.scalars(entries_query))
    assigned_map: Dict[Tuple[str, str, int], int] = {}
    for entry in entries:
        key = (entry.service_code, entry.shift_code, entry.day)
        assigned_map[key] = assigned_map.get(key, 0) + 1
    type_order = {"M": 0, "T": 1, "L": 2, "N": 3}
    def _shift_sort_key(row: tuple[str, str]) -> tuple[str, int, str]:
        service_code, shift_code = row
        shift_type = shifts.get(shift_code).shift_type if shifts.get(shift_code) else ""
        return (
            service_names.get(service_code, service_code),
            type_order.get(shift_type, 9),
            shift_code,
        )
    rows_set.sort(key=_shift_sort_key)
    day_headers = _day_headers(year, month)
    table_data = []
    header = [_label(lang, "header_service_shift", "Serviço/Turno"), ""] + [
        str(day) for day in day_headers
    ] + [
        "",
        "",
        "",
    ]
    table_data.append(header)
    for service_code, shift_code in rows_set:
        label = f"{service_names.get(service_code, service_code)} {shift_code}"
        row = [label, ""]
        for day in day_headers:
            row.append(required_map.get((service_code, shift_code, day), 0))
        row.extend(["", "", ""])
        table_data.append(row)
    col_widths = leading_widths + [day_width] * len(day_headers) + trailing_widths
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    style = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 5),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    weekend_set = _weekend_set(year, month)
    holiday_set = _holiday_set(session, year, month)
    for day in day_headers:
        col = 2 + day - 1
        if day in holiday_set:
            style.append(("BACKGROUND", (col, 0), (col, 0), HOLIDAY_COLOR))
        elif day in weekend_set:
            style.append(("BACKGROUND", (col, 0), (col, 0), WEEKEND_COLOR))
    for row_idx, (service_code, shift_code) in enumerate(rows_set, start=1):
        for day in day_headers:
            required = required_map.get((service_code, shift_code, day), 0)
            if required <= 0:
                continue
            assigned = assigned_map.get((service_code, shift_code, day), 0)
            col = 2 + day - 1
            color = GREEN_OK if assigned >= required else RED_BAD
            style.append(("BACKGROUND", (col, row_idx), (col, row_idx), color))
    table.setStyle(TableStyle(style))
    return table


def export_schedule_pdf(
    session: Session,
    year: int,
    month: int,
    app_logo_path: str | None,
    org_logo_path: str | None,
    app_name: str | None = None,
    org_name: str | None = None,
    info_text: str | None = None,
    group: str | None = None,
    lang: str | None = None,
) -> io.BytesIO:
    data = []
    day_headers = _day_headers(year, month)
    weekend_set = _weekend_set(year, month)
    holiday_set = _holiday_set(session, year, month)
    header = [
        _label(lang, "header_professional", "Profissional"),
        _label(lang, "header_balance", "Saldo (h)"),
    ] + [str(day) for day in day_headers] + [
        _label(lang, "header_total_hours", "Total Horas"),
        _label(lang, "header_current_balance", "Saldo atual"),
        _label(lang, "header_monthly_hours", "Horas Mensais"),
    ]
    data.append(header)

    nurse_query = select(Nurse)
    role = _role_from_group(session, group)
    if role:
        categories = _categories_for_role(session, role)
        if categories:
            nurse_query = nurse_query.where(Nurse.category.in_(categories))
        else:
            nurse_query = nurse_query.where(Nurse.category == role)
    nurses = list(session.scalars(nurse_query))

    schedule_entries = list(
        session.scalars(
            select(ScheduleEntry).where(
                ScheduleEntry.year == year,
                ScheduleEntry.month == month,
            )
        )
    )
    shift_colors = {
        row.shift_code: row.color
        for row in session.exec(
            select(ServiceShift.shift_code, Service.color)
            .join(Service, Service.code == ServiceShift.service_code)
        ).all()
    }
    shifts = {shift.code: shift for shift in session.scalars(select(Shift))}
    shift_types = {shift.code: shift.shift_type for shift in session.scalars(select(Shift))}
    day_assignments: Dict[Tuple[int, int], list[str]] = {}
    for entry in schedule_entries:
        key = (entry.nurse_id, entry.day)
        day_assignments.setdefault(key, []).append(entry.shift_code)

    constraint_map: Dict[Tuple[int, int], str] = {
        (item.nurse_id, item.day): item.code
        for item in session.scalars(
            select(ConstraintEntry).where(
                ConstraintEntry.year == year,
                ConstraintEntry.month == month,
            )
        )
    }

    adjustments = {
        item.nurse_id: item
        for item in session.scalars(
            select(NurseMonthAdjustment).where(
                NurseMonthAdjustment.year == year,
                NurseMonthAdjustment.month == month,
            )
        )
    }
    stats_map = {
        item.nurse_id: item
        for item in session.scalars(
            select(NurseMonthStat).where(
                NurseMonthStat.year == year,
                NurseMonthStat.month == month,
            )
        )
    }

    cell_backgrounds = []
    for nurse_idx, nurse in enumerate(nurses, start=1):
        row = [nurse.name]
        stat = stats_map.get(nurse.id)
        saldo_minutes = nurse.hour_balance_minutes or 0
        previous_bank = saldo_minutes - (stat.delta_minutes if stat else 0)
        row.append(f"{round(previous_bank / 60, 1)}")
        for day in day_headers:
            assignments = day_assignments.get((nurse.id, day), [])
            if assignments:
                assignments_sorted = sorted(
                    assignments,
                    key=lambda code: (
                        shifts.get(code).start_minute if shifts.get(code) else 9999,
                        code,
                    ),
                )
                row.append("".join(assignments_sorted))
                if len(assignments_sorted) == 1:
                    color = _hex_to_color(shift_colors.get(assignments_sorted[0]))
                    if color:
                        cell_backgrounds.append((2 + day - 1, nurse_idx, color))
            else:
                constraint = constraint_map.get((nurse.id, day))
                row.append(_constraint_display(constraint) if constraint else "")
                if day in holiday_set:
                    cell_backgrounds.append((2 + day - 1, nurse_idx, HOLIDAY_COLOR))
                elif day in weekend_set:
                    cell_backgrounds.append((2 + day - 1, nurse_idx, WEEKEND_COLOR))
        actual_minutes = stat.actual_minutes if stat else 0
        target_minutes = stat.target_minutes if stat else 0
        saldo_atual_minutes = actual_minutes + previous_bank - target_minutes
        row.extend(
            [
                f"{round(actual_minutes / 60, 1)}",
                f"{round(saldo_atual_minutes / 60, 1)}",
                f"{round(target_minutes / 60, 1)}",
            ]
        )
        data.append(row)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )
    resolved_app_name = app_name or APP_NAME
    resolved_org_name = org_name or ORG_NAME
    title = (
        f"{resolved_app_name} · {resolved_org_name} · "
        f"{_label(lang, 'title_schedule', 'Escala')} {month:02d}/{year}"
    )
    header_table = _build_header(app_logo_path, org_logo_path, title)
    available_width = doc.width
    base_cols = 2 + len(day_headers) + 3
    summary_widths = [36, 36, 40]
    day_width = (available_width - 80 - 40 - sum(summary_widths)) / len(day_headers)
    col_widths = [80, 40] + [day_width] * len(day_headers) + summary_widths
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table_style = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 5),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for day in day_headers:
        col = 2 + day - 1
        if day in holiday_set:
            table_style.append(("BACKGROUND", (col, 0), (col, 0), HOLIDAY_COLOR))
        elif day in weekend_set:
            table_style.append(("BACKGROUND", (col, 0), (col, 0), WEEKEND_COLOR))
    for col, row_idx, color in cell_backgrounds:
        table_style.append(("BACKGROUND", (col, row_idx), (col, row_idx), color))
    table.setStyle(TableStyle(table_style))
    small_style = getSampleStyleSheet()["Normal"]
    small_style.fontSize = 5
    small_style.leading = 6
    legend_rows = _shift_legend_rows(session, group)
    legend = None
    if legend_rows:
        legend = _legend_table(legend_rows, doc.width, lang)
    info_block = Paragraph(_tiny_text_block(info_text), small_style)
    signature = _signature_table(doc.width, lang)
    requirements_table = _requirements_summary_table(
        session, year, month, group, day_width, [80, 40], summary_widths, lang
    )
    elements = [header_table, table]
    if requirements_table:
        elements.extend([requirements_table])
    elements.append(Spacer(1, 4))
    if legend:
        elements.extend([legend, Spacer(1, 4)])
    elements.extend([info_block, Spacer(1, 6), signature])
    doc.build(elements)
    buffer.seek(0)
    return buffer


def export_constraints_pdf(
    session: Session,
    year: int,
    month: int,
    app_logo_path: str | None,
    org_logo_path: str | None,
    app_name: str | None = None,
    org_name: str | None = None,
    info_text: str | None = None,
    group: str | None = None,
    lang: str | None = None,
) -> io.BytesIO:
    data = []
    day_headers = _day_headers(year, month)
    weekend_set = _weekend_set(year, month)
    holiday_set = _holiday_set(session, year, month)
    header = [_label(lang, "header_professional", "Profissional")] + [
        str(day) for day in day_headers
    ]
    data.append(header)

    nurse_query = select(Nurse)
    role = _role_from_group(session, group)
    if role:
        categories = _categories_for_role(session, role)
        if categories:
            nurse_query = nurse_query.where(Nurse.category.in_(categories))
        else:
            nurse_query = nurse_query.where(Nurse.category == role)
    nurses = list(session.scalars(nurse_query))

    constraint_map: Dict[Tuple[int, int], str] = {
        (item.nurse_id, item.day): item.code
        for item in session.scalars(
            select(ConstraintEntry).where(
                ConstraintEntry.year == year,
                ConstraintEntry.month == month,
            )
        )
    }

    cell_backgrounds = []
    for nurse_idx, nurse in enumerate(nurses, start=1):
        row = [nurse.name]
        for day in day_headers:
            constraint = constraint_map.get((nurse.id, day))
            row.append(_constraint_text(constraint) if constraint else "")
            if day in holiday_set:
                cell_backgrounds.append((1 + day - 1, nurse_idx, HOLIDAY_COLOR))
            elif day in weekend_set:
                cell_backgrounds.append((1 + day - 1, nurse_idx, WEEKEND_COLOR))
        data.append(row)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )
    resolved_app_name = app_name or APP_NAME
    resolved_org_name = org_name or ORG_NAME
    title = (
        f"{resolved_app_name} · {resolved_org_name} · "
        f"{_label(lang, 'title_constraints', 'Disponibilidades')} {month:02d}/{year}"
    )
    header_table = _build_header(app_logo_path, org_logo_path, title)
    available_width = doc.width
    col_widths = [100] + [
        (available_width - 100) / len(day_headers)
    ] * len(day_headers)
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table_style = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 5),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for day in day_headers:
        col = 1 + day - 1
        if day in holiday_set:
            table_style.append(("BACKGROUND", (col, 0), (col, 0), HOLIDAY_COLOR))
        elif day in weekend_set:
            table_style.append(("BACKGROUND", (col, 0), (col, 0), WEEKEND_COLOR))
    for col, row_idx, color in cell_backgrounds:
        table_style.append(("BACKGROUND", (col, row_idx), (col, row_idx), color))
    table.setStyle(TableStyle(table_style))
    small_style = getSampleStyleSheet()["Normal"]
    small_style.fontSize = 5
    small_style.leading = 6
    legend_rows = _shift_legend_rows(session, group)
    legend = None
    if legend_rows:
        legend = _legend_table(legend_rows, doc.width, lang)
    info_block = Paragraph(_tiny_text_block(info_text), small_style)
    signature = _signature_table(doc.width, lang)
    elements = [header_table, table, Spacer(1, 4)]
    if legend:
        elements.extend([legend, Spacer(1, 4)])
    elements.extend([info_block, Spacer(1, 6), signature])
    doc.build(elements)
    buffer.seek(0)
    return buffer
