"""
els – Emotion Language Stack (demo)

This package provides a minimal public demo of the ELS pipeline:

    Canonical  →  XC (cross-connector)  →  UL (Universal Language)

The goal is to show the *shape* of the stack, not any real-world
policy or product behavior. All mappings are intentionally soft,
illustrative, and poetic.
"""

from .Canonical import (
    EmotionCanonical,
    SafetyGateResult,
    SafetyLevel,
    apply_redline_safety,
)

from .xc import (
    CanonicalSnapshot,
    XCState,
    XCConnector,
    canonical_to_xc,
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
    # Canonical layer
    "EmotionCanonical",
    "SafetyGateResult",
    "SafetyLevel",
    "apply_redline_safety",

    # XC layer
    "CanonicalSnapshot",
    "XCState",
    "XCConnector",
    "canonical_to_xc",
    "to_xc_state",

    # UL layer
    "Intensity",
    "EmotionState",
    "ULResult",
    "ULMapper",
    "to_metaphor",
]
