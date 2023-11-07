price(standardframe,15). part(standardframe).
price(saddlebag,5).      part(saddlebag).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V :- selected(P), price(P,V).
&sus{price(P) : selected(P)} = price(total).

min_price(P) :- &min{price(P') : selected(P')} = price(P),
                part(P).
max_price(P) :- &max{price(P') : selected(P')} = price(P),
                part(P).

#show selected/1.
#show min_price/1.
#show max_price/1.
&show{price/1}.