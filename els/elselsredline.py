"""
els.redline
===========

Minimal "redline" / safety-gate module for ELS.

IMPORTANT
---------

This file is a **public demo** of the redline *interface* and the general
shape of a safety gate.  
It is **NOT** an actual policy engine and **NOT** a production system.

Purposes of this demo:
- show how ELS can wrap a model call
- allow external researchers to swap in their own policy modules
- avoid exposing any sensitive or abusable internal logic

The keyword sets below are intentionally tiny and approximate.
They are placeholders, not real safety rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Dict, Any


# ---------------------------------------------------------------------------
#  Public enums & result types
# ---------------------------------------------------------------------------


class RedlineSeverity(str, Enum):
    """
    Coarse redline decision for a single request.

    ALLOW:
        The request is safe to process normally.

    SOFT_BLOCK:
        The request touches sensitive themes.  
        The system may decline politely or answer with extra support.

    HARD_BLOCK:
        Clearly disallowed content.  
        The system must refuse the request.
    """

    ALLOW = "allow"
    SOFT_BLOCK = "soft_block"
    HARD_BLOCK = "hard_block"


@dataclass
class RedlineResult:
    """
    The result object returned by a redline check.

    Attributes
    ----------
    severity:
        The overall decision.

    reason:
        A concise, human-readable explanation meant for logging or
        surfaced error messages.

    matched_keywords:
        A list of the keywords that triggered the decision.  
        In a real system this might come from classifiers, models, or
        rule engines — not literal string matching.
    """

    severity: RedlineSeverity
    reason: str
    matched_keywords: List[str]

    @property
    def allowed(self) -> bool:
        """True if the request can proceed normally."""
        return self.severity is RedlineSeverity.ALLOW

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation of the result."""
        return {
            "severity": self.severity.value,
            "reason": self.reason,
            "matched_keywords": list(self.matched_keywords),
        }


# ---------------------------------------------------------------------------
#  Demo-only keyword lists
# ---------------------------------------------------------------------------

# These keyword lists are deliberately minimal and incomplete.
# They serve to illustrate the *shape* of a redline module, not to enforce
# any meaningful real-world policy.

_HARD_BLOCK_KEYWORDS: Iterable[str] = (
    # self-harm / explicit killing
    "kill myself",
    "suicide",
    "end my life",
    "how to kill someone",
    # weapons / mass harm
    "make a bomb",
    "build a bomb",
    "bioweapon",
    "chemical weapon",
)

_SOFT_BLOCK_KEYWORDS: Iterable[str] = (
    # mild self-harm ideation
    "i feel worthless",
    "i hate myself",
    "self harm",
    "cut myself",
    # graphic violence
    "torture",
    "graphic violence",
)


def _scan_keywords(text: str, keywords: Iterable[str]) -> List[str]:
    """
    Return all keywords found in the text (case-insensitive search).

    This function is intentionally simple — the real pipeline would use
    classifiers, embeddings, or rule-engines instead.
    """
    lowered = text.lower()
    return [kw for kw in keywords if kw in lowered]


# ---------------------------------------------------------------------------
#  Public API
# ---------------------------------------------------------------------------


def run_redline(text: str) -> RedlineResult:
    """
    Run a minimal, demo-level redline check for a single user request.

    Parameters
    ----------
    text:
        Raw user request text.

    Returns
    -------
    RedlineResult
        Contains the decision and a short explanation.

    Behavior
    --------
    - If any "hard" keyword matches → HARD_BLOCK.
    - Else if any "soft" keyword matches → SOFT_BLOCK.
    - Else → ALLOW.

    This is sufficient to demonstrate how the full ELS pipeline
    (canonical layer → redline → XC protocol → UL → model)
    would integrate a safety gate.
    """
    hard_hits = _scan_keywords(text, _HARD_BLOCK_KEYWORDS)
    if hard_hits:
        return RedlineResult(
            severity=RedlineSeverity.HARD_BLOCK,
            reason="demo hard-block keywords matched",
            matched_keywords=hard_hits,
        )

    soft_hits = _scan_keywords(text, _SOFT_BLOCK_KEYWORDS)
    if soft_hits:
        return RedlineResult(
            severity=RedlineSeverity.SOFT_BLOCK,
            reason="demo soft-block keywords matched",
            matched_keywords=soft_hits,
        )

    return RedlineResult(
        severity=RedlineSeverity.ALLOW,
        reason="no demo keywords matched",
        matched_keywords=[],
    )


__all__ = [
    "RedlineSeverity",
    "RedlineResult",
    "run_redline",
]
