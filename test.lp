%*
weight(frame,42).
selected(frame).
selected(basket).

&sus{ weight(P) } = W :- selected(P), weight(P,W).
:- &sus { weight(P) : selected(P)  } >= 40.
:- &sum { weight(P) : selected(P)  } >= 40.
*%

&sum{4*price(P) :: selected(P) : part(P)} <= X :- pricel(X).
