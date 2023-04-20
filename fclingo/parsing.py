"""
This module contains functions for parsing and normalizing constraints.
"""

from clingo import ast

PREFIX = "__"
HEAD = "_h"
BODY = "_b"
THEORY = (
    """\
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
    &"""
    + PREFIX
    + """fsum"""
    + BODY
    + """/0 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, body;
    &"""
    + PREFIX
    + """fsum"""
    + HEAD
    + """/0 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, head;
    &"""
    + PREFIX
    + """fmax"""
    + BODY
    + """/0 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, body;
    &"""
    + PREFIX
    + """fmax"""
    + HEAD
    + """/0 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, head;
    &"""
    + PREFIX
    + """fmin"""
    + BODY
    + """/0 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, body;
    &"""
    + PREFIX
    + """fmin"""
    + HEAD
    + """/0 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, head;
    &"""
    + PREFIX
    + """fin"""
    + HEAD
    + """/0 : dom_term, {=:}, sum_term, head
}.
"""
)


class HeadBodyTransformer(ast.Transformer):
    """
    Class for tagging location of theory atoms.
    """

    def visit_Literal(self, lit, in_lit=False):
        """
        Visit all literals.
        """
        return lit.update(**self.visit_children(lit, True))

    def visit_TheoryAtom(self, atom, in_lit=False):
        """
        Rewrite theory atoms depending on location.
        """
        term = atom.term
        if term.name in ["fsum", "fin", "fmax", "fmin"] and not term.arguments:
            loc = BODY if in_lit else HEAD
            atom = atom.update(
                term=ast.Function(
                    term.location,
                    PREFIX + term.name + loc,
                    [],
                    False,
                )
            )
        return atom
