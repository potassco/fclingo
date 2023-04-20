"""
This is provided for compatibility.
"""
from setuptools import setup

setup(
    name="fclingo",
    version="1.0",
    description="Solver for ASP modulo conditional linear constraints with founded variables",
    url="http://github.com/krr-up/fclingo",
    author="Philipp Wanko",
    author_email="wanko@cs.uni-potsdam.de",
    license="MIT",
    packages=["fclingo"],
    install_requires=["clingo", "clingcon"],
    dependency_links=[
        "https://test.pypi.org/simple/clingo",
        "https://test.pypi.org/simple/clingcon",
    ],
)
