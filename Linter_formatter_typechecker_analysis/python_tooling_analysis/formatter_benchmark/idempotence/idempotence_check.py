import shutil
import subprocess
import sys
from pathlib import Path
import difflib


BASE_DIR = Path(__file__).parent
SAMPLE = BASE_DIR / "sample.py"
RUN1 = BASE_DIR / "run1"
RUN2 = BASE_DIR / "run2"


def run_formatter(command: str, cwd: Path) -> None:
    subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def read_file(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python idempotence_check.py '<formatter command>'")
        sys.exit(1)

    formatter_cmd = sys.argv[1]

    # Clean runs
    shutil.rmtree(RUN1, ignore_errors=True)
    shutil.rmtree(RUN2, ignore_errors=True)
    RUN1.mkdir()
    RUN2.mkdir()

    # Copy original sample
    shutil.copy(SAMPLE, RUN1 / "sample.py")
    shutil.copy(SAMPLE, RUN2 / "sample.py")

    # First format
    run_formatter(formatter_cmd, RUN1)

    # Second format (on already formatted output)
    shutil.copy(RUN1 / "sample.py", RUN2 / "sample.py")
    run_formatter(formatter_cmd, RUN2)

    # Compare
    run1_lines = read_file(RUN1 / "sample.py")
    run2_lines = read_file(RUN2 / "sample.py")

    diff = list(
        difflib.unified_diff(
            run1_lines,
            run2_lines,
            fromfile="run1/sample.py",
            tofile="run2/sample.py",
        )
    )

    if diff:
        print("❌ NOT IDEMPOTENT — differences detected:\n")
        print("".join(diff))
    else:
        print("✅ IDEMPOTENT — no differences detected")


if __name__ == "__main__":
    main()
