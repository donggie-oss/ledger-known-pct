import io
import pandas as pd
import streamlit as st

# -------------------------------------------------
# PAGE SETUP (VIEWER ONLY)
# -------------------------------------------------

st.title("Module One v2 — Execution Viewer")
st.caption("Viewer-only. No execution. No adjudication. Canon-bound output display.")

# -------------------------------------------------
# EXPECTED SCHEMA (MODULE ONE v2 OUTPUT)
# -------------------------------------------------

REQUIRED_COLS = {
    "entity_id",
    "STRUCTURAL_CORE_fact_count",
    "STRAIN_FACTORS_fact_count",
    "GOVERNANCE_SIGNAL_fact_count",
}

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------

uploaded = st.file_uploader(
    "Upload module_one_v2_output.csv",
    type=["csv"],
)

if uploaded is None:
    st.info("Upload a Module One v2 output CSV to view results.")
    st.stop()

# -------------------------------------------------
# LOAD + VALIDATE
# -------------------------------------------------

try:
    df = pd.read_csv(io.BytesIO(uploaded.getvalue()))
except Exception as e:
    st.error("Failed to read CSV.")
    st.code(str(e))
    st.stop()

missing = REQUIRED_COLS - set(df.columns)
if missing:
    st.error("Viewer failed.")
    st.code(f"Missing required columns: {sorted(list(missing))}")
    st.stop()

# -------------------------------------------------
# DISPLAY
# -------------------------------------------------

st.success(f"Loaded {len(df):,} entities")

st.subheader("Module One v2 Output (Raw)")
st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# OPTIONAL SUMMARY (NON-DETERMINISTIC, DISPLAY ONLY)
# -------------------------------------------------

st.subheader("Dataset Coverage Summary")

summary = pd.DataFrame({
    "Dataset": [
        "STRUCTURAL_CORE",
        "STRAIN_FACTORS",
        "GOVERNANCE_SIGNAL",
    ],
    "Entities with ≥1 fact": [
        (df["STRUCTURAL_CORE_fact_count"] > 0).sum(),
        (df["STRAIN_FACTORS_fact_count"] > 0).sum(),
        (df["GOVERNANCE_SIGNAL_fact_count"] > 0).sum(),
    ],
})

st.dataframe(summary, use_container_width=True)
