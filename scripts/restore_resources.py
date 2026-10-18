#!/usr/bin/env python3
"""Restore missing original course resources from the recorded primary URLs.

No dependencies; does not overwrite an existing file or accept changed bytes.
Run from anywhere: python scripts/restore_resources.py --week 9
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--week', type=int, choices=range(1, 27))
    parser.add_argument('--check', action='store_true', help='Only check local files; no network or changes')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'RESOURCE_CATALOG.json').read_text(encoding='utf-8'))
    failed = 0
    for item in catalog['resources']:
        if args.week is not None and item['week'] != args.week:
            continue
        target = (ROOT / item['relative_path']).resolve()
        if not target.is_relative_to(ROOT) or target == ROOT:
            raise ValueError('Unsafe resource path in catalog')
        if target.exists():
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            ok = actual == item['sha256'] and target.stat().st_size == item['bytes']
            print(('OK      ' if ok else 'CHANGED '), item['relative_path'])
            failed += int(not ok)
            continue
        if args.check:
            print('MISSING ', item['relative_path'])
            failed += 1
            continue
        temporary = None
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            request = Request(item['download_url'], headers={'User-Agent': 'Tech-Orda-course-resource-restore/1.0'})
            digest = hashlib.sha256()
            size = 0
            with urlopen(request, timeout=60) as response, tempfile.NamedTemporaryFile(
                dir=target.parent, prefix='.resource-', delete=False
            ) as output:
                temporary = Path(output.name)
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
                    digest.update(chunk)
                    size += len(chunk)
            if digest.hexdigest() != item['sha256'] or size != item['bytes']:
                raise ValueError('Source changed since the recorded snapshot; manual review required')
            # Same-directory hard link publishes verified bytes atomically and
            # fails if another file appeared; interrupted copies cannot linger.
            os.link(temporary, target)
            print('RESTORED', item['relative_path'])
        except (OSError, ValueError) as exc:
            print('FAILED  ', item['relative_path'], type(exc).__name__, str(exc))
            failed += 1
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
