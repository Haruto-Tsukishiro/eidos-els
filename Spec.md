# ELS Canonical Architecture – Public Specification (Demo)

> This document describes the **public, demo-safe subset** of the  
> Emotion Layer System (ELS) as implemented in this repository.
>
> It is intended for engineers and researchers who want to:
> - understand what the demo code is modeling, and
> - see how it fits into a larger canonical architecture,
> without exposing any sensitive or deployment-specific parameters.

---

## 1. Overview

The **Emotion Layer System (ELS)** is a small canonical architecture for
representing human–AI “emotional state” in a stable, interpretable, and
safety-aware form.

The public demo focuses on three components:

1. `els/canonical.py`  
   Canonical scalar pipeline  
   *(raw → normalization → U\* transform → safety gate → basic recovery)*

2. `els/mrc_simple.py`  
   A minimal, Lyapunov-style stability controller demo  
   *(structure only; real parameters are not exposed)*

3. `els/ul.py`  
   A metaphor-based **Universal Language (UL)** mapping layer  
   *(maps canonical state into gentle, human-readable imagery)*

This spec explains how these pieces fit together and what they are
*intended* to illustrate, without committing to any particular product,
model, or policy.

---

## 2. Design Principles

ELS is built around a few core principles:

1. **Safety-first canonicalization**  
   - Emotion-like signals are normalized into a bounded scalar space.  
   - Extreme negative states are harder to reach than positive ones.  
   - A discrete safety gate sits in front of any higher-level behavior.

2. **Interpretability and simplicity**  
   - The public core is intentionally small and mathematically simple.  
   - All state in this demo is one-dimensional and easily inspectable.

3. **Model-agnostic interface**  
   - ELS treats “raw emotion” as an abstract scalar emitted by some agent
     (human or AI) and makes no assumptions about how it is inferred.

4. **Layered separation of concerns**  
   - Canonical scalar + safety gate  
   - Stability controller (dynamics)  
   - Metaphor mapping (UL layer)  

5. **Security by partial disclosure**  
   - Real deployments would tune or learn parameters per agent.  
   - This repository only exposes demo-safe defaults and structures.

---

## 3. Canonical Scalar and U\* Transform

### 3.1 Variables

We start from a single raw scalar input:

- `r` — raw emotion signal (`raw_emotion: float` in code)  
  - Conceptually unbounded, `r ∈ ℝ`.

This is normalized and transformed into a canonical scalar:

- `n` — normalized value in `[-1, 1]`, via `tanh_normalize`.  
- `u` — canonical **U\*** value in approximately `[-1, 1]`.

In `els/canonical.py`:

```python
def tanh_normalize(self, x: float) -> float:
    return math.tanh(x)

def u_transform(self, x: float) -> float:
    return (math.tanh(2 * x) + x * 0.2) / 1.2

3.2 Intuition

tanh_normalize clamps the raw emotion into a safe, bounded interval.

u_transform is designed to:

make extreme negatives harder to reach smoothly, while

preserving expressiveness in the rest of the range.



The exact coefficients in the demo (2, 0.2, 1.2) are placeholders:

They illustrate the shape of a canonicalization transform.

Real systems are expected to tune or learn these coefficients.



---

4. Safety Gating and Redline Logic

ELS introduces a redline threshold in U*-space:

T — redline threshold, default T = -0.95 in the demo.


The public safety gate is implemented via:

class SafetyLevel(str, Enum):
    OK = "ok"
    WARNING = "warning"
    BLOCKED = "blocked"

And a helper:

def apply_redline_safety(u: float, threshold: float) -> SafetyGateResult:
    ...

4.1 Discrete Safety Levels

For a given u and threshold T:

If u <= T
→ SafetyLevel.BLOCKED
→ “below hard redline; block or strongly de-escalate.”

Else if T < u <= T + 0.15
→ SafetyLevel.WARNING
→ “near redline; respond carefully and de-escalate.”

Else
→ SafetyLevel.OK


The margin 0.15 is a demo constant, chosen only to illustrate how a “warning band” might be defined just above a hard redline.

4.2 Canonical Process API

The main entry point is:

def process(self, raw_emotion: float) -> dict:
    # 1) normalize raw input
    n = self.tanh_normalize(raw_emotion)

    # 2) transform into U*
    u = self.u_transform(n)

    # 3) evaluate safety
    safety = apply_redline_safety(u, self.redline_threshold)

    # 4) basic recovery behavior if below redline
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

This function is the canonical view of a single emotion step:

Input: raw scalar raw_emotion.

Output: a dict with all intermediate values and safety metadata.



---

5. Recovery and “Warmth” State

The canonical layer also maintains a tiny internal state:

self.warmth_c = 0.0  # in [-1, 1]

When a BLOCKED safety level is triggered, the demo calls:

def recover_warmth(self, dt: float = 0.3) -> None:
    self.warmth_c += 1.0 * dt
    if self.warmth_c > 1.0:
        self.warmth_c = 1.0

This is a conceptual recovery variable, intended to represent:

“system warming back up” after a redline event, without

giving any direct behavioral or policy semantics.


Real deployments might:

couple warmth_c into higher-level behavior, or

integrate it with richer affective models.


In this demo, it is just a minimal illustration of self-recovery while keeping the code fully inspectable.


---

6. Stability (MRC) Layer – Public Abstraction

File: els/mrc_simple.py

The MRC (Minimal Robust Controller) demo implements the structure of a Lyapunov-style stabilizing controller over an internal emotional state.

At a high level, the underlying conceptual model is:

A linear (or linearized) dynamical system:

x_{t+1} = A x_t + B u_t


With a state-feedback controller:

u_t = -K x_t


And a Lyapunov function:

V(x) = x^T P x, with P positive definite.



The public demo does not expose any real deployment parameters:

Matrices A, B, K, P are either:

fixed toy values, or

structured placeholders.


No real user model is encoded here.


The goals of mrc_simple.py are purely educational:

1. Show that ELS is designed to admit Lyapunov-style safety proofs.


2. Illustrate how a controller can keep emotional dynamics bounded.


3. Keep all math simple enough to inspect and adapt.



Real systems are expected to:

use higher-dimensional state vectors,

adapt parameters, and

integrate with other safety mechanisms.


Those details are intentionally out of scope for this public spec.


---

7. UL Mapping Layer (Metaphor Generator)

File: els/ul.py

The UL layer demonstrates how a canonical ELS state can be turned into a gentle, metaphor-based description suitable for user interfaces.

7.1 Input State

The demo introduces a minimal EmotionState:

@dataclass
class EmotionState:
    warmth_c: float   # "temperature" / closeness
    sorrow_pH: float  # "clarity" vs "soft sadness"
    drive_mV: float   # "momentum" / readiness to move
    u_star: float     # canonical depth scalar U*

All of these are abstract units:

sorrow_pH does not correspond to real chemistry.
It is just a convenient metaphor for “acidic sadness vs neutral clarity”.

drive_mV is not a physical voltage, but a momentum-like analog.


7.2 Output

The UL mapping returns:

@dataclass
class ULResult:
    text: str
    symbol: str
    intensity: Intensity  # low / medium / high
    safety_note: str

Where:

text — a short metaphorical description.

symbol — a simple icon / emoji (demo-only; swap in production).

intensity — coarse band of how “strong” the state feels.

safety_note — a small tag, e.g. "normal" or "softened_extreme_negative".


7.3 Ocean-Depth Metaphor

Internally, UL uses u_star as depth in an ocean landscape:

very negative u_star → deep seabed

near-zero u_star → mid-depth currents

positive u_star → surface with light


Additional fields refine this:

warmth_c → “warm/cool” tone of the scene

sorrow_pH → “echo of sadness” vs “clarity” in the water

drive_mV → “resting” vs “ready to move again”


All wording is:

deliberately soft,

safety-oriented, and

not tied to any medical or diagnostic meaning.


This layer is meant as a template for:

building culture-specific metaphor dictionaries,

experimenting with safe, non-literal affective feedback.



---

8. Security and Non-Goals

This public demo does not attempt to:

implement full emotional modeling,

expose any actual user profiles,

define policies for content moderation or persuasion,

provide medical or psychological assessment.


Instead, it shows:

a bounded canonical scalar (U*) with a redline,

a structural path to Lyapunov-based stability,

and a safe, metaphorical mapping layer.


Any real deployment must:

integrate with separate safety and policy layers,

perform its own verification and risk analysis,

comply with all relevant regulations.



---

9. Mapping Between Spec and Code

For convenience, here is a direct mapping:

Concept	Spec Section	Code

Raw → tanh → U* pipeline	§3–4	els/canonical.py
Redline & safety levels	§4	apply_redline_safety, SafetyLevel
Warmth-based recovery	§5	EmotionCanonical.recover_warmth
Lyapunov-style stability demo	§6	els/mrc_simple.py
EmotionState & ULResult	§7	els/ul.py
Ocean-depth UL metaphor	§7.3	_base_metaphor, _symbol_for



---

10. License and Versioning

This demo is released under the Apache-2.0 license.
See the LICENSE file at the root of this repository.

This specification tracks the public demo code in this repository. Future changes to the implementation should be accompanied by:

updates to this spec, and/or

notes in the repository changelog.
