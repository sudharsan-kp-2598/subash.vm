import subprocess
import time
from pathlib import Path
from statistics import mean

# =========================
# CONFIGURATION
# =========================

SOURCE_DIR = Path(
    "/home/subash-nts0300/Typing-Analysis/cpython-src/Python-3.10.19/Lib"
)

RUNS = 3
TIMEOUT_SECONDS = 60 * 60  # 1 hour safety timeout

TYPE_CHECKERS = {
    "pyright": ["pyright"],
    "mypy": ["mypy", "--ignore-missing-imports"],
    "pytype": ["pytype"],
    "pyre": ["pyre", "check"],
    "pyanalyze": ["pyanalyze"],
}

# =========================
# BENCHMARK LOGIC
# =========================

def run_checker(name: str, cmd: list[str]) -> list[float]:
    times: list[float] = []

    for i in range(RUNS):
        start = time.perf_counter()

        try:
            result = subprocess.run(
                cmd + [str(SOURCE_DIR)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=TIMEOUT_SECONDS,
                check=False,  # IMPORTANT: do NOT raise on non-zero exit
            )

            elapsed = time.perf_counter() - start
            times.append(elapsed)

            # For type checkers:
            # non-zero exit code usually just means "type errors found"
            status = "COMPLETED"

        except subprocess.TimeoutExpired:
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            status = "TIMEOUT"

        except Exception as exc:
            # Real unexpected failure (crash, OS error, etc.)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            status = f"CRASH ({exc.__class__.__name__})"

        print(f"{name:<10} | run {i+1}: {elapsed:8.3f}s | status: {status}")

    return times


def main() -> None:
    print("\n=== TYPE CHECKER SPEED BENCHMARK ===\n")

    results: dict[str, list[float]] = {}

    for name, cmd in TYPE_CHECKERS.items():
        print(f"--- {name.upper()} ---")
        times = run_checker(name, cmd)
        results[name] = times
        print()

    print("=== SUMMARY ===")
    for name, times in results.items():
        print(
            f"{name:<10} | "
            f"avg: {mean(times):8.3f}s | "
            f"min: {min(times):8.3f}s | "
            f"max: {max(times):8.3f}s"
        )


if __name__ == "__main__":
    main()
