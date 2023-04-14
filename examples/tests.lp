
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

&fsum{ 0 } =: deduction(P) :- person(P), not deduction(P,_,_).
&fin{ L..H } =: deduction(P) :- deduction(P,L,H).
&fsum{ T } =: rate(P) :- lives(P,R), income(P,I),
                        T = #max{ T' : rate(R,L,T'), I>=L}.

&fsum{ I*rate(P)-100*deduction(P) } =: 100*tax(P) :- income(P,I).
&fsum{ tax(P) : lives(P,R) } =: total(R) :- region(R).
&fmin{ tax(P) : person(P) } =: fmin.
&fmax{ tax(P) : person(P) } =: fmax.
min_taxes(P) :- &fmin{ tax(P') : person(P') } = tax(P), person(P).
max_taxes(P) :- &fmax{ tax(P') : person(P') } = tax(P), person(P).

#show lives/2.
#show min_taxes/1.
#show max_taxes/1.
&show{tax/1;deduction/1;rate/1}.
%*
% Standard GZ unsat (theory atom bug)
&fsum{x}=1 :- &fsum{ 1 : a }>= 0.
a :- &fsum{x}=1.


% TODO: Weird conditional minimum body example (1 or no stable models?)
&fsum{x} = 1.
a :- &fmin{3; x:a} > 2.


#show a/0.


% Assignment fact
&fsum{1} =: x.
&fsum{z} =: y.

% Conditional assignment fact

{a}.
&fsum{z : a; 1} =: x.
&fsum{x} =: y.

#show __def/1.

% Assignment head, body check
{a}.
&fsum{1} =: x :- a.
b :- &fsum{x} > 0.

% In assignment
&fin{0..2} =: x.

% In assignment, vars undef
&fin{y..z} =: x.

% In assignment, vars def, unsat

&fsum{z} = 1.
&fsum{y} = 2.
&fin{y..z} =: x.

% In assignment, vars def, sat
&fsum{z} = 2.
&fsum{y} = 1.
&fin{y..z} =: x.

% In assignment, vars def conditional, sat
{a}.
&fsum{z} = 2 :- a.
&fsum{y} = 1.
&fin{y..z} =: x.

% Conditional linear constraint, head
{a}.
&fsum{1:a} = x.

% Conditional linear constraint, body
{a}.
&fsum{1} = x.
b :- &fsum{1:a} < x.

% Minimum assignment fact
&fmin{3;2;1}=:x.

% Minimum body
&fsum{x} = 1.
a :- &fmin{3;x} < 2.

% Conditional minimum assignment fact
{a}.
&fmin{3;2;1:a}=:x.

% Conditional minimum body
{b}.
&fsum{x} = 1.
a :- &fmin{3; x:b} < 2.

% Maximum assignment fact
&fmax{3;2;1}=:x.

% Maximum body
&fsum{x} = 3.
a :- &fmax{1;x} > 2.

% Conditional maximum assignment fact
{a}.
&fmax{3;2;4:a}=:x.

% Conditional maximum body
{b}.
&fsum{x} = 2.
a :- &fmax{1; x:b} <= 1.

*%
