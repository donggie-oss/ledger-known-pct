# Ledger → Known% Calculator

## What this is
This repository contains a standalone Streamlit application that converts an explicit evidence ledger into deterministic Known% / Unknown% outputs for the following datasets:

- STRUCTURAL  
- COMPLEXITY  
- STRAIN  

The tool is designed to safely feed Module One adjudication without contaminating it with interpretation, inference, or heuristics.

---

## What this tool does
- Reads an evidence ledger from CSV
- Applies fixed, transparent weighting rules
- Computes Known% as evidence coverage, not confidence
- Outputs auditable results per entity and dataset
- Exports results as CSV for downstream use

Everything is deterministic.  
If you run the same ledger twice, you get the same answer.

---

## What this tool explicitly does NOT do
This tool does not:
- Interpret language
- Parse free text
- Guess intent
- Infer meaning
- Perform NLP
- Assign confidence heuristically
- Make PURSUE / PARK / DISCARD decisions

If you are looking for “smart scoring” or “AI insights,” this is the wrong tool.

---

## Why this exists
Module One adjudication must never:
- read raw text
- invent evidence
- silently smooth gaps
- confuse uncertainty with confidence

This calculator creates a hard mechanical boundary between:
- human judgment (upstream research)
- and automated decision grammar (Module One)

Known% answers only one question:
How much do we explicitly know, based on declared evidence?

---

## Evidence Ledger Schema (Required)

The input CSV must contain the following columns exactly:

| Column | Description | Allowed Values |
|------|------------|----------------|
| entity_id | Stable account identifier | string |
| dataset | Evidence category | STRUCTURAL, COMPLEXITY, STRAIN |
| source_tier | Source credibility tier | 1, 2, 3, 4 |
| signal_strength | Strength of signal | STRONG, WEAK |
| date_observed | Observation date | YYYY-MM-DD |
| valid | Explicit validity flag | true, false |

Invalid or malformed rows are ignored, not corrected.

---

## Deterministic Rules (Summary)

### Source tier weights
- Tier 1 → 1.00  
- Tier 2 → 0.75  
- Tier 3 → 0.50  
- Tier 4 → 0.25  

### Signal strength multipliers
- STRONG → 1.00  
- WEAK → 0.60  

### Freshness multipliers
- < 12 months → 1.00  
- 12–24 months → 0.70  
- 24–36 months → 0.40  
- > 36 months → excluded  

### Required coverage (per dataset)
- STRUCTURAL → 2.50  
- COMPLEXITY → 2.00  
- STRAIN → 1.75  

Known% = min(1.0, total_weight / required_weight)

---

## Running the app (recommended)
This app is intended to be run on Streamlit Community Cloud.

1. Deploy this repository via Streamlit Cloud
2. Open the app in your browser
3. Upload your evidence ledger CSV
4. Select the “as-of” date
5. Click Run Known% Calculation
6. Download the results CSV

No local Python installation is required.

---

## Output
The app outputs one row per:
- entity
- dataset

With the following fields:
- known_pct
- unknown_pct
- raw_weight
- required_weight

These outputs are designed to be consumed directly by Module One adjudication.

---

## Design philosophy
This tool is intentionally:
- strict
- boring
- unforgiving

Those are features, not limitations.

---

## License / usage
Internal operational tool.  
Use only with explicit evidence ledgers and trained operators.
