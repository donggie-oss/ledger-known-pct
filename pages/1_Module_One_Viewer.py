import io
import pandas as pd
import streamlit as st


st.title("Module One v2 — Execution Viewer")
st.caption("Viewer-only. No execution. No adjudication. Canon-bound output display.")
st.caption("Canon-bound. Read-only. No adjudication.")

REQUIRED_COLS = {
    "entity_id",
    "dataset",
    "fact_count"
}

uploaded = st.file_uploader(
    "Upload module_one_v2_output.csv",
    type=["csv"]
)

if uploaded is None:
    st.info("Upload a Module One v2 output CSV to view results.")
    st.stop()

try:
    df = pd.read_csv(io.BytesIO(uploaded.getvalue()))

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    st.success(f"Loaded {len(df):,} entities")

    st.subheader("Dataset Coverage Summary")
    summary = df.describe(include="all")
    st.dataframe(summary, use_container_width=True)

    st.subheader("Detail View")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Viewer failed.")
    st.code(str(e))
