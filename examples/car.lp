#const n = 8.
time(0..n).        step(I,I+1) :- time(I), I < n.

&sus {s(I)+D} =: s(I') :-  acc(D,I'), step(I,I').
&sus {s(I)-D} =: s(I') :- slow(D,I'), step(I,I').

&sus {s(I)} =: s(I') :- not &sus{ s(I') } != s(I), step(I,I').

&sus {p(I)+s(I)} =: p(I') :- step(I,I').

&sus {400000} =: rdpos.
&sus {90000} =: rdlimit.    %  <<< ADDED <<<

fine(I') :- &sus{ p(I) } < rdpos, &sus{ p(I') } >= rdpos, step(I,I'),
            &sus{ s(I') } > rdlimit.

&sus {0} =: p(0).
&sus {80000} =: s(0).

acc(11350,4).
slow(2301,6).
