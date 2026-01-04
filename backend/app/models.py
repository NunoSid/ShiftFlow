from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, JSON, UniqueConstraint
from sqlmodel import Field, SQLModel

from .constants import DEFAULT_PENALTIES


class Nurse(SQLModel, table=True):
    __tablename__ = "nurse"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    services_permitted: List[str] = Field(
        sa_column=Column(JSON, nullable=False, default=list)
    )
    can_work_night: bool = Field(default=True)
    max_noites_mes: Optional[int] = Field(default=None)
    weekly_hours: int = Field(default=40)
    hour_balance_minutes: int = Field(default=0)
    display_order: int = Field(
        default=0,
        sa_column=Column(Integer, nullable=False, default=0),
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    full_name: str
    role: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )


class Setting(SQLModel, table=True):
    __tablename__ = "setting"

    key: str = Field(primary_key=True)
    value: str
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )


class Team(SQLModel, table=True):
    __tablename__ = "team"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    service_code: Optional[str] = Field(default=None)
    role: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)


class TeamMember(SQLModel, table=True):
    __tablename__ = "team_member"
    __table_args__ = (UniqueConstraint("team_id", "user_id", name="uq_team_member"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(index=True, foreign_key="team.id")
    user_id: int = Field(index=True, foreign_key="user.id")


class Service(SQLModel, table=True):
    __tablename__ = "service"

    code: str = Field(primary_key=True)
    name: str
    color: str = Field(default="#e2e8f0")
    role: str = Field(default="ENFERMEIRO")
    is_active: bool = Field(default=True)


class Shift(SQLModel, table=True):
    __tablename__ = "shift"

    code: str = Field(primary_key=True)
    label: str
    shift_type: str
    start_minute: int
    end_minute: int


class ServiceShift(SQLModel, table=True):
    __tablename__ = "service_shift"
    __table_args__ = (
        UniqueConstraint("service_code", "shift_code", name="uq_service_shift"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    service_code: str = Field(index=True, foreign_key="service.code")
    shift_code: str = Field(index=True, foreign_key="shift.code")


class ScheduleRelease(SQLModel, table=True):
    __tablename__ = "schedule_release"
    __table_args__ = (
        UniqueConstraint("year", "month", "team_id", name="uq_schedule_release"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    month: int
    team_id: int = Field(index=True, foreign_key="team.id")
    created_by: int = Field(index=True, foreign_key="user.id")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )


class MonthlyRequirement(SQLModel, table=True):
    __tablename__ = "monthly_requirement"
    __table_args__ = (
        UniqueConstraint(
            "year", "month", "day", "service_code", "shift_code", name="uq_requirement"
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    month: int
    day: int
    service_code: str
    shift_code: str
    required_count: int = Field(default=0)


class ConstraintEntry(SQLModel, table=True):
    __tablename__ = "constraint_entry"
    __table_args__ = (
        UniqueConstraint("nurse_id", "year", "month", "day", name="uq_constraint_day"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nurse_id: int = Field(index=True, foreign_key="nurse.id")
    year: int
    month: int
    day: int
    code: str = Field(default="")


class ScheduleEntry(SQLModel, table=True):
    __tablename__ = "schedule_entry"

    id: Optional[int] = Field(default=None, primary_key=True)
    nurse_id: int = Field(index=True, foreign_key="nurse.id")
    year: int
    month: int
    day: int
    service_code: str
    shift_code: str
    locked: bool = Field(default=False)
    source: str = Field(default="auto")


class MonthConfig(SQLModel, table=True):
    __tablename__ = "month_config"
    __table_args__ = (UniqueConstraint("year", "month", name="uq_month_config"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    month: int
    max_hours_week_contratado: int = Field(default=52)
    target_hours_week: int = Field(default=40)
    pedidos_folga_hard: bool = Field(default=False)
    prefer_folga_after_nd: bool = Field(default=False)
    min_rest_hours: int = Field(default=11)
    penalty_weights: dict = Field(
        default_factory=lambda: DEFAULT_PENALTIES,
        sa_column=Column(JSON, nullable=False, default=DEFAULT_PENALTIES),
    )


class ProfessionalCategory(SQLModel, table=True):
    __tablename__ = "professional_category"
    __table_args__ = (
        UniqueConstraint("name", "role", name="uq_professional_category"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)


class ManualHoliday(SQLModel, table=True):
    __tablename__ = "manual_holiday"
    __table_args__ = (
        UniqueConstraint("year", "month", "day", name="uq_manual_holiday"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    month: int
    day: int
    label: str = Field(default="Feriado Municipal")
    action: str = Field(default="ADD")


class NurseMonthStat(SQLModel, table=True):
    __tablename__ = "nurse_month_stat"
    __table_args__ = (
        UniqueConstraint("nurse_id", "year", "month", name="uq_nurse_month_stat"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nurse_id: int = Field(index=True, foreign_key="nurse.id")
    year: int
    month: int
    target_minutes: int = 0
    actual_minutes: int = 0
    delta_minutes: int = 0


class NurseMonthAdjustment(SQLModel, table=True):
    __tablename__ = "nurse_month_adjustment"
    __table_args__ = (
        UniqueConstraint("nurse_id", "year", "month", name="uq_nurse_month_adjustment"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nurse_id: int = Field(index=True, foreign_key="nurse.id")
    year: int
    month: int
    feriados_trabalhados: int = 0
    extra_minutes: int = 0
    reduced_minutes: int = 0


class ShiftSetting(SQLModel, table=True):
    __tablename__ = "shift_setting"

    code: str = Field(primary_key=True)
    start_minute: int = Field(default=0)
    end_minute: int = Field(default=0)


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_message"

    id: Optional[int] = Field(default=None, primary_key=True)
    from_user_id: int = Field(index=True, foreign_key="user.id")
    to_user_id: Optional[int] = Field(default=None, index=True)
    to_role: Optional[str] = Field(default=None)
    message: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )


class ChatThreadState(SQLModel, table=True):
    __tablename__ = "chat_thread_state"
    __table_args__ = (
        UniqueConstraint("user_id", "peer_id", name="uq_chat_thread_state"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    peer_id: int = Field(index=True, foreign_key="user.id")
    is_archived: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    last_read_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=True)
    )


class SwapRequest(SQLModel, table=True):
    __tablename__ = "swap_request"

    id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: int = Field(index=True, foreign_key="user.id")
    year: int
    month: int
    day: int
    service_code: Optional[str] = Field(default=None)
    shift_code: Optional[str] = Field(default=None)
    desired_service_code: Optional[str] = Field(default=None)
    desired_shift_code: Optional[str] = Field(default=None)
    reason: Optional[str] = Field(default=None)
    observations: Optional[str] = Field(default=None)
    status: str = Field(default="PENDING_PARTICIPANTS")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )


class SwapParticipant(SQLModel, table=True):
    __tablename__ = "swap_participant"
    __table_args__ = (
        UniqueConstraint("request_id", "user_id", name="uq_swap_participant"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(index=True, foreign_key="swap_request.id")
    user_id: int = Field(index=True, foreign_key="user.id")
    status: str = Field(default="PENDING")
    responded_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=True)
    )


class SwapDecision(SQLModel, table=True):
    __tablename__ = "swap_decision"

    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(index=True, foreign_key="swap_request.id")
    coordinator_id: int = Field(index=True, foreign_key="user.id")
    status: str
    reason: Optional[str] = Field(default=None)
    decided_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )


class AvailabilityRequest(SQLModel, table=True):
    __tablename__ = "availability_request"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "year", "month", "day", name="uq_availability_request"
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    nurse_id: int = Field(index=True, foreign_key="nurse.id")
    year: int
    month: int
    day: int
    code: str
    status: str = Field(default="PENDING")
    reason: Optional[str] = Field(default=None)
    decided_by: Optional[int] = Field(default=None, foreign_key="user.id")
    decided_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=True)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow),
    )
