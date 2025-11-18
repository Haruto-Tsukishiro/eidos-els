"""
ELS: Emotion Layer System (Demo)

Public package interface.
"""

from .core import ELSCore, ELSConfig
from .canonical import EmotionCanonical, SafetyLevel, SafetyGateResult

__all__ = [
    "ELSCore",
    "ELSConfig",
    "EmotionCanonical",
    "SafetyLevel",
    "SafetyGateResult",
]
