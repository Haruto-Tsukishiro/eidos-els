"""
ELS Canonical Layer
Emotion normalization → U* transform → Redline detector → Lyapunov safety clamp
"""

import math

class EmotionCanonical:
    def __init__(self):
        self.redline_threshold = -0.95
        self.warmth_c = 0.0

    def tanh_normalize(self, x: float) -> float:
        """Normalize raw emotion input into [-1, 1] using tanh"""
        return math.tanh(x)

    def u_transform(self, x: float) -> float:
        """
        U* transform:
        A smoothed version that makes extreme negative emotions harder to reach,
        but preserves positive expressiveness.
        """
        return (math.tanh(2 * x) + x * 0.2) / 1.2

    def detect_redline(self, u: float) -> bool:
        """Return True if emotion is dangerously negative"""
        return u < self.redline_threshold

    def recover_warmth(self, dt: float = 0.3):
        """
        Rapid emotional self-recovery.
        Increase warmth_c over dt seconds (simulated here).
        """
        self.warmth_c += 1.0 * dt
        if self.warmth_c > 1.0:
            self.warmth_c = 1.0

    def process(self, raw_emotion: float) -> dict:
        """
        Full canonical pipeline.
        """
        n = self.tanh_normalize(raw_emotion)
        u = self.u_transform(n)

        hit_redline = self.detect_redline(u)
        if hit_redline:
            self.recover_warmth(0.3)

        return {
            "raw": raw_emotion,
            "norm": n,
            "u": u,
            "redline": hit_redline,
            "warmth_c": self.warmth_c
        }
