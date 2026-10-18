#!/usr/bin/env python3
"""Create the requested private GitHub repository and push this course.

Requires Git and an authenticated GitHub CLI (gh). No tokens are requested
by this script. Without --publish it checks local readiness and prints the
intended target without creating a repository, committing, or pushing.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'AssylbekGizatov'
NAME = 'tech-orda-course-authored-by-gizatov-a-s'
FULL = f'{OWNER}/{NAME}'
DESCRIPTION = 'Tech Orda course authored by Gizatov A. S. — 26-week beginner ML & AI course, lectures, datasets, labs and homework'
EXPECTED_URLS = (f'https://github.com/{FULL}.git', f'https://github.com/{FULL}', f'git@github.com:{FULL}.git')


def run(*command: str, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, text=True, check=check,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)


def verify_origin() -> None:
    """Check effective fetch/push destinations, including Git URL rewriting."""
    configured = run('git', 'config', '--get-all', 'remote.origin.pushurl', capture=True, check=False)
    if configured.returncode == 0:
        raise RuntimeError('origin has an explicit pushurl; remove it after reviewing the intended destination.')
    if configured.returncode != 1:
        raise RuntimeError('Could not inspect the push destination.')
    fetch = run('git', 'remote', 'get-url', '--all', 'origin', capture=True).stdout.splitlines()
    push = run('git', 'remote', 'get-url', '--push', '--all', 'origin', capture=True).stdout.splitlines()
    if len(fetch) != 1 or len(push) != 1 or fetch[0] not in EXPECTED_URLS or push[0] not in EXPECTED_URLS:
        raise RuntimeError('Effective origin fetch/push destination differs from the verified private repository.')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true', help='Create PRIVATE repository and push main')
    args = parser.parse_args()
    print(f'Target: https://github.com/{FULL}\nVisibility: PRIVATE\nSource: {ROOT}')
    run(sys.executable, str(ROOT / 'scripts' / 'validate_course.py'))
    if not args.publish:
        print('Readiness check only. To create and push: python scripts/publish_private_repo.py --publish')
        return 0
    for command in ('git', 'gh'):
        if shutil.which(command) is None:
            raise RuntimeError(f'{command} is not installed; see 00_course_admin/GITHUB_PUBLISH.md')
    login = run('gh', 'api', 'user', '--jq', '.login', capture=True).stdout.strip()
    if login.casefold() != OWNER.casefold():
        raise RuntimeError(f'Authenticated account is {login!r}; expected {OWNER!r}. Nothing was created.')
    if not (ROOT / '.git').is_dir():
        run('git', 'init', '-b', 'main')
    branch = run('git', 'symbolic-ref', '--short', 'HEAD', capture=True).stdout.strip()
    if branch != 'main':
        raise RuntimeError(f'Current branch is {branch!r}; expected main. No branch was changed.')
    remotes = run('git', 'remote', capture=True).stdout.split()
    if 'origin' in remotes:
        verify_origin()
    # Explicitly require a new repository. A failed lookup alone is not treated as
    # proof of absence; gh repo create is authoritative and will not overwrite one.
    existing = run('gh', 'repo', 'view', FULL, '--json', 'nameWithOwner,visibility', capture=True, check=False)
    if existing.returncode == 0:
        raise RuntimeError('Target already exists. This script will not overwrite or repurpose an existing repository.')
    # Git identity must be configured by the user. No personal identity is invented.
    run('git', 'var', 'GIT_AUTHOR_IDENT', capture=True)
    run('git', 'var', 'GIT_COMMITTER_IDENT', capture=True)
    run('git', 'add', '--all')
    changes = run('git', 'diff', '--cached', '--quiet', check=False).returncode
    if changes == 1:
        run('git', 'commit', '-m', 'Add complete 26-week Tech Orda ML and AI course')
    elif changes != 0:
        raise RuntimeError('Could not inspect the staged changes')
    run('git', 'rev-parse', '--verify', 'HEAD', capture=True)
    run('gh', 'repo', 'create', FULL, '--private', '--description', DESCRIPTION)
    repo = json.loads(run('gh', 'repo', 'view', FULL, '--json', 'nameWithOwner,visibility,url', capture=True).stdout)
    if repo['nameWithOwner'].casefold() != FULL.casefold() or repo['visibility'] != 'PRIVATE':
        raise RuntimeError('Private target verification failed; no files were pushed.')
    if 'origin' not in remotes:
        run('git', 'remote', 'add', 'origin', f'https://github.com/{FULL}.git')
    verify_origin()
    run('git', 'push', '--set-upstream', 'origin', 'main')
    head = run('git', 'rev-parse', 'HEAD', capture=True).stdout.strip()
    remote = run('gh', 'api', f'repos/{FULL}/commits/main', '--jq', '.sha', capture=True).stdout.strip()
    privacy = run('gh', 'api', f'repos/{FULL}', '--jq', '.private', capture=True).stdout.strip()
    if head != remote or privacy != 'true':
        raise RuntimeError('Final remote commit/privacy check failed; inspect the repository before sharing.')
    print(f'Published and verified PRIVATE: {repo["url"]}\nCommit: {head}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'STOP: {exc}', file=sys.stderr)
        raise SystemExit(1)
