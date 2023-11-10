price(frame,15).


  selected(frame).
{ selected(bag) }.

&sus{V} = price(P) :- selected(P), price(P,V).
&sus{price(P) : selected(P)} =: price(total).

#show selected/1.
&show{price/1}.