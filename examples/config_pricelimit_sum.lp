price(frame,15).

pricelimit(14).

  selected(frame).
{ selected(bag) }.

&sum{price(P)} = V :- selected(P), price(P,V).
:- &sum { price(P) : selected(P)  } >= L,
   pricelimit(L).

#show selected/1.
&show{price/1}.