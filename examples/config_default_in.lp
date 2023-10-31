price(standardframe,15).
default_range(1,2).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V    :- selected(P), price(P,V).
&in{L..U} =: price(P) :- selected(P), not price(P,_), 
                         default_range(L,U).
&sus{price(P) : selected(P)} =: price(total).

#show selected/1.
&show{price/1}.