#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

VENV = Path('venv')


def main() -> None:
    """
    This function assumes that directory 'venv' can only be
    created by the function itself.
    """

    assert Path.cwd() == Path(__file__).parent

    if os.name == 'nt':
        activate = f'. {VENV}\\Scripts\\activate'
    else:
        activate = f'. {VENV}/bin/activate'

    if not VENV.is_dir():
        VENV.unlink(missing_ok=True)
        set_venv = subprocess.run(
            f"""
            python -m venv ./venv               && \\
            {activate}                          && \\
            pip install -r requirements.txt
            """,
            shell=True
        )
        if set_venv.returncode != 0:
            sys.exit(set_venv.returncode)

    deployment = subprocess.run(
        f"""
        {activate}                              && \\
        python scripts/_deploy.py
        """,
        shell=True
    )
    sys.exit(deployment.returncode)


if __name__ == '__main__':
    main()
