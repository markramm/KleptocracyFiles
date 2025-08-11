import subprocess
import sys


def test_whitespace_linter():
    subprocess.check_call([sys.executable, 'scripts/check_whitespace.py'])
