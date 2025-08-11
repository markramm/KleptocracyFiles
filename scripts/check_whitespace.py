#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def is_binary(path: Path) -> bool:
    try:
        with path.open('rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except OSError:
        return False

def check_file(path: Path):
    issues = []
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return issues
    if '\r' in text:
        issues.append(f"{path}: CRLF line endings")
    return issues

def main() -> int:
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True)
    files = [Path(line) for line in result.stdout.splitlines()]
    problems = []
    for path in files:
        if is_binary(path):
            continue
        problems.extend(check_file(path))
    if problems:
        print('Whitespace issues found:')
        for p in problems:
            print(p)
        return 1
    print('No whitespace issues found.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
