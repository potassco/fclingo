price(frame,15).
default_range(1,2).

  selected(frame).
{ selected(bag) }.

&sus{V} = price(P)    :- selected(P), price(P,V).
&in{L..U} =: price(P) :- selected(P), not price(P,_), 
                         default_range(L,U).
&sus{price(P) : selected(P)} =: price(total).

#show selected/1.
&show{price/1}.