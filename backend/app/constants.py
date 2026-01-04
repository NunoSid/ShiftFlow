from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ServiceShift:
    service: str
    code: str
    label: str
    shift_type: str  # M, T, N, L
    start_minute: int
    end_minute: int
    minutes: int


MINUTES_PER_DAY = 24 * 60


def _duration(start_minute: int, end_minute: int) -> int:
    if end_minute > start_minute:
        return end_minute - start_minute
    return MINUTES_PER_DAY - start_minute + end_minute


DEFAULT_SHIFT_WINDOWS: Dict[str, Tuple[int, int]] = {
    "M": (8 * 60, 14 * 60),  # 08:00-14:00
    "T": (14 * 60, 20 * 60),  # 14:00-20:00
    "N": (20 * 60, (24 + 8) * 60),  # 20:00-08:00 next day
    "L": (14 * 60, 24 * 60),  # 14:00-24:00 (TLs)
}

CODE_SHIFT_WINDOWS: Dict[str, Tuple[int, int]] = {
    "Ma": (450, 720),  # 07:30-12:00
    "TLs": (14 * 60, 24 * 60),
    "Ls": (20 * 60, 24 * 60),
    "MR": (10 * 60, 16 * 60),
    "MR2": (10 * 60, 16 * 60),
}


def default_window_for(code: str, shift_type: str) -> Tuple[int, int]:
    if code in CODE_SHIFT_WINDOWS:
        return CODE_SHIFT_WINDOWS[code]
    return DEFAULT_SHIFT_WINDOWS.get(shift_type, DEFAULT_SHIFT_WINDOWS["M"])


SERVICE_SHIFT_DEFS: List[Tuple[str, str, str, str]] = [
    ("SAP", "Ms", "SAP - Ms", "M"),
    ("SAP", "Ts", "SAP - Ts", "T"),
    ("SAP", "Ls", "SAP - Ls", "L"),
    ("SAP", "TLs", "SAP - TLs", "L"),
    ("Análises", "Ma", "Análises - Ma", "M"),
    ("Consulta Externa", "Me", "Consulta Externa - Me", "M"),
    ("Consulta Externa", "Te", "Consulta Externa - Te", "T"),
    ("Pequenas Cirurgias", "Mp", "Pequenas Cirurgias - Mp", "M"),
    ("Pequenas Cirurgias", "Tp", "Pequenas Cirurgias - Tp", "T"),
    ("Gastroenterologia", "Mg", "Gastroenterologia - Mg", "M"),
    ("Gastroenterologia", "Tg", "Gastroenterologia - Tg", "T"),
    ("Piso 1", "M1", "Piso 1 - M1", "M"),
    ("Piso 1", "T1", "Piso 1 - T1", "T"),
    ("Piso 1", "N1", "Piso 1 - N1", "N"),
    ("Piso 3", "M3", "Piso 3 - M3", "M"),
    ("Piso 3", "T3", "Piso 3 - T3", "T"),
    ("Piso 3", "N3", "Piso 3 - N3", "N"),
    ("Reforço", "MR", "Reforço - MR", "M"),
    ("Reforço", "MR2", "Reforço - MR2", "M"),
    ("Reforço", "NR", "Reforço - NR", "N"),
]


def make_shift(
    service: str,
    code: str,
    label: str,
    shift_type: str,
    override: Optional[Tuple[int, int]] = None,
) -> ServiceShift:
    if override:
        start_minute, end_minute = override
    else:
        start_minute, end_minute = default_window_for(code, shift_type)
    minutes = _duration(start_minute, end_minute)
    return ServiceShift(
        service=service,
        code=code,
        label=label,
        shift_type=shift_type,
        start_minute=start_minute,
        end_minute=end_minute,
        minutes=minutes,
    )


def build_service_shifts(overrides: Optional[Dict[str, Tuple[int, int]]] = None):
    override_map = overrides or {}
    return [
        make_shift(service, code, label, shift_type, override_map.get(code))
        for service, code, label, shift_type in SERVICE_SHIFT_DEFS
    ]


SERVICE_SHIFTS: List[ServiceShift] = build_service_shifts()
SHIFT_LOOKUP: Dict[str, ServiceShift] = {item.code: item for item in SERVICE_SHIFTS}


def apply_shift_overrides(overrides: Dict[str, Tuple[int, int]]) -> None:
    global SERVICE_SHIFTS, SHIFT_LOOKUP
    SERVICE_SHIFTS = build_service_shifts(overrides)
    SHIFT_LOOKUP = {item.code: item for item in SERVICE_SHIFTS}

CATEGORY_SORT_ORDER = {
    "COORDENADOR": 0,
    "CONTRATADO": 1,
    "CONTRATADO_TEMPO_PARCIAL": 2,
    "RV_TEMPO_INTEIRO": 3,
    "RV_TEMPO_PARCIAL": 4,
    "ASSISTENTE_OPERACIONAL": 5,
}


NURSE_CATEGORIES = [
    "COORDENADOR",
    "CONTRATADO",
    "CONTRATADO_TEMPO_PARCIAL",
    "RV_TEMPO_INTEIRO",
    "RV_TEMPO_PARCIAL",
    "ASSISTENTE_OPERACIONAL",
]

BASE_CONSTRAINT_CODES = {
    "": "Livre (segue regra da categoria)",
    "FERIAS": "Férias (bloqueia)",
    "DISPENSA": "Dispensa / DS",
    "INDISPONIVEL": "Indisponível",
    "PEDIDO_FOLGA": "Pedido de folga",
    "PEDIDO_DESCANSO": "Pedido descanso",
    "PEDIDO_DESCANSO_FOLGA": "Descanso ou folga",
    "DISPONIVEL": "Disponível (parcial)",
    "FERIADO": "Feriado",
    "FERIADO_TRAB": "Feriado trabalhado",
}

CONSTRAINT_CODES = dict(BASE_CONSTRAINT_CODES)
CONSTRAINT_COMBOS = [
    "M",
    "T",
    "L",
    "N",
    "MT",
    "ML",
    "MN",
    "TL",
    "TN",
    "LN",
    "MTL",
    "MTN",
    "MLN",
    "TLN",
    "MTLN",
]
for combo in CONSTRAINT_COMBOS:
    CONSTRAINT_CODES[f"DISPONIVEL_{combo}"] = f"Disponível ({combo})"
    CONSTRAINT_CODES[f"INDISPONIVEL_{combo}"] = f"Indisponível ({combo})"

DEFAULT_PENALTIES = {
    "unfilled": 5000,
    "pedido": 300,
    "hours_target": 5,
    "night_sequence": 50,
    "rest_followup": 100,
    "double_service_mismatch": 40,
    "bank_balance": 2,
    "shift_balance": 4,
}

PORTUGAL_FIXED_HOLIDAYS = [
    (1, 1),
    (4, 25),
    (5, 1),
    (6, 10),
    (8, 15),
    (10, 5),
    (11, 1),
    (12, 1),
    (12, 8),
    (12, 25),
]

WEEKDAY_PT = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
WEEKDAY_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

SERVICE_COLORS = {
    "SAP": "#fde68a",
    "Análises": "#bfdbfe",
    "Consulta Externa": "#c4b5fd",
    "Pequenas Cirurgias": "#fbcfe8",
    "Gastroenterologia": "#bbf7d0",
    "Piso 1": "#fecaca",
    "Piso 3": "#ddd6fe",
    "Reforço": "#fed7aa",
}
