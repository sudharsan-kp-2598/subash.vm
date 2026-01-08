import shutil
import subprocess
import time
import statistics
import tempfile
import hashlib
from pathlib import Path
from typing import Dict, Tuple

ORIGINAL_PATH = Path(
    "/home/subash-nts0300/Typing-Analysis/cpython-src/Python-3.10.19/Lib"
)

FORMATTERS = {
    "black": ["black"],
    "ruff_format": ["ruff", "format"],
    "isort": ["isort"],
    "yapf": ["yapf", "-ir"],
    "autopep8": ["autopep8", "--in-place", "--recursive"],
}

WARM_RUNS = 3


# -------------------- helpers --------------------

def hash_py_files(root: Path) -> Dict[Path, str]:
    hashes: Dict[Path, str] = {}
    for path in root.rglob("*.py"):
        try:
            hashes[path.relative_to(root)] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
        except OSError:
            continue
    return hashes


def count_changed_files(
    before: Dict[Path, str], after: Dict[Path, str]
) -> int:
    changed = 0
    for path, h in before.items():
        if path in after and after[path] != h:
            changed += 1
    return changed


# -------------------- single run --------------------

def run_single_formatter_run(
    base_cmd,
) -> Tuple[float, bool, int]:
    """
    Returns:
        elapsed_time, success, files_formatted
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "Lib"
        shutil.copytree(ORIGINAL_PATH, tmp_path)

        before_hashes = hash_py_files(tmp_path)

        start = time.perf_counter()
        success = True
        try:
            subprocess.run(
                base_cmd + [str(tmp_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError:
            success = False

        elapsed = time.perf_counter() - start

        after_hashes = hash_py_files(tmp_path)
        formatted_files = count_changed_files(before_hashes, after_hashes)

        return elapsed, success, formatted_files


# -------------------- formatter benchmark --------------------

def run_formatter(name, base_cmd):
    print(f"\n=== {name.upper()} ===")

    runs = []

    for i in range(1 + WARM_RUNS):
        elapsed, success, formatted = run_single_formatter_run(base_cmd)

        label = "Cold run" if i == 0 else f"Warm run {i}"

        if success:
            print(
                f"{label}: {elapsed:.3f}s | files formatted: {formatted}"
            )
        else:
            print(
                f"{label}: FAILED after {elapsed:.3f}s | "
                f"files formatted before failure: {formatted}"
            )

        runs.append((elapsed, success, formatted))

    successful_times = [t for t, ok, _ in runs if ok]
    avg_time = (
        statistics.mean(successful_times)
        if successful_times
        else None
    )

    return {
        "runs": runs,
        "avg_time": avg_time,
    }


# -------------------- main --------------------

def main():
    results = {}

    for name, cmd in FORMATTERS.items():
        results[name] = run_formatter(name, cmd)

    print("\n=== SUMMARY ===")
    for name, data in results.items():
        avg = data["avg_time"]

        if avg is not None:
            print(
                f"{name:<12} | avg time (successful runs): {avg:.3f}s | status: OK"
            )
        else:
            print(
                f"{name:<12} | avg time: N/A | status: FAILED"
            )


if __name__ == "__main__":
    main()
