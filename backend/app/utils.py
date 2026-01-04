from typing import Iterable, List, Sequence, TypeVar

from .constants import CATEGORY_SORT_ORDER
from .models import Nurse

T = TypeVar("T", bound=Nurse)


def sort_nurses_by_category(nurses: Sequence[T]) -> List[T]:
    return sorted(
        nurses,
        key=lambda nurse: (
            CATEGORY_SORT_ORDER.get(nurse.category, 99),
            nurse.display_order or 0,
            nurse.name.lower(),
        ),
    )
