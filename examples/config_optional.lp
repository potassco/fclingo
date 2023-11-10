price(frame,15).
price(bag,5).

  selected(frame).
{ selected(bag) }.

&sum{V} = price(P) :- selected(P), price(P,V).
&sum{price(P) : selected(P)} = price(total).

#show selected/1.
&show{price/1}.