price(standardframe,15).
price(saddlebag,5).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V :- selected(P), price(P,V).
&sus{price(P) : selected(P)} = price(total).

#show selected/1.
&show{price/1}.