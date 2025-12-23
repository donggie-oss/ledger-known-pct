import pandas as pd

INPUT_FILE = "known_pct_results.csv"
OUTPUT_FILE = "module_one_states.csv"

# Canon thresholds — deterministic, no inference
RULES = {
    "STRUCTURAL": {
        "GREEN": 0.70,
        "YELLOW": 0.40
    },
    "COMPLEXITY": {
        "GREEN": 0.60,
        "YELLOW": 0.30
    },
    "STRAIN": {
        "GREEN": 0.65,
        "YELLOW": 0.35
    }
}

def adjudicate(row):
    dataset = row["dataset"]
    known = row["known_pct"]

    thresholds = RULES[dataset]

    if known >= thresholds["GREEN"]:
        return "GREEN"
    elif known >= thresholds["YELLOW"]:
        return "YELLOW"
    else:
        return "RED"

def main():
    df = pd.read_csv(INPUT_FILE)

    required_cols = {"entity_id", "dataset", "known_pct"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Known% CSV missing required columns")

    df["module_one_state"] = df.apply(adjudicate, axis=1)

    df_out = df[["entity_id", "dataset", "known_pct", "module_one_state"]]
    df_out.to_csv(OUTPUT_FILE, index=False)

    print(f"Module One adjudication complete: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
