import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Module Two Viewer", layout="wide")

st.title("Module Two — Decision Viewer")
st.caption("Canon-bound. Read-only. No execution, no adjudication.")

REQUIRED_COLS = {
    "entity_id",
    "module_two_outcome",
    "module_two_reason"
}

st.subheader("Upload Module Two Output")

uploaded = st.file_uploader(
    "Upload module_two_output.csv",
    type=["csv"]
)

if uploaded is None:
    st.info("Upload a Module Two output CSV to view results.")
    st.stop()

try:
    raw = uploaded.getvalue()
    df = pd.read_csv(io.BytesIO(raw))

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    st.success(f"Loaded {len(df):,} entities")

    # ------------------------------
    # SUMMARY
    # ------------------------------
    st.subheader("Outcome Summary")

    summary = (
        df.groupby("module_two_outcome")
        .size()
        .reset_index(name="count")
        .sort_values("module_two_outcome")
    )

    st.dataframe(summary, use_container_width=True)

    # ------------------------------
    # DETAIL VIEW
    # ------------------------------
    st.subheader("Decision Detail")
    st.dataframe(df, use_container_width=True)

    # ------------------------------
    # DOWNLOAD
    # ------------------------------
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download module_two_output.csv",
        data=csv_bytes,
        file_name="module_two_output.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error("Viewer failed.")
    st.code(str(e))
