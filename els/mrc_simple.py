# els/mrc_simple.py

"""
mrc_simple.py
--------------

Minimal "stability scoring" module for ELS.

This is intentionally **not** a real Lyapunov controller.
It only provides:
- a generic interface
- a dummy stability score in [-2.0, +2.0]
- a few helper functions

So that:
- the public repository can demonstrate the *shape* of the system,
- while any real control logic / parameters stay private.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class StabilityBand(str, Enum):
    """Coarse bands for interpreting the stability score."""
    STABLE = "stable"
    BORDERLINE = "borderline"
    UNSTABLE = "unstable"


@dataclass
class StabilityResult:
    """
    High-level result of the stability scoring.

    Attributes
    ----------
    score : float
        Normalized stability score in approximately [-2.0, +2.0].
        Convention (suggested, not mathematically strict):
        - score >= 0.0 : more stable
        - score <= -1.0: critically unstable (red line)
    band : StabilityBand
        Coarse interpretation of the score.
    meta : dict
        Optional metadata for downstream modules.
    """
    score: float
    band: StabilityBand
    meta: Dict[str, Any]


def _dummy_stability_core(state: Dict[str, Any]) -> float:
    """
    Internal placeholder for the real stability computation.

    This function is deliberately simple and **not** scientifically meaningful.
    It just:
    - collects a few numeric hints from `state`
    - combines them into a rough score in [-2.0, +2.0]

    Replace this with your own implementation in private forks.
    """
    # Extract a few heuristic features with defaults
    # NOTE: these keys are intentionally generic and optional.
    intensity = float(state.get("intensity", 0.0))      # e.g. |emotion intensity|
    volatility = float(state.get("volatility", 0.0))    # e.g. slope / variability
    fatigue = float(state.get("fatigue", 0.0))          # e.g. conversation length, etc.

    # Very simple heuristic:
    # - higher intensity, volatility, fatigue → more negative (less stable)
    raw = -(0.4 * intensity + 0.3 * volatility + 0.3 * fatigue)

    # Clamp to a safe range
    if raw > 2.0:
        raw = 2.0
    if raw < -2.0:
        raw = -2.0

    return raw


def interpret_band(score: float) -> StabilityBand:
    """
    Map a numeric score onto a coarse band.

    Thresholds are intentionally loose and can be tuned per project.
    """
    if score <= -1.0:
        return StabilityBand.UNSTABLE
    if score <= -0.2:
        return StabilityBand.BORDERLINE
    return StabilityBand.STABLE


def compute_stability(
    state: Dict[str, Any],
    *,
    previous_score: Optional[float] = None,
) -> StabilityResult:
    """
    Public entry-point for ELS to obtain a stability score.

    Parameters
    ----------
    state : dict
        Arbitrary ELS state snapshot.
        It may contain keys like:
        - "intensity"
        - "volatility"
        - "fatigue"
      but all are optional.
    previous_score : float, optional
        If provided, allows simple smoothing / hysteresis.

    Returns
    -------
    StabilityResult
        A coarse view of stability for use by higher layers
        (e.g. safety gating, logging, UI).
    """
    score = _dummy_stability_core(state)

    # Optional simple smoothing with previous value
    if previous_score is not None:
        score = 0.7 * previous_score + 0.3 * score

    band = interpret_band(score)
    meta = {
        "previous_score": previous_score,
    }

    return StabilityResult(score=score, band=band, meta=meta)
