import subprocess
import time
import statistics
from pathlib import Path

TARGET_PATH = Path(
    "/home/subash-nts0300/Typing-Analysis/cpython-src/Python-3.10.19/Lib"
)

LINTERS = {
    "ruff": ["ruff", "check"],
    "pylint": ["pylint"],
    "flake8": ["flake8"],
    "bandit": ["bandit", "-r"],
    "pyflakes": ["pyflakes"],
}

WARM_RUNS = 3


def run_linter(name, base_cmd):
    cmd = base_cmd + [str(TARGET_PATH)]

    print(f"\n=== {name.upper()} ===")

    # Cold run
    start = time.perf_counter()
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cold_time = time.perf_counter() - start
    print(f"Cold run: {cold_time:.3f}s")

    # Warm runs
    warm_times = []
    for i in range(WARM_RUNS):
        start = time.perf_counter()
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elapsed = time.perf_counter() - start
        warm_times.append(elapsed)
        print(f"Warm run {i + 1}: {elapsed:.3f}s")

    avg_warm = statistics.mean(warm_times)
    print(f"Avg warm: {avg_warm:.3f}s")

    return {
        "cold": cold_time,
        "warm_avg": avg_warm,
    }


def main():
    results = {}

    for name, cmd in LINTERS.items():
        results[name] = run_linter(name, cmd)

    print("\n=== SUMMARY ===")
    for name, data in results.items():
        print(
            f"{name:<8} | cold: {data['cold']:.3f}s | warm avg: {data['warm_avg']:.3f}s"
        )


if __name__ == "__main__":
    main()
