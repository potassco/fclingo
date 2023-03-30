&sum{#($\mathit{aux}_i$#)} = #($\mathit{e}_i$#) :- #($\mathit{c}_i$#), def(#($x_1$)#),#(\dots#),def(#($x_n$)#).
&sum{#($\mathit{aux}_i$#)} = #($0_t$#) :- not #($\mathit{c}_i$#).
&sum{#($\mathit{aux}_i$#)} = #($\mathit{e}_i$#) :- #($\mathit{c}_i$#), def(#($\mathit{aux}_i$#)).
&sum{#($\mathit{aux}_i$#)} = #($0_t$#) :- not #($\mathit{c}_i$#), def(#($\mathit{aux}_i$#)).
{#($\mathit{c}_i$#)} :- def(#($\mathit{aux}_i$#)).
#($\mathtt{\&}t(l)\mathtt{\{}\dots,e_1:c_1,\dots,e_n:c_n,\dots\mathtt{\}} \prec k$#) :-
            #($\mathtt{\&}t(l)\mathtt{\{}\dots,\mathit{aux}_1,\dots,\mathit{aux}_n,\dots\mathtt{\}} \prec k$#).
#($\mathtt{\&}t(l)\mathtt{\{}\dots,\mathit{aux}_1,\dots,\mathit{aux}_n,\dots\mathtt{\}} \prec k$#)   :-
            #($\mathtt{\&}t(l)\mathtt{\{}\dots,e_1:c_1,\dots,e_n:c_n,\dots\mathtt{\}} \prec k$#).
