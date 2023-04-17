"""
Test cases for HTc to Clingcon translation
"""

import unittest

from tests import solve

# pylint: disable=missing-docstring, line-too-long

SOL_TAXES = [
    [
        "lives(mary,germany)",
        "lives(paul,germany)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10000),
        ("deduction(paul)", 0),
        ("max", 32000),
        ("min", 15000),
        ("rate(mary)", 35),
        ("rate(paul)", 25),
        ("tax(mary)", 32000),
        ("tax(paul)", 15000),
        ("total(germany)", 47000),
        ("total(luxemburg)", 0),
    ],
    [
        "lives(mary,germany)",
        "lives(paul,germany)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10001),
        ("deduction(paul)", 0),
        ("max", 31999),
        ("min", 15000),
        ("rate(mary)", 35),
        ("rate(paul)", 25),
        ("tax(mary)", 31999),
        ("tax(paul)", 15000),
        ("total(germany)", 46999),
        ("total(luxemburg)", 0),
    ],
    [
        "lives(mary,germany)",
        "lives(paul,luxemburg)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10000),
        ("deduction(paul)", 0),
        ("max", 32000),
        ("min", 13800),
        ("rate(mary)", 35),
        ("rate(paul)", 23),
        ("tax(mary)", 32000),
        ("tax(paul)", 13800),
        ("total(germany)", 32000),
        ("total(luxemburg)", 13800),
    ],
    [
        "lives(mary,germany)",
        "lives(paul,luxemburg)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10001),
        ("deduction(paul)", 0),
        ("max", 31999),
        ("min", 13800),
        ("rate(mary)", 35),
        ("rate(paul)", 23),
        ("tax(mary)", 31999),
        ("tax(paul)", 13800),
        ("total(germany)", 31999),
        ("total(luxemburg)", 13800),
    ],
    [
        "lives(mary,luxemburg)",
        "lives(paul,germany)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10000),
        ("deduction(paul)", 0),
        ("max", 26000),
        ("min", 15000),
        ("rate(mary)", 30),
        ("rate(paul)", 25),
        ("tax(mary)", 26000),
        ("tax(paul)", 15000),
        ("total(germany)", 15000),
        ("total(luxemburg)", 26000),
    ],
    [
        "lives(mary,luxemburg)",
        "lives(paul,germany)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10001),
        ("deduction(paul)", 0),
        ("max", 25999),
        ("min", 15000),
        ("rate(mary)", 30),
        ("rate(paul)", 25),
        ("tax(mary)", 25999),
        ("tax(paul)", 15000),
        ("total(germany)", 15000),
        ("total(luxemburg)", 25999),
    ],
    [
        "lives(mary,luxemburg)",
        "lives(paul,luxemburg)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10000),
        ("deduction(paul)", 0),
        ("max", 26000),
        ("min", 13800),
        ("rate(mary)", 30),
        ("rate(paul)", 23),
        ("tax(mary)", 26000),
        ("tax(paul)", 13800),
        ("total(germany)", 0),
        ("total(luxemburg)", 39800),
    ],
    [
        "lives(mary,luxemburg)",
        "lives(paul,luxemburg)",
        "max_taxes(mary)",
        "min_taxes(paul)",
        ("deduction(mary)", 10001),
        ("deduction(paul)", 0),
        ("max", 25999),
        ("min", 13800),
        ("rate(mary)", 30),
        ("rate(paul)", 23),
        ("tax(mary)", 25999),
        ("tax(paul)", 13800),
        ("total(germany)", 0),
        ("total(luxemburg)", 39799),
    ],
]

SOL_CAR = [
    [
        "acc(11350,4)",
        "def_s(0)",
        "def_s(1)",
        "def_s(2)",
        "def_s(3)",
        "def_s(4)",
        "def_s(5)",
        "def_s(6)",
        "def_s(7)",
        "def_s(8)",
        "fine(5)",
        "slow(2301,6)",
        "step(0,1)",
        "step(1,2)",
        "step(2,3)",
        "step(3,4)",
        "step(4,5)",
        "step(5,6)",
        "step(6,7)",
        "step(7,8)",
        "time(0)",
        "time(1)",
        "time(2)",
        "time(3)",
        "time(4)",
        "time(5)",
        "time(6)",
        "time(7)",
        "time(8)",
        ("p(0)", 0),
        ("p(1)", 80000),
        ("p(2)", 160000),
        ("p(3)", 240000),
        ("p(4)", 320000),
        ("p(5)", 411350),
        ("p(6)", 502700),
        ("p(7)", 591749),
        ("p(8)", 680798),
        ("rdlimit", 90000),
        ("rdpos", 400000),
        ("s(0)", 80000),
        ("s(1)", 80000),
        ("s(2)", 80000),
        ("s(3)", 80000),
        ("s(4)", 91350),
        ("s(5)", 91350),
        ("s(6)", 89049),
        ("s(7)", 89049),
        ("s(8)", 89049),
    ]
]


class TestMain(unittest.TestCase):
    def test_conditionals(self):
        self.assertEqual(
            solve(
                """\
            {a}.
            &fsum{1:a} = x.
            """,
                -10,
                10,
            ),
            [[("x", 0)], ["a", ("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            {a}.
            &fsum{1} = x.
            b :- &fsum{1:a} < x.
            """,
                -10,
                10,
            ),
            [["a", ("x", 1)], ["b", ("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            &fsum{x}=1 :- &fsum{ 1 : a }>= 0.
            a :- &fsum{x}=1.
            """,
                -10,
                10,
            ),
            [],
        )

    def test_assignments(self):
        self.assertEqual(
            solve(
                """\
            &fsum{1} =: x.
            &fsum{z} =: y.
            """,
                -10,
                10,
            ),
            [[("x", 1), ("y", 0), ("z", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            {a}.
            &fsum{z : a; 1} =: x.
            &fsum{x} =: y.
            """,
                -10,
                10,
            ),
            [[("x", 1), ("y", 1), ("z", 0)], ["a", ("x", 0), ("y", 0), ("z", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            {a}.
            &fsum{1} =: x :- a.
            b :- &fsum{x} > 0.
            """,
                -10,
                10,
            ),
            [[("x", 0)], ["a", "b", ("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            &fin{0..2} =: x.
            """,
                -10,
                10,
            ),
            [[("x", 0)], [("x", 1)], [("x", 2)]],
        )
        self.assertEqual(
            solve(
                """\
            &fin{y..z} =: x.
            """,
                -10,
                10,
            ),
            [[("x", 0), ("y", 0), ("z", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            &fsum{z} = 1.
            &fsum{y} = 2.
            &fin{y..z} =: x.
            """,
                -10,
                10,
            ),
            [],
        )
        self.assertEqual(
            solve(
                """\
            &fsum{z} = 2.
            &fsum{y} = 1.
            &fin{y..z} =: x.
            """,
                -10,
                10,
            ),
            [
                [("x", 1), ("y", 1), ("z", 2)],
                [("x", 2), ("y", 1), ("z", 2)],
            ],
        )
        self.assertEqual(
            solve(
                """\
            {a}.
            &fsum{z} = 2 :- a.
            &fsum{y} = 1.
            &fin{y..z} =: x.
            """,
                -10,
                10,
            ),
            [
                [("x", 0), ("y", 1), ("z", 0)],
                ["a", ("x", 1), ("y", 1), ("z", 2)],
                ["a", ("x", 2), ("y", 1), ("z", 2)],
            ],
        )

    def test_min(self):
        self.assertEqual(
            solve(
                """\
            &fmin{3;2;1}=:x.
            """,
                -10,
                10,
            ),
            [[("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            &fsum{x} = 1.
            a :- &fmin{3;x} < 2.
            """,
                -10,
                10,
            ),
            [["a", ("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            {a}.
            &fmin{3;2;1:a}=:x.
            """,
                -10,
                10,
            ),
            [
                [
                    ("x", 2),
                ],
                [
                    "a",
                    ("x", 1),
                ],
            ],
        )
        self.assertEqual(
            solve(
                """\
            {b}.
            &fsum{x} = 1.
            a :- &fmin{3; x:b} < 2.
            """,
                -10,
                10,
            ),
            [
                [
                    ("x", 1),
                ],
                [
                    "a",
                    "b",
                    ("x", 1),
                ],
            ],
        )
        self.assertEqual(
            solve(
                """\
            a :- &fmin{1:a} > 0.
            """,
                -10,
                10,
            ),
            [],
        )

    def test_max(self):
        self.assertEqual(
            solve(
                """\
            &fmax{3;2;1}=:x.
            """,
                -10,
                10,
            ),
            [[("x", 3)]],
        )
        self.assertEqual(
            solve(
                """\
            &fsum{x} = 3.
            a :- &fmax{1;x} > 2.
            """,
                -10,
                10,
            ),
            [["a", ("x", 3)]],
        )
        self.assertEqual(
            solve(
                """\
            {a}.
            &fmax{3;2;4:a}=:x.
            """,
                -10,
                10,
            ),
            [
                [
                    ("x", 3),
                ],
                [
                    "a",
                    ("x", 4),
                ],
            ],
        )
        self.assertEqual(
            solve(
                """\
            {b}.
            &fsum{x} = 2.
            a :- &fmax{1; x:b} <= 1.
            """,
                -10,
                10,
            ),
            [
                [
                    "a",
                    ("x", 2),
                ],
                [
                    "b",
                    ("x", 2),
                ],
            ],
        )

    def test_taxes(self):
        answers = solve(
            """\
            person(paul;mary).
            region(luxemburg;germany).
            rate(germany,  25000, 15).
            rate(germany,  50000, 25).
            rate(germany, 100000, 35).
            rate(luxemburg,  38700, 14).
            rate(luxemburg,  58000, 23).
            rate(luxemburg,  96700, 30).
            income(paul,   60000).
            income(mary,  120000).
            deduction(mary, 10000, 10001).

            1 { lives(P,R) : region(R) } 1 :- person(P).

            &fsum{ 0 } =: deduction(P) :- person(P), not deduction(P,_,_).
            &fin{ L..H } =: deduction(P) :- deduction(P,L,H).
            &fsum{ T } =: rate(P) :- lives(P,R), income(P,I),
                                    T = #max{ T' : rate(R,L,T'), I>=L}.

            &fsum{ I*rate(P)-100*deduction(P) } =: 100*tax(P) :- income(P,I).
            &fsum{ tax(P) : lives(P,R) } =: total(R) :- region(R).
            &fmin{ tax(P) : person(P) } =: min.
            &fmax{ tax(P) : person(P) } =: max.
            min_taxes(P) :- &fmin{ tax(P') : person(P') } = tax(P), person(P).
            max_taxes(P) :- &fmax{ tax(P') : person(P') } = tax(P), person(P).

            #show lives/2.
            #show min_taxes/1.
            #show max_taxes/1.
            """,
            -100000,
            100000,
        )
        self.assertEqual(
            answers,
            SOL_TAXES,
        )

    def test_car(self):
        self.assertEqual(
            solve(
                """\
            #const n = 8.
            time(0..n).        step(I,I+1) :- time(I), I < n.

            &fsum {s(I)+D} =: s(I') :-  acc(D,I'), step(I,I').
            &fsum {s(I)-D} =: s(I') :- slow(D,I'), step(I,I').

            &fsum {s(I)} =: s(I') :- not &fsum{ s(I') } != s(I), step(I,I').

            def_s(I) :- time(I), &fsum{s(I); -s(I)}=0.

            &fsum {p(I)+s(I)} =: p(I') :- def_s(I), step(I,I').

            &fsum {400000} =: rdpos.
            &fsum {90000} =: rdlimit.    %  <<< ADDED <<<

            fine(I') :- &fsum{ p(I) } < rdpos, &fsum{ p(I') } >= rdpos, step(I,I'),
                        &fsum{ s(I') } > rdlimit.

            &fsum {0} =: p(0).
            &fsum {80000} =: s(0).

            acc(11350,4).
            slow(2301,6).
            """,
                -1000000,
                1000000,
            ),
            SOL_CAR,
        )
