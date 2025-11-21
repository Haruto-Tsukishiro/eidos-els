"""
ELS Cross-Connector (XC) Demo Layer

This module demonstrates the *shape* of a cross-connector layer
that links the Canonical ELS pipeline to downstream modules such
as UL (Universal Language layer).

XC acts as:
  - a hub for normalized emotion states
  - a compatibility layer for downstream modules
  - a transparent pass-through for safety information

This file intentionally contains *no* sensitive logic.
Everything here is minimal and safe for a public demo.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class XCState:
    """
    Unified representation of a canonical emotion state,
    ready to be delivered to downstream layers.

    This is what UL, UI, or analytics modules consume.
    """
    raw: float
    n: float
    u: float
    safety_level: str
    safety_reason: str
    warmth_c: float


class XCConnector:
    """
    Minimal cross-connector for ELS.

    In a full system, XC would support:
      - personality hooks
      - culture adaptation
      - conversation context
      - multi-signal fusion
      - caching / batching

    In this public demo, XC simply exposes a clean normalized
    structure so external researchers can plug in UL or
    other experimental modules.
    """

    def __init__(self, mode: str = "demo") -> None:
        self.mode = mode

    def canonical_to_xc(
        self,
        canonical_dict: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> XCState:
        """
        Convert the canonical pipeline output into an XCState.

        Args:
          canonical_dict:
            Dictionary emitted by EmotionCanonical.process().
          context:
            Optional metadata or runtime hints.

        Returns:
          XCState: clean normalized state for downstream modules.
        """
        return XCState(
            raw=canonical_dict["raw"],
            n=canonical_dict["n"],
            u=canonical_dict["u"],
            safety_level=str(canonical_dict["safety_level"]),
            safety_reason=str(canonical_dict["safety_reason"]),
            warmth_c=float(canonical_dict.get("warmth_c", 0.0)),
        )


# convenience wrapper ----------------------------------------------------------

def to_xc_state(
    canonical_dict: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Convert to a plain dict instead of XCState, for quick logging
    or for languages that do not want Python dataclasses.

    Returns:
      A dict with normalized fields.
    """
    xc = XCConnector()
    state = xc.canonical_to_xc(canonical_dict, context=context)
    return {
        "raw": state.raw,
        "n": state.n,
        "u": state.u,
        "safety_level": state.safety_level,
        "safety_reason": state.safety_reason,
        "warmth_c": state.warmth_c,
    }
