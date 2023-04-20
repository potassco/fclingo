#const n = 8.
time(0..n).        step(I,I+1) :- time(I), I < n.

&fsum {s(I)+D} =: s(I') :-  acc(D,I'), step(I,I').
&fsum {s(I)-D} =: s(I') :- slow(D,I'), step(I,I').

&fsum {s(I)} =: s(I') :- not &fsum{ s(I') } != s(I), step(I,I').

&fsum {p(I)+s(I)} =: p(I') :- step(I,I').

&fsum {400000} =: rdpos.
&fsum {90000} =: rdlimit.    %  <<< ADDED <<<

fine(I') :- &fsum{ p(I) } < rdpos, &fsum{ p(I') } >= rdpos, step(I,I'),
            &fsum{ s(I') } > rdlimit.

&fsum {0} =: p(0).
&fsum {80000} =: s(0).

acc(11350,4).
slow(2301,6).
