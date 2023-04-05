import watchfiles
from invoke import Context, task

REMOTE_HOST = "c17.abilian.com"
REMOTE_DIR = "/home/fermigier/nua-vagrant"

EXCLUDES = [
    ".idea",
    ".vagrant",
    ".git",
    ".env",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".nox",
    ".tox",
    ".cache",
    ".coverage",
]


@task
def test(c: Context):
    """Run full orchestrator lifecycle in vagrant."""
    c.run("vagrant destroy -f")
    c.run("vagrant up")
    ssh(c, "cd /vagrant/nua-infra-abilian/ && poetry install")
    ssh(c, "cd /vagrant/nua-infra-abilian/ && poetry run inv all --host=localhost")
    print("Cleaning up...")
    c.run("vagrant destroy -f")


@task
def watch(c: Context, host=None):
    """Watch for changes a push to a remote server."""
    host = host or REMOTE_HOST

    excludes_args = " ".join([f"--exclude={e}" for e in EXCLUDES])
    for _ in watchfiles.watch("."):
        print("Syncing to remote server...")
        c.run(f"rsync -e ssh -avz {excludes_args} ./ {host}:{REMOTE_DIR}")


def ssh(c, cmd):
    c.run(f"vagrant ssh -c '{cmd}'")
