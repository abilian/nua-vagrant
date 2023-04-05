#!/usr/bin/env python3

import subprocess
from pathlib import Path

NUA_GIT = "https://github.com/abilian/nua"

DIM = "\033[2m"
RESET = "\033[0m"


APT_CONF = """
Acquire::http {No-Cache=True;};
APT::Install-Recommends "0";
APT::Install-Suggests "0";
Acquire::GzipIndexes "true";
Acquire::CompressionTypes::Order:: "gz";
Dir::Cache { srcpkgcache ""; pkgcache ""; }
"""


def main():
    Path("/etc/apt/apt.conf.d/00-nua").write_text(APT_CONF)

    install_packages()
    clone_nua()
    install_nua()


def install_packages():
    sh("apt-get update -q")
    sh("apt-get upgrade -y")
    sh("apt-get install -y git python3 python3-pip python3-venv python3-dev curl")
    sh("curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -")


def clone_nua():
    if not Path("nua").exists():
        sh(f"git clone {NUA_GIT}")


def install_nua():
    sh("./install.py", cwd="nua/nua-orchestrator")
    sh("sudo ./env/bin/nua-bootstrap", cwd="nua/nua-orchestrator")


def sh(cmd: str, cwd: str = "."):
    """Run a shell command."""
    print(f'{DIM}Running "{cmd}" locally in "{cwd}"...{RESET}')
    subprocess.run(cmd, shell=True, cwd=cwd, check=True)


if __name__ == "__main__":
    main()
