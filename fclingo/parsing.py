"""
This module contains functions for parsing and normalizing constraints.
"""

from functools import reduce  # pylint: disable=redefined-builtin

import clingo
from clingo import ast

THEORY = """\
#theory htc {
    sum_term {
    -  : 3, unary;
    ** : 2, binary, right;
    *  : 1, binary, left;
    /  : 1, binary, left;
    \\ : 1, binary, left;
    +  : 0, binary, left;
    -  : 0, binary, left
    };
    dom_term {
    -  : 4, unary;
    ** : 3, binary, right;
    *  : 2, binary, left;
    /  : 2, binary, left;
    \\ : 2, binary, left;
    +  : 1, binary, left;
    -  : 1, binary, left;
    .. : 0, binary, left
    };
    &fsum/1 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, any;
    &fmax/1 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, any;
    &fmin/1 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, any;
    &fin/1 : dom_term, {=:}, sum_term, head
}.
"""


class HeadBodyTransformer(ast.Transformer):
    def visit_Literal(self, lit, in_lit=False):
        return lit.update(**self.visit_children(lit, True))

    def visit_TheoryAtom(self, atom, in_lit=False):
        term = atom.term
        if term.name in ["fsum", "fin", "fmax", "fmin"] and not term.arguments:
            loc = "body" if in_lit else "head"
            atom = atom.update(
                term=ast.Function(
                    term.location,
                    term.name,
                    [ast.Function(term.location, loc, [], False)],
                    False,
                )
            )
        return atom
