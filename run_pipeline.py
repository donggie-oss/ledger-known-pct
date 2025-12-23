import subprocess
import sys
from pathlib import Path

# -------------------------------------------------
# PIPELINE CONFIG (NO LOGIC)
# -------------------------------------------------

INPUT_FILE = Path("input.csv")

MODULE_ONE_SCRIPT = Path("module_one_assigner.py")
MODULE_ONE_OUTPUT = Path("module_one_v2_output.csv")

MODULE_TWO_SCRIPT = Path("module_two_executor.py")
MODULE_TWO_OUTPUT = Path("module_two_output.csv")


# -------------------------------------------------
# UTIL
# -------------------------------------------------

def run_step(name: str, command: list[str]):
    print(f"\n▶ Running {name}")
    print("  ", " ".join(command))

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\n✖ {name} failed")
        sys.exit(result.returncode)

    print(f"✔ {name} completed")


def assert_file_exists(path: Path, label: str):
    if not path.exists():
        print(f"\n✖ Expected {label} not found: {path}")
        sys.exit(1)


# -------------------------------------------------
# PIPELINE
# -------------------------------------------------

def main():
    print("\n=== GigaSphere Execution Pipeline ===")

    # --- Preflight ---
    assert_file_exists(INPUT_FILE, "input CSV")
    assert_file_exists(MODULE_ONE_SCRIPT, "Module One executor")
    assert_file_exists(MODULE_TWO_SCRIPT, "Module Two executor")

    # --- Module One ---
    run_step(
        "Module One",
        [
            sys.executable,
            str(MODULE_ONE_SCRIPT),
        ],
    )

    assert_file_exists(MODULE_ONE_OUTPUT, "Module One output")

    # --- Module Two ---
    run_step(
        "Module Two",
        [
            sys.executable,
            str(MODULE_TWO_SCRIPT),
        ],
    )

    assert_file_exists(MODULE_TWO_OUTPUT, "Module Two output")

    print("\n=== PIPELINE COMPLETE ===")
    print(f"✔ {MODULE_ONE_OUTPUT}")
    print(f"✔ {MODULE_TWO_OUTPUT}")


if __name__ == "__main__":
    main()
