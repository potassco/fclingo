"""
This module provides a propagator for CSP constraints. It can also be used as a
stand-alone application.
"""

from .parsing import THEORY, transform
from .propagator import Propagator
from .translator import AUX, Translator
