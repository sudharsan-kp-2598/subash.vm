import subprocess
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path(
    "/home/subash-nts0300/Typing-Analysis/cpython-src/Python-3.10.19/Lib"
)

RESULT_FILE = Path("formatter_failures_summary.txt")

FORMATTERS = [
    {
        "name": "BLACK",
        "command": ["black", "--verbose"],
    },
    {
        "name": "RUFF_FORMAT",
        "command": ["ruff", "format", "--verbose"],
    },
    {
        "name": "YAPF",
        "command": ["yapf", "-r", "--verbose"],
    },
]


def collect_py_files(root: Path):
    return sorted(p for p in root.rglob("*.py"))


def extract_first_error(stderr: str):
    for line in stderr.splitlines():
        if any(word in line.lower() for word in ("error", "failed", "exception")):
            return line.strip()
    return "No explicit error line found"


def run_formatter(formatter):
    name = formatter["name"]
    cmd = formatter["command"]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        work_dir = tmp_path / "Lib"

        shutil.copytree(SOURCE_DIR, work_dir)

        py_files = collect_py_files(work_dir)

        process = subprocess.Popen(
            cmd + [str(work_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate()
        combined = stdout + "\n" + stderr

        last_file = None
        next_file = None

        for line in reversed(combined.splitlines()):
            if ".py" in line:
                for f in py_files:
                    if str(f) in line:
                        last_file = f
                        break
            if last_file:
                break

        if last_file and last_file in py_files:
            idx = py_files.index(last_file)
            if idx + 1 < len(py_files):
                next_file = py_files[idx + 1]

        error_line = extract_first_error(stderr)

        with RESULT_FILE.open("a") as f:
            f.write(f"\nFormatter: {name}\n")
            f.write(f"Status: {'FAILED' if process.returncode != 0 else 'SUCCESS'}\n")
            f.write(f"Last successful file: {last_file}\n")
            f.write(f"Next file (likely failure): {next_file}\n")
            f.write(f"Error summary: {error_line}\n")
            f.write("-" * 60 + "\n")


def main():
    RESULT_FILE.write_text(
        f"Formatter Failure Summary\nGenerated: {datetime.now()}\n"
    )

    for formatter in FORMATTERS:
        run_formatter(formatter)

    print(f"Done. Clean summary written to {RESULT_FILE.resolve()}")


if __name__ == "__main__":
    main()
