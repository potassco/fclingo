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
&show{tax/1; deduction(P) : person(P)}.
