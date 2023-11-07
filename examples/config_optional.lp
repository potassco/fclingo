price(standardframe,15).
price(saddlebag,5).

  selected(standardframe).
{ selected(saddlebag) }.

&sum{price(P)} = V :- selected(P), price(P,V).
&sum{price(P) : selected(P)} = price(total).

#show selected/1.
&show{price/1}.