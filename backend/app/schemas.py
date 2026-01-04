from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class NurseBase(BaseModel):
    name: str
    category: str
    services_permitted: List[str] = Field(default_factory=list)
    can_work_night: bool = True
    max_noites_mes: Optional[int] = None
    weekly_hours: int = 40
    user_id: Optional[int] = None


class NurseCreate(NurseBase):
    user_id: int


class NurseUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    services_permitted: Optional[List[str]] = None
    can_work_night: Optional[bool] = None
    max_noites_mes: Optional[int] = None
    weekly_hours: Optional[int] = None
    hour_balance_minutes: Optional[int] = None
    user_id: Optional[int] = None


class NurseRead(NurseBase):
    id: int
    hour_balance_minutes: int
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class AvailabilityItem(BaseModel):
    day: int
    code: str


class AvailabilityBulkRequest(BaseModel):
    year: int
    month: int
    items: List[AvailabilityItem]


class AvailabilityDecision(BaseModel):
    status: str
    reason: Optional[str] = None


class AvailabilityRequestRead(BaseModel):
    id: int
    year: int
    month: int
    day: int
    code: str
    status: str
    reason: Optional[str] = None
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class AvailabilityPendingRead(AvailabilityRequestRead):
    user_id: int
    nurse_id: int
    user_name: str
    user_role: str

    model_config = ConfigDict(from_attributes=True)


class RequirementItem(BaseModel):
    day: int
    service_code: str
    shift_code: str
    required_count: int


class RequirementBulkRequest(BaseModel):
    year: int
    month: int
    items: List[RequirementItem]
    group: Optional[str] = None


class RequirementRead(RequirementItem):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ConstraintItem(BaseModel):
    nurse_id: int
    day: int
    code: str


class ConstraintBulkRequest(BaseModel):
    year: int
    month: int
    items: List[ConstraintItem]


class ConstraintRead(ConstraintItem):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ScheduleEntrySchema(BaseModel):
    id: int
    nurse_id: int
    day: int
    service_code: str
    shift_code: str
    locked: bool
    source: str

    model_config = ConfigDict(from_attributes=True)


class UnfilledSlot(BaseModel):
    day: int
    service_code: str
    shift_code: str
    reason: str


class NurseStat(BaseModel):
    nurse_id: int
    target_minutes: int
    actual_minutes: int
    delta_minutes: int
    bank_minutes: int
    previous_bank_minutes: int


class ScheduleResponse(BaseModel):
    entries: List[ScheduleEntrySchema]
    unfilled: List[UnfilledSlot]
    violations: List[str] = Field(default_factory=list)
    stats: List[NurseStat] = Field(default_factory=list)


class GenerateRequest(BaseModel):
    year: int
    month: int


class ScheduleCellUpdate(BaseModel):
    nurse_id: int
    day: int
    service_code: Optional[str] = None
    shift_code: Optional[str] = None
    shift_codes: Optional[List[str]] = None
    locked: Optional[bool] = None


class MonthConfigSchema(BaseModel):
    year: int
    month: int
    max_hours_week_contratado: int
    target_hours_week: int
    pedidos_folga_hard: bool
    prefer_folga_after_nd: bool
    min_rest_hours: int
    penalty_weights: Dict[str, int]

    model_config = ConfigDict(from_attributes=True)


class ManualHolidaySchema(BaseModel):
    id: int
    year: int
    month: int
    day: int
    label: str
    action: str

    model_config = ConfigDict(from_attributes=True)


class ManualHolidayCreate(BaseModel):
    year: int
    month: int
    day: int
    label: Optional[str] = None
    action: str = "ADD"


class HolidayInfo(BaseModel):
    day: int
    label: str
    type: str


class NurseMoveRequest(BaseModel):
    direction: str


class AdjustmentItem(BaseModel):
    nurse_id: int
    feriados_trabalhados: int = 0
    extra_minutes: int = 0
    reduced_minutes: int = 0


class AdjustmentRead(AdjustmentItem):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AdjustmentBulkRequest(BaseModel):
    year: int
    month: int
    items: List[AdjustmentItem]


class StatUpdateRequest(BaseModel):
    nurse_id: int
    year: int
    month: int
    target_minutes: int


class ShiftSchema(BaseModel):
    code: str
    service: str
    label: str
    shift_type: str
    start_minute: int
    end_minute: int
    minutes: int


class ShiftUpdate(BaseModel):
    start_time: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    full_name: str
    role: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool
    nurse_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SettingsRead(BaseModel):
    app_name: str
    org_name: str
    app_logo_url: Optional[str] = None
    org_logo_url: Optional[str] = None
    show_app_logo: bool = True
    show_org_logo: bool = True
    primary_color: str
    accent_color: str
    background: str
    pdf_info_text: str


class SettingsUpdate(BaseModel):
    app_name: Optional[str] = None
    org_name: Optional[str] = None
    app_logo_url: Optional[str] = None
    org_logo_url: Optional[str] = None
    show_app_logo: Optional[bool] = None
    show_org_logo: Optional[bool] = None
    primary_color: Optional[str] = None
    accent_color: Optional[str] = None
    background: Optional[str] = None
    pdf_info_text: Optional[str] = None


class TeamCreate(BaseModel):
    name: str
    service_code: Optional[str] = None
    role: str


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    service_code: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class TeamRead(TeamCreate):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TeamMemberRequest(BaseModel):
    user_ids: List[int]


class ServiceCreate(BaseModel):
    code: str
    name: str
    color: str
    role: str


class ServiceRead(ServiceCreate):
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class ShiftCreate(BaseModel):
    code: str
    label: str
    shift_type: str
    start_time: str
    end_time: str


class ShiftCatalogUpdate(BaseModel):
    label: Optional[str] = None
    shift_type: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class ServiceShiftCreate(BaseModel):
    service_code: str
    shift_code: str


class ScheduleReleaseCreate(BaseModel):
    year: int
    month: int
    team_id: int


class ScheduleReleaseRead(BaseModel):
    id: int
    year: int
    month: int
    team_id: int
    created_by: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class ChatMessageCreate(BaseModel):
    to_user_id: Optional[int] = None
    to_user_ids: Optional[List[int]] = None
    to_role: Optional[str] = None
    to_all: Optional[bool] = None
    message: str


class ChatMessageRead(BaseModel):
    id: int
    from_user_id: int
    to_user_id: Optional[int]
    to_role: Optional[str]
    message: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class ChatThreadRead(BaseModel):
    peer_id: int
    peer_name: str
    peer_role: str
    last_message: Optional[str] = None
    last_at: Optional[str] = None
    unread_count: int = 0
    is_archived: bool = False


class ChatThreadStateUpdate(BaseModel):
    is_archived: Optional[bool] = None
    is_deleted: Optional[bool] = None


class SwapCreate(BaseModel):
    year: int
    month: int
    day: int
    service_code: Optional[str] = None
    shift_code: Optional[str] = None
    desired_service_code: Optional[str] = None
    desired_shift_code: Optional[str] = None
    reason: Optional[str] = None
    observations: Optional[str] = None
    participant_ids: List[int]


class SwapParticipantUpdate(BaseModel):
    status: str


class SwapDecisionRequest(BaseModel):
    status: str
    reason: Optional[str] = None


class SwapParticipantRead(BaseModel):
    user_id: int
    status: str
    responded_at: Optional[str] = None


class SwapDecisionRead(BaseModel):
    status: str
    reason: Optional[str] = None
    decided_at: str
    coordinator_id: int


class SwapRead(BaseModel):
    id: int
    requester_id: int
    year: int
    month: int
    day: int
    service_code: Optional[str] = None
    shift_code: Optional[str] = None
    desired_service_code: Optional[str] = None
    desired_shift_code: Optional[str] = None
    reason: Optional[str] = None
    observations: Optional[str] = None
    status: str
    created_at: str
    participants: List[SwapParticipantRead] = Field(default_factory=list)
    decision: Optional[SwapDecisionRead] = None


class ProfessionalCategoryCreate(BaseModel):
    name: str
    role: str
    sort_order: int = 0
    is_active: bool = True


class ProfessionalCategoryUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class ProfessionalCategoryRead(BaseModel):
    id: int
    name: str
    role: str
    sort_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
