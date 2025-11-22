"""
els – Emotion Language Stack (demo)

Public-safe subset:
- Canonical layer (U* transform + safety gate)
- UL layer (metaphor mapping)

XC and advanced controllers are intentionally excluded from the public API.
"""

from .canonical import (
    EmotionCanonical,
    SafetyGateResult,
    SafetyLevel,
    apply_redline_safety,
)

from .ul import (
    Intensity,
    EmotionState,
    ULResult,
    ULMapper,
    to_metaphor,
)

__all__ = [
    "EmotionCanonical",
    "SafetyGateResult",
    "SafetyLevel",
    "apply_redline_safety",
    "Intensity",
    "EmotionState",
    "ULResult",
    "ULMapper",
    "to_metaphor",
]

__version__ = "0.1.0"
