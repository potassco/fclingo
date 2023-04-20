import os

import nox

nox.options.sessions = "lint_flake8", "lint_pylint", "test"

PYTHON_VERSIONS = ["3.6", "3.9"] if "GITHUB_ACTIONS" in os.environ else None


@nox.session
def lint_flake8(session):
    session.install("flake8", "flake8-black", "flake8-isort")
    session.run("flake8", "fclingo")


@nox.session
def lint_pylint(session):
    session.install("-r", f".github/requirements.txt", "pylint")
    session.run("pylint", "fclingo")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    session.install("-r", f".github/requirements.txt")
    session.run("python", "-m", "unittest", "discover", "-v")
