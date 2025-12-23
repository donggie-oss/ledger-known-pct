import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# -------------------------------------------------------------------
# CONFIG (NO LOGIC HERE)
# -------------------------------------------------------------------

CANON_PATH = Path("canon/module-one-v2/execution.json")

REQUIRED_INPUT_COLUMNS = [
    "entity_id",
    "dataset"
]

# -------------------------------------------------------------------
# CANON LOADER
# -------------------------------------------------------------------

def load_canon() -> Dict[str, Any]:
    if not CANON_PATH.exists():
        raise FileNotFoundError(f"Canon not found at {CANON_PATH}")

    with open(CANON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------------------------------
# MODULE ONE EXECUTOR (NO DECISIONS)
# -------------------------------------------------------------------

def execute_module_one(input_df: pd.DataFrame) -> pd.DataFrame:
    canon = load_canon()
    datasets = canon.get("datasets", {})

    output_rows = []

    for entity_id, group in input_df.groupby("entity_id"):
        row = {"entity_id": entity_id}

        for dataset_name, rules in datasets.items():
            dataset_rows = group[group["dataset"] == dataset_name]

            fact_count = len(dataset_rows)
            min_facts = rules.get("min_facts_to_measure", 1)

            row[f"{dataset_name}_measured"] = fact_count >= min_facts
            row[f"{dataset_name}_fact_count"] = fact_count

        output_rows.append(row)

    return pd.DataFrame(output_rows)

# -------------------------------------------------------------------
# CLI ENTRYPOINT
# -------------------------------------------------------------------

def main():
    input_path = Path("input.csv")
    output_path = Path("module_one_v2_output.csv")

    if not input_path.exists():
        raise FileNotFoundError("Expected input.csv in repo root")

    df = pd.read_csv(input_path)

    missing_cols = set(REQUIRED_INPUT_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    result = execute_module_one(df)
    result.to_csv(output_path, index=False)

    print(f"[OK] Module One v2 output written to {output_path}")

if __name__ == "__main__":
    main()

