price(standardframe,15).
price(saddlebag,5).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V :- selected(P), price(P,V).

#show selected/1.
&show{price/1}.