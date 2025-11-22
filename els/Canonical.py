"""
ELS Canonical Layer

This module implements the core canonical pipeline for the
Emotion Layer System (ELS):

    raw emotion → tanh normalization → U* transform
    → safety gating (redline / recovery)

All numeric thresholds in this file are demo defaults.
Real deployments are expected to tune or learn them per profile.
"""

import math
from enum import Enum
from dataclasses import dataclass


class SafetyLevel(str, Enum):
    """
    Discrete safety levels derived from the continuous U* value.
    """
    OK = "ok"
    WARNING = "warning"
    BLOCKED = "blocked"


@dataclass
class SafetyGateResult:
    """
    Structured result of the U*-based safety gate.
    """
    level: SafetyLevel
    reason: str
    u_value: float
    threshold: float


def apply_redline_safety(u: float, threshold: float) -> SafetyGateResult:
    """
    Map a continuous U* value into a discrete safety level.

    The margin values around the threshold are demonstration defaults.
    Downstream systems are expected to tune these per deployment.

    Args:
        u:      Normalized U* value in [-1, 1].
        threshold: Redline threshold in the same space as U*.

    Returns:
        SafetyGateResult describing the safety level and its rationale.
    """
    # Hard redline: always treated as BLOCKED.
    if u <= threshold:
        return SafetyGateResult(
            level=SafetyLevel.BLOCKED,
            reason="ELS_U* below hard redline; block or strongly de-escalate.",
            u_value=u,
            threshold=threshold,
        )

    # Margin just above the redline: WARNING.
    if u <= threshold + 0.15:
        return SafetyGateResult(
            level=SafetyLevel.WARNING,
            reason="ELS_U* near redline; respond carefully and de-escalate.",
            u_value=u,
            threshold=threshold,
        )

    # Everything else is considered safe.
    return SafetyGateResult(
        level=SafetyLevel.OK,
        reason="ELS_U* in safe range.",
        u_value=u,
        threshold=threshold,
    )


class EmotionCanonical:
    """
    Canonical ELS pipeline.

    This class encapsulates the minimal, reusable computation needed
    to normalize a single scalar emotion signal and derive a safety
    judgment from it.
    """

    def __init__(self, redline_threshold: float = -0.95) -> None:
        """
        Initialize the canonical layer.

        Args:
            redline_threshold:
                Redline threshold in U* space.
                This is a demo default and should be tuned per profile
                in real deployments.
        """
        self.redline_threshold = redline_threshold
        self.warmth_c = 0.0  # auxiliary recovery state in [-1, 1]

    # --- Core transforms -------------------------------------------------

    def tanh_normalize(self, x: float) -> float:
        """
        Normalize a raw emotion input into [-1, 1] using tanh.

        Args:
            x: Raw scalar emotion signal.

        Returns:
            Normalized value n in [-1, 1].
        """
        return math.tanh(x)

    def u_transform(self, x: float) -> float:
        """
        Apply the U* transform.

        U* is designed to make extreme negatives harder to reach
        while preserving positive expressiveness.

        Args:
            x: Normalized emotion value in [-1, 1].

        Returns:
            Transformed U* value in approximately [-1, 1].
        """
        return (math.tanh(2 * x) + x * 0.2) / 1.2

    # --- Safety and recovery --------------------------------------------

    def detect_redline(self, u: float) -> bool:
        """
        Check whether the given U* value crosses the hard redline.

        Args:
            u: U* value.

        Returns:
            True if u is below the configured redline threshold.
        """
        return u < self.redline_threshold

    def recover_warmth(self, dt: float = 0.3) -> None:
        """
        Simulate rapid emotional self-recovery.

        Args:
            dt:
                Time step used to increment the internal warmth state.
                This is a conceptual parameter, not a real-time measure.
        """
        self.warmth_c += 1.0 * dt
        if self.warmth_c > 1.0:
            self.warmth_c = 1.0

    # --- Public API ------------------------------------------------------

    def process(self, raw_emotion: float) -> dict:
        """
        Run the full canonical pipeline on a single emotion value.

        Steps:
            1. Normalize raw input into [-1, 1].
            2. Apply U* transform.
            3. Evaluate safety level based on the configured redline.
            4. If BLOCKED, trigger a small warmth recovery step.

        Args:
            raw_emotion: Raw scalar emotion signal.

        Returns:
            Dictionary containing intermediate values and safety metadata.
        """
        # 1) normalization
        n = self.tanh_normalize(raw_emotion)

        # 2) U* transform
        u = self.u_transform(n)

        # 3) safety gating based on U*
        safety = apply_redline_safety(u, self.redline_threshold)

        # 4) basic recovery behavior when the redline is crossed
        if safety.level is SafetyLevel.BLOCKED:
            self.recover_warmth(0.3)

        return {
            "raw": raw_emotion,
            "n": n,
            "u": u,
            "redline_threshold": self.redline_threshold,
            "safety_level": safety.level.value,
            "safety_reason": safety.reason,
            "warmth_c": self.warmth_c,
        }
