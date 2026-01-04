from backend.app.excel import export_constraints, export_schedule
from backend.app.models import ConstraintEntry, Nurse, ScheduleEntry
from backend.tests.helpers import build_session


def test_export_functions_generate_files(tmp_path):
    session = build_session()
    nurse = Nurse(
        name="Helena",
        category="CONTRATADO",
        services_permitted=["M1"],
    )
    session.add(nurse)
    session.flush()

    session.add(
        ScheduleEntry(
            nurse_id=nurse.id,
            year=2025,
            month=9,
            day=1,
            service_code="M1",
            shift_code="M1",
        )
    )
    session.add(
        ConstraintEntry(
            nurse_id=nurse.id,
            year=2025,
            month=9,
            day=2,
            code="FERIAS",
        )
    )
    session.commit()

    schedule_stream = export_schedule(session, 2025, 9)
    constraints_stream = export_constraints(session, 2025, 9)

    assert schedule_stream.getbuffer().nbytes > 0
    assert constraints_stream.getbuffer().nbytes > 0
