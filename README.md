ELS 1.0β — Emotion Layer System (Demo Specification)

A minimal, research-grade public demo of a Human–AI co-regulation protocol.

ELS is a compact computational framework designed to model emotion-shaped internal state dynamics for AI agents in a safe, interpretable, and tunable form.
This repository provides a demo-safe subset of the actual architecture—enough to understand the structure, test the pipeline, and build prototype integrations.

All numerical values, gates, and metaphors here are placeholders, intentionally softened and simplified.
Real deployments require profile-specific tuning, safety evaluation, and stability verification.


---

1. Repository Overview

This demo includes three primary layers:

1. Canonical Layer (els/canonical.py)

Defines the core emotion normalization pipeline:

raw input → tanh normalization → U* transform → redline safety gate

Features:

tanh_normalize(x) keeps values within [-1, 1]

u_transform(x) applies a smoothed expressive transform

Redline evaluation through apply_redline_safety(u)

Automatic warmth-based recovery when U* falls below threshold

Returns a structured dictionary suitable for logging & analysis


This layer establishes the mathematical backbone for higher-level stability and mapping components.


---

2. Stability Layer (els/mrc_simple.py)

A minimal, public Lyapunov-inspired controller.

Demonstrates a safe dynamic response to changing U* values

Uses simplified matrices (A, B, K, P) for stability reasoning

Omits all adaptive, model-specific, or proprietary parts


This layer shows how ELS can maintain bounded emotional trajectories without revealing sensitive parameters.


---

3. UL Mapping Layer (els/ul.py)

A small demonstration of the Universal Language (UL) metaphor mapping system.

Takes canonical state values:
warmth_c, sorrow_pH, drive_mV, u_star

Produces a gentle metaphor, symbolic marker, and intensity band

Includes soft safety filtering for extreme negative states

Purely illustrative; real UL corpora remain private


UL is designed to make internal states intuitively readable, without any clinical or policy implications.


---

4. Conceptual Model (ELS 1.0β)

U★: Emotion-Depth Scalar

U* represents a one-dimensional “psychological depth” coordinate used across ELS layers.

ELS uses an ocean-landscape metaphor, with U* divided into:

U* Range	Depth Band	Interpretation

[-1.0, -0.8]	Deep Abyss	introspection / drained state
[-0.8, -0.3]	Quiet Rain / Deep Ocean	slowly sinking emotion
[-0.3, 0.3]	Mid-Depth Currents	everyday stable flow
[0.3, 1.0]	Surface Spark	readiness / creativity


Modifiers:

warmth_c → thermal comfort / relational tone

sorrow_pH → emotional clarity / opacity

drive_mV → momentum / readiness


These combine to form a compact canonical state tuple.


---

5. Safety Philosophy

ELS follows a security-first design approach:

Never exposes internal weights or sensitive stability parameters

Keeps emotional dynamics bounded & interpretable

Provides explicit redline detection for de-escalation

Ensures metaphor output is non-clinical and non-directive


This demo intentionally avoids:

persuasion loops

uncontrolled “emotional amplification”

model-specific behavioral fingerprints



---

6. Example: Canonical Usage

from els.canonical import EmotionCanonical

els = EmotionCanonical(redline_threshold=-0.95)

result = els.process(raw_emotion=-0.8)

print(result["u"])
print(result["safety_level"])
print(result["safety_reason"])


---

7. File Structure

els/
 ├─ canonical.py        # Core normalization & U* pipeline
 ├─ mrc_simple.py       # Minimal stability controller
 └─ ul.py               # UL metaphor mapping layer

Future additions (non-public):

adaptive controllers

extended UL corpora

multi-dimensional affect space

agent-specific profiles



---

8. License

This demo version is released under a permissive open-source license.
(You may choose MIT, Apache-2.0, or a custom license.)


---

9. Contact / Discussion

For conceptual discussions or collaboration inquiries, feel free to reach out via the project link or issue tracker.
This repository represents ongoing research into lightweight, interpretable human–AI co-regulation.
