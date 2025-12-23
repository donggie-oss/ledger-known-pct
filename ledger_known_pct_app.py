# ledger_known_pct_app.py
# Standalone Streamlit app: Ledger → Known% Calculator
#
# Run with:
#   streamlit run ledger_known_pct_app.py
#
# Dependencies (auto-handled by Streamlit Cloud or local install):
#   streamlit, pandas

import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIG (EXPLICIT RULES)
# =========================

SOURCE_TIER_WEIGHT = {
    1: 1.00,
    2: 0.75,
    3: 0.50,
    4: 0.25
}

SIGNAL_STRENGTH_MULT = {
    "STRONG": 1.00,
    "WEAK": 0.60
}

def freshness_multiplier(months_old: int) -> float:
    if months_old < 12:
        return 1.00
    if months_old < 24:
        return 0.70
    if months_old < 36:
        return 0.40
    return 0.00

DATASET_REQUIREMENTS = {
    "STRUCTURAL": 2.50,
    "COMPLEXITY": 2.00,
    "STRAIN": 1.75
}

REQUIRED_COLUMNS = [
    "entity_id",
    "dataset",
    "source_tier",
    "signal_strength",
    "date_observed",
    "valid"
]

# =========================
# CORE CALCULATION
# =========================

def compute_known_pct(df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    results = []

    for entity_id in df["entity_id"].unique():
        entity_rows = df[df["entity_id"] == entity_id]

        for dataset, required_weight in DATASET_REQUIREMENTS.items():
            total_weight = 0.0

            subset = entity_rows[
                (entity_rows["dataset"] == dataset) &
                (entity_rows["valid"] == True)
            ]

            for _, row in subset.iterrows():
                months_old = (as_of - row["date_observed"]).days // 30
                freshness = freshness_multiplier(months_old)
                if freshness == 0.0:
                    continue

                weight = (
                    SOURCE_TIER_WEIGHT[row["source_tier"]] *
                    SIGNAL_STRENGTH_MULT[row["signal_strength"]] *
                    freshness
                )

                total_weight += weight

            known_pct = min(1.0, total_weight / required_weight)
            unknown_pct = 1.0 - known_pct

            results.append({
                "entity_id": entity_id,
                "dataset": dataset,
                "known_pct": round(known_pct, 3),
                "unknown_pct": round(unknown_pct, 3),
                "raw_weight": round(total_weight, 3),
                "required_weight": required_weight
            })

    return pd.DataFrame(results)

# =========================
# STREAMLIT UI
# =========================

st.set_page_config(page_title="Ledger → Known% Calculator", layout="wide")
st.title("Ledger → Known% Calculator (Canon-Safe)")
st.caption("No interpretation. No inference. Pure evidence coverage math.")

uploaded = st.file_uploader(
    "Upload evidence_ledger.csv",
    type=["csv"]
)

if not uploaded:
    st.info("Upload a CSV using the required ledger schema.")
    st.stop()

df = pd.read_csv(uploaded)

# Validate schema
missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

# Normalize & coerce
df["dataset"] = df["dataset"].str.upper()
df["signal_strength"] = df["signal_strength"].str.upper()
df["valid"] = df["valid"].astype(bool)
df["date_observed"] = pd.to_datetime(df["date_observed"], errors="coerce")

invalid_rows = df[
    ~df["dataset"].isin(DATASET_REQUIREMENTS.keys()) |
    ~df["signal_strength"].isin(SIGNAL_STRENGTH_MULT.keys()) |
    ~df["source_tier"].isin(SOURCE_TIER_WEIGHT.keys()) |
    df["date_observed"].isna()
]

if not invalid_rows.empty:
    st.warning("Some rows are invalid and will be ignored.")
    st.dataframe(invalid_rows)

as_of = st.date_input("As-of date for freshness calculation", value=datetime.utcnow().date())

if st.button("Run Known% Calculation"):
    results = compute_known_pct(df, datetime.combine(as_of, datetime.min.time()))

    st.subheader("Results")
    st.dataframe(results, use_container_width=True)

    csv = results.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Known% Results CSV",
        csv,
        "known_pct_results.csv",
        "text/csv"
    )

st.divider()
st.caption("Deterministic • Auditable • Ironclad-safe")
