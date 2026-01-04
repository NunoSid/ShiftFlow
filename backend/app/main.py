from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, Response, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete, func, select, and_, or_
from sqlmodel import SQLModel, Session

from .config import (
    ACCENT_COLOR,
    APP_NAME,
    APP_LOGO_URL,
    BACKGROUND_COLOR,
    BASE_DIR,
    DATA_DIR,
    ORG_LOGO_URL,
    ORG_NAME,
    PRIMARY_COLOR,
    SHOW_APP_LOGO,
    SHOW_ORG_LOGO,
    HOST,
    PORT,
    SEED_MODE,
)
from .constants import (
    CONSTRAINT_CODES,
    DEFAULT_PENALTIES,
    MINUTES_PER_DAY,
    NURSE_CATEGORIES,
)
from .database import engine, get_session, run_migrations
from .defaults import (
    clear_demo_data,
    ensure_admin_user,
    ensure_default_categories,
    ensure_default_nurses,
    ensure_default_requirements,
    ensure_default_service_shifts,
    ensure_default_services,
    ensure_default_shifts,
    ensure_default_users,
    seed_demo_data,
)
from .excel import export_constraints, export_schedule, export_swaps
from .pdf import export_constraints_pdf, export_schedule_pdf, export_swap_pdf
from .holidays import month_holidays
from .models import (
    ChatMessage,
    ChatThreadState,
    ConstraintEntry,
    ManualHoliday,
    MonthlyRequirement,
    Nurse,
    NurseMonthAdjustment,
    NurseMonthStat,
    ProfessionalCategory,
    ScheduleEntry,
    ScheduleRelease,
    Service,
    ServiceShift,
    Setting,
    Shift,
    AvailabilityRequest,
    SwapDecision,
    SwapParticipant,
    SwapRequest,
    Team,
    TeamMember,
    User,
)
from .schemas import (
    AdjustmentBulkRequest,
    AdjustmentRead,
    AvailabilityBulkRequest,
    AvailabilityDecision,
    AvailabilityPendingRead,
    AvailabilityRequestRead,
    ConstraintBulkRequest,
    ConstraintRead,
    GenerateRequest,
    HolidayInfo,
    ManualHolidayCreate,
    ManualHolidaySchema,
    MonthConfigSchema,
    NurseCreate,
    NurseMoveRequest,
    NurseRead,
    NurseUpdate,
    RequirementBulkRequest,
    RequirementRead,
    ScheduleCellUpdate,
    ScheduleEntrySchema,
    ScheduleResponse,
    NurseStat,
    StatUpdateRequest,
    ShiftSchema,
    ShiftUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
    LoginRequest,
    TeamCreate,
    TeamRead,
    TeamUpdate,
    TeamMemberRequest,
    ProfessionalCategoryCreate,
    ProfessionalCategoryRead,
    ProfessionalCategoryUpdate,
    ServiceCreate,
    ServiceRead,
    ServiceUpdate,
    ShiftCreate,
    ShiftCatalogUpdate,
    ServiceShiftCreate,
    ChatMessageCreate,
    ChatMessageRead,
    ChatThreadRead,
    ChatThreadStateUpdate,
    SwapCreate,
    SwapDecisionRequest,
    SwapParticipantUpdate,
    SwapRead,
    ScheduleReleaseCreate,
    ScheduleReleaseRead,
    SettingsRead,
    SettingsUpdate,
)
from .solver import (
    _allows_double_shift,
    _contracted_target_minutes,
    collect_nurse_stats,
    generate_schedule,
    get_or_create_month_config,
)
from .shift_settings import refresh_shift_settings
from .utils import sort_nurses_by_category
from .auth import create_access_token, get_current_user, hash_password, require_roles, verify_password

app = FastAPI(title=f"{APP_NAME} API")

FRONTEND_PATH = BASE_DIR / "frontend"
UPLOADS_PATH = DATA_DIR / "uploads"
UPLOADS_PATH.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
def on_startup():
    run_migrations()
    SQLModel.metadata.create_all(engine)
    with get_session() as session:
        ensure_default_categories(session)
        if SEED_MODE == "demo":
            ensure_admin_user(session)
            seed_demo_data(session)
        elif SEED_MODE == "none":
            ensure_admin_user(session)
        else:
            ensure_default_services(session)
            ensure_default_shifts(session)
            ensure_default_service_shifts(session)
            ensure_default_nurses(session)
            ensure_default_users(session)


app.mount(
    "/static/uploads",
    StaticFiles(directory=str(UPLOADS_PATH)),
    name="uploads",
)
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_PATH)),
    name="static",
)


@app.get("/")
def serve_frontend():
    index_path = FRONTEND_PATH / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Interface não encontrada")
    return FileResponse(index_path)


@app.get("/login")
def serve_login():
    login_path = FRONTEND_PATH / "login.html"
    if not login_path.exists():
        raise HTTPException(status_code=404, detail="Login não encontrado")
    return FileResponse(login_path)


def get_db_session():
    with get_session() as session:
        yield session


LEGACY_PDF_INFO_TEXT = (
    "Santa Casa da Misericórdia de Lousada\n"
    "Serviço de Atendimento Permanente\n"
    "Serviço de Internamento Cirúrgico\n"
    "Serviço de Consulta Externa\n"
    "Serviço de Colheitas\n"
    "Morada: Av. Major Arrochela Lobo n.º 157, 4620-697, Lousada\n"
    "\n"
    "Atividade: Prestação de Cuidados de Saúde\n"
    "IRCT: 15681\n"
    "\n"
    "Periodo de Funcionamento: Segunda-Feira a Domingo\n"
    "\n"
    "Encerramento: Não Encerra"
)

SETTINGS_DEFAULTS = {
    "app_name": APP_NAME,
    "org_name": ORG_NAME,
    "app_logo_url": APP_LOGO_URL,
    "org_logo_url": ORG_LOGO_URL,
    "show_app_logo": SHOW_APP_LOGO,
    "show_org_logo": SHOW_ORG_LOGO,
    "primary_color": PRIMARY_COLOR,
    "accent_color": ACCENT_COLOR,
    "background": BACKGROUND_COLOR,
    "pdf_info_text": "",
}


def _setting_value(session: Session, key: str):
    record = session.get(Setting, key)
    if record is None:
        return SETTINGS_DEFAULTS.get(key)
    value = record.value
    if key == "pdf_info_text" and value == LEGACY_PDF_INFO_TEXT:
        return ""
    if key in {"show_app_logo", "show_org_logo"}:
        return value.lower() == "true"
    return value


def _update_setting(session: Session, key: str, value):
    if value is None:
        return
    record = session.get(Setting, key)
    if record:
        record.value = str(value)
    else:
        record = Setting(key=key, value=str(value))
        session.add(record)
    session.add(record)


def _user_with_nurse_id(session: Session, user: User) -> UserRead:
    nurse_id = session.scalar(select(Nurse.id).where(Nurse.user_id == user.id))
    data = UserRead.model_validate(user).model_dump()
    data["nurse_id"] = nurse_id
    return UserRead(**data)


@app.post("/api/auth/login")
def login(payload: LoginRequest, session: Session = Depends(get_db_session)):
    user = session.scalar(select(User).where(User.username == payload.username))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(user.id)
    return {"token": token, "user": _user_with_nurse_id(session, user)}


@app.get("/api/auth/me", response_model=UserRead)
def get_me(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session),
):
    db_user = session.get(User, user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return _user_with_nurse_id(session, db_user)


@app.get("/api/auth/users", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    return [_user_with_nurse_id(session, user) for user in session.scalars(select(User))]


@app.get("/api/users", response_model=List[UserRead])
def list_active_users(
    session: Session = Depends(get_db_session),
    _user: User = Depends(get_current_user),
):
    users = session.scalars(select(User).where(User.is_active))
    return [_user_with_nurse_id(session, user) for user in users]


@app.post("/api/auth/users", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    existing = session.scalar(select(User).where(User.username == payload.username))
    if existing:
        raise HTTPException(status_code=400, detail="Utilizador já existe")
    if payload.role not in {"ADMIN", "COORDENADOR"} and not _is_professional_role(
        session, payload.role
    ):
        raise HTTPException(status_code=400, detail="Perfil inválido")
    user = User(
        username=payload.username,
        full_name=payload.full_name,
        role=payload.role,
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    session.add(user)
    session.flush()
    session.refresh(user)
    category = _role_to_category(session, user.role)
    if category:
        service_role = _service_role_for_category(session, category)
        services_permitted = _service_shift_codes_for_role(session, service_role)
        max_order = session.scalar(select(func.max(Nurse.display_order))) or 0
        session.add(
            Nurse(
                name=user.full_name,
                category=category,
                services_permitted=services_permitted,
                can_work_night=True,
                weekly_hours=40,
                display_order=max_order + 1,
                user_id=user.id,
            )
        )
        session.flush()
    return _user_with_nurse_id(session, user)


@app.put("/api/auth/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    if payload.full_name is not None:
        user.full_name = payload.full_name
        nurse = session.scalar(select(Nurse).where(Nurse.user_id == user.id))
        if nurse:
            nurse.name = payload.full_name
            session.add(nurse)
    if payload.role is not None:
        if payload.role not in {"ADMIN", "COORDENADOR"} and not _is_professional_role(
            session, payload.role
        ):
            raise HTTPException(status_code=400, detail="Perfil inválido")
        user.role = payload.role
    if payload.password:
        user.password_hash = hash_password(payload.password)
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.role is not None:
        nurse = session.scalar(select(Nurse).where(Nurse.user_id == user.id))
        category = _role_to_category(session, user.role)
        if category and nurse:
            nurse.category = category
            session.add(nurse)
        elif category and not nurse:
            service_role = _service_role_for_category(session, category)
            services_permitted = _service_shift_codes_for_role(session, service_role)
            max_order = session.scalar(select(func.max(Nurse.display_order))) or 0
            session.add(
                Nurse(
                    name=user.full_name,
                    category=category,
                    services_permitted=services_permitted,
                    can_work_night=True,
                    weekly_hours=40,
                    display_order=max_order + 1,
                    user_id=user.id,
                )
            )
    session.add(user)
    session.flush()
    session.refresh(user)
    return _user_with_nurse_id(session, user)


def _delete_nurse_records(session: Session, nurse: Nurse) -> None:
    nurse_id = nurse.id
    session.execute(delete(ScheduleEntry).where(ScheduleEntry.nurse_id == nurse_id))
    session.execute(delete(ConstraintEntry).where(ConstraintEntry.nurse_id == nurse_id))
    session.execute(
        delete(NurseMonthAdjustment).where(NurseMonthAdjustment.nurse_id == nurse_id)
    )
    session.execute(
        delete(NurseMonthStat).where(NurseMonthStat.nurse_id == nurse_id)
    )
    session.execute(
        delete(AvailabilityRequest).where(AvailabilityRequest.nurse_id == nurse_id)
    )
    if nurse.user_id:
        session.execute(
            delete(AvailabilityRequest).where(
                AvailabilityRequest.user_id == nurse.user_id
            )
        )
        session.execute(
            delete(TeamMember).where(TeamMember.user_id == nurse.user_id)
        )
    session.delete(nurse)


@app.delete("/api/auth/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    nurse = session.scalar(select(Nurse).where(Nurse.user_id == user.id))
    if nurse:
        _delete_nurse_records(session, nurse)
    session.delete(user)
    session.flush()
    return Response(status_code=204)


@app.post("/api/demo/seed", status_code=204)
def create_demo_data(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    seed_demo_data(session)
    return Response(status_code=204)


@app.delete("/api/demo", status_code=204)
def delete_demo_data(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    clear_demo_data(session)
    return Response(status_code=204)


@app.get("/api/meta")
def get_meta(session: Session = Depends(get_db_session)):
    service_colors = {
        svc.code: svc.color for svc in session.scalars(select(Service)).all()
    }
    category_rows = list(session.scalars(select(ProfessionalCategory)))
    active_categories = [item for item in category_rows if item.is_active]
    fallback_categories = session.scalars(select(Nurse.category).distinct()).all()
    fallback = {cat for cat in fallback_categories if cat}
    fallback |= set(NURSE_CATEGORIES)
    for item in active_categories:
        fallback.discard(item.name)
    categories = sorted([item.name for item in active_categories] + list(fallback))
    category_map: dict[str, list[str]] = {}
    category_order: dict[str, int] = {}
    roles: set[str] = set()
    for item in active_categories:
        category_map.setdefault(item.role, []).append(item.name)
        category_order[item.name] = item.sort_order
        roles.add(item.role)
    for name in fallback:
        role = (
            "ASSISTENTE_OPERACIONAL"
            if name == "ASSISTENTE_OPERACIONAL"
            else "ENFERMEIRO"
        )
        category_map.setdefault(role, []).append(name)
        category_order.setdefault(name, 99)
        roles.add(role)
    for role, items in category_map.items():
        items.sort(key=lambda item: (category_order.get(item, 99), item))
    return {
        "service_shifts": _service_shifts_payload(session),
        "constraint_codes": CONSTRAINT_CODES,
        "categories": categories,
        "category_map": category_map,
        "category_order": category_order,
        "roles": sorted(roles),
        "default_penalties": DEFAULT_PENALTIES,
        "service_colors": service_colors,
    }


@app.get("/api/settings", response_model=SettingsRead)
def get_settings(session: Session = Depends(get_db_session)):
    return {
        "app_name": _setting_value(session, "app_name"),
        "org_name": _setting_value(session, "org_name"),
        "app_logo_url": _setting_value(session, "app_logo_url"),
        "org_logo_url": _setting_value(session, "org_logo_url"),
        "show_app_logo": _setting_value(session, "show_app_logo"),
        "show_org_logo": _setting_value(session, "show_org_logo"),
        "primary_color": _setting_value(session, "primary_color"),
        "accent_color": _setting_value(session, "accent_color"),
        "background": _setting_value(session, "background"),
        "pdf_info_text": _setting_value(session, "pdf_info_text"),
    }


@app.put("/api/settings", response_model=SettingsRead)
def update_settings(
    payload: SettingsUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    _update_setting(session, "app_name", payload.app_name)
    _update_setting(session, "org_name", payload.org_name)
    _update_setting(session, "app_logo_url", payload.app_logo_url)
    _update_setting(session, "org_logo_url", payload.org_logo_url)
    if payload.show_app_logo is not None:
        _update_setting(session, "show_app_logo", payload.show_app_logo)
    if payload.show_org_logo is not None:
        _update_setting(session, "show_org_logo", payload.show_org_logo)
    _update_setting(session, "primary_color", payload.primary_color)
    _update_setting(session, "accent_color", payload.accent_color)
    _update_setting(session, "background", payload.background)
    _update_setting(session, "pdf_info_text", payload.pdf_info_text)
    session.flush()
    return get_settings(session)


@app.get("/api/categories", response_model=List[ProfessionalCategoryRead])
def list_categories(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    return list(session.scalars(select(ProfessionalCategory).order_by(ProfessionalCategory.sort_order, ProfessionalCategory.name)))


@app.post("/api/categories", response_model=ProfessionalCategoryRead, status_code=201)
def create_category(
    payload: ProfessionalCategoryCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    role = payload.role.strip()
    if not role:
        raise HTTPException(status_code=400, detail="Perfil inválido")
    existing = session.scalar(
        select(ProfessionalCategory).where(
            ProfessionalCategory.name == payload.name,
            ProfessionalCategory.role == role,
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    category = ProfessionalCategory(
        name=payload.name,
        role=role,
        sort_order=payload.sort_order,
        is_active=payload.is_active,
    )
    session.add(category)
    session.flush()
    session.refresh(category)
    return category


@app.put("/api/categories/{category_id}", response_model=ProfessionalCategoryRead)
def update_category(
    category_id: int,
    payload: ProfessionalCategoryUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    category = session.get(ProfessionalCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    update_data = payload.dict(exclude_unset=True)
    if "role" in update_data:
        role = update_data["role"].strip()
        if not role:
            raise HTTPException(status_code=400, detail="Perfil inválido")
        update_data["role"] = role
    new_name = update_data.get("name", category.name)
    new_role = update_data.get("role", category.role)
    exists = session.scalar(
        select(ProfessionalCategory).where(
            ProfessionalCategory.name == new_name,
            ProfessionalCategory.role == new_role,
            ProfessionalCategory.id != category_id,
        )
    )
    if exists:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    old_name = category.name
    for key, value in update_data.items():
        setattr(category, key, value)
    if payload.name and payload.name != old_name:
        for nurse in session.scalars(select(Nurse).where(Nurse.category == old_name)):
            nurse.category = payload.name
            session.add(nurse)
    session.add(category)
    session.flush()
    session.refresh(category)
    return category


@app.delete("/api/categories/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    category = session.get(ProfessionalCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    used = session.scalar(
        select(func.count()).select_from(Nurse).where(Nurse.category == category.name)
    )
    if used and used > 0:
        raise HTTPException(
            status_code=400,
            detail="Não é possível apagar: categoria associada a profissionais",
        )
    session.delete(category)
    session.flush()
    return Response(status_code=204)


@app.post("/api/settings/logo", response_model=SettingsRead)
def upload_logo(
    target: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN")),
):
    target = target.lower()
    if target not in {"app", "org"}:
        raise HTTPException(status_code=400, detail="Destino inválido")
    if not file.filename:
        raise HTTPException(status_code=400, detail="Ficheiro inválido")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
        raise HTTPException(status_code=400, detail="Formato inválido")
    filename = f"{target}_logo{suffix}"
    dest = UPLOADS_PATH / filename
    content = file.file.read()
    dest.write_bytes(content)
    logo_url = f"/static/uploads/{filename}"
    if target == "app":
        _update_setting(session, "app_logo_url", logo_url)
    else:
        _update_setting(session, "org_logo_url", logo_url)
    session.flush()
    return get_settings(session)


def _shift_to_schema(shift) -> ShiftSchema:
    return ShiftSchema(
        code=shift.code,
        service=shift.service,
        label=shift.label,
        shift_type=shift.shift_type,
        start_minute=shift.start_minute,
        end_minute=shift.end_minute,
        minutes=shift.minutes,
    )


def _service_shifts_payload(session: Session):
    rows = session.exec(
        select(ServiceShift, Service, Shift)
        .join(Service, Service.code == ServiceShift.service_code)
        .join(Shift, Shift.code == ServiceShift.shift_code)
        .where(Service.is_active == True)
    ).all()
    payload = []
    for mapping, service, shift in rows:
        end_minute = shift.end_minute
        start_minute = shift.start_minute
        minutes = (
            end_minute - start_minute
            if end_minute > start_minute
            else MINUTES_PER_DAY - start_minute + end_minute
        )
        payload.append(
            {
                "service": service.name,
                "service_code": service.code,
                "service_role": service.role,
                "code": shift.code,
                "label": shift.label,
                "shift_type": shift.shift_type,
                "start_minute": start_minute,
                "end_minute": end_minute,
                "minutes": minutes,
            }
        )
    return payload


def _parse_time_string(value: str) -> int:
    if not value:
        raise HTTPException(status_code=400, detail="Hora inválida")
    value = value.strip()
    if len(value.split(":")) != 2:
        raise HTTPException(status_code=400, detail="Formato deve ser HH:MM")
    hours, minutes = value.split(":")
    try:
        hour = int(hours)
        minute = int(minutes)
    except ValueError as exc:  # pragma: no cover - validado pelo bloco acima
        raise HTTPException(status_code=400, detail="Hora inválida") from exc
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise HTTPException(status_code=400, detail="Hora inválida")
    return hour * 60 + minute


def _resolve_logo_path(url: str | None) -> str | None:
    if not url:
        return None
    if url.startswith("/static/uploads/"):
        relative = url.replace("/static/uploads/", "", 1)
        path = UPLOADS_PATH / relative
    elif url.startswith("/static/"):
        relative = url.replace("/static/", "", 1)
        path = FRONTEND_PATH / relative
    else:
        path = Path(url)
    if path.exists():
        return str(path)
    return None


def _export_branding(session: Session) -> tuple[str, str, str | None, str | None]:
    app_name = _setting_value(session, "app_name") or APP_NAME
    org_name = _setting_value(session, "org_name") or ORG_NAME
    show_app_logo = _setting_value(session, "show_app_logo")
    show_org_logo = _setting_value(session, "show_org_logo")
    app_logo_url = _setting_value(session, "app_logo_url") if show_app_logo else None
    org_logo_url = _setting_value(session, "org_logo_url") if show_org_logo else None
    return (
        app_name,
        org_name,
        _resolve_logo_path(app_logo_url),
        _resolve_logo_path(org_logo_url),
    )


def _role_names(session: Session) -> List[str]:
    roles = list(
        {
            role
            for role in session.scalars(select(ProfessionalCategory.role)).all()
            if role
        }
    )
    if not roles:
        roles = ["ENFERMEIRO", "ASSISTENTE_OPERACIONAL"]
    return sorted(roles)


def _role_for_group(session: Session, group: str | None) -> str | None:
    normalized = (group or "").strip().lower()
    if normalized in {"ao", "assistente_operacional", "assistente operacional"}:
        return "ASSISTENTE_OPERACIONAL"
    if normalized in {"enf", "enfermagem"}:
        return "ENFERMEIRO"
    for role in _role_names(session):
        if role.lower() == normalized:
            return role
    return None


def _category_names_for_role(session: Session, role: str) -> List[str]:
    return list(
        session.scalars(
            select(ProfessionalCategory.name).where(
                ProfessionalCategory.role == role,
                ProfessionalCategory.is_active.is_(True),
            )
        )
    )


def _nurse_ids_for_group(session: Session, group: str | None) -> List[int]:
    role = _role_for_group(session, group)
    if not role:
        return []
    categories = _category_names_for_role(session, role)
    query = select(Nurse.id)
    if categories:
        query = query.where(Nurse.category.in_(categories))
    else:
        query = query.where(Nurse.category == role)
    return list(session.scalars(query))


def _service_codes_for_group(session: Session, group: str | None) -> List[str]:
    role = _role_for_group(session, group)
    if not role:
        return []
    return list(session.scalars(select(Service.code).where(Service.role == role)))


def _role_to_category(session: Session, role: str) -> str | None:
    if role == "COORDENADOR":
        coordinator = session.scalar(
            select(ProfessionalCategory.name).where(
                ProfessionalCategory.name == "COORDENADOR"
            )
        )
        if coordinator:
            return coordinator
        role = "ENFERMEIRO"
    category = session.scalar(
        select(ProfessionalCategory.name)
        .where(ProfessionalCategory.role == role)
        .order_by(ProfessionalCategory.sort_order, ProfessionalCategory.name)
    )
    return category


def _service_role_for_category(session: Session, category_name: str) -> str:
    role = session.scalar(
        select(ProfessionalCategory.role).where(ProfessionalCategory.name == category_name)
    )
    return role or category_name


def _service_shift_codes_for_role(session: Session, role: str) -> List[str]:
    codes = session.exec(
        select(ServiceShift.shift_code)
        .join(Service, Service.code == ServiceShift.service_code)
        .where(Service.role == role)
    ).all()
    return list({code for code in codes})


def _is_professional_role(session: Session, role: str | None) -> bool:
    if not role:
        return False
    return role in _role_names(session)


def _nurse_for_user(session: Session, user_id: int) -> Nurse:
    nurse = session.scalar(select(Nurse).where(Nurse.user_id == user_id))
    if not nurse:
        raise HTTPException(status_code=400, detail="Utilizador sem perfil profissional")
    return nurse


def _team_ids_for_user(session: Session, user_id: int) -> List[int]:
    return list(
        session.scalars(
            select(TeamMember.team_id).where(TeamMember.user_id == user_id)
        )
    )


def _team_member_user_ids(session: Session, team_ids: List[int]) -> List[int]:
    if not team_ids:
        return []
    return list(
        {
            user_id
            for user_id in session.scalars(
                select(TeamMember.user_id).where(TeamMember.team_id.in_(team_ids))
            )
        }
    )


def _recalculate_nurse_stat(session: Session, nurse_id: int, year: int, month: int) -> None:
    nurse = session.get(Nurse, nurse_id)
    if not nurse:
        return
    shifts = {shift.code: shift for shift in session.scalars(select(Shift))}
    entries = list(
        session.scalars(
            select(ScheduleEntry).where(
                ScheduleEntry.year == year,
                ScheduleEntry.month == month,
                ScheduleEntry.nurse_id == nurse_id,
            )
        )
    )
    actual_minutes = 0
    for entry in entries:
        if entry.service_code == "REST":
            continue
        shift = shifts.get(entry.shift_code)
        if not shift:
            continue
        end_minute = shift.end_minute
        start_minute = shift.start_minute
        minutes = (
            end_minute - start_minute
            if end_minute > start_minute
            else MINUTES_PER_DAY - start_minute + end_minute
        )
        actual_minutes += minutes
    adjustment = session.scalar(
        select(NurseMonthAdjustment).where(
            NurseMonthAdjustment.year == year,
            NurseMonthAdjustment.month == month,
            NurseMonthAdjustment.nurse_id == nurse_id,
        )
    )
    if adjustment:
        actual_minutes += adjustment.extra_minutes
        actual_minutes -= adjustment.reduced_minutes
    constraint_map = {
        (item.nurse_id, item.day): item.code
        for item in session.scalars(
            select(ConstraintEntry).where(
                ConstraintEntry.year == year,
                ConstraintEntry.month == month,
                ConstraintEntry.nurse_id == nurse_id,
            )
        )
    }
    target_minutes = _contracted_target_minutes(
        nurse, year, month, constraint_map, adjustment
    )
    if target_minutes is None:
        target_minutes = 0
    stat = session.scalar(
        select(NurseMonthStat).where(
            NurseMonthStat.year == year,
            NurseMonthStat.month == month,
            NurseMonthStat.nurse_id == nurse_id,
        )
    )
    old_delta = stat.delta_minutes if stat else 0
    if not stat:
        stat = NurseMonthStat(
            nurse_id=nurse_id,
            year=year,
            month=month,
            target_minutes=target_minutes,
            actual_minutes=actual_minutes,
            delta_minutes=actual_minutes - target_minutes,
        )
    else:
        stat.target_minutes = target_minutes
        stat.actual_minutes = actual_minutes
        stat.delta_minutes = actual_minutes - target_minutes
    nurse.hour_balance_minutes += stat.delta_minutes - old_delta
    session.add(stat)
    session.add(nurse)


def _nurse_ids_for_users(session: Session, user_ids: List[int]) -> List[int]:
    if not user_ids:
        return []
    return list(
        session.scalars(select(Nurse.id).where(Nurse.user_id.in_(user_ids)))
    )


@app.get("/api/teams", response_model=List[TeamRead])
def list_teams(
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    role = _role_for_group(session, group)
    query = select(Team)
    if role:
        query = query.where(Team.role == role)
    return list(session.scalars(query).all())


@app.post("/api/teams", response_model=TeamRead, status_code=201)
def create_team(
    payload: TeamCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    if not _is_professional_role(session, payload.role):
        raise HTTPException(status_code=400, detail="Perfil inválido")
    team = Team(
        name=payload.name,
        service_code=payload.service_code,
        role=payload.role,
    )
    session.add(team)
    session.flush()
    session.refresh(team)
    return team


@app.put("/api/teams/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int,
    payload: TeamUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    if payload.role and not _is_professional_role(session, payload.role):
        raise HTTPException(status_code=400, detail="Perfil inválido")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(team, key, value)
    session.add(team)
    session.flush()
    session.refresh(team)
    return team


@app.delete("/api/teams/{team_id}", status_code=204)
def delete_team(
    team_id: int,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    session.execute(delete(TeamMember).where(TeamMember.team_id == team_id))
    session.delete(team)
    session.flush()
    return Response(status_code=204)


@app.get("/api/teams/{team_id}/members", response_model=List[UserRead])
def list_team_members(
    team_id: int,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    user_ids = list(
        session.scalars(
            select(TeamMember.user_id).where(TeamMember.team_id == team_id)
        )
    )
    if not user_ids:
        return []
    return list(session.scalars(select(User).where(User.id.in_(user_ids))))


@app.put("/api/teams/{team_id}/members", status_code=204)
def update_team_members(
    team_id: int,
    payload: TeamMemberRequest,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    if payload.user_ids:
        allowed_roles = (
            {"ENFERMEIRO", "COORDENADOR"}
            if team.role == "ENFERMEIRO"
            else {team.role}
        )
        invalid = list(
            session.scalars(
                select(User.id).where(
                    User.id.in_(payload.user_ids),
                    User.role.notin_(allowed_roles),
                )
            )
        )
        if invalid:
            raise HTTPException(
                status_code=400,
                detail="Utilizadores com perfil incompatível",
            )
    session.execute(delete(TeamMember).where(TeamMember.team_id == team_id))
    for user_id in payload.user_ids:
        session.add(TeamMember(team_id=team_id, user_id=user_id))
    session.flush()
    return Response(status_code=204)


@app.get("/api/services", response_model=List[ServiceRead])
def list_services(
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    role = _role_for_group(session, group)
    query = select(Service)
    if role:
        query = query.where(Service.role == role)
    return list(session.scalars(query).all())


@app.post("/api/services", response_model=ServiceRead, status_code=201)
def create_service(
    payload: ServiceCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    if not _is_professional_role(session, payload.role):
        raise HTTPException(status_code=400, detail="Perfil inválido")
    existing_codes = {
        code for code in session.scalars(select(Service.code)).all()
    }
    code = payload.code
    if code in existing_codes:
        if payload.role == "ASSISTENTE_OPERACIONAL":
            suffix = "AO"
        elif payload.role == "ENFERMEIRO":
            suffix = "ENF"
        else:
            suffix = payload.role
        base = f"{code} - {suffix}"
        candidate = base
        counter = 2
        while candidate in existing_codes:
            candidate = f"{base} {counter}"
            counter += 1
        code = candidate
    service = Service(
        code=code,
        name=payload.name,
        color=payload.color,
        role=payload.role,
        is_active=True,
    )
    session.add(service)
    session.flush()
    session.refresh(service)
    return service


@app.put("/api/services/{code}", response_model=ServiceRead)
def update_service(
    code: str,
    payload: ServiceUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    service = session.get(Service, code)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    if payload.role and not _is_professional_role(session, payload.role):
        raise HTTPException(status_code=400, detail="Perfil inválido")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)
    session.add(service)
    session.flush()
    session.refresh(service)
    return service


@app.delete("/api/services/{code}", status_code=204)
def delete_service(
    code: str,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    service = session.get(Service, code)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    session.execute(delete(ServiceShift).where(ServiceShift.service_code == code))
    session.delete(service)
    session.flush()
    return Response(status_code=204)


@app.get("/api/shifts/catalog", response_model=List[Shift])
def list_shift_catalog(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    return list(session.scalars(select(Shift)).all())


@app.post("/api/shifts/catalog", response_model=Shift, status_code=201)
def create_shift_catalog(
    payload: ShiftCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    start = _parse_time_string(payload.start_time)
    end = _parse_time_string(payload.end_time)
    if end <= start:
        end += MINUTES_PER_DAY
    shift = Shift(
        code=payload.code,
        label=payload.label,
        shift_type=payload.shift_type,
        start_minute=start,
        end_minute=end,
    )
    session.add(shift)
    session.flush()
    session.refresh(shift)
    return shift


@app.put("/api/shifts/catalog/{code}", response_model=Shift)
def update_shift_catalog(
    code: str,
    payload: ShiftCatalogUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    shift = session.get(Shift, code)
    if not shift:
        raise HTTPException(status_code=404, detail="Turno não encontrado")
    if payload.label is not None:
        shift.label = payload.label
    if payload.shift_type is not None:
        shift.shift_type = payload.shift_type
    start_minute = shift.start_minute
    end_minute = shift.end_minute
    if payload.start_time is not None:
        start_minute = _parse_time_string(payload.start_time)
    if payload.end_time is not None:
        end_minute = _parse_time_string(payload.end_time)
    if end_minute <= start_minute:
        end_minute += MINUTES_PER_DAY
    shift.start_minute = start_minute
    shift.end_minute = end_minute
    session.add(shift)
    session.flush()
    session.refresh(shift)
    return shift


@app.delete("/api/shifts/catalog/{code}", status_code=204)
def delete_shift_catalog(
    code: str,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    shift = session.get(Shift, code)
    if not shift:
        raise HTTPException(status_code=404, detail="Turno não encontrado")
    session.execute(delete(ServiceShift).where(ServiceShift.shift_code == code))
    session.delete(shift)
    session.flush()
    return Response(status_code=204)


@app.post("/api/service-shifts", status_code=201)
def create_service_shift(
    payload: ServiceShiftCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    service = session.get(Service, payload.service_code)
    shift = session.get(Shift, payload.shift_code)
    if not service or not shift:
        raise HTTPException(status_code=400, detail="Serviço/turno inválido")
    existing = session.scalar(
        select(ServiceShift).where(
            ServiceShift.service_code == payload.service_code,
            ServiceShift.shift_code == payload.shift_code,
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail="Ligação já existe")
    session.add(
        ServiceShift(
            service_code=payload.service_code,
            shift_code=payload.shift_code,
        )
    )
    session.flush()
    return {"status": "ok"}


@app.delete("/api/service-shifts", status_code=204)
def delete_service_shift(
    service_code: str = Query(...),
    shift_code: str = Query(...),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    session.execute(
        delete(ServiceShift).where(
            ServiceShift.service_code == service_code,
            ServiceShift.shift_code == shift_code,
        )
    )
    session.flush()
    return Response(status_code=204)


def _ensure_thread_state(session: Session, user_id: int, peer_id: int) -> ChatThreadState:
    state = session.scalar(
        select(ChatThreadState).where(
            ChatThreadState.user_id == user_id,
            ChatThreadState.peer_id == peer_id,
        )
    )
    if state:
        return state
    state = ChatThreadState(user_id=user_id, peer_id=peer_id)
    session.add(state)
    session.flush()
    return state


def _touch_thread_for_message(session: Session, user_id: int, peer_id: int) -> None:
    state = _ensure_thread_state(session, user_id, peer_id)
    if state.is_deleted:
        state.is_deleted = False
    session.add(state)


@app.get("/api/chat/threads", response_model=List[ChatThreadRead])
def list_chat_threads(
    include_archived: bool = Query(False),
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    messages = list(
        session.scalars(
            select(ChatMessage)
            .where(
                or_(
                    ChatMessage.from_user_id == user.id,
                    ChatMessage.to_user_id == user.id,
                )
            )
            .order_by(ChatMessage.created_at.desc())
        )
    )
    thread_map = {}
    for message in messages:
        peer_id = (
            message.to_user_id
            if message.from_user_id == user.id
            else message.from_user_id
        )
        if peer_id is None:
            continue
        if peer_id in thread_map:
            continue
        state = session.scalar(
            select(ChatThreadState).where(
                ChatThreadState.user_id == user.id,
                ChatThreadState.peer_id == peer_id,
            )
        )
        if state and state.is_deleted:
            continue
        if state and state.is_archived and not include_archived:
            continue
        last_read = state.last_read_at if state else None
        if last_read:
            unread_count = (
                session.scalar(
                    select(func.count(ChatMessage.id)).where(
                        ChatMessage.from_user_id == peer_id,
                        ChatMessage.to_user_id == user.id,
                        ChatMessage.created_at > last_read,
                    )
                )
                or 0
            )
        else:
            unread_count = (
                session.scalar(
                    select(func.count(ChatMessage.id)).where(
                        ChatMessage.from_user_id == peer_id,
                        ChatMessage.to_user_id == user.id,
                    )
                )
                or 0
            )
        peer = session.get(User, peer_id)
        if not peer:
            continue
        thread_map[peer_id] = {
            "peer_id": peer_id,
            "peer_name": peer.full_name,
            "peer_role": peer.role,
            "last_message": message.message,
            "last_at": message.created_at.isoformat(),
            "unread_count": unread_count,
            "is_archived": bool(state.is_archived) if state else False,
        }
    return list(thread_map.values())


@app.get("/api/chat/messages", response_model=List[ChatMessageRead])
def list_chat_messages(
    peer_id: int = Query(...),
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    messages = list(
        session.scalars(
            select(ChatMessage)
            .where(
                or_(
                    and_(
                        ChatMessage.from_user_id == user.id,
                        ChatMessage.to_user_id == peer_id,
                    ),
                    and_(
                        ChatMessage.from_user_id == peer_id,
                        ChatMessage.to_user_id == user.id,
                    ),
                )
            )
            .order_by(ChatMessage.created_at.asc())
        )
    )
    state = _ensure_thread_state(session, user.id, peer_id)
    state.last_read_at = datetime.utcnow()
    session.add(state)
    session.flush()
    return [
        ChatMessageRead(
            id=item.id,
            from_user_id=item.from_user_id,
            to_user_id=item.to_user_id,
            to_role=item.to_role,
            message=item.message,
            created_at=item.created_at.isoformat(),
        )
        for item in messages
    ]


@app.post("/api/chat/messages", response_model=ChatMessageRead, status_code=201)
def send_chat_message(
    payload: ChatMessageCreate,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    if not payload.to_user_id and not payload.to_role and not payload.to_user_ids and not payload.to_all:
        raise HTTPException(status_code=400, detail="Destino inválido")
    targets = []
    if payload.to_all:
        targets = list(
            session.scalars(select(User.id).where(User.is_active.is_(True)))
        )
    elif payload.to_user_ids:
        targets = list({int(value) for value in payload.to_user_ids})
    elif payload.to_user_id:
        targets = [payload.to_user_id]
    elif payload.to_role:
        targets = list(
            session.scalars(
                select(User.id).where(User.role == payload.to_role, User.is_active)
            )
        )
    targets = [target for target in targets if target and target != user.id]
    if not targets:
        raise HTTPException(status_code=400, detail="Destino inválido")
    created = None
    for target_id in targets:
        message = ChatMessage(
            from_user_id=user.id,
            to_user_id=target_id,
            to_role=payload.to_role,
            message=payload.message,
        )
        session.add(message)
        session.flush()
        _touch_thread_for_message(session, user.id, target_id)
        _touch_thread_for_message(session, target_id, user.id)
        created = message
    session.flush()
    return ChatMessageRead(
        id=created.id,
        from_user_id=created.from_user_id,
        to_user_id=created.to_user_id,
        to_role=created.to_role,
        message=created.message,
        created_at=created.created_at.isoformat(),
    )


@app.put("/api/chat/threads/{peer_id}", status_code=204)
def update_thread_state(
    peer_id: int,
    payload: ChatThreadStateUpdate,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    state = _ensure_thread_state(session, user.id, peer_id)
    if payload.is_archived is not None:
        state.is_archived = payload.is_archived
    if payload.is_deleted is not None:
        state.is_deleted = payload.is_deleted
    session.add(state)
    session.flush()
    return Response(status_code=204)


@app.get("/api/nurses", response_model=List[NurseRead])
def list_nurses(
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(get_current_user),
):
    query = select(Nurse)
    role = _role_for_group(session, group)
    if role:
        categories = _category_names_for_role(session, role)
        if categories:
            query = query.where(Nurse.category.in_(categories))
        else:
            query = query.where(Nurse.category == role)
    nurses = list(session.scalars(query))
    return sort_nurses_by_category(nurses)


@app.post("/api/nurses", response_model=NurseRead, status_code=201)
def create_nurse(
    nurse: NurseCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    if not nurse.user_id:
        raise HTTPException(status_code=400, detail="Utilizador obrigatório")
    existing_link = session.scalar(
        select(Nurse).where(Nurse.user_id == nurse.user_id)
    )
    if existing_link:
        raise HTTPException(status_code=400, detail="Utilizador já associado")
    max_order = session.scalar(select(func.max(Nurse.display_order))) or 0
    payload = nurse.dict()
    db_nurse = Nurse(**payload, display_order=max_order + 1)
    session.add(db_nurse)
    session.flush()
    session.refresh(db_nurse)
    return db_nurse


@app.put("/api/nurses/{nurse_id}", response_model=NurseRead)
def update_nurse(
    nurse_id: int,
    payload: NurseUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    db_nurse = session.get(Nurse, nurse_id)
    if not db_nurse:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    if payload.user_id is not None:
        existing_link = session.scalar(
            select(Nurse).where(
                Nurse.user_id == payload.user_id,
                Nurse.id != nurse_id,
            )
        )
        if existing_link:
            raise HTTPException(status_code=400, detail="Utilizador já associado")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_nurse, key, value)
    session.add(db_nurse)
    session.flush()
    session.refresh(db_nurse)
    return db_nurse


@app.delete("/api/nurses/{nurse_id}", status_code=204)
def delete_nurse(
    nurse_id: int,
    session: Session = Depends(get_db_session),
    _user: User = Depends(get_current_user),
):
    db_nurse = session.get(Nurse, nurse_id)
    if not db_nurse:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    _delete_nurse_records(session, db_nurse)
    session.flush()
    return Response(status_code=204)


@app.post("/api/nurses/{nurse_id}/move", response_model=NurseRead)
def move_nurse(
    nurse_id: int,
    payload: NurseMoveRequest,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    direction = (payload.direction or "").lower()
    if direction not in {"up", "down"}:
        raise HTTPException(status_code=400, detail="Direção inválida (up/down)")
    nurse = session.get(Nurse, nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    order_clause = [Nurse.display_order, Nurse.name]
    peers = list(
        session.scalars(
            select(Nurse)
            .where(Nurse.category == nurse.category)
            .order_by(*order_clause)
        )
    )
    current_index = next(
        (idx for idx, item in enumerate(peers) if item.id == nurse_id), None
    )
    if current_index is None:
        return nurse
    delta = -1 if direction == "up" else 1
    swap_index = current_index + delta
    if swap_index < 0 or swap_index >= len(peers):
        return nurse
    target = peers.pop(current_index)
    peers.insert(swap_index, target)
    for idx, item in enumerate(peers):
        item.display_order = idx
        session.add(item)
    session.flush()
    session.refresh(nurse)
    return nurse


@app.get("/api/shifts", response_model=List[ShiftSchema])
def list_shifts(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    rows = session.exec(
        select(Shift, ServiceShift, Service)
        .join(ServiceShift, ServiceShift.shift_code == Shift.code)
        .join(Service, Service.code == ServiceShift.service_code)
    ).all()
    payload = []
    for shift, mapping, service in rows:
        end_minute = shift.end_minute
        start_minute = shift.start_minute
        minutes = (
            end_minute - start_minute
            if end_minute > start_minute
            else MINUTES_PER_DAY - start_minute + end_minute
        )
        payload.append(
            ShiftSchema(
                code=shift.code,
                service=service.name,
                label=shift.label,
                shift_type=shift.shift_type,
                start_minute=start_minute,
                end_minute=end_minute,
                minutes=minutes,
            )
        )
    return payload


@app.put("/api/shifts/{code}", response_model=ShiftSchema)
def update_shift_definition(
    code: str,
    payload: ShiftUpdate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    shift = session.get(Shift, code)
    if not shift:
        raise HTTPException(status_code=404, detail="Turno não encontrado")
    start = _parse_time_string(payload.start_time)
    end = _parse_time_string(payload.end_time)
    if end <= start:
        end += MINUTES_PER_DAY
    shift.start_minute = start
    shift.end_minute = end
    session.add(shift)
    session.flush()
    refresh_shift_settings(session)
    service_link = session.exec(
        select(ServiceShift, Service)
        .join(Service, Service.code == ServiceShift.service_code)
        .where(ServiceShift.shift_code == code)
    ).first()
    service_name = service_link[1].name if service_link else ""
    minutes = (
        end - start
        if end > start
        else MINUTES_PER_DAY - start + end
    )
    return ShiftSchema(
        code=shift.code,
        service=service_name,
        label=shift.label,
        shift_type=shift.shift_type,
        start_minute=start,
        end_minute=end,
        minutes=minutes,
    )


@app.get("/api/requirements", response_model=List[RequirementRead])
def list_requirements(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    ensure_default_requirements(session, year, month)
    query = select(MonthlyRequirement).where(
        MonthlyRequirement.year == year,
        MonthlyRequirement.month == month,
    )
    group_codes = _service_codes_for_group(session, group)
    if group and not group_codes:
        return []
    if group_codes:
        query = query.where(MonthlyRequirement.service_code.in_(group_codes))
    return list(session.scalars(query))


@app.post("/api/requirements/bulk", status_code=204)
def save_requirements(
    payload: RequirementBulkRequest,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    service_codes = list({item.service_code for item in payload.items})
    if not service_codes and payload.group:
        service_codes = _service_codes_for_group(session, payload.group)
    if service_codes:
        session.execute(
            delete(MonthlyRequirement).where(
                MonthlyRequirement.year == payload.year,
                MonthlyRequirement.month == payload.month,
                MonthlyRequirement.service_code.in_(service_codes),
            )
        )
    elif not payload.items:
        return Response(status_code=204)
    for item in payload.items:
        session.add(
            MonthlyRequirement(
                year=payload.year,
                month=payload.month,
                day=item.day,
                service_code=item.service_code,
                shift_code=item.shift_code,
                required_count=item.required_count,
            )
        )
    session.flush()
    return Response(status_code=204)


@app.get("/api/constraints", response_model=List[ConstraintRead])
def list_constraints(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    query = select(ConstraintEntry).where(
        ConstraintEntry.year == year,
        ConstraintEntry.month == month,
    )
    nurse_ids = _nurse_ids_for_group(session, group)
    if group and not nurse_ids:
        return []
    if nurse_ids:
        query = query.where(ConstraintEntry.nurse_id.in_(nurse_ids))
    return list(session.scalars(query))


@app.get("/api/availability/current", response_model=List[ConstraintRead])
def list_my_constraints(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    nurse = _nurse_for_user(session, user.id)
    query = select(ConstraintEntry).where(
        ConstraintEntry.year == year,
        ConstraintEntry.month == month,
        ConstraintEntry.nurse_id == nurse.id,
    )
    return list(session.scalars(query))


@app.get("/api/availability/requests", response_model=List[AvailabilityRequestRead])
def list_my_availability_requests(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    query = select(AvailabilityRequest).where(
        AvailabilityRequest.user_id == user.id,
        AvailabilityRequest.year == year,
        AvailabilityRequest.month == month,
    )
    return list(session.scalars(query))


@app.post("/api/availability/requests/bulk", status_code=204)
def create_availability_requests(
    payload: AvailabilityBulkRequest,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    nurse = _nurse_for_user(session, user.id)
    session.execute(
        delete(AvailabilityRequest).where(
            AvailabilityRequest.user_id == user.id,
            AvailabilityRequest.year == payload.year,
            AvailabilityRequest.month == payload.month,
            AvailabilityRequest.status == "PENDING",
        )
    )
    day_map = {}
    for item in payload.items:
        if item.code != "__CLEAR__" and item.code not in CONSTRAINT_CODES:
            raise HTTPException(status_code=400, detail="Código inválido")
        day_map[item.day] = item.code
    for day, code in day_map.items():
        session.add(
            AvailabilityRequest(
                user_id=user.id,
                nurse_id=nurse.id,
                year=payload.year,
                month=payload.month,
                day=day,
                code=code,
                status="PENDING",
            )
        )
    session.flush()
    return Response(status_code=204)


@app.get(
    "/api/availability/requests/pending",
    response_model=List[AvailabilityPendingRead],
)
def list_pending_availability_requests(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    role = _role_for_group(session, group)
    role_filter = None
    if role == "ENFERMEIRO":
        role_filter = ["ENFERMEIRO", "COORDENADOR"]
    elif role:
        role_filter = [role]
    query = (
        select(AvailabilityRequest, User)
        .join(User, User.id == AvailabilityRequest.user_id)
        .where(
            AvailabilityRequest.year == year,
            AvailabilityRequest.month == month,
            AvailabilityRequest.status == "PENDING",
        )
    )
    if role_filter:
        query = query.where(User.role.in_(role_filter))
    rows = session.exec(query).all()
    return [
        AvailabilityPendingRead(
            id=req.id,
            year=req.year,
            month=req.month,
            day=req.day,
            code=req.code,
            status=req.status,
            reason=req.reason,
            created_at=req.created_at.isoformat(),
            user_id=req.user_id,
            nurse_id=req.nurse_id,
            user_name=user.full_name,
            user_role=user.role,
        )
        for req, user in rows
    ]


@app.put(
    "/api/availability/requests/{request_id}/decision",
    response_model=AvailabilityRequestRead,
)
def decide_availability_request(
    request_id: int,
    payload: AvailabilityDecision,
    session: Session = Depends(get_db_session),
    user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    req = session.get(AvailabilityRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if req.status != "PENDING":
        raise HTTPException(status_code=400, detail="Pedido já tratado")
    if payload.status not in {"APPROVED", "REJECTED"}:
        raise HTTPException(status_code=400, detail="Estado inválido")
    req.status = payload.status
    req.reason = payload.reason
    req.decided_by = user.id
    req.decided_at = datetime.utcnow()
    session.add(req)
    if payload.status == "APPROVED":
        session.execute(
            delete(ConstraintEntry).where(
                ConstraintEntry.nurse_id == req.nurse_id,
                ConstraintEntry.year == req.year,
                ConstraintEntry.month == req.month,
                ConstraintEntry.day == req.day,
            )
        )
        if req.code != "__CLEAR__":
            session.add(
                ConstraintEntry(
                    nurse_id=req.nurse_id,
                    year=req.year,
                    month=req.month,
                    day=req.day,
                    code=req.code,
                )
            )
    session.flush()
    return AvailabilityRequestRead(
        id=req.id,
        year=req.year,
        month=req.month,
        day=req.day,
        code=req.code,
        status=req.status,
        reason=req.reason,
        created_at=req.created_at.isoformat(),
    )

@app.post("/api/constraints/bulk", status_code=204)
def save_constraints(
    payload: ConstraintBulkRequest,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    nurse_ids = list({item.nurse_id for item in payload.items})
    if nurse_ids:
        session.execute(
            delete(ConstraintEntry).where(
                ConstraintEntry.year == payload.year,
                ConstraintEntry.month == payload.month,
                ConstraintEntry.nurse_id.in_(nurse_ids),
            )
        )
    elif not payload.items:
        return Response(status_code=204)
    for item in payload.items:
        if not item.code:
            continue
        session.add(
            ConstraintEntry(
                nurse_id=item.nurse_id,
                year=payload.year,
                month=payload.month,
                day=item.day,
                code=item.code,
            )
        )
    session.flush()
    return Response(status_code=204)


@app.get("/api/config/month", response_model=MonthConfigSchema)
def get_month_config(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    config = get_or_create_month_config(session, year, month)
    return config


@app.put("/api/config/month", response_model=MonthConfigSchema)
def update_month_config(
    payload: MonthConfigSchema,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    config = get_or_create_month_config(session, payload.year, payload.month)
    config.max_hours_week_contratado = payload.max_hours_week_contratado
    config.target_hours_week = payload.target_hours_week
    config.pedidos_folga_hard = payload.pedidos_folga_hard
    config.prefer_folga_after_nd = payload.prefer_folga_after_nd
    config.min_rest_hours = payload.min_rest_hours
    config.penalty_weights = payload.penalty_weights
    session.add(config)
    session.flush()
    session.refresh(config)
    return config


@app.get("/api/adjustments", response_model=List[AdjustmentRead])
def list_adjustments(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    query = select(NurseMonthAdjustment).where(
        NurseMonthAdjustment.year == year,
        NurseMonthAdjustment.month == month,
    )
    nurse_ids = _nurse_ids_for_group(session, group)
    if group and not nurse_ids:
        return []
    if nurse_ids:
        query = query.where(NurseMonthAdjustment.nurse_id.in_(nurse_ids))
    return list(session.scalars(query))


@app.post("/api/adjustments/bulk", status_code=204)
def save_adjustments(
    payload: AdjustmentBulkRequest,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    nurse_ids = list({item.nurse_id for item in payload.items})
    if nurse_ids:
        session.execute(
            delete(NurseMonthAdjustment).where(
                NurseMonthAdjustment.year == payload.year,
                NurseMonthAdjustment.month == payload.month,
                NurseMonthAdjustment.nurse_id.in_(nurse_ids),
            )
        )
    elif not payload.items:
        return Response(status_code=204)
    for item in payload.items:
        if (
            item.feriados_trabalhados == 0
            and item.extra_minutes == 0
            and item.reduced_minutes == 0
        ):
            continue
        session.add(
            NurseMonthAdjustment(
                nurse_id=item.nurse_id,
                year=payload.year,
                month=payload.month,
                feriados_trabalhados=item.feriados_trabalhados,
                extra_minutes=item.extra_minutes,
                reduced_minutes=item.reduced_minutes,
            )
        )
    session.flush()
    return Response(status_code=204)


@app.get("/api/holidays", response_model=List[HolidayInfo])
def list_holidays(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    session: Session = Depends(get_db_session),
):
    manual_entries = list(session.scalars(select(ManualHoliday)))
    manual_data = [
        {
            "year": item.year,
            "month": item.month,
            "day": item.day,
            "label": item.label,
            "action": item.action,
        }
        for item in manual_entries
    ]
    return month_holidays(year, month, manual_data)


@app.get("/api/holidays/manual", response_model=List[ManualHolidaySchema])
def list_manual_holidays(
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    return list(session.scalars(select(ManualHoliday)))


@app.post("/api/holidays/manual", response_model=ManualHolidaySchema, status_code=201)
def create_manual_holiday(
    payload: ManualHolidayCreate,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    data = payload.dict()
    if data["action"] == "REMOVE" and not data.get("label"):
        data["label"] = "Remover feriado"
    entry = ManualHoliday(**data)
    session.add(entry)
    session.flush()
    session.refresh(entry)
    return entry


@app.delete("/api/holidays/manual/{holiday_id}", status_code=204)
def delete_manual_holiday(
    holiday_id: int,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    entry = session.get(ManualHoliday, holiday_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Feriado manual não encontrado")
    session.delete(entry)
    session.flush()
    return Response(status_code=204)


@app.get("/api/schedule", response_model=ScheduleResponse)
def get_schedule(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    entries_query = select(ScheduleEntry).where(
        ScheduleEntry.year == year,
        ScheduleEntry.month == month,
    )
    group_nurse_ids = _nurse_ids_for_group(session, group)
    if group and not group_nurse_ids:
        return ScheduleResponse(entries=[], unfilled=[], violations=[], stats=[])
    if group_nurse_ids:
        entries_query = entries_query.where(ScheduleEntry.nurse_id.in_(group_nurse_ids))
    if user.role not in {"ADMIN", "COORDENADOR"}:
        team_ids = _team_ids_for_user(session, user.id)
        released = session.exec(
            select(ScheduleRelease).where(
                ScheduleRelease.year == year,
                ScheduleRelease.month == month,
                ScheduleRelease.team_id.in_(team_ids),
            )
        ).first()
        if not released:
            return ScheduleResponse(entries=[], unfilled=[], violations=[], stats=[])
        service_codes = session.exec(
            select(Team.service_code).where(Team.id.in_(team_ids))
        ).all()
        service_codes = [code for code in service_codes if code]
        if service_codes:
            shift_codes = session.exec(
                select(ServiceShift.shift_code).where(
                    ServiceShift.service_code.in_(service_codes)
                )
            ).all()
            if shift_codes:
                entries_query = entries_query.where(
                    ScheduleEntry.shift_code.in_(shift_codes)
                )
        entries = list(session.scalars(entries_query))
        nurse_ids = list({entry.nurse_id for entry in entries})
        nurses = list(
            session.scalars(select(Nurse).where(Nurse.id.in_(nurse_ids)))
        )
        stats = collect_nurse_stats(session, nurses, year, month)
        return ScheduleResponse(entries=entries, unfilled=[], violations=[], stats=stats)
    else:
        nurse_query = select(Nurse)
        if group_nurse_ids:
            nurse_query = nurse_query.where(Nurse.id.in_(group_nurse_ids))
        nurses = sort_nurses_by_category(list(session.scalars(nurse_query)))

    entries = list(session.scalars(entries_query))
    stats = collect_nurse_stats(session, nurses, year, month)
    return ScheduleResponse(entries=entries, unfilled=[], violations=[], stats=stats)


@app.get("/api/releases", response_model=List[ScheduleReleaseRead])
def list_schedule_releases(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    return list(
        session.scalars(
            select(ScheduleRelease).where(
                ScheduleRelease.year == year,
                ScheduleRelease.month == month,
            )
        )
    )


@app.post("/api/releases", response_model=ScheduleReleaseRead, status_code=201)
def create_schedule_release(
    payload: ScheduleReleaseCreate,
    session: Session = Depends(get_db_session),
    user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    team = session.get(Team, payload.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    existing = session.scalar(
        select(ScheduleRelease).where(
            ScheduleRelease.year == payload.year,
            ScheduleRelease.month == payload.month,
            ScheduleRelease.team_id == payload.team_id,
        )
    )
    if existing:
        return existing
    release = ScheduleRelease(
        year=payload.year,
        month=payload.month,
        team_id=payload.team_id,
        created_by=user.id,
    )
    session.add(release)
    session.flush()
    session.refresh(release)
    member_ids = list(
        session.scalars(
            select(TeamMember.user_id).where(TeamMember.team_id == payload.team_id)
        )
    )
    for member_id in member_ids:
        message = ChatMessage(
            from_user_id=user.id,
            to_user_id=member_id,
            message=(
                f"Horário publicado: {payload.month:02d}/{payload.year} "
                f"({team.name})."
            ),
        )
        session.add(message)
        _touch_thread_for_message(session, user.id, member_id)
        _touch_thread_for_message(session, member_id, user.id)
    session.flush()
    return release


@app.put("/api/schedule/cell")
def update_schedule_cell(
    payload: ScheduleCellUpdate,
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    entries = list(
        session.scalars(
            select(ScheduleEntry).where(
                ScheduleEntry.year == year,
                ScheduleEntry.month == month,
                ScheduleEntry.day == payload.day,
                ScheduleEntry.nurse_id == payload.nurse_id,
            )
        )
    )
    locked_entries = [item for item in entries if item.locked]
    nurse = session.get(Nurse, payload.nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    shift_codes = payload.shift_codes or ([] if payload.shift_code is None else [payload.shift_code])
    shift_codes = [code for code in shift_codes if code]
    if len(shift_codes) > 3:
        raise HTTPException(status_code=400, detail="Máximo de 3 turnos por dia")

    if not shift_codes:
        if payload.locked is not None and entries:
            for item in entries:
                item.locked = payload.locked
                session.add(item)
            session.flush()
            _recalculate_nurse_stat(session, payload.nurse_id, year, month)
            return entries[0]
        if entries:
            if locked_entries:
                raise HTTPException(status_code=400, detail="Célula bloqueada")
            for item in entries:
                session.delete(item)
            session.flush()
        _recalculate_nurse_stat(session, payload.nurse_id, year, month)
        return Response(status_code=204)

    if locked_entries and payload.locked is not False:
        raise HTTPException(status_code=400, detail="Célula bloqueada")
    if locked_entries and payload.locked is False:
        for item in locked_entries:
            item.locked = False
            session.add(item)

    for item in entries:
        session.delete(item)

    service_map = {
        row.shift_code: row.service_code
        for row in session.exec(
            select(ServiceShift.shift_code, ServiceShift.service_code).where(
                ServiceShift.shift_code.in_(shift_codes)
            )
        ).all()
    }
    shift_map = {
        row.code: row
        for row in session.scalars(select(Shift).where(Shift.code.in_(shift_codes)))
    }
    for idx, first_code in enumerate(shift_codes):
        first = shift_map.get(first_code)
        if not first:
            continue
        for second_code in shift_codes[idx + 1 :]:
            second = shift_map.get(second_code)
            if not second:
                continue
            if first.shift_type == second.shift_type:
                raise HTTPException(
                    status_code=400,
                    detail="Turnos do mesmo tipo no mesmo dia",
                )
            if not _allows_double_shift(nurse, first.shift_type, second.shift_type):
                raise HTTPException(
                    status_code=400,
                    detail="Combinação de turnos não permitida",
                )
            intervals_a = (
                [(first.start_minute, first.end_minute)]
                if first.end_minute > first.start_minute
                else [(first.start_minute, 24 * 60), (0, first.end_minute)]
            )
            intervals_b = (
                [(second.start_minute, second.end_minute)]
                if second.end_minute > second.start_minute
                else [(second.start_minute, 24 * 60), (0, second.end_minute)]
            )
            for start_a, end_a in intervals_a:
                for start_b, end_b in intervals_b:
                    if start_a < end_b and start_b < end_a:
                        raise HTTPException(
                            status_code=400,
                            detail="Turnos sobrepostos no mesmo dia",
                        )
    created_entries = []
    for code in shift_codes:
        service_code = payload.service_code or service_map.get(code) or code
        entry = ScheduleEntry(
            nurse_id=payload.nurse_id,
            year=year,
            month=month,
            day=payload.day,
            service_code=service_code,
            shift_code=code,
            locked=payload.locked or False,
            source="manual",
        )
        session.add(entry)
        created_entries.append(entry)
    session.flush()
    session.refresh(created_entries[0])
    _recalculate_nurse_stat(session, payload.nurse_id, year, month)
    return created_entries[0]


@app.put("/api/schedule/stat", response_model=NurseStat)
def update_stat_target(
    payload: StatUpdateRequest,
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    nurse = session.get(Nurse, payload.nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    stat = session.scalar(
        select(NurseMonthStat).where(
            NurseMonthStat.nurse_id == payload.nurse_id,
            NurseMonthStat.year == payload.year,
            NurseMonthStat.month == payload.month,
        )
    )
    if not stat:
        stat = NurseMonthStat(
            nurse_id=payload.nurse_id,
            year=payload.year,
            month=payload.month,
            target_minutes=payload.target_minutes,
            actual_minutes=0,
            delta_minutes=-payload.target_minutes,
        )
    old_delta = stat.delta_minutes
    stat.target_minutes = payload.target_minutes
    stat.delta_minutes = stat.actual_minutes - stat.target_minutes
    nurse.hour_balance_minutes += stat.delta_minutes - old_delta
    session.add(stat)
    session.add(nurse)
    session.flush()
    previous_bank = nurse.hour_balance_minutes - stat.delta_minutes
    return NurseStat(
        nurse_id=nurse.id,
        target_minutes=stat.target_minutes,
        actual_minutes=stat.actual_minutes,
        delta_minutes=stat.delta_minutes,
        bank_minutes=nurse.hour_balance_minutes,
        previous_bank_minutes=previous_bank,
    )


@app.post("/api/schedule/generate", response_model=ScheduleResponse)
def generate_endpoint(
    payload: GenerateRequest,
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    assignments, unfilled, violations, stats = generate_schedule(
        session, payload.year, payload.month, group
    )
    return ScheduleResponse(
        entries=assignments, unfilled=unfilled, violations=violations, stats=stats
    )


@app.delete("/api/schedule", status_code=204)
def clear_schedule_endpoint(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    nurse_ids = _nurse_ids_for_group(session, group)
    stat_lookup: Dict[int, NurseMonthStat] = {}
    stat_query = select(NurseMonthStat).where(
        NurseMonthStat.year == year,
        NurseMonthStat.month == month,
    )
    if nurse_ids:
        stat_query = stat_query.where(NurseMonthStat.nurse_id.in_(nurse_ids))
    for stat in session.scalars(stat_query):
        stat_lookup[stat.nurse_id] = stat
    for nurse_id, stat in stat_lookup.items():
        nurse = session.get(Nurse, nurse_id)
        if not nurse:
            continue
        nurse.hour_balance_minutes = (nurse.hour_balance_minutes or 0) - (
            stat.delta_minutes or 0
        )
        session.add(nurse)
    entry_query = delete(ScheduleEntry).where(
        ScheduleEntry.year == year,
        ScheduleEntry.month == month,
    )
    stat_query = delete(NurseMonthStat).where(
        NurseMonthStat.year == year,
        NurseMonthStat.month == month,
    )
    adj_query = delete(NurseMonthAdjustment).where(
        NurseMonthAdjustment.year == year,
        NurseMonthAdjustment.month == month,
    )
    if nurse_ids:
        entry_query = entry_query.where(ScheduleEntry.nurse_id.in_(nurse_ids))
        stat_query = stat_query.where(NurseMonthStat.nurse_id.in_(nurse_ids))
        adj_query = adj_query.where(NurseMonthAdjustment.nurse_id.in_(nurse_ids))
    session.execute(entry_query)
    session.execute(stat_query)
    session.execute(adj_query)
    session.flush()
    return Response(status_code=204)


def _swap_participants(session: Session, request_id: int) -> List[SwapParticipant]:
    return list(
        session.scalars(
            select(SwapParticipant).where(SwapParticipant.request_id == request_id)
        )
    )


def _swap_decision(session: Session, request_id: int) -> SwapDecision | None:
    return session.scalar(
        select(SwapDecision).where(SwapDecision.request_id == request_id)
    )


def _notify_swap(
    session: Session,
    from_user_id: int,
    target_ids: List[int],
    message: str,
    swap_id: int | None = None,
):
    if swap_id and "[SWAP_ID=" not in message:
        message = f"{message} [SWAP_ID={swap_id}]"
    for target_id in target_ids:
        msg = ChatMessage(
            from_user_id=from_user_id,
            to_user_id=target_id,
            message=message,
        )
        session.add(msg)
        _touch_thread_for_message(session, from_user_id, target_id)
        _touch_thread_for_message(session, target_id, from_user_id)


@app.get("/api/swaps", response_model=List[SwapRead])
def list_swaps(
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    query = select(SwapRequest)
    if user.role not in {"ADMIN", "COORDENADOR"}:
        participant_request_ids = list(
            session.scalars(
                select(SwapParticipant.request_id).where(
                    SwapParticipant.user_id == user.id
                )
            )
        )
        query = query.where(
            or_(
                SwapRequest.requester_id == user.id,
                SwapRequest.id.in_(participant_request_ids or [-1]),
            )
        )
    requests = list(session.scalars(query.order_by(SwapRequest.created_at.desc())))
    payload = []
    for req in requests:
        participants = _swap_participants(session, req.id)
        decision = _swap_decision(session, req.id)
        payload.append(
            SwapRead(
                id=req.id,
                requester_id=req.requester_id,
                year=req.year,
                month=req.month,
                day=req.day,
                service_code=req.service_code,
                shift_code=req.shift_code,
                desired_service_code=req.desired_service_code,
                desired_shift_code=req.desired_shift_code,
                reason=req.reason,
                observations=req.observations,
                status=req.status,
                created_at=req.created_at.isoformat(),
                participants=[
                    {
                        "user_id": part.user_id,
                        "status": part.status,
                        "responded_at": part.responded_at.isoformat()
                        if part.responded_at
                        else None,
                    }
                    for part in participants
                ],
                decision=(
                    {
                        "status": decision.status,
                        "reason": decision.reason,
                        "decided_at": decision.decided_at.isoformat(),
                        "coordinator_id": decision.coordinator_id,
                    }
                    if decision
                    else None
                ),
            )
        )
    return payload


@app.post("/api/swaps", response_model=SwapRead, status_code=201)
def create_swap_request(
    payload: SwapCreate,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    if user.role == "ADMIN":
        raise HTTPException(status_code=403, detail="Sem permissões")
    if not payload.participant_ids:
        raise HTTPException(status_code=400, detail="Participantes obrigatórios")
    if len(payload.participant_ids) != 1:
        raise HTTPException(status_code=400, detail="Seleciona apenas um destinatário")
    swap = SwapRequest(
        requester_id=user.id,
        year=payload.year,
        month=payload.month,
        day=payload.day,
        service_code=payload.service_code,
        shift_code=payload.shift_code,
        desired_service_code=payload.desired_service_code,
        desired_shift_code=payload.desired_shift_code,
        reason=payload.reason,
        observations=payload.observations,
        status="PENDING_PARTICIPANTS",
    )
    session.add(swap)
    session.flush()
    for participant_id in payload.participant_ids:
        session.add(
            SwapParticipant(
                request_id=swap.id,
                user_id=participant_id,
                status="PENDING",
            )
        )
    session.flush()
    _notify_swap(
        session,
        user.id,
        payload.participant_ids,
        "Pedido de troca de turno: responde no ShiftFlow.",
        swap.id,
    )
    coordinator_ids = list(
        session.scalars(select(User.id).where(User.role == "COORDENADOR"))
    )
    _notify_swap(
        session,
        user.id,
        coordinator_ids,
        "Novo pedido de troca criado (aguarda respostas).",
        swap.id,
    )
    participants = _swap_participants(session, swap.id)
    return SwapRead(
        id=swap.id,
        requester_id=swap.requester_id,
        year=swap.year,
        month=swap.month,
        day=swap.day,
        service_code=swap.service_code,
        shift_code=swap.shift_code,
        desired_service_code=swap.desired_service_code,
        desired_shift_code=swap.desired_shift_code,
        reason=swap.reason,
        observations=swap.observations,
        status=swap.status,
        created_at=swap.created_at.isoformat(),
        participants=[
            {
                "user_id": part.user_id,
                "status": part.status,
                "responded_at": None,
            }
            for part in participants
        ],
    )


@app.put("/api/swaps/{request_id}/participants/me", response_model=SwapRead)
def respond_swap_participant(
    request_id: int,
    payload: SwapParticipantUpdate,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    participant = session.scalar(
        select(SwapParticipant).where(
            SwapParticipant.request_id == request_id,
            SwapParticipant.user_id == user.id,
        )
    )
    if not participant:
        raise HTTPException(status_code=404, detail="Participação não encontrada")
    if payload.status not in {"ACCEPTED", "REJECTED"}:
        raise HTTPException(status_code=400, detail="Estado inválido")
    participant.status = payload.status
    participant.responded_at = datetime.utcnow()
    session.add(participant)
    swap = session.get(SwapRequest, request_id)
    participants = _swap_participants(session, request_id)
    if payload.status == "REJECTED":
        swap.status = "REJECTED_BY_PARTICIPANT"
        coordinator_ids = list(
            session.scalars(select(User.id).where(User.role == "COORDENADOR"))
        )
        target_ids = [swap.requester_id] + [part.user_id for part in participants]
        _notify_swap(
            session,
            user.id,
            list({*target_ids, *coordinator_ids}),
            "Pedido de troca recusado por um participante.",
            swap.id,
        )
    else:
        if all(part.status == "ACCEPTED" for part in participants):
            swap.status = "PENDING_COORDINATOR"
            coordinator_ids = list(
                session.scalars(select(User.id).where(User.role == "COORDENADOR"))
            )
            _notify_swap(
                session,
                user.id,
                coordinator_ids,
                "Pedido de troca pronto para validação.",
                swap.id,
            )
    session.add(swap)
    session.flush()
    decision = _swap_decision(session, request_id)
    return SwapRead(
        id=swap.id,
        requester_id=swap.requester_id,
        year=swap.year,
        month=swap.month,
        day=swap.day,
        service_code=swap.service_code,
        shift_code=swap.shift_code,
        desired_service_code=swap.desired_service_code,
        desired_shift_code=swap.desired_shift_code,
        reason=swap.reason,
        observations=swap.observations,
        status=swap.status,
        created_at=swap.created_at.isoformat(),
        participants=[
            {
                "user_id": part.user_id,
                "status": part.status,
                "responded_at": part.responded_at.isoformat()
                if part.responded_at
                else None,
            }
            for part in participants
        ],
        decision=(
            {
                "status": decision.status,
                "reason": decision.reason,
                "decided_at": decision.decided_at.isoformat(),
                "coordinator_id": decision.coordinator_id,
            }
            if decision
            else None
        ),
    )


@app.put("/api/swaps/{request_id}/decision", response_model=SwapRead)
def decide_swap(
    request_id: int,
    payload: SwapDecisionRequest,
    session: Session = Depends(get_db_session),
    user: User = Depends(require_roles("ADMIN", "COORDENADOR")),
):
    swap = session.get(SwapRequest, request_id)
    if not swap:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if payload.status not in {"APPROVED", "REJECTED"}:
        raise HTTPException(status_code=400, detail="Estado inválido")
    participants = _swap_participants(session, request_id)
    if swap.status != "PENDING_COORDINATOR":
        raise HTTPException(status_code=400, detail="Pedido ainda não validável")
    swap.status = payload.status
    decision = SwapDecision(
        request_id=swap.id,
        coordinator_id=user.id,
        status=payload.status,
        reason=payload.reason,
    )
    session.add(decision)
    session.add(swap)
    session.flush()
    target_ids = [swap.requester_id] + [part.user_id for part in participants]
    if payload.status == "APPROVED":
        message = "Pedido de troca aprovado pelo coordenador."
    else:
        reason = payload.reason or "Sem motivo indicado."
        message = f"Pedido de troca rejeitado: {reason}"
    _notify_swap(session, user.id, target_ids, message, swap.id)
    return SwapRead(
        id=swap.id,
        requester_id=swap.requester_id,
        year=swap.year,
        month=swap.month,
        day=swap.day,
        service_code=swap.service_code,
        shift_code=swap.shift_code,
        desired_service_code=swap.desired_service_code,
        desired_shift_code=swap.desired_shift_code,
        reason=swap.reason,
        observations=swap.observations,
        status=swap.status,
        created_at=swap.created_at.isoformat(),
        participants=[
            {
                "user_id": part.user_id,
                "status": part.status,
                "responded_at": part.responded_at.isoformat()
                if part.responded_at
                else None,
            }
            for part in participants
        ],
        decision={
            "status": decision.status,
            "reason": decision.reason,
            "decided_at": decision.decided_at.isoformat(),
            "coordinator_id": decision.coordinator_id,
        },
    )


@app.delete("/api/swaps/{request_id}", status_code=204)
def delete_swap_request(
    request_id: int,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    swap = session.get(SwapRequest, request_id)
    if not swap:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if user.role in {"ADMIN", "COORDENADOR"}:
        allowed = True
    else:
        allowed = user.id == swap.requester_id and swap.status != "APPROVED"
    if not allowed:
        raise HTTPException(status_code=403, detail="Sem permissões")
    participants = _swap_participants(session, request_id)
    target_ids = [swap.requester_id] + [part.user_id for part in participants]
    coordinator_ids = list(
        session.scalars(select(User.id).where(User.role == "COORDENADOR"))
    )
    session.execute(
        delete(SwapParticipant).where(SwapParticipant.request_id == request_id)
    )
    session.execute(delete(SwapDecision).where(SwapDecision.request_id == request_id))
    session.delete(swap)
    session.flush()
    _notify_swap(
        session,
        user.id,
        list({*target_ids, *coordinator_ids}),
        "Pedido de troca eliminado.",
        swap.id,
    )
    return Response(status_code=204)

@app.get("/api/export/schedule")
def download_schedule(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    format: str = Query("xlsx"),
    lang: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(get_current_user),
):
    lang_key = "en" if (lang or "").lower().startswith("en") else "pt"
    normalized = format.strip().lower()
    if normalized == "pdf":
        app_name, org_name, app_logo, org_logo = _export_branding(session)
        pdf_info_text = _setting_value(session, "pdf_info_text")
        stream = export_schedule_pdf(
            session,
            year,
            month,
            app_logo,
            org_logo,
            app_name=app_name,
            org_name=org_name,
            info_text=pdf_info_text,
            group=group,
            lang=lang_key,
        )
        filename = (
            f"shiftflow_schedule_{year}_{month:02d}.pdf"
            if lang_key == "en"
            else f"shiftflow_escala_{year}_{month:02d}.pdf"
        )
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
        return StreamingResponse(stream, media_type="application/pdf", headers=headers)
    if normalized != "xlsx":
        raise HTTPException(status_code=400, detail="Formato inválido")
    stream = export_schedule(session, year, month, group, lang=lang_key)
    filename = (
        f"shiftflow_schedule_{year}_{month:02d}.xlsx"
        if lang_key == "en"
        else f"shiftflow_escala_{year}_{month:02d}.xlsx"
    )
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(
        stream,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers=headers,
    )


@app.get("/api/export/constraints")
def download_constraints(
    year: int = Query(..., ge=2020),
    month: int = Query(..., ge=1, le=12),
    group: str | None = Query(None),
    format: str = Query("xlsx"),
    lang: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(get_current_user),
):
    lang_key = "en" if (lang or "").lower().startswith("en") else "pt"
    normalized = format.strip().lower()
    if normalized == "pdf":
        app_name, org_name, app_logo, org_logo = _export_branding(session)
        pdf_info_text = _setting_value(session, "pdf_info_text")
        stream = export_constraints_pdf(
            session,
            year,
            month,
            app_logo,
            org_logo,
            app_name=app_name,
            org_name=org_name,
            info_text=pdf_info_text,
            group=group,
            lang=lang_key,
        )
        filename = (
            f"shiftflow_availability_{year}_{month:02d}.pdf"
            if lang_key == "en"
            else f"shiftflow_disponibilidades_{year}_{month:02d}.pdf"
        )
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
        return StreamingResponse(stream, media_type="application/pdf", headers=headers)
    if normalized != "xlsx":
        raise HTTPException(status_code=400, detail="Formato inválido")
    stream = export_constraints(session, year, month, group, lang=lang_key)
    filename = (
        f"shiftflow_availability_{year}_{month:02d}.xlsx"
        if lang_key == "en"
        else f"shiftflow_disponibilidades_{year}_{month:02d}.xlsx"
    )
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(
        stream,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers=headers,
    )


@app.get("/api/export/swaps")
def download_swaps(
    lang: str | None = Query(None),
    session: Session = Depends(get_db_session),
    _user: User = Depends(get_current_user),
):
    lang_key = "en" if (lang or "").lower().startswith("en") else "pt"
    stream = export_swaps(session, lang=lang_key)
    filename = "shiftflow_swaps.xlsx" if lang_key == "en" else "shiftflow_trocas.xlsx"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(
        stream,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers=headers,
    )


@app.get("/api/swaps/{request_id}/export")
def download_swap_proof(
    request_id: int,
    format: str = Query("pdf"),
    lang: str | None = Query(None),
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    normalized = format.strip().lower()
    if normalized != "pdf":
        raise HTTPException(status_code=400, detail="Formato inválido")
    req = session.get(SwapRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    participant_ids = list(
        session.scalars(
            select(SwapParticipant.user_id).where(
                SwapParticipant.request_id == request_id
            )
        )
    )
    if user.role not in {"ADMIN", "COORDENADOR"} and user.id not in participant_ids and user.id != req.requester_id:
        raise HTTPException(status_code=403, detail="Sem permissões")
    lang_key = "en" if (lang or "").lower().startswith("en") else "pt"
    app_name, org_name, app_logo, org_logo = _export_branding(session)
    pdf_info_text = _setting_value(session, "pdf_info_text")
    stream = export_swap_pdf(
        session,
        request_id,
        app_logo,
        org_logo,
        app_name=app_name,
        org_name=org_name,
        info_text=pdf_info_text,
        exported_for=user,
        lang=lang_key,
    )
    filename = (
        f"shiftflow_swap_{request_id}.pdf"
        if lang_key == "en"
        else f"shiftflow_troca_{request_id}.pdf"
    )
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(stream, media_type="application/pdf", headers=headers)
