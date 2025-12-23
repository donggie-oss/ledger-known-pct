import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Module One v2 Viewer", layout="wide")

st.title("Module One v2 — Execution Viewer")
st.caption("Canon-bound. Read-only. No adjudication.")

REQUIRED_COLS = {
    "entity_id",
    "STRUCTURAL_CORE_measured",
    "STRUCTURAL_CORE_fact_count",
    "EXCEPTION_SURFACE_fact_count",
    "STRAIN_FACTORS_measured",
    "GOVERNANCE_SIGNAL_measured"
}

st.subheader("Upload Module One v2 Output")

uploaded = st.file_uploader(
    "Upload module_one_v2_output.csv",
    type=["csv"]
)

if uploaded is None:
    st.info("Upload a Module One v2 output CSV to view results.")
    st.stop()

try:
    raw = uploaded.getvalue()
    df = pd.read_csv(io.BytesIO(raw))

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    st.success(f"Loaded {len(df):,} entities")

    st.subheader("Preview")
    st.dataframe(df.head(50), use_container_width=True)

    st.subheader("Measurement Coverage Summary")

    summary = pd.DataFrame({
        "STRUCTURAL_CORE_measured": df["STRUCTURAL_CORE_measured"].mean(),
        "STRAIN_FACTORS_measured": df["STRAIN_FACTORS_measured"].mean(),
        "GOVERNANCE_SIGNAL_measured": df["GOVERNANCE_SIGNAL_measured"].mean(),
    }, index=["coverage"]).T

    st.dataframe(summary, use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name="module_one_v2_output.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error("Viewer failed.")
    st.code(str(e))
