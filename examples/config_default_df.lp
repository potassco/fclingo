price(standardframe,15).

default_price(20).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V    :- selected(P), price(P,V).
&sus{price(P) : selected(P)} =: calc_price(total).

&sus{price(total)} = calc_price(total) :- &df{calc_price(total)}.
&sus{price(total)} = D                 :- not &df{calc_price(total)},
                                          default_price(D).

#show selected/1.
&show{price/1}.