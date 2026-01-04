import calendar
from datetime import date
from typing import List

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session

from .constants import SERVICE_COLORS, SERVICE_SHIFT_DEFS, default_window_for
from .models import (
    MonthlyRequirement,
    Nurse,
    ProfessionalCategory,
    Service,
    ServiceShift,
    Shift,
    Team,
    TeamMember,
    User,
)
from .auth import hash_password


SAP_CODES = ["Ms", "Ts", "Ls", "TLs"]
ANALISES_CODE = "Ma"
CONSULTA_MANHA = "Me"
CONSULTA_TARDE = "Te"
PISO1_CODES = {"M1": {"weekdays": range(1, 6)}, "T1": {"weekdays": range(0, 6)}, "N1": {"weekdays": range(0, 6)}}
PISO3_CODES = ["M3", "T3", "N3"]
REFORCO_CODES = {
    "MR": range(1, 5),  # Tue-Fri
    "MR2": [5],  # Sat
    "NR": range(2, 5),  # Wed-Fri
}

DEFAULT_NURSES = [
    ("Nuno S. Magalhães", "COORDENADOR"),
    ("Joel Sousa", "COORDENADOR"),
    ("Fátima Ferreira", "CONTRATADO"),
    ("Andreia Leal", "CONTRATADO"),
    ("Gonçalo Oliveira", "CONTRATADO"),
    ("Adriana Ribeiro", "RV_TEMPO_INTEIRO"),
    ("Marta Ferreira", "RV_TEMPO_INTEIRO"),
    ("Sandra Ferreira", "RV_TEMPO_INTEIRO"),
    ("Sérgio Faria", "RV_TEMPO_INTEIRO"),
    ("Andreia Coelho", "RV_TEMPO_PARCIAL"),
    ("Beatriz Barbosa", "RV_TEMPO_PARCIAL"),
    ("Bruno Faria", "RV_TEMPO_PARCIAL"),
    ("Carmen Silva", "RV_TEMPO_PARCIAL"),
    ("Catarina Mendonça", "RV_TEMPO_PARCIAL"),
    ("Celia Correia", "RV_TEMPO_PARCIAL"),
    ("Cristina Magalhães", "RV_TEMPO_PARCIAL"),
    ("Daniela Moreira", "RV_TEMPO_PARCIAL"),
    ("Dulce Barbosa", "RV_TEMPO_PARCIAL"),
    ("Gisela Monteiro", "RV_TEMPO_PARCIAL"),
    ("Goretti Gomes", "RV_TEMPO_PARCIAL"),
    ("Inês Faria", "RV_TEMPO_PARCIAL"),
    ("Inês Sousa Alves", "RV_TEMPO_PARCIAL"),
    ("Jéssica Sousa", "RV_TEMPO_PARCIAL"),
    ("Joana Correia", "RV_TEMPO_PARCIAL"),
    ("Luana Pinto", "RV_TEMPO_PARCIAL"),
    ("Lúcia Amorim", "RV_TEMPO_PARCIAL"),
    ("Manuela Sousa", "RV_TEMPO_PARCIAL"),
    ("Marisa Ferreira", "RV_TEMPO_PARCIAL"),
    ("Marisa Miranda", "RV_TEMPO_PARCIAL"),
    ("Marta Dâmaso", "RV_TEMPO_PARCIAL"),
    ("Neuza Cunha", "RV_TEMPO_PARCIAL"),
    ("Norberto Almeida", "RV_TEMPO_PARCIAL"),
    ("Nuno Meireles", "RV_TEMPO_PARCIAL"),
    ("Paulo Alves", "RV_TEMPO_PARCIAL"),
    ("Raquel Santos", "RV_TEMPO_PARCIAL"),
    ("Ricardo Casal", "RV_TEMPO_PARCIAL"),
    ("Rosa Teixeira", "RV_TEMPO_PARCIAL"),
    ("Susana Ferreira", "RV_TEMPO_PARCIAL"),
    ("Tania Silva", "RV_TEMPO_PARCIAL"),
    ("Tatiana Ferreira", "RV_TEMPO_PARCIAL"),
    ("Teresa Magalhães", "RV_TEMPO_PARCIAL"),
    ("Tiago Brás", "RV_TEMPO_PARCIAL"),
    ("Vera Seabra", "RV_TEMPO_PARCIAL"),
    ("Vitor Caldas", "RV_TEMPO_PARCIAL"),
]

DEFAULT_USERS = [
    ("admin", "Admin", "ADMIN"),
    ("coord", "Enfermeiro Coordenador", "COORDENADOR"),
    ("enf1", "Enfermeiro", "ENFERMEIRO"),
    ("ao1", "Assistente Operacional", "ASSISTENTE_OPERACIONAL"),
]

DEFAULT_CATEGORIES = [
    ("COORDENADOR", "ENFERMEIRO", 0),
    ("CONTRATADO", "ENFERMEIRO", 1),
    ("CONTRATADO_TEMPO_PARCIAL", "ENFERMEIRO", 2),
    ("RV_TEMPO_INTEIRO", "ENFERMEIRO", 3),
    ("RV_TEMPO_PARCIAL", "ENFERMEIRO", 4),
    ("ASSISTENTE_OPERACIONAL", "ASSISTENTE_OPERACIONAL", 0),
]

DEMO_USERS = [
    ("demo_coord", "Helena Duarte", "COORDENADOR"),
    ("demo_enf01", "Rita Sousa", "ENFERMEIRO"),
    ("demo_enf02", "Mário Coelho", "ENFERMEIRO"),
    ("demo_enf03", "Inês Pires", "ENFERMEIRO"),
    ("demo_enf04", "João Amado", "ENFERMEIRO"),
    ("demo_enf05", "Clara Fonseca", "ENFERMEIRO"),
    ("demo_enf06", "Leonor Tavares", "ENFERMEIRO"),
    ("demo_enf07", "Hugo Matias", "ENFERMEIRO"),
    ("demo_enf08", "Sara Gouveia", "ENFERMEIRO"),
    ("demo_ao01", "Ângela Faria", "ASSISTENTE_OPERACIONAL"),
    ("demo_ao02", "Bruno Pinto", "ASSISTENTE_OPERACIONAL"),
    ("demo_ao03", "Carla Leite", "ASSISTENTE_OPERACIONAL"),
    ("demo_ao04", "Diogo Paiva", "ASSISTENTE_OPERACIONAL"),
    ("demo_ao05", "Marta Fialho", "ASSISTENTE_OPERACIONAL"),
    ("demo_ao06", "Nuno Costa", "ASSISTENTE_OPERACIONAL"),
]

DEMO_TEAMS = ["Equipa Orvalho", "Equipa Vento Sul", "Equipa Maré", "Equipa Horizonte"]

DEMO_SERVICES = [
    ("HOSP_DIA", "Hospital de Dia", "ENFERMEIRO", "#a5b4fc"),
    ("U_INTERNA", "Unidade Interna", "ENFERMEIRO", "#fcd34d"),
    ("C_REABIL", "Centro de Reabilitação", "ENFERMEIRO", "#86efac"),
    ("NEO_AMB", "Neonatologia Amb.", "ENFERMEIRO", "#f9a8d4"),
    ("URGENCIA", "Urgência", "ENFERMEIRO", "#fde047"),
    ("SUP_OPER", "Suporte Operacional", "ASSISTENTE_OPERACIONAL", "#fca5a5"),
    ("LOGIST", "Logística", "ASSISTENTE_OPERACIONAL", "#93c5fd"),
    ("HOTELAR", "Hotelaria", "ASSISTENTE_OPERACIONAL", "#fdba74"),
    ("TRANSP", "Transportes", "ASSISTENTE_OPERACIONAL", "#67e8f9"),
]

DEMO_SHIFTS = [
    ("HDM", "Hospital de Dia - Manhã", "M", 7 * 60, 13 * 60),
    ("HDT", "Hospital de Dia - Tarde", "T", 13 * 60, 19 * 60),
    ("HDN", "Hospital de Dia - Noite", "N", 19 * 60, 7 * 60),
    ("UIM", "Unidade Interna - Manhã", "M", 8 * 60, 14 * 60),
    ("UIT", "Unidade Interna - Tarde", "T", 14 * 60, 20 * 60),
    ("UIN", "Unidade Interna - Noite", "N", 20 * 60, 8 * 60),
    ("CRM", "Centro de Reabilitação - Manhã", "M", 8 * 60, 12 * 60),
    ("CRT", "Centro de Reabilitação - Tarde", "T", 12 * 60, 18 * 60),
    ("NEOM", "Neonatologia - Manhã", "M", 8 * 60, 14 * 60),
    ("NEOT", "Neonatologia - Tarde", "T", 14 * 60, 20 * 60),
    ("URGM", "Urgência - Manhã", "M", 8 * 60, 14 * 60),
    ("URGT", "Urgência - Tarde", "T", 14 * 60, 20 * 60),
    ("URGN", "Urgência - Noite", "N", 20 * 60, 8 * 60),
    ("SOM", "Suporte Operacional - Manhã", "M", 8 * 60, 14 * 60),
    ("SOT", "Suporte Operacional - Tarde", "T", 14 * 60, 20 * 60),
    ("LOM", "Logística - Manhã", "M", 7 * 60, 13 * 60),
    ("LOT", "Logística - Tarde", "T", 13 * 60, 19 * 60),
    ("HOM", "Hotelaria - Manhã", "M", 7 * 60, 13 * 60),
    ("HOT", "Hotelaria - Tarde", "T", 13 * 60, 19 * 60),
    ("TRM", "Transportes - Manhã", "M", 7 * 60, 13 * 60),
    ("TRT", "Transportes - Tarde", "T", 13 * 60, 19 * 60),
]

DEMO_SERVICE_SHIFTS = [
    ("HOSP_DIA", "HDM"),
    ("HOSP_DIA", "HDT"),
    ("HOSP_DIA", "HDN"),
    ("U_INTERNA", "UIM"),
    ("U_INTERNA", "UIT"),
    ("U_INTERNA", "UIN"),
    ("C_REABIL", "CRM"),
    ("C_REABIL", "CRT"),
    ("NEO_AMB", "NEOM"),
    ("NEO_AMB", "NEOT"),
    ("URGENCIA", "URGM"),
    ("URGENCIA", "URGT"),
    ("URGENCIA", "URGN"),
    ("SUP_OPER", "SOM"),
    ("SUP_OPER", "SOT"),
    ("LOGIST", "LOM"),
    ("LOGIST", "LOT"),
    ("HOTELAR", "HOM"),
    ("HOTELAR", "HOT"),
    ("TRANSP", "TRM"),
    ("TRANSP", "TRT"),
]


def _seed_demo_requirements(session: Session, year: int, month: int) -> None:
    demo_service_codes = [item[0] for item in DEMO_SERVICES]
    demo_shift_codes = [item[0] for item in DEMO_SHIFTS]
    existing = session.scalar(
        select(func.count(MonthlyRequirement.id)).where(
            MonthlyRequirement.year == year,
            MonthlyRequirement.month == month,
            MonthlyRequirement.service_code.in_(demo_service_codes),
            MonthlyRequirement.shift_code.in_(demo_shift_codes),
        )
    )
    if existing:
        return

    shift_types = {code: shift_type for code, _, shift_type, _, _ in DEMO_SHIFTS}
    entries: List[MonthlyRequirement] = []
    _, total_days = calendar.monthrange(year, month)

    for day in range(1, total_days + 1):
        weekday = date(year, month, day).weekday()
        is_weekend = weekday >= 5
        for service_code, shift_code in DEMO_SERVICE_SHIFTS:
            shift_type = shift_types.get(shift_code, "M")
            if shift_type == "N" and is_weekend:
                required_count = 1
            elif shift_type in {"M", "T", "L"}:
                required_count = 1 if not is_weekend else 1
            else:
                required_count = 1
            entries.append(
                MonthlyRequirement(
                    year=year,
                    month=month,
                    day=day,
                    service_code=service_code,
                    shift_code=shift_code,
                    required_count=required_count,
                )
            )

    if entries:
        session.add_all(entries)
        session.flush()


def _should_create_defaults(session: Session, year: int, month: int) -> bool:
    existing = session.scalar(
        select(func.count(MonthlyRequirement.id)).where(
            MonthlyRequirement.year == year,
            MonthlyRequirement.month == month,
        )
    )
    return existing == 0


def _add_requirement(
    entries: List[MonthlyRequirement],
    year: int,
    month: int,
    day: int,
    service: str,
    code: str,
):
    entries.append(
        MonthlyRequirement(
            year=year,
            month=month,
            day=day,
            service_code=service,
            shift_code=code,
            required_count=1,
        )
    )


def ensure_default_requirements(session: Session, year: int, month: int) -> None:
    if not _should_create_defaults(session, year, month):
        return

    entries: List[MonthlyRequirement] = []
    _, total_days = calendar.monthrange(year, month)

    for day in range(1, total_days + 1):
        weekday = date(year, month, day).weekday()  # Monday=0

        for code in SAP_CODES:
            _add_requirement(entries, year, month, day, "SAP", code)

        if weekday <= 5:  # Monday-Saturday
            _add_requirement(entries, year, month, day, "Análises", ANALISES_CODE)

        if weekday <= 4:  # Monday-Friday
            _add_requirement(entries, year, month, day, "Consulta Externa", CONSULTA_TARDE)
        if weekday == 5:  # Saturday
            _add_requirement(entries, year, month, day, "Consulta Externa", CONSULTA_MANHA)

        # Piso 1
        for code, rule in PISO1_CODES.items():
            if weekday in rule["weekdays"]:
                _add_requirement(entries, year, month, day, "Piso 1", code)

        # Piso 3 everyday
        for code in PISO3_CODES:
            _add_requirement(entries, year, month, day, "Piso 3", code)

        # Reforço
        for code, allowed_days in REFORCO_CODES.items():
            if weekday in allowed_days:
                _add_requirement(entries, year, month, day, "Reforço", code)

    if entries:
        session.add_all(entries)
        session.flush()


def ensure_default_nurses(session: Session) -> None:
    existing = list(session.scalars(select(Nurse)))
    max_order = session.scalar(select(func.max(Nurse.display_order))) or 0
    added = []
    users = list(session.scalars(select(User)))
    existing_user_ids = {nurse.user_id for nurse in existing if nurse.user_id}
    if users:
        for user in users:
            if user.role not in {"COORDENADOR", "ENFERMEIRO", "ASSISTENTE_OPERACIONAL"}:
                continue
            if user.id in existing_user_ids:
                continue
            max_order += 1
            category = (
                "COORDENADOR"
                if user.role == "COORDENADOR"
                else "ASSISTENTE_OPERACIONAL"
                if user.role == "ASSISTENTE_OPERACIONAL"
                else "CONTRATADO"
            )
            service_codes = [
                row.shift_code
                for row in session.scalars(
                    select(ServiceShift)
                    .join(Service, Service.code == ServiceShift.service_code)
                    .where(
                        Service.role
                        == (
                            "ASSISTENTE_OPERACIONAL"
                            if user.role == "ASSISTENTE_OPERACIONAL"
                            else "ENFERMEIRO"
                        )
                    )
                )
            ]
            added.append(
                Nurse(
                    name=user.full_name,
                    category=category,
                    services_permitted=service_codes,
                    can_work_night=True,
                    weekly_hours=40,
                    display_order=max_order,
                    user_id=user.id,
                )
            )
    if not users and not existing:
        service_codes = [row.shift_code for row in session.scalars(select(ServiceShift))]
        for name, category in DEFAULT_NURSES:
            max_order += 1
            weekly_hours = 18 if category == "CONTRATADO_TEMPO_PARCIAL" else 40
            added.append(
                Nurse(
                    name=name,
                    category=category,
                    services_permitted=service_codes,
                    can_work_night=True,
                    weekly_hours=weekly_hours,
                    display_order=max_order,
                )
            )
    if added:
        session.add_all(added)
        session.flush()


def ensure_default_services(session: Session) -> None:
    existing = {svc.code for svc in session.scalars(select(Service))}
    service_defs = {service for service, _, _, _ in SERVICE_SHIFT_DEFS}
    for service in sorted(service_defs):
        if service in existing:
            continue
        session.add(
            Service(
                code=service,
                name=service,
                color=SERVICE_COLORS.get(service, "#e2e8f0"),
                role="ENFERMEIRO",
                is_active=True,
            )
        )
    session.flush()


def ensure_default_shifts(session: Session) -> None:
    existing = {shift.code for shift in session.scalars(select(Shift))}
    for service, code, label, shift_type in SERVICE_SHIFT_DEFS:
        if code in existing:
            continue
        start_minute, end_minute = default_window_for(code, shift_type)
        session.add(
            Shift(
                code=code,
                label=label,
                shift_type=shift_type,
                start_minute=start_minute,
                end_minute=end_minute,
            )
        )
    session.flush()


def ensure_default_service_shifts(session: Session) -> None:
    existing = {(row.service_code, row.shift_code) for row in session.scalars(select(ServiceShift))}
    for service, code, _, _ in SERVICE_SHIFT_DEFS:
        key = (service, code)
        if key in existing:
            continue
        session.add(ServiceShift(service_code=service, shift_code=code))
    session.flush()


def ensure_default_categories(session: Session) -> None:
    existing = {
        (item.name, item.role)
        for item in session.scalars(select(ProfessionalCategory))
    }
    for name, role, sort_order in DEFAULT_CATEGORIES:
        if (name, role) in existing:
            continue
        session.add(
            ProfessionalCategory(
                name=name,
                role=role,
                sort_order=sort_order,
                is_active=True,
            )
        )
    session.flush()


def ensure_default_users(session: Session) -> None:
    existing = {user.username for user in session.scalars(select(User))}
    for username, full_name, role in DEFAULT_USERS:
        if username in existing:
            continue
        session.add(
            User(
                username=username,
                full_name=full_name,
                role=role,
                password_hash=hash_password("123456"),
                is_active=True,
            )
        )
    session.flush()


def ensure_admin_user(session: Session) -> None:
    existing = {user.username for user in session.scalars(select(User))}
    if "admin" in existing:
        return
    session.add(
        User(
            username="admin",
            full_name="Admin",
            role="ADMIN",
            password_hash=hash_password("123456"),
            is_active=True,
        )
    )
    session.flush()


def seed_demo_data(session: Session) -> None:
    existing = {user.username for user in session.scalars(select(User))}
    created_users = []
    for username, full_name, role in DEMO_USERS:
        if username in existing:
            continue
        user = User(
            username=username,
            full_name=full_name,
            role=role,
            password_hash=hash_password("123456"),
            is_active=True,
        )
        session.add(user)
        session.flush()
        session.refresh(user)
        created_users.append(user)

    users = created_users or list(
        session.scalars(select(User).where(User.username.in_([u[0] for u in DEMO_USERS])))
    )
    existing_services = {svc.code for svc in session.scalars(select(Service))}
    for code, name, role, color in DEMO_SERVICES:
        if code in existing_services:
            continue
        session.add(
            Service(
                code=code,
                name=name,
                color=color,
                role=role,
                is_active=True,
            )
        )
    session.flush()

    existing_shifts = {shift.code for shift in session.scalars(select(Shift))}
    for code, label, shift_type, start_minute, end_minute in DEMO_SHIFTS:
        if code in existing_shifts:
            continue
        session.add(
            Shift(
                code=code,
                label=label,
                shift_type=shift_type,
                start_minute=start_minute,
                end_minute=end_minute,
            )
        )
    session.flush()

    existing_service_shifts = {
        (row.service_code, row.shift_code)
        for row in session.scalars(select(ServiceShift))
    }
    for service_code, shift_code in DEMO_SERVICE_SHIFTS:
        key = (service_code, shift_code)
        if key in existing_service_shifts:
            continue
        session.add(ServiceShift(service_code=service_code, shift_code=shift_code))
    session.flush()
    existing_user_ids = {nurse.user_id for nurse in session.scalars(select(Nurse)) if nurse.user_id}
    max_order = session.scalar(select(func.max(Nurse.display_order))) or 0
    for user in users:
        if user.role not in {"COORDENADOR", "ENFERMEIRO", "ASSISTENTE_OPERACIONAL"}:
            continue
        if user.id in existing_user_ids:
            continue
        max_order += 1
        category = (
            "COORDENADOR"
            if user.role == "COORDENADOR"
            else "ASSISTENTE_OPERACIONAL"
            if user.role == "ASSISTENTE_OPERACIONAL"
            else "CONTRATADO"
        )
        role = "ASSISTENTE_OPERACIONAL" if user.role == "ASSISTENTE_OPERACIONAL" else "ENFERMEIRO"
        service_codes = [
            row.shift_code
            for row in session.scalars(
                select(ServiceShift)
                .join(Service, Service.code == ServiceShift.service_code)
                .where(Service.role == role)
            )
        ]
        session.add(
            Nurse(
                name=user.full_name,
                category=category,
                services_permitted=service_codes,
                can_work_night=True,
                weekly_hours=40,
                display_order=max_order,
                user_id=user.id,
            )
        )

    def _ensure_team(name: str, role: str) -> Team:
        team = session.scalar(select(Team).where(Team.name == name))
        if not team:
            team = Team(name=name, role=role, is_active=True)
            session.add(team)
            session.flush()
        return team

    team_enf_main = _ensure_team(DEMO_TEAMS[0], "ENFERMEIRO")
    team_ao_main = _ensure_team(DEMO_TEAMS[1], "ASSISTENTE_OPERACIONAL")
    team_enf_alt = _ensure_team(DEMO_TEAMS[2], "ENFERMEIRO")
    team_ao_alt = _ensure_team(DEMO_TEAMS[3], "ASSISTENTE_OPERACIONAL")

    session.execute(
        delete(TeamMember).where(
            TeamMember.team_id.in_(
                [team_enf_main.id, team_enf_alt.id, team_ao_main.id, team_ao_alt.id]
            )
        )
    )
    demo_user_ids = [user.id for user in users]
    if demo_user_ids:
        demo_users = list(session.scalars(select(User).where(User.id.in_(demo_user_ids))))
        ao_toggle = True
        enf_toggle = True
        for user in demo_users:
            if user.role == "ASSISTENTE_OPERACIONAL":
                team_id = team_ao_main.id if ao_toggle else team_ao_alt.id
                ao_toggle = not ao_toggle
                session.add(TeamMember(team_id=team_id, user_id=user.id))
            else:
                team_id = team_enf_main.id if enf_toggle else team_enf_alt.id
                enf_toggle = not enf_toggle
                session.add(TeamMember(team_id=team_id, user_id=user.id))
    session.flush()

    today = date.today()
    _seed_demo_requirements(session, today.year, today.month)


def clear_demo_data(session: Session) -> None:
    demo_usernames = [u[0] for u in DEMO_USERS]
    demo_users = list(session.scalars(select(User).where(User.username.in_(demo_usernames))))
    if not demo_users:
        return
    demo_user_ids = [user.id for user in demo_users]
    demo_nurse_ids = list(
        session.scalars(select(Nurse.id).where(Nurse.user_id.in_(demo_user_ids)))
    )
    if demo_nurse_ids:
        session.execute(delete(Nurse).where(Nurse.id.in_(demo_nurse_ids)))
    session.execute(delete(TeamMember).where(TeamMember.user_id.in_(demo_user_ids)))
    session.execute(delete(Team).where(Team.name.in_(DEMO_TEAMS)))
    session.execute(delete(User).where(User.id.in_(demo_user_ids)))
    demo_service_codes = [item[0] for item in DEMO_SERVICES]
    demo_shift_codes = [item[0] for item in DEMO_SHIFTS]
    if demo_service_codes or demo_shift_codes:
        session.execute(
            delete(ServiceShift).where(
                or_(
                    ServiceShift.service_code.in_(demo_service_codes),
                    ServiceShift.shift_code.in_(demo_shift_codes),
                )
            )
        )
    if demo_service_codes:
        session.execute(delete(Service).where(Service.code.in_(demo_service_codes)))
    if demo_shift_codes:
        session.execute(delete(Shift).where(Shift.code.in_(demo_shift_codes)))
    if demo_service_codes or demo_shift_codes:
        session.execute(
            delete(MonthlyRequirement).where(
                or_(
                    MonthlyRequirement.service_code.in_(demo_service_codes),
                    MonthlyRequirement.shift_code.in_(demo_shift_codes),
                )
            )
        )
    session.flush()
