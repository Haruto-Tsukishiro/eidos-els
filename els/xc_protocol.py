"""
xc.py – XC mapping “hub” layer for ELS.

This module shows a tiny public demo of how an XC (“cross-context”)
envelope could look. It takes a canonical emotion snapshot plus some
lightweight context and returns a JSON-like dict that is easy to log
or pass into other layers (e.g. UL or tools).

XC does not interpret emotions. It only carries:
    - the canonical numeric state,
    - some context metadata, and
    - a small safety header.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class CanonicalSnapshot:
    """
    Minimal canonical state carried through XC.

    This mirrors the Emotion-Depth Model used elsewhere in ELS.
    """
    warmth_c: float
    sorrow_pH: float
    drive_mV: float
    u_star: float

    def depth_band(self) -> str:
        """
        Convenience helper: map u_star into a coarse depth band.

        The names are deliberately neutral; UL is free to render them
        as ocean, sky, or any other metaphor family.
        """
        u = self.u_star
        if u <= -0.8:
            return "abyss"
        if u <= -0.3:
            return "deep_rain"
        if u <= 0.3:
            return "mid"
        return "surface"


@dataclass
class XCContext:
    """Lightweight metadata describing where this snapshot came from."""
    source: str = "chat"
    channel: str = "web"
    culture: str = "generic"
    user_id: Optional[str] = None
    tags: Optional[List[str]] = None


@dataclass
class XCSafetyMeta:
    """
    Tiny safety header describing how the signal may be used.

    safety_level:
        "ok"      – safe for normal downstream use.
        "caution" – handle gently (e.g. extreme depth, high distress).
        "hold"    – do not use for user-visible output.
    """
    safety_level: str = "ok"
    reason: str = "normal"
    version: str = "1.0b"


def _auto_safety_for(c: CanonicalSnapshot) -> XCSafetyMeta:
    """
    Derive a very rough safety meta from the canonical state.

    This is intentionally simple and illustrative only. Real systems
    should apply their own safety policies on top of XC.
    """
    # Example rule: extreme negative depth → caution
    if c.u_star <= -0.95:
        return XCSafetyMeta(
            safety_level="caution",
            reason="extreme_depth",
            version="1.0b",
        )
    return XCSafetyMeta()


def to_xc_envelope(
    warmth_c: float,
    sorrow_pH: float,
    drive_mV: float,
    u_star: float,
    *,
    source: str = "chat",
    channel: str = "web",
    culture: str = "generic",
    user_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    safety: Optional[XCSafetyMeta] = None,
) -> Dict[str, Any]:
    """
    Build a minimal XC envelope from canonical values and context.

    Returns:
        A plain dict suitable for logging, debugging, or passing into
        higher-level components (e.g. UL for metaphor rendering).
    """
    canonical = CanonicalSnapshot(
        warmth_c=warmth_c,
        sorrow_pH=sorrow_pH,
        drive_mV=drive_mV,
        u_star=u_star,
    )
    ctx = XCContext(
        source=source,
        channel=channel,
        culture=culture,
        user_id=user_id,
        tags=tags or [],
    )
    safety_meta = safety or _auto_safety_for(canonical)

    # ISO 8601 UTC timestamp
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    envelope: Dict[str, Any] = {
        "xc_version": "1.0b",
        "timestamp": now,
        "canonical": {
            **asdict(canonical),
            "depth_band": canonical.depth_band(),
        },
        "context": asdict(ctx),
        "safety": asdict(safety_meta),
    }
    return envelopeclass XCConnector:
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
