import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Module One Adjudication", layout="wide")

st.title("Module One Adjudication (Canon-safe)")
st.caption("Upload Known% results → adjudicate → download module_one_states.csv")

# ---- Canon thresholds (deterministic; no inference) ----
RULES = {
    "STRUCTURAL": {"GREEN": 0.70, "YELLOW": 0.40},
    "COMPLEXITY": {"GREEN": 0.60, "YELLOW": 0.30},
    "STRAIN": {"GREEN": 0.65, "YELLOW": 0.35},
}

REQUIRED_COLS = {"entity_id", "dataset", "known_pct"}

def adjudicate_row(dataset: str, known_pct: float) -> str:
    ds = str(dataset).strip().upper()
    if ds not in RULES:
        return "ERROR_UNKNOWN_DATASET"

    try:
        known = float(known_pct)
    except Exception:
        return "ERROR_BAD_KNOWN_PCT"

    t = RULES[ds]
    if known >= t["GREEN"]:
        return "GREEN"
    elif known >= t["YELLOW"]:
        return "YELLOW"
    else:
        return "RED"

def run_module_one(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names (common CSV issues)
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    # Normalize dataset values
    df["dataset"] = df["dataset"].astype(str).str.strip().str.upper()

    # Adjudicate
    df["module_one_state"] = df.apply(
        lambda r: adjudicate_row(r["dataset"], r["known_pct"]),
        axis=1
    )

    # Canon output shape (keep it tight + deterministic)
    out = df[["entity_id", "dataset", "known_pct", "module_one_state"]].copy()
    return out

# ---- UI ----
left, right = st.columns([1, 1])

with left:
    st.subheader("1) Upload Known% Results CSV")
    uploaded = st.file_uploader(
        "Upload your Known% results CSV (must include: entity_id, dataset, known_pct)",
        type=["csv"]
    )

    st.markdown("**Datasets supported (canonical):** STRUCTURAL, COMPLEXITY, STRAIN")
    st.markdown("**Output:** module_one_states.csv")

with right:
    st.subheader("2) Run + Download")
    if uploaded is None:
        st.info("Upload a CSV to enable adjudication.")
    else:
        try:
            raw = uploaded.getvalue()
            df_in = pd.read_csv(io.BytesIO(raw))

            st.success(f"Loaded: {len(df_in):,} rows")
            st.caption("Preview (first 50 rows):")
            st.dataframe(df_in.head(50), use_container_width=True)

            if st.button("Run Module One Adjudication", type="primary"):
                out = run_module_one(df_in)

                # Show summary counts
                st.subheader("Result Summary")
                summary = (
                    out.groupby(["dataset", "module_one_state"])
                    .size()
                    .reset_index(name="rows")
                    .sort_values(["dataset", "module_one_state"])
                )
                st.dataframe(summary, use_container_width=True)

                # Prepare CSV download
                csv_bytes = out.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download module_one_states.csv",
                    data=csv_bytes,
                    file_name="module_one_states.csv",
                    mime="text/csv"
                )

                st.caption("Preview output (first 50 rows):")
                st.dataframe(out.head(50), use_container_width=True)

        except Exception as e:
            st.error("Adjudication failed.")
            st.code(str(e))
            st.stop()
