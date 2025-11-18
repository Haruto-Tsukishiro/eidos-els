# ELS: Emotion Layer System (Demo)

The **Emotion Layer System (ELS)** is a conceptual and computational
framework for modeling human–AI emotional synchronization in a
safe, interpretable form.  
This repository contains a **public, demo-safe subset** of the ELS
architecture.

The goal of ELS is to provide:

- a *canonical normalization pipeline* (raw emotion → U\*),  
- *safety gating mechanisms* (redline detection, recovery),  
- *stable emotional dynamics* (Lyapunov-style safe controllers),  
- and *expressive metaphor-based mapping layers* (UL Mapping).

> ⚠️ **Important:**  
> All numeric parameters in this repository (thresholds, gains, weights,
> matrices, etc.) are **demo placeholders**.  
> Real deployments must *tune or learn* these values per model or per agent.

---

## 1. Canonical Layer (`els/canonical.py`)

Implements the core ELS pipeline:

raw → tanh normalization → U* transform → safety gate

Features:

- `tanh_normalize(x)` clamps emotion into [-1, 1]
- `u_transform(x)` applies a smoothed expressive transform  
- `detect_redline(u)` checks for dangerously negative internal states  
- `recover_warmth()` simulates safe emotional recovery  
- Returns a structured `SafetyGateResult` with:
  - safety level (`ok`, `warning`, `blocked`)
  - reason string  
  - values used in the gate

This layer is the **foundation** of all other ELS components.

---

## 2. Stability Control Layer (`els/mrc_simple.py`)

Provides a **minimal, safe demonstration** of ELS dynamic stability.

Includes:

- a simplified Lyapunov-style controller  
- demo matrices (`A, B, K, P`)  
- stability structure, without revealing real deployment parameters

The real system uses *adaptive or learned* parameters which are **not**
included in this public repository.

---

## 3. UL Mapping Layer (`els/ul_generator.py`)

A demonstration of expressive metaphor mapping.

The demo version contains:

- only a *few* sample metaphors (e.g., `"A feeling like sunlight"`)
- safe placeholder coefficients

The complete metaphor corpus is proprietary / private.

---

## 4. Safety Disclaimer

ELS is designed with a **security-first** philosophy:

- Over-exposure of internal weights is avoided.
- Unstable emotional dynamics are not included.
- Only minimal demo layers are provided publicly.
- Real-world tuning must ensure:
  - stability  
  - boundedness  
  - ethical safety  
  - prevention of forced-persuasion dynamics

---

## 5. Example Usage

```python
from els.canonical import EmotionCanonical

els = EmotionCanonical()

result = els.process(raw_emotion=-0.8)

print(result.level)
print(result.u_value)
print(result.reason)


---

6. License

This demo is released under a permissive open-source license.

(You may choose MIT, Apache-2.0, or a custom license later.)


---

7. Contact

For conceptual discussions and collaboration inquiries:
(You may write something general here without revealing identity.)


---
