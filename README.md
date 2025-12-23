# ledger-known-pct

## Status
**ACTIVE · CANON-BOUND · EXECUTION ONLY**

This repository implements **Forge GTM Module One execution** and its supporting UI.
It is **not** a place for theory, experimentation, or ad‑hoc logic.

If it is not defined in **canon**, it does not belong here.

---

## What This Repo Is
- An **execution surface** for Module One
- A **viewer UI** for adjudication outputs
- A **runner** that consumes canon and produces artifacts

## What This Repo Is NOT
- Not a design document
- Not a playground
- Not a place to redefine rules
- Not a sales tool

---

## Canonical Source of Truth

All logic is defined externally in **canon**.

```
/canon
  /module-one-v2
    execution.md
    execution.json
  /module-two
    logic.md
    logic.json
```

Rules:
- Python **must consume canon**
- Python **must not embed thresholds**
- UI **must not adjudicate**

Any deviation is a canon violation.

---

## Repository Structure (Enforced)

```
/canon          # Read-only doctrine (JSON + MD)
/engine         # Pure executors (no logic definition)
/ui             # Streamlit viewer only
/examples       # Sample inputs only
/artifacts      # Generated outputs only
```

---

## Execution Flow

1. **Canon is authored or updated** (outside this repo)
2. Canon JSON is placed under `/canon`
3. Engine scripts:
   - Read canon
   - Execute adjudication
   - Emit artifacts
4. Streamlit UI:
   - Renders artifacts
   - Never decides outcomes

---

## Guardrails

- No GREEN/YELLOW/RED logic unless defined in canon
- No `known_pct` thresholds unless defined in canon
- No UI-side branching
- No silent logic changes

If you need to change behavior:
1. Update canon
2. Version canon
3. Re-run engine

---

## Contribution Rules

- All PRs are reviewed for **canon compliance**
- Logic embedded in Python = automatic rejection
- UI changes must not affect execution

---

## Operating Principle

> **Execution before explanation.  
> Measurement before decision.  
> Canon before code.**

Forge GTM standard.
