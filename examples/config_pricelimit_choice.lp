part(sportsframe).    price(sportsframe,15).   type(sportsframe,frame).
part(standardframe).  price(standardframe,14). type(standardframe,frame).
part(fancysaddle).    price(fancysaddle,6).    type(fancysaddle,saddle). 
part(standardsaddle). price(standardsaddle,5). type(standardsaddle,saddle). 

&sum{V} = price(P) :- price(P,V).

pricelimit(20).

&sum{price(P) :: selected(P) : part(P)} <= X :- pricelimit(X).
:- selected(P), selected(P'), P<P', 
   type(P,T),   type(P',T).
:- type(_,T), { selected(P) : type(P,T) }0.

#show selected/1.
&show{}.