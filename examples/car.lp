#const n = 8.
time(0..n).        step(I,I+1) :- time(I), I < n.

&sum {s(I)+D} =: s(I') :-  acc(D,I'), step(I,I').
&sum {s(I)-D} =: s(I') :- slow(D,I'), step(I,I').

&sum {s(I)} =: s(I') :- not &sum{ s(I') } != s(I), step(I,I').

&sum {p(I)+s(I)} =: p(I') :- step(I,I').

&sum {400000} =: rdpos.
&sum {90000} =: rdlimit.    %  <<< ADDED <<<

fine(I') :- &sum{ p(I) } < rdpos, &sum{ p(I') } >= rdpos, step(I,I'),
            &sum{ s(I') } > rdlimit.

&sum {0} =: p(0).
&sum {80000} =: s(0).

acc(11350,4).
slow(2301,6).
