"""
Main module providing the application logic.
"""

import sys

import clingo
from clingcon import ClingconTheory
from clingo.ast import ProgramBuilder, parse_files

from fclingo import THEORY
from fclingo.parsing import HeadBodyTransformer

_FALSE = ["0", "no", "false"]
_TRUE = ["1", "yes", "true"]


class AppConfig(object):
    """
    Class for application specific options.
    """

    def __init__(self):
        self.shift_constraints = clingo.Flag(True)
        self.print_aux = clingo.Flag(False)
        self.print_trans = clingo.Flag(False)


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

    def on_model(self, model):
        """
        Report models to the propagator.
        """
        self._theory.on_model(model)

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

    def main(self, prg, files):
        """
        Entry point of the application registering the propagator and
        implementing the standard ground and solve functionality.
        """

        self._theory.register(prg)

        if not files:
            files = ["-"]

        with ProgramBuilder(prg) as bld:
            hbt = HeadBodyTransformer()
            parse_files(
                files,
                lambda ast: self._theory.rewrite_ast(
                    ast, lambda stm: bld.add(hbt.visit(stm))
                ),
            )

        prg.add("base", [], THEORY)
        prg.ground([("base", [])])
        print_conf(prg.configuration, "")
        # translator = Translator(prg, self.config, self._propagator.config)
        # translator.translate(self._propagator)

        prg.solve(on_model=self.on_model, on_statistics=self._theory.on_statistics)


def print_conf(conf, ident):
    for key in conf.keys:
        subconf = getattr(conf, key)
        if isinstance(subconf, clingo.Configuration):
            label = key
            if subconf.is_array:
                label += "[0.." + str(len(subconf)) + "]"
            print("{0}{1} - {2}".format(ident, label, conf.description(key)))
            print_conf(subconf, "  " + ident + label + ".")
        else:
            print(
                "{0}{1}[={2}] - {3}".format(ident, key, subconf, conf.description(key))
            )


if __name__ == "__main__":
    sys.exit(int(clingo.clingo_main(FclingoApp(), sys.argv[1:])))
