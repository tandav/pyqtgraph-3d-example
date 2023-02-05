import subprocess
import sys
import os
from unittest import mock


def test_smoke():
    with mock.patch.dict(os.environ, {'TEST': 'true'}):
        subprocess.check_call([sys.executable, "main.py"])
