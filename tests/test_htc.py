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
    def test_naming(self):
        self.assertEqual(
            solve(
                """\
            &sus{x((),y)}=4.""",
                -10,
                10,
            ),
            [[("x((),y)", 4)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{4}=x(y,()).""",
                -10,
                10,
            ),
            [[("x(y,())", 4)]],
        )

    def test_defined(self):
        self.assertEqual(
            solve(
                """\
            b :- &df{x}.""",
                -10,
                10,
            ),
            [[("x", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            b :- not &df{x}.""",
                -10,
                10,
            ),
            [["b",("x", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            b :- &df{x}.
            &sus{x} = 0.""",
                -10,
                10,
            ),
            [["b",("x", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            b :- &df{x}.
            &sus{y} =: x.""",
                -10,
                10,
            ),
            [[("x", 0),("y", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            b :- &df{x}.
            &sus{y} =: x.
            &sus{y} = 2.""",
                -10,
                10,
            ),
            [["b",("x",2),("y",2)]],
        )

    def test_multiset(self):
        self.assertEqual(
            solve(
                """\
            &sus{1;1}=2.""",
                -10,
                10,
            ),
            [[]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{N:N=1..2; M:M=2..3} = 8.""",
                -10,
                10,
            ),
            [[]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{x;x} = 2*x.""",
                2,
                2,
            ),
            [[("x", 2)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{x(N):N=1..2;x(M):M=2..3} = x(1)+2*x(2)+x(3).""",
                2,
                2,
            ),
            [[("x(1)", 2), ("x(2)", 2), ("x(3)", 2)]],
        )

    def test_conditionals(self):
        self.assertEqual(
            solve(
                """\
            {a}.
            &sus{1:a} = x.
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
            &sus{1} = x.
            b :- &sus{1:a} < x.
            """,
                -10,
                10,
            ),
            [["a", ("x", 1)], ["b", ("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{x}=1 :- &sus{ 1 : a }>= 0.
            a :- &sus{x}=1.
            """,
                -10,
                10,
            ),
            [],
        )
        self.assertEqual(
            solve(
                """\
                      {a;b}.
            &sus{1:a,b;2:a;3:b} = x.
            """,
                -10,
                10,
            ),
            [[("x", 0)], ["a", ("x", 2)], ["a", "b", ("x", 6)], ["b", ("x", 3)]],
        )
        self.assertEqual(
            solve(
                """\
            {a;b}.
            &sus{1:a,b} = x.
            """,
                -10,
                10,
            ),
            [[("x", 0)], ["a", ("x", 0)], ["a", "b", ("x", 1)], ["b", ("x", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            b :- &sus{ v : not b } >= 1.
            """,
                -10,
                10,
            ),
            [[("v", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            {a;b}.
            &sus{1:a, not b} = x.
            """,
                -10,
                10,
            ),
            [[("x", 0)], ["a", ("x", 1)], ["a", "b", ("x", 0)], ["b", ("x", 0)]],
        )

    def test_assignments(self):
        self.assertEqual(
            solve(
                """\
            &sus{1} =: x.
            &sus{z} =: y.
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
            &sus{z : a; 1} =: x.
            &sus{x} =: y.
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
            &sus{1} =: x :- a.
            b :- &sus{x} > 0.
            """,
                -10,
                10,
            ),
            [[("x", 0)], ["a", "b", ("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            &in{0..2} =: x.
            """,
                -10,
                10,
            ),
            [[("x", 0)], [("x", 1)], [("x", 2)]],
        )
        self.assertEqual(
            solve(
                """\
            &in{y..z} =: x.
            """,
                -10,
                10,
            ),
            [[("x", 0), ("y", 0), ("z", 0)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{z} = 1.
            &sus{y} = 2.
            &in{y..z} =: x.
            """,
                -10,
                10,
            ),
            [],
        )
        self.assertEqual(
            solve(
                """\
            &sus{z} = 2.
            &sus{y} = 1.
            &in{y..z} =: x.
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
            &sus{z} = 2 :- a.
            &sus{y} = 1.
            &in{y..z} =: x.
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
            &min{3;2;1}=:x.
            """,
                -10,
                10,
            ),
            [[("x", 1)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{x} = 1.
            a :- &min{3;x} < 2.
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
            &min{3;2;1:a}=:x.
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
            &sus{x} = 1.
            a :- &min{3; x:b} < 2.
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
            a :- &min{1:a} > 0.
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
            &max{3;2;1}=:x.
            """,
                -10,
                10,
            ),
            [[("x", 3)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{x} = 3.
            a :- &max{1;x} > 2.
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
            &max{3;2;4:a}=:x.
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
            &sus{x} = 2.
            a :- &max{1; x:b} <= 1.
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

    def test_choice_sum(self):
        self.assertEqual(
            solve(
                """\
            &sum{ 4 :: a } = 4.
            """,
                -10,
                10,
            ),
            [["a"]],
        )
        self.assertEqual(
            solve(
                """\
            &sum{ x :: a } = 4.
            """,
                -10,
                10,
            ),
            [['a', ('x', 4)]],
        )
        self.assertEqual(
            solve(
                """\
            &sum{ x } = 2.
            &sum{ x :: a } = 4.
            """,
                -10,
                10,
            ),
            [],
        )
        self.assertEqual(
            solve(
                """\
            &sum{ x :: a ; y :: b ; 2} = 4.
            """,
                -2,
                2,
            ),
            [['a', ('x', 2), ('y', 0)], ['a', 'b', ('x', 0), ('y', 2)], ['a', 'b', ('x', 0), ('y', 2)], ['a', 'b', ('x', 1), ('y', 1)], ['a', 'b', ('x', 2), ('y', 0)], ['a', 'b', ('x', 2), ('y', 0)], ['b', ('x', 0), ('y', 2)]],
        )
        self.assertEqual(
            solve(
                """\
            &sum{ 2*x-12 :: a } = 4.
            """,
                -10,
                10,
            ),
            [['a', ('x', 8)]],
        )
        self.assertEqual(
            solve(
                """\
            r(1). {r(2)}.
            &sum{ x(P) :: a(P) : r(P) } = 4.
            """,
                -2,
                2,
            ),
            [['a(1)', 'a(2)', 'r(1)', 'r(2)', ('x(1)', 2), ('x(2)', 2)]],
        )
        self.assertEqual(
            solve(
                """\
            r(1). {r(2)}.
            &sum{ x(P) :: a(P) : r(P) } = 4 :- r(P).
            """,
                -4,
                4,
            ),
            [['a(1)', 'a(2)', 'r(1)', 'r(2)', ('x(1)', 4), ('x(2)', 4)], ['a(1)', 'r(1)', ('x(1)', 4), ('x(2)', 0)]],
        )

    def test_choice_sus(self):
        self.assertEqual(
            solve(
                """\
            &sus{ 4 :: a } = 4.
            """,
                -10,
                10,
            ),
            [["a"]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{ x :: a } = 4.
            """,
                -10,
                10,
            ),
            [['a', ('x', 4)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{ x } = 2.
            &sus{ x :: a } = 4.
            """,
                -10,
                10,
            ),
            [],
        )
        self.assertEqual(
            solve(
                """\
            &sus{ x :: a ; y :: b ; 2} = 4.
            """,
                -2,
                2,
            ),
            [['a', ('x', 2), ('y', 0)], ['a', 'b', ('x', 0), ('y', 2)], ['a', 'b', ('x', 1), ('y', 1)], ['a', 'b', ('x', 2), ('y', 0)], ['b', ('x', 0), ('y', 2)]],
        )
        self.assertEqual(
            solve(
                """\
            &sus{ 2*x-12 :: a } = 4.
            """,
                -10,
                10,
            ),
            [['a', ('x', 8)]],
        )
        self.assertEqual(
            solve(
                """\
            r(1). {r(2)}.
            &sus{ x(P) :: a(P) : r(P) } = 4.
            """,
                -2,
                2,
            ),
            [['a(1)', 'a(2)', 'r(1)', 'r(2)', ('x(1)', 2), ('x(2)', 2)]],
        )
        self.assertEqual(
            solve(
                """\
            r(1). {r(2)}.
            &sus{ x(P) :: a(P) : r(P) } = 4 :- r(P).
            """,
                -4,
                4,
            ),
            [['a(1)', 'a(2)', 'r(1)', 'r(2)', ('x(1)', 4), ('x(2)', 4)], ['a(1)', 'r(1)', ('x(1)', 4), ('x(2)', 0)]],
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

            &sus{ 0 } =: deduction(P) :- person(P), not deduction(P,_,_).
            &in{ L..H } =: deduction(P) :- deduction(P,L,H).
            &sus{ T } =: rate(P) :- lives(P,R), income(P,I),
                                    T = #max{ T' : rate(R,L,T'), I>=L}.

            &sus{ I*rate(P)-100*deduction(P) } =: 100*tax(P) :- income(P,I).
            &sus{ tax(P) : lives(P,R) } =: total(R) :- region(R).
            &min{ tax(P) : person(P) } =: min.
            &max{ tax(P) : person(P) } =: max.
            min_taxes(P) :- &min{ tax(P') : person(P') } = tax(P), person(P).
            max_taxes(P) :- &max{ tax(P') : person(P') } = tax(P), person(P).

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

            &sus {s(I)+D} =: s(I') :-  acc(D,I'), step(I,I').
            &sus {s(I)-D} =: s(I') :- slow(D,I'), step(I,I').

            &sus {s(I)} =: s(I') :- not &sus{ s(I') } != s(I), step(I,I').

            def_s(I) :- time(I), &sus{s(I); -s(I)}=0.

            &sus {p(I)+s(I)} =: p(I') :- def_s(I), step(I,I').

            &sus {400000} =: rdpos.
            &sus {90000} =: rdlimit.    %  <<< ADDED <<<

            fine(I') :- &sus{ p(I) } < rdpos, &sus{ p(I') } >= rdpos, step(I,I'),
                        &sus{ s(I') } > rdlimit.

            &sus {0} =: p(0).
            &sus {80000} =: s(0).

            acc(11350,4).
            slow(2301,6).
            """,
                -1000000,
                1000000,
            ),
            SOL_CAR,
        )
