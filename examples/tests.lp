%*
% Application taxes
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

&sum{ 0 } =: deduction(P) :- person(P), not deduction(P,_,_).
&in{ L..H } =: deduction(P) :- deduction(P,L,H).
&sum{ T } =: rate(P) :- lives(P,R), income(P,I),
                        T = #max{ T' : rate(R,L,T'), I>=L}.

&sum{ I*rate(P)-100*deduction(P) } =: 100*tax(P) :- income(P,I).
&sum{ tax(P) : lives(P,R) } =: total(R) :- region(R).
&min{ tax(P) : person(P) } =: min.
&max{ tax(P) : person(P) } =: max.
min_taxes(P) :- &min{ tax(P') : person(P') } = tax(P), person(P).
max_taxes(P) :- &max{ tax(P') : person(P') } = tax(P), person(P).

#show lives/2.
#show min_taxes/1.
#show max_taxes/1.

% Standard GZ unsat (theory atom bug)
&sum{x}=1 :- &sum{ 1 : a }>= 0.
a :- &sum{x}=1.

% TODO: Weird conditional minimum body example (1 or no stable models?)
&sum{x} = 1.
a :- &min{3; x:a} > 2.

#show a/0.

% Assignment fact
&sum{1} =: x.
&sum{z} =: y.

% Conditional assignment fact
{a}.
&sum{z : a; 1} =: x.
&sum{x} =: y.

% Assignment head, body check
{a}.
&sum{1} =: x :- a.
b :- &sum{x} > 0.

% In assignment
&in{0..2} =: x.

% In assignment, vars undef
&in{y..z} =: x.

% In assignment, vars def, unsat
&sum{z} = 1.
&sum{y} = 2.
&in{y..z} =: x.

% In assignment, vars def, sat
&sum{z} = 2.
&sum{y} = 1.
&in{y..z} =: x.

% In assignment, vars def conditional, sat
{a}.
&sum{z} = 2 :- a.
&sum{y} = 1.
&in{y..z} =: x.

% Conditional linear constraint, head
{a}.
&sum{1:a} = x.

% Conditional linear constraint, body
{a}.
&sum{1} = x.
b :- &sum{1:a} < x.

% Minimum assignment fact
&min{3;2;1}=:x.

% Minimum body
&sum{x} = 1.
a :- &min{3;x} < 2.

% Conditional minimum assignment fact
{a}.
&min{3;2;1:a}=:x.

% Conditional minimum body
{b}.
&sum{x} = 1.
a :- &min{3; x:b} < 2.

% Maximum assignment fact
&max{3;2;1}=:x.

% Maximum body
&sum{x} = 3.
a :- &max{1;x} > 2.

% Conditional maximum assignment fact
{a}.
&max{3;2;4:a}=:x.

% Conditional maximum body
{b}.
&sum{x} = 2.
a :- &max{1; x:b} <= 1.


*%
