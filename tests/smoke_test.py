import os
import subprocess
import sys
from unittest import mock


def test_smoke():
    with mock.patch.dict(os.environ, {'TEST': 'true'}):
        subprocess.check_call([sys.executable, 'main.py'])
