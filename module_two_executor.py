import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# -------------------------------------------------------------------
# CONFIG (NO LOGIC HERE)
# -------------------------------------------------------------------

CANON_PATH = Path("canon/module-two/logic.json")

REQUIRED_INPUT_COLUMNS = {
    "entity_id",
    "STRUCTURAL_CORE_measured",
    "STRUCTURAL_CORE_fact_count",
    "EXCEPTION_SURFACE_fact_count",
    "STRAIN_FACTORS_measured",
    "GOVERNANCE_SIGNAL_measured"
}

# -------------------------------------------------------------------
# CANON LOADER
# -------------------------------------------------------------------

def load_canon() -> Dict[str, Any]:
    if not CANON_PATH.exists():
        raise FileNotFoundError(f"Canon not found at {CANON_PATH}")

    with open(CANON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------------------------------
# MODULE TWO EXECUTOR (POLICY, NOT FACTS)
# -------------------------------------------------------------------

def execute_module_two(df: pd.DataFrame) -> pd.DataFrame:
    canon = load_canon()
    rules = canon["rules"]

    output = df.copy()

    def decide(row):
        # BLOCK — exception surface too large
        if row["EXCEPTION_SURFACE_fact_count"] > rules["max_exception_surface"]:
            return "BLOCK", "EXCEPTION_SURFACE_EXCEEDED"

        # HOLD — missing required measurements
        for field in rules["required_measurements"]:
            if not row[field]:
                return "HOLD", f"{field}_UNMEASURED"

        # AUTH — all requirements satisfied
        return "AUTH", "MEASUREMENTS_SUFFICIENT"

    decisions = output.apply(
        lambda r: decide(r),
        axis=1,
        result_type="expand"
    )

    output["module_two_outcome"] = decisions[0]
    output["module_two_reason"] = decisions[1]

    return output

# -------------------------------------------------------------------
# CLI ENTRYPOINT
# -------------------------------------------------------------------

def main():
    input_path = Path("module_one_v2_output.csv")
    output_path = Path("module_two_output.csv")

    if not input_path.exists():
        raise FileNotFoundError("Expected module_one_v2_output.csv in repo root")

    df = pd.read_csv(input_path)

    missing = REQUIRED_INPUT_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    result = execute_module_two(df)
    result.to_csv(output_path, index=False)

    print(f"[OK] Module Two output written to {output_path}")

if __name__ == "__main__":
    main()
