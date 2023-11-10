price(frame,15). part(frame).
price(bag,5).      part(bag).

  selected(frame).
{ selected(bag) }.

&sus{V} = price(P) :- selected(P), price(P,V).
&sus{price(P) : selected(P)} = price(total).

min_price(P) :- &min{price(P') : selected(P')} = price(P),
                part(P).
max_price(P) :- &max{price(P') : selected(P')} = price(P),
                part(P).

#show selected/1.
#show min_price/1.
#show max_price/1.
&show{price/1}.