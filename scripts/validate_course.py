#!/usr/bin/env python3
"""Read-only structural and integrity audit of the packaged Tech Orda course.

Uses only Python's standard library. It does not execute notebook code, download
resources, regenerate files, or modify outputs/reports. Exit 0 means the requested
checks passed; exit 1 means at least one integrity/structure check failed.

    python scripts/validate_course.py
    python scripts/validate_course.py --require-catalog
    python scripts/validate_course.py --require-catalog --json

The optional resource catalog accepts {"resources": [...]} or a top-level list.
Supported local-path fields: relative_path, path; otherwise week + filename.
Resource bytes/size_bytes and sha256 are checked whenever supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys

EXPECTED_WEEKS = 26
EXPECTED_NOTEBOOKS = 54
EXPECTED_ACADEMIC_HOURS = 104
EXPECTED_MODULE_HOURS = {1: 4, 2: 8, 3: 6, 4: 8, 5: 6, 6: 12, 7: 8,
                         8: 4, 9: 6, 10: 8, 11: 6, 12: 8, 13: 8, 14: 8, 15: 4}
WEEK_SUBDIRS = ("presentations", "practice", "datasets", "homework")
PRESENTATION_SUFFIXES = {".pdf", ".ppt", ".pptx", ".html", ".htm", ".md"}
SHA256_PATTERN = re.compile(r"[0-9a-fA-F]{64}\Z")


@dataclass
class Audit:
    errors: list[dict] = field(default_factory=list)
    warnings: list[dict] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def error(self, code, location, message):
        self.errors.append({"code": code, "location": str(location), "message": str(message)})

    def warning(self, code, location, message):
        self.warnings.append({"code": code, "location": str(location), "message": str(message)})


def load_json(path: Path, audit: Audit):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        audit.error("invalid_json", path, error)
        return None


def sha256_file(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_file(root: Path, raw, audit: Audit, location):
    if not isinstance(raw, str) or not raw.strip():
        audit.error("missing_relative_path", location, "A nonempty repository-relative file path is required.")
        return None
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or "\\" in raw:
        audit.error("nonportable_path", location, f"Use a relative POSIX path inside the repository: {raw!r}")
        return None
    candidate = (root / Path(*path.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        audit.error("path_outside_repository", location, raw)
        return None
    return candidate


def check_nonempty_text(path: Path, audit: Audit):
    try:
        if not path.read_text(encoding="utf-8").strip():
            audit.error("empty_text", path, "Required document is empty.")
    except (OSError, UnicodeError) as error:
        audit.error("missing_or_invalid_text", path, error)


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_course_plan(root: Path, audit: Audit):
    plan = load_json(root / "course_plan.json", audit)
    if not isinstance(plan, list):
        audit.error("plan_shape", "course_plan.json", "Expected a list of 26 week objects.")
        return {}, set(), set()
    weeks, presentation_files, notebook_files = {}, set(), set()
    module_hours = Counter()
    total_hours = total_minutes = total_theory = total_practice = session_count = 0
    if len(plan) != EXPECTED_WEEKS:
        audit.error("week_count", "course_plan.json", f"Expected 26 weeks, found {len(plan)}.")
    for position, entry in enumerate(plan):
        location = f"course_plan.json[{position}]"
        if not isinstance(entry, dict):
            audit.error("week_shape", location, "Week must be an object.")
            continue
        number = entry.get("week")
        if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= 26:
            audit.error("week_number", location, "Week must be an integer in 1..26.")
            continue
        if number in weeks:
            audit.error("duplicate_week", location, number)
        folder = relative_file(root, entry.get("folder"), audit, location)
        if folder is None:
            continue
        if folder.name != entry.get("folder") or not folder.name.startswith(f"week_{number:02d}_"):
            audit.error("week_folder_name", location, "Expected a direct root folder named week_XX_<topic>.")
        weeks[number] = folder
        if not folder.is_dir():
            audit.error("missing_week_folder", folder, "Week directory does not exist.")
            continue
        for dirname in WEEK_SUBDIRS:
            if not (folder / dirname).is_dir():
                audit.error("missing_week_subdir", folder / dirname, "Required weekly directory is missing.")
        check_nonempty_text(folder / "README.md", audit)
        check_nonempty_text(folder / "homework" / f"Homework_Week_{number:02d}.md", audit)
        if (folder / "data").exists():
            audit.error("legacy_data_directory", folder / "data", "The canonical dataset directory is datasets/.")
        for dirname in ("practice", "homework"):
            found = {path for path in (folder / dirname).glob("*.ipynb") if path.is_file()}
            notebook_files.update(found)
            if not found:
                audit.error("missing_notebook", folder / dirname, "At least one notebook is required.")
        dataset_files = [path for path in (folder / "datasets").rglob("*")
                         if path.is_file() and path.name.lower() != "readme.md"
                         and not path.name.endswith("_metadata.json") and not path.name.startswith(".")]
        if not dataset_files:
            audit.error("missing_local_dataset", folder / "datasets", "Expected local data/fixtures in addition to documentation.")
        material_files = {path for path in (folder / "presentations").rglob("*")
                          if path.is_file() and path.suffix.lower() in PRESENTATION_SUFFIXES
                          and path.name.lower() != "readme.md"}
        presentation_files.update(material_files)
        if not material_files:
            audit.error("missing_presentation_material", folder / "presentations", "Expected a local PDF, PPT/PPTX, HTML or Markdown resource in addition to README.md.")
        hours, minutes = entry.get("academic_hours"), entry.get("clock_minutes")
        if hours != 4 or minutes != 180:
            audit.error("weekly_hours", location, "Each week must contain 4 academic hours = 180 clock minutes.")
        if finite_number(hours):
            total_hours += hours
        if finite_number(minutes):
            total_minutes += minutes
        sessions = entry.get("sessions")
        if not isinstance(sessions, list) or len(sessions) != 2:
            audit.error("session_count", location, "Each week must have two 90-minute sessions.")
            continue
        for index, session in enumerate(sessions):
            session_location = f"{location}.sessions[{index}]"
            if not isinstance(session, dict):
                audit.error("session_shape", session_location, "Session must be an object.")
                continue
            session_count += 1
            academic = session.get("academic_hours")
            theory, practice = session.get("theory_minutes"), session.get("practice_minutes")
            module = session.get("module")
            if academic != 2 or theory != 36 or practice != 54:
                audit.error("session_hours", session_location, "Expected 2 academic hours, 36 min theory + 54 min practice.")
            if finite_number(theory):
                total_theory += theory
            if finite_number(practice):
                total_practice += practice
            if isinstance(module, int) and not isinstance(module, bool) and finite_number(academic):
                module_hours[module] += academic
            else:
                audit.error("module_hours", session_location, "Module and academic_hours must be numeric identifiers/hours.")
    if set(weeks) != set(range(1, 27)):
        audit.error("week_coverage", "course_plan.json", "Week numbers must cover 1..26 exactly.")
    actual_week_dirs = {path.resolve() for path in root.glob("week_*") if path.is_dir()}
    if actual_week_dirs != set(weeks.values()):
        audit.error("week_directory_coverage", root, "Week folders differ from the course plan.")
    if dict(module_hours) != EXPECTED_MODULE_HOURS:
        audit.error("syllabus_module_hours", "course_plan.json", f"Expected {EXPECTED_MODULE_HOURS}; found {dict(module_hours)}.")
    if total_hours != 104 or total_minutes != 4680 or session_count != 52:
        audit.error("syllabus_total_hours", "course_plan.json", "Expected 104 academic hours, 4680 minutes / 78 clock hours, 52 sessions.")
    if total_theory != 1872 or total_practice != 2808 or total_theory + total_practice != total_minutes:
        audit.error("theory_practice_balance", "course_plan.json", "Expected 1872 theory minutes and 2808 practice minutes (40%/60%).")
    syllabus = root / "00_course_admin" / "original_syllabus.pdf"
    if not syllabus.is_file():
        audit.error("missing_original_syllabus", syllabus, "The source syllabus must be retained.")
    else:
        with syllabus.open("rb") as stream:
            if b"%PDF-" not in stream.read(1024):
                audit.error("invalid_syllabus_pdf", syllabus, "PDF signature is missing.")
    audit.metrics["schedule"] = {"weeks": len(weeks), "sessions": session_count,
        "academic_hours": total_hours, "clock_minutes": total_minutes,
        "theory_minutes": total_theory, "practice_minutes": total_practice,
        "module_academic_hours": dict(sorted(module_hours.items()))}
    audit.metrics["local_presentation_files"] = len(presentation_files)
    return weeks, presentation_files, notebook_files


def source_text(cell, audit: Audit, location):
    value = cell.get("source")
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(line, str) for line in value):
        return "".join(value)
    audit.error("invalid_cell_source", location, "Notebook source must be a string or list of strings.")
    return ""


def inspect_notebook(path: Path, record: dict, root: Path, audit: Audit):
    notebook = load_json(path, audit)
    if not isinstance(notebook, dict) or notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        audit.error("notebook_structure", path, "Expected nbformat 4 notebook with cells.")
        return None
    source_data, code_count, executed_count, errors, images = [], 0, 0, 0, 0
    for index, cell in enumerate(notebook["cells"]):
        location = f"{path.relative_to(root)}:cell{index + 1}"
        if not isinstance(cell, dict) or cell.get("cell_type") not in {"code", "markdown", "raw"}:
            audit.error("cell_structure", location, "Unexpected notebook cell structure/type.")
            continue
        source_data.append((cell["cell_type"], source_text(cell, audit, location)))
        if cell["cell_type"] == "code":
            code_count += 1
            if isinstance(cell.get("execution_count"), int) and not isinstance(cell.get("execution_count"), bool):
                executed_count += 1
            outputs = cell.get("outputs", [])
            if not isinstance(outputs, list):
                audit.error("cell_outputs", location, "Code outputs must be a list.")
                continue
            for output in outputs:
                if not isinstance(output, dict):
                    audit.error("output_structure", location, "Output must be an object.")
                    continue
                errors += output.get("output_type") == "error"
                data = output.get("data", {})
                images += isinstance(data, dict) and "image/png" in data
    if code_count == 0 or executed_count != code_count:
        audit.error("unexecuted_code", path, f"Executed {executed_count}/{code_count} code cells.")
    if errors:
        audit.error("notebook_error_output", path, f"Found {errors} error outputs.")
    if record.get("status") != "passed" or record.get("outputs_saved") is not True:
        audit.error("unpassed_validation_record", path, "Canonical report must mark this notebook passed with outputs saved.")
    actual_counts = {"total_cells": len(notebook["cells"]), "code_cells": code_count,
                     "executed_code_cells": executed_count, "image_outputs": images, "error_outputs": errors}
    for key, value in actual_counts.items():
        if record.get(key) != value:
            audit.error("validation_count_mismatch", path, f"{key}: report={record.get(key)!r}, actual={value}.")
    actual_source_sha = hashlib.sha256(json.dumps(source_data, ensure_ascii=False).encode()).hexdigest()
    if record.get("source_sha256") != actual_source_sha:
        audit.error("notebook_source_hash", path, "Notebook source differs from the executed/recorded source.")
    if record.get("file_sha256") != sha256_file(path):
        audit.error("notebook_file_hash", path, "Notebook bytes differ from the saved executed artifact.")
    return actual_counts


def check_notebooks(root: Path, paths: set[Path], audit: Audit):
    report_path = root / "00_course_admin" / "validation_all.json"
    report = load_json(report_path, audit)
    if not isinstance(report, dict) or not isinstance(report.get("results"), list):
        audit.error("validation_report_shape", report_path, "Expected canonical report with results list.")
        return
    if len(paths) != EXPECTED_NOTEBOOKS or len(report["results"]) != EXPECTED_NOTEBOOKS:
        audit.error("notebook_count", root, f"Expected 54 files and 54 records; found {len(paths)} files and {len(report['results'])} records.")
    seen, totals = set(), Counter()
    for index, record in enumerate(report["results"]):
        location = f"validation_all.json.results[{index}]"
        if not isinstance(record, dict):
            audit.error("validation_record_shape", location, "Expected a record object.")
            continue
        path = relative_file(root, record.get("path"), audit, location)
        if path is None:
            continue
        if path in seen:
            audit.error("duplicate_notebook_record", location, record.get("path"))
        seen.add(path)
        if path not in paths:
            audit.error("unexpected_notebook_record", location, "Record does not refer to a current weekly notebook.")
            continue
        counts = inspect_notebook(path, record, root, audit)
        if counts:
            totals.update(counts)
    if seen != paths:
        missing = sorted(str(path.relative_to(root)) for path in paths - seen)
        audit.error("notebook_record_coverage", report_path, f"Report coverage differs from files. Missing records: {missing}")
    summary = report.get("summary", {})
    if not isinstance(summary, dict) or summary.get("total") != 54 or summary.get("passed") != 54 or summary.get("failed") != 0:
        audit.error("validation_summary", report_path, "Canonical summary must report 54 passed, 0 failed.")
    elif summary.get("executed_code_cells") != totals["executed_code_cells"] or summary.get("image_outputs") != totals["image_outputs"]:
        audit.error("validation_summary_counts", report_path, "Summary code/image counts differ from actual notebooks.")
    audit.metrics["notebooks"] = {"total": len(paths), "practice": sum(path.parent.name == "practice" for path in paths),
        "homework_starters": sum(path.parent.name == "homework" for path in paths),
        "executed_code_cells": totals["executed_code_cells"], "png_outputs": totals["image_outputs"],
        "error_outputs": totals["error_outputs"], "records_checked": len(seen)}


def check_catalog(root: Path, weeks: dict, presentation_files: set[Path], catalog: Path,
                  require_catalog: bool, audit: Audit):
    if not catalog.is_file():
        message = "Resource catalog is not present; byte/checksum verification of downloaded materials was not performed."
        (audit.error if require_catalog else audit.warning)("missing_resource_catalog", catalog, message)
        audit.metrics["resources"] = {"catalog_present": False, "resources_checked": 0}
        return
    payload = load_json(catalog, audit)
    resources = payload.get("resources") if isinstance(payload, dict) else payload
    if not isinstance(resources, list):
        audit.error("resource_catalog_shape", catalog, 'Expected {"resources": [...]} or a top-level list.')
        return
    seen, bytes_verified, hashes_verified, linked_only = set(), 0, 0, 0
    for index, resource in enumerate(resources):
        location = f"{catalog.name}.resources[{index}]"
        if not isinstance(resource, dict):
            audit.error("resource_record_shape", location, "Expected resource object.")
            continue
        raw = resource.get("relative_path") or resource.get("path")
        if not raw and isinstance(resource.get("week"), int) and resource["week"] in weeks and resource.get("filename"):
            raw = f"{weeks[resource['week']].name}/presentations/{resource['filename']}"
        if not raw:
            linked_only += 1
            audit.warning("external_reference_only", location, "No local file path: URL reference is not a verified downloaded artifact.")
            continue
        path = relative_file(root, raw, audit, location)
        if path is None:
            continue
        seen.add(path)
        if not path.is_file():
            audit.error("missing_catalog_resource", location, raw)
            continue
        expected_bytes = resource.get("bytes", resource.get("size_bytes"))
        if expected_bytes is not None:
            if not isinstance(expected_bytes, int) or isinstance(expected_bytes, bool) or expected_bytes < 0:
                audit.error("invalid_resource_byte_count", location, expected_bytes)
            elif path.stat().st_size != expected_bytes:
                audit.error("resource_byte_mismatch", location, f"Expected {expected_bytes}, found {path.stat().st_size}: {raw}")
            else:
                bytes_verified += 1
        expected_sha = resource.get("sha256")
        if expected_sha is not None:
            if not isinstance(expected_sha, str) or not SHA256_PATTERN.fullmatch(expected_sha):
                audit.error("invalid_resource_sha256", location, "sha256 must contain exactly 64 hexadecimal characters.")
            elif sha256_file(path) != expected_sha.lower():
                audit.error("resource_hash_mismatch", location, raw)
            else:
                hashes_verified += 1
        if path.suffix.lower() == ".pdf":
            with path.open("rb") as stream:
                if b"%PDF-" not in stream.read(1024):
                    audit.error("invalid_resource_pdf", location, f"Missing PDF signature: {raw}")
            if "pages" in resource and (not isinstance(resource["pages"], int)
                                        or isinstance(resource["pages"], bool) or resource["pages"] < 1):
                audit.error("invalid_resource_page_count", location, "PDF page count, when supplied, must be a positive integer.")
    unlisted = sorted(str(path.relative_to(root)) for path in presentation_files - seen)
    if unlisted:
        (audit.error if require_catalog else audit.warning)("unlisted_presentation_files", catalog,
            f"Presentation files without a catalog record: {unlisted}")
    audit.metrics["resources"] = {"catalog_present": True, "catalog_entries": len(resources),
        "local_paths": len(seen), "byte_counts_verified": bytes_verified,
        "sha256_verified": hashes_verified, "external_links_only": linked_only,
        "unlisted_presentation_files": len(unlisted)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--catalog", type=Path, help="Catalog path, relative to repository root unless absolute")
    parser.add_argument("--require-catalog", action="store_true", help="Fail if catalog is missing or presentation files are unlisted")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results to stdout; no file is written")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.catalog:
        catalog = args.catalog if args.catalog.is_absolute() else root / args.catalog
    else:
        catalog = root / "RESOURCE_CATALOG.json"
        if not catalog.exists() and (root / "00_course_admin" / "RESOURCE_CATALOG.json").exists():
            catalog = root / "00_course_admin" / "RESOURCE_CATALOG.json"
    audit = Audit()
    weeks, presentations, notebooks = check_course_plan(root, audit)
    check_notebooks(root, notebooks, audit)
    check_catalog(root, weeks, presentations, catalog, args.require_catalog, audit)
    result = {"status": "passed" if not audit.errors else "failed", "read_only": True,
              "metrics": audit.metrics, "errors": audit.errors, "warnings": audit.warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status'].upper()}: read-only structural and integrity audit")
        for category, values in audit.metrics.items():
            print(f"  {category}: {json.dumps(values, ensure_ascii=False)}")
        for item in audit.errors:
            print(f"ERROR [{item['code']}] {item['location']}: {item['message']}")
        for item in audit.warnings:
            print(f"NOTE [{item['code']}] {item['location']}: {item['message']}")
        print(f"Errors: {len(audit.errors)}; notes: {len(audit.warnings)}. No files were changed.")
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
