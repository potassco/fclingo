"""
Basic functions to run tests.
"""

import clingo
from clingcon import ClingconTheory
from clingo.ast import ProgramBuilder, parse_string

from fclingo import THEORY, Translator
from fclingo.__main__ import CSP
from fclingo.parsing import HeadBodyTransformer
from fclingo.translator import DEF


class Config:
    def __init__(self, max_int, min_int, print_trans) -> None:
        self.max_int = max_int
        self.min_int = min_int
        self.print_trans = print_trans


class Solver(object):
    """
    Simplistic solver for multi-shot solving.
    """

    def __init__(self, minint=-20, maxint=20, threads=8, options=()):
        self.prg = clingo.Control(
            ["0", "-t", str(threads)] + list(options), message_limit=0
        )
        self.optimize = False
        self.bound = None
        self.propagator = ClingconTheory()
        self.propagator.register(self.prg)
        self.maxint = maxint
        self.minint = minint
        self.propagator.configure("max-int", str(maxint))
        self.propagator.configure("min-int", str(minint))

        self.prg.add("base", [], THEORY)

    def _parse_model(self, ret, model):
        """
        Combine model and assignment in one list.
        """
        self.propagator.on_model(model)
        m = []
        for sym in model.symbols(shown=True):
            s = str(sym)
            if not s.startswith("_"):
                m.append(s)

        a = [
            (str(assignment.arguments[0]), assignment.arguments[1].number)
            for assignment in model.symbols(theory=True)
            if assignment.name == CSP
            and len(assignment.arguments) == 2
            and not assignment.arguments[0].name.startswith("_")
        ]

        ret.append((sorted(m), sorted(a)))

    def solve(self, s):
        """
        Translate and solve program s.
        """
        # pylint: disable=unsubscriptable-object,cell-var-from-loop,no-member
        with ProgramBuilder(self.prg) as bld:
            hbt = HeadBodyTransformer()
            parse_string(
                s,
                lambda ast: self.propagator.rewrite_ast(
                    ast, lambda stm: bld.add(hbt.visit(stm))
                ),
            )

        self.prg.ground([("base", [])])
        translator = Translator(self.prg, Config(self.maxint, self.minint, False))
        translator.translate()

        ret = []
        self.propagator.prepare(self.prg)
        self.prg.solve(on_model=lambda m: self._parse_model(ret, m))
        ret.sort()

        return [m + a for m, a in ret]


def _solve(solver, s):
    ret = solver.solve(s)
    return ret


def solve(s, minint=-20, maxint=20, threads=8, options=()):
    """
    Return the (optimal) models/assignments of the program in the given string.
    """
    solver = Solver(minint, maxint, threads, options)
    ret = _solve(solver, s)

    return ret
