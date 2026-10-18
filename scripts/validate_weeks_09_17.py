#!/usr/bin/env python3
"""Execute week 09–17 notebooks in real Jupyter kernels and retain their outputs.

Use a Python environment containing the dependencies recorded in the version
manifest. This script is intentionally separate from the content generator.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path(os.environ.get("TECH_ORDA_QA_CACHE", "/tmp/tech-orda-ml-runtime"))
for environment_key, dirname in {
    "JUPYTER_CONFIG_DIR": "jupyter-config", "JUPYTER_DATA_DIR": "jupyter-data",
    "JUPYTER_RUNTIME_DIR": "jupyter-runtime", "IPYTHONDIR": "ipython",
    "MPLCONFIGDIR": "matplotlib", "XDG_CACHE_HOME": "cache",
}.items():
    directory = SCRATCH / dirname
    directory.mkdir(parents=True, exist_ok=True)
    os.environ[environment_key] = str(directory)
for environment_key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                        "TF_NUM_INTRAOP_THREADS", "TF_NUM_INTEROP_THREADS"]:
    os.environ[environment_key] = "1"
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import nbformat
from nbclient import NotebookClient


def write_versions(path):
    packages = ["numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "seaborn", "plotly", "ipywidgets",
                "xgboost", "lightgbm", "shap", "lime", "torch", "tensorflow-cpu", "keras",
                "nbformat", "nbclient", "ipykernel", "ipython", "jupyter-client"]
    versions = {}
    for name in packages:
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    manifest = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "python_version": platform.python_version(),
                "platform": platform.platform(), "packages": versions,
                "execution": "CPU, fixed notebook seeds, fresh real Jupyter kernel per notebook",
                "thread_limit": 1}
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Validate every week in the common environment")
    parser.add_argument("--only", nargs="*", help="Optional repository-relative notebook paths")
    args = parser.parse_args()
    if args.all:
        result_path = ROOT / "00_course_admin" / "validation_all.json"
        version_path = ROOT / "00_course_admin" / "validation_all_versions.json"
    else:
        result_path = ROOT / "scripts" / "validation_weeks_09_17.json"
        version_path = ROOT / "scripts" / "validation_weeks_09_17_versions.json"
    write_versions(version_path)
    if args.only:
        paths = [ROOT / relative for relative in args.only]
    else:
        paths = sorted(p for p in ROOT.glob("week_*/*/*.ipynb")
                       if args.all or 9 <= int(p.parent.parent.name.split("_")[1]) <= 17)
    previous = json.loads(result_path.read_text()) if args.only and result_path.exists() else {"results": []}
    records = {entry["path"]: entry for entry in previous["results"]}
    for path in paths:
        relative = str(path.relative_to(ROOT))
        started = time.monotonic()
        record = {"path": relative, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                  "kind": "homework_starter" if path.parent.name == "homework" else "worked_practice"}
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            source_data = [(cell.cell_type, cell.source) for cell in notebook.cells]
            record["source_sha256"] = hashlib.sha256(json.dumps(source_data, ensure_ascii=False).encode()).hexdigest()
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None
            NotebookClient(notebook, timeout=360, startup_timeout=180,
                kernel_name="python3", allow_errors=False, record_timing=True,
                resources={"metadata": {"path": str(path.parent)}}).execute()
            nbformat.validate(notebook)
            nbformat.write(notebook, path)
            code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
            record.update(status="passed", total_cells=len(notebook.cells),
                code_cells=len(code_cells), executed_code_cells=sum(c.execution_count is not None for c in code_cells),
                image_outputs=sum("image/png" in output.get("data", {}) for cell in code_cells for output in cell.outputs),
                error_outputs=sum(output.get("output_type") == "error" for cell in code_cells for output in cell.outputs),
                outputs_saved=True, file_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            assert record["executed_code_cells"] == record["code_cells"]
            assert record["error_outputs"] == 0
        except Exception as error:
            record.update(status="failed", error_type=type(error).__name__, error=str(error)[-18000:],
                          traceback=traceback.format_exc()[-18000:], outputs_saved=False)
        record["duration_seconds"] = round(time.monotonic() - started, 3)
        records[relative] = record
        report = {"scope": "all 26 weeks" if args.all else "weeks 09–17", "executor": "nbclient real Jupyter kernels",
                  "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                  "versions_file": str(version_path.relative_to(ROOT)),
                  "summary": {"total": len(records), "passed": sum(r["status"] == "passed" for r in records.values()),
                              "failed": sum(r["status"] == "failed" for r in records.values()),
                              "executed_code_cells": sum(r.get("executed_code_cells", 0) for r in records.values()),
                              "image_outputs": sum(r.get("image_outputs", 0) for r in records.values()),
                              "practice_notebooks": sum("/practice/" in r["path"] for r in records.values()),
                              "homework_starters": sum("/homework/" in r["path"] for r in records.values()),
                              "total_duration_seconds": round(sum(r["duration_seconds"] for r in records.values()), 3)},
                  "limits": ["Run All verifies offline worked examples and runnable starters, not completion of student TODO exercises.",
                             "Live API, Copilot Studio and n8n account/deployment activities are not authenticated by offline execution."],
                  "results": sorted(records.values(), key=lambda r: r["path"])}
        result_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{record['status'].upper()} {relative} {record['duration_seconds']}s", flush=True)
        if record["status"] == "failed":
            print(record["error"][-4000:], flush=True)
    return 1 if any(record["status"] == "failed" for record in records.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
