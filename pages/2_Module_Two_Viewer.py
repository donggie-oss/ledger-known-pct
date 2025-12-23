import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Module Two Viewer", layout="wide")

st.title("Module Two — Decision Viewer")
st.caption("Canon-bound. Read-only. No execution.")

REQUIRED_COLS = {
    "entity_id",
    "module_two_outcome",
    "module_two_reason"
}

uploaded = st.file_uploader(
    "Upload module_two_output.csv",
    type=["csv"]
)

if uploaded is None:
    st.info("Upload a Module Two output CSV to view results.")
    st.stop()

try:
    df = pd.read_csv(io.BytesIO(uploaded.getvalue()))

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    st.success(f"Loaded {len(df):,} entities")

    st.subheader("Outcome Summary")
    summary = (
        df.groupby("module_two_outcome")
        .size()
        .reset_index(name="count")
    )
    st.dataframe(summary, use_container_width=True)

    st.subheader("Decision Detail")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Viewer failed.")
    st.code(str(e))
