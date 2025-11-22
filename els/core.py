"""
ELS Core API

High-level one-line interface for the Emotion Layer System (ELS).
"""

from dataclasses import dataclass
from typing import Optional

from .canonical import EmotionCanonical, SafetyGateResult


@dataclass
class ELSConfig:
    """
    Configuration for the ELSCore wrapper.

    All values here are demo defaults. Real deployments
    are expected to tune or learn them per agent.
    """
    redline_threshold: float = -0.95


class ELSCore:
    """
    High-level wrapper around the canonical ELS pipeline.

    Usage:
        els = ELSCore()
        result = els.step(raw_emotion=-0.8)
    """

    def __init__(self, config: Optional[ELSConfig] = None) -> None:
        if config is None:
            config = ELSConfig()

        self.config = config
        self.canonical = EmotionCanonical()
        # apply config to the canonical layer
        self.canonical.redline_threshold = config.redline_threshold

    def step(self, raw_emotion: float) -> dict:
        """
        Process a single raw emotion sample through the canonical pipeline
        and return a structured SafetyGateResult.
        """
        return self.canonical.process(raw_emotion)
