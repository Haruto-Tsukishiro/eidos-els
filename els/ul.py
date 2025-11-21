"""
ul.py – UL mapping layer for ELS.

This module is a tiny *public demo* of how an ELS-style
"Universal Language" layer **could** look.

It takes a small numeric emotion state (warmth_c, sorrow_pH, drive_mV, u_star)
and returns:
  - a safe metaphorical description,
  - a simple symbol,
  - a coarse intensity band,
  - and a lightweight safety note.

All mappings here are deliberately soft, poetic, and *not* tied to any
real-world policy or product behavior. They are placeholders to show
the *shape* of a UL layer only.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple


class Intensity(str, Enum):
    """Coarse intensity band for the demo output."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class EmotionState:
    """
    Minimal emotion state passed into the UL layer.

    All values are assumed to be already normalized into the
    ELS canonical ranges (e.g. U* in [-1.0, 1.0]).
    """
    warmth_c: float
    sorrow_pH: float
    drive_mV: float
    u_star: float


@dataclass
class ULResult:
    """Result of the metaphor mapping."""
    text: str
    symbol: str
    intensity: Intensity
    safety_note: str


class ULMapper:
    """
    Minimal metaphor generator for the ELS demo.

    This class intentionally avoids any real-world policy logic.
    It only demonstrates the *shape* of a mapping layer that
    turns internal ELS scalars into a human-readable description.
    """

    def __init__(self, culture: str = "generic", style: str = "poetic") -> None:
        self.culture = culture
        self.style = style

    # ---- public API -----------------------------------------------------

    def map(
        self,
        state: EmotionState,
        context: Optional[Dict[str, Any]] = None,
    ) -> ULResult:
        """
        Map an EmotionState into a ULResult.

        Args:
            state:
                Canonical emotion state in ELS units.
            context:
                Optional lightweight context dict. Not used in this
                demo, but kept to show where culture- or user-specific
                hooks would plug in.

        Returns:
            ULResult with a metaphorical description.
        """
        base_text = self._base_metaphor(state)
        safe_text, safety_note = self._apply_safety_filters(base_text, state)
        symbol = self._symbol_for(state)
        intensity = self._intensity_for(state)

        return ULResult(
            text=safe_text,
            symbol=symbol,
            intensity=intensity,
            safety_note=safety_note,
        )

    # ---- internal helpers -----------------------------------------------

    def _base_metaphor(self, s: EmotionState) -> str:
        """
        Build a base metaphor string from the numeric state.

        U* controls the overall depth of the scene.
        Warmth / sorrow / drive add gentle modifiers.
        """
        u = s.u_star

        # Depth image from U*
        if u <= -0.8:
            core = "a deep seabed where light is faint"
        elif u <= -0.3:
            core = "rain falling in the quiet ocean"
        elif u <= 0.3:
            core = "slow mid-depth currents"
        else:
            core = "surface waves glittering with light"

        # Warmth modulation
        if s.warmth_c >= 0.7:
            core = "warm " + core
        elif s.warmth_c <= 0.2:
            core = "cool " + core

        # Sorrow: lower pH → more sorrow, higher → clearer feeling
        if s.sorrow_pH < 6.7:
            core += ", carrying a soft echo of sadness"
        elif s.sorrow_pH > 7.3:
            core += ", feeling unusually clear"

        # Drive: near 0 → rest, high → ready to move again
        if s.drive_mV > 180:
            core += ", already ready to move again"
        elif s.drive_mV < 40:
            core += ", almost at rest"

        return core

    def _intensity_for(self, s: EmotionState) -> Intensity:
        """Rough intensity band derived from the state."""
        if abs(s.u_star) > 0.9 or s.drive_mV > 220:
            return Intensity.HIGH

        if abs(s.u_star) < 0.3 and 0.3 <= s.warmth_c <= 0.7:
            return Intensity.LOW

        return Intensity.MEDIUM

    def _symbol_for(self, s: EmotionState) -> str:
        """
        Map the state into a simple symbolic icon.

        This is mostly for UI / visualization demos.
        """
        u = s.u_star
        if u <= -0.8:
            return "🌊"  # deep wave
        if u <= -0.3:
            return "🌧️"  # gentle rain
        if u <= 0.3:
            return "💧"  # droplet / current
        return "❇️"      # sparkling surface

    def _apply_safety_filters(
        self,
        text: str,
        s: EmotionState,
    ) -> Tuple[str, str]:
        """
        Apply a few toy safety rules on top of the metaphor.

        In a real system this is where we would run semantic safety,
        user preferences, and cultural adaptation. Here we only soften
        very extreme negative states and keep everything gentle.
        """
        note = "normal"

        # Example: extreme negative U* → soften and add a clear note.
        if s.u_star <= -0.95:
            softened = (
                "Even in the deepest water, you are gently held by the ocean."
            )
            note = "softened_extreme_negative"
            return softened, note

        return text, note


def to_metaphor(
    warmth_c: float,
    sorrow_pH: float,
    drive_mV: float,
    u_star: float,
    culture: str = "generic",
    style: str = "poetic",
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Convenience wrapper for callers that do not want to manage a ULMapper.

    Returns:
        A plain dict that is easy to log or serialize.
    """
    mapper = ULMapper(culture=culture, style=style)
    state = EmotionState(
        warmth_c=warmth_c,
        sorrow_pH=sorrow_pH,
        drive_mV=drive_mV,
        u_star=u_star,
    )
    result = mapper.map(state, context=context)
    return {
        "text": result.text,
        "symbol": result.symbol,
        "intensity": result.intensity.value,
        "safety_note": result.safety_note,
    }
