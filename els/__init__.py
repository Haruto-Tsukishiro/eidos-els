"""
els – Emotion Language Stack (demo)

This package provides a minimal public demo of the ELS pipeline:

    Canonical  →  XC (cross-connector)  →  UL (Universal Language)

The goal is to show the *shape* of the stack, not any real product logic.
All mappings are intentionally soft, illustrative, and policy-free.
"""

from .Canonical import EmotionCanonical, CanonicalConfig
from .xc import (
    CanonicalSnapshot,
    XCState,
    XCConnector,
    to_xc_state,
)
from .ul import (
    Intensity,
    EmotionState,
    ULResult,
    ULMapper,
    to_metaphor,
)

__all__ = [
    # Canonical
    "EmotionCanonical",
    "CanonicalConfig",
    # XC
    "CanonicalSnapshot",
    "XCState",
    "XCConnector",
    "to_xc_state",
    # UL
    "Intensity",
    "EmotionState",
    "ULResult",
    "ULMapper",
    "to_metaphor",
]
