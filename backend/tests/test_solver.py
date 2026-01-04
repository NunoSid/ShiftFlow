from sqlalchemy import delete

from backend.app.models import ConstraintEntry, MonthlyRequirement, Nurse, ScheduleEntry
from backend.app.solver import generate_schedule
from backend.tests.helpers import build_session


def test_solver_respects_hard_constraints():
    session = build_session()
    nurse_a = Nurse(
        name="Ana",
        category="CONTRATADO",
        services_permitted=["M1"],
        can_work_night=True,
    )
    nurse_b = Nurse(
        name="Beatriz",
        category="CONTRATADO",
        services_permitted=["M1"],
    )
    session.add(nurse_a)
    session.add(nurse_b)
    session.flush()

    session.add(
        MonthlyRequirement(
            year=2025,
            month=9,
            day=1,
            service_code="M1",
            shift_code="M1",
            required_count=1,
        )
    )
    session.add(
        ConstraintEntry(
            nurse_id=nurse_a.id, year=2025, month=9, day=1, code="FERIAS"
        )
    )
    session.commit()

    assignments, unfilled, violations, stats = generate_schedule(session, 2025, 9)
    assert len(assignments) == 1
    assert assignments[0].nurse_id == nurse_b.id
    assert not unfilled
    assert not violations
    assert isinstance(stats, list)


def test_solver_partial_needs_availability():
    session = build_session()
    partial = Nurse(
        name="Carla",
        category="RV_TEMPO_PARCIAL",
        services_permitted=["M1"],
    )
    full = Nurse(
        name="David",
        category="RV_TEMPO_INTEIRO",
        services_permitted=["M1"],
    )
    session.add(partial)
    session.add(full)
    session.flush()
    session.add(
        MonthlyRequirement(
            year=2025,
            month=9,
            day=2,
            service_code="M1",
            shift_code="M1",
            required_count=1,
        )
    )
    session.add(
        ConstraintEntry(
            nurse_id=partial.id, year=2025, month=9, day=2, code="DISPONIVEL"
        )
    )
    session.commit()

    assignments, _, _, _ = generate_schedule(session, 2025, 9)
    assert len(assignments) == 1
    assert assignments[0].nurse_id == partial.id

    # Remove disponibilidade and ensure fallback to other nurse.
    session.execute(
        delete(ConstraintEntry).where(
            ConstraintEntry.nurse_id == partial.id,
            ConstraintEntry.day == 2,
        )
    )
    session.execute(delete(ScheduleEntry))
    session.execute(delete(MonthlyRequirement))
    session.add(
        MonthlyRequirement(
            year=2025,
            month=9,
            day=2,
            service_code="M1",
            shift_code="M1",
            required_count=1,
        )
    )
    session.commit()

    assignments, _, _, _ = generate_schedule(session, 2025, 9)
    assert len(assignments) == 1
    assert assignments[0].nurse_id == full.id
