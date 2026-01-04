from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlmodel import Session

from .config import DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, future=True
)


@contextmanager
def get_session() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def run_migrations():
    with engine.begin() as conn:
        table_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='nurse'"
            )
        ).fetchone()
        if table_exists:
            columns = {
                row[1]
                for row in conn.execute(text("PRAGMA table_info(nurse)")).fetchall()
            }
            if "weekly_hours" not in columns:
                conn.execute(
                    text("ALTER TABLE nurse ADD COLUMN weekly_hours INTEGER DEFAULT 40")
                )
            if "hour_balance_minutes" not in columns:
                conn.execute(
                    text(
                        "ALTER TABLE nurse ADD COLUMN hour_balance_minutes INTEGER DEFAULT 0"
                    )
                )
            if "display_order" not in columns:
                conn.execute(
                    text("ALTER TABLE nurse ADD COLUMN display_order INTEGER DEFAULT 0")
                )
            if "user_id" not in columns:
                conn.execute(text("ALTER TABLE nurse ADD COLUMN user_id INTEGER"))
            # Ensure defaults applied
            conn.execute(
                text(
                    "UPDATE nurse SET weekly_hours = COALESCE(weekly_hours, 40), "
                    "hour_balance_minutes = COALESCE(hour_balance_minutes, 0), "
                    "display_order = COALESCE(display_order, id)"
                )
            )
        manual_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='manual_holiday'"
            )
        ).fetchone()
        if manual_exists:
            columns = {
                row[1]
                for row in conn.execute(text("PRAGMA table_info(manual_holiday)")).fetchall()
            }
            if "action" not in columns:
                conn.execute(
                    text("ALTER TABLE manual_holiday ADD COLUMN action TEXT DEFAULT 'ADD'")
                )

        month_config_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='month_config'"
            )
        ).fetchone()
        if month_config_exists:
            columns = {
                row[1]
                for row in conn.execute(text("PRAGMA table_info(month_config)")).fetchall()
            }
            if "min_rest_hours" not in columns:
                conn.execute(
                    text("ALTER TABLE month_config ADD COLUMN min_rest_hours INTEGER DEFAULT 11")
                )
            if "prefer_folga_after_nd" not in columns:
                conn.execute(
                    text(
                        "ALTER TABLE month_config ADD COLUMN prefer_folga_after_nd INTEGER DEFAULT 0"
                    )
                )
            conn.execute(
                text(
                    "UPDATE month_config SET prefer_folga_after_nd = COALESCE(prefer_folga_after_nd, 0)"
                )
            )

        service_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='service'"
            )
        ).fetchone()
        if service_exists:
            columns = {
                row[1]
                for row in conn.execute(text("PRAGMA table_info(service)")).fetchall()
            }
            if "role" not in columns:
                conn.execute(
                    text("ALTER TABLE service ADD COLUMN role TEXT DEFAULT 'ENFERMEIRO'")
                )
            conn.execute(text("UPDATE service SET role = COALESCE(role, 'ENFERMEIRO')"))

        availability_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='availability_request'"
            )
        ).fetchone()
        if not availability_exists:
            conn.execute(
                text(
                    """
                    CREATE TABLE availability_request (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        nurse_id INTEGER NOT NULL,
                        year INTEGER NOT NULL,
                        month INTEGER NOT NULL,
                        day INTEGER NOT NULL,
                        code TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'PENDING',
                        reason TEXT,
                        decided_by INTEGER,
                        decided_at DATETIME,
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT uq_availability_request UNIQUE (user_id, year, month, day)
                    )
                    """
                )
            )

        requirements_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='monthly_requirement'"
            )
        ).fetchone()
        service_shift_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='service_shift'"
            )
        ).fetchone()
        if requirements_exists and service_shift_exists:
            conn.execute(
                text(
                    """
                    UPDATE monthly_requirement
                    SET service_code = (
                        SELECT service_code FROM service_shift
                        WHERE service_shift.shift_code = monthly_requirement.shift_code
                        LIMIT 1
                    )
                    WHERE service_code NOT IN (SELECT code FROM service)
                    """
                )
            )

        swap_exists = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='swap_request'")
        ).fetchone()
        if swap_exists:
            columns = {
                row[1]
                for row in conn.execute(text("PRAGMA table_info(swap_request)")).fetchall()
            }
            if "observations" not in columns:
                conn.execute(
                    text("ALTER TABLE swap_request ADD COLUMN observations TEXT")
                )

        category_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='professional_category'"
            )
        ).fetchone()
        if not category_exists:
            conn.execute(
                text(
                    """
                    CREATE TABLE professional_category (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        role TEXT NOT NULL,
                        sort_order INTEGER NOT NULL DEFAULT 0,
                        is_active INTEGER NOT NULL DEFAULT 1,
                        CONSTRAINT uq_professional_category UNIQUE (name, role)
                    )
                    """
                )
            )

        swap_exists = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='swap_request'"
            )
        ).fetchone()
        if swap_exists:
            columns = {
                row[1]
                for row in conn.execute(text("PRAGMA table_info(swap_request)")).fetchall()
            }
            if "desired_service_code" not in columns:
                conn.execute(
                    text("ALTER TABLE swap_request ADD COLUMN desired_service_code TEXT")
                )
            if "desired_shift_code" not in columns:
                conn.execute(
                    text("ALTER TABLE swap_request ADD COLUMN desired_shift_code TEXT")
                )
