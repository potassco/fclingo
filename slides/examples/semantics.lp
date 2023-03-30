a :- &sum{x} = 1.
a :- &sum(body){x} = 1.
&sum(head){ #($e_1,\dots,e_n$#) } #($\prec k$#)
def(x) :- &sum(head){ #($e_1,\dots,e_n$#) } #($\prec k$#).
&sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#)
&sum(#($l$#)){ #($e_1,\dots,e_n$#) } #($\prec k$#).
&sum{x} = 0 :- not def(x).
&sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#)
'&sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#)'
            :- &sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#),
               def(x#($_1$#)),#($\dots$#),def(x#($_n$#)).
{&sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#)}.
c :- &sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#),
     def(x#($_1$#)),#($\dots$#),def(x#($_n$#)).
{&sum(body){ #($e_1,\dots,e_n$#) } #($\prec k$#)}.
a :- '&sum{x} = 1'.
'&sum{x} = 1' :- &sum{x} = 1, def(x).
{&sum{x} = 1}.
&sum{x} = 0 :- not def(x).
a :- c.
c :- &sum{x} = 1, def(x).
{&sum{x} = 1}.
&sum{x} = 0 :- not def(x).
