"""
Main module providing the application logic.
"""

import sys

import clingo
from clingcon import ClingconTheory
from clingo.ast import ProgramBuilder, parse_files

from fclingo import THEORY
from fclingo.parsing import HeadBodyTransformer
from fclingo.translator import AUX, DEF, Translator

MAX_INT = 1073741823
MIN_INT = -1073741823
CSP = "__csp"


class AppConfig:
    """
    Class for application specific options.
    """

    def __init__(self):
        self.print_aux = clingo.Flag(False)
        self.print_trans = clingo.Flag(False)
        self.min_int = MIN_INT
        self.max_int = MAX_INT


class FclingoApp(clingo.Application):
    """
    Application class that can be used with `clingo.clingo_main` to solve AMT
    problems.
    """

    def __init__(self):
        self.program_name = "fclingo"
        self.version = "0.1"
        self.config = AppConfig()
        self._theory = ClingconTheory()
        self._answer = 0

    def on_model(self, model):
        """
        Report models to the propagator.
        """
        self._theory.on_model(model)

    def print_model(self, model, printer):
        shown = [
            str(atom)
            for atom in model.symbols(shown=True)
            if not (atom.name == DEF and len(atom.arguments) == 1)
        ]
        valuation = [
            "val("
            + str(assignment.arguments[0])
            + ","
            + str(assignment.arguments[1])
            + ")"
            for assignment in model.symbols(theory=True)
            if assignment.name == CSP
            and len(assignment.arguments) == 2
            and model.contains(clingo.Function(DEF, [assignment.arguments[0]]))
            and not assignment.arguments[0].name == AUX
        ]
        shown.extend(valuation)
        print(" ".join(shown))
        if self.config.print_aux:
            defs = [
                str(atom)
                for atom in model.symbols(shown=True)
                if atom.name == DEF and len(atom.arguments) == 1
            ]
            auxvars = [
                "val("
                + str(assignment.arguments[0])
                + ","
                + str(assignment.arguments[1])
                + ")"
                for assignment in model.symbols(theory=True)
                if assignment.name == CSP
                and len(assignment.arguments) == 2
                and assignment.arguments[0].name == AUX
            ]
            defs.extend(auxvars)
            print(" ".join(defs))

    def _flag_str(self, flag):
        return "yes" if flag else "no"

    def register_options(self, options):
        """
        Register fclingo related options.
        """

        self._theory.register_options(options)

        group = "Translation Options"
        options.add_flag(
            group,
            "print-auxvars,@2",
            "Print value of auxiliary variables [{}]".format(
                self._flag_str(self.config.print_aux)
            ),
            self.config.print_aux,
        )
        options.add_flag(
            group,
            "print-translation,@2",
            "Print translation [{}]".format(self._flag_str(self.config.print_trans)),
            self.config.print_trans,
        )

    def _on_statistics(self, step, akku):
        self._theory.on_statistics(step, akku)
        return True

    def _read(self, path):
        if path == "-":
            return sys.stdin.read()
        with open(path) as file_:
            return file_.read()

    def main(self, control, files):
        """
        Entry point of the application registering the propagator and
        implementing the standard ground and solve functionality.
        """

        self._theory.register(control)

        if not files:
            files = ["-"]

        with ProgramBuilder(control) as bld:
            hbt = HeadBodyTransformer()
            parse_files(
                files,
                lambda ast: self._theory.rewrite_ast(
                    ast, lambda stm: bld.add(hbt.visit(stm))
                ),
            )

        control.add("base", [], THEORY)
        control.ground([("base", [])])
        translator = Translator(control, self.config)
        translator.translate()

        self._theory.prepare(control)
        control.solve(on_model=self.on_model, on_statistics=self._theory.on_statistics)


def main():
    """
    Main function executing the fclingo application.
    """

    arguments = sys.argv[1:]
    sys.exit(int(clingo.clingo_main(FclingoApp(), arguments)))


if __name__ == "__main__":
    main()
