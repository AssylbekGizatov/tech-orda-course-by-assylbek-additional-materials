#!/usr/bin/env python3
"""Execute the whole course using the verified runner, updating notebook outputs.

Usage:
    python scripts/execute_course.py
    python scripts/execute_course.py --only week_09_linear_regression/practice/01_linear_regression_from_scratch.ipynb

Install requirements-ml.txt first. This is an execution command: it updates
notebook outputs and the validation report. For a read-only integrity audit,
use scripts/validate_course.py instead. No generator is invoked here.
"""
from pathlib import Path
import subprocess
import sys


def main():
    runner = Path(__file__).resolve().with_name("validate_weeks_09_17.py")
    return subprocess.call([sys.executable, str(runner), "--all", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
