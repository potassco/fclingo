price(frame,15).

  selected(frame).
{ selected(bag) }.

&sus{price(P)} = V :- selected(P), price(P,V).
&sus{price(P)} = 1 :- selected(P), not price(P,_).
&sus{price(P) : selected(P)} =: price(total).

#show selected/1.
&show{price/1}.