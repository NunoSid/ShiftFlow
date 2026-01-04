from sqlalchemy.orm import Session

from .solver import refresh_shift_lookup


def ensure_shift_settings(session: Session) -> None:
    refresh_shift_lookup(session)


def refresh_shift_settings(session: Session) -> None:
    refresh_shift_lookup(session)
