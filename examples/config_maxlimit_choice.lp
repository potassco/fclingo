part(sportsframe).    price(sportsframe,15).   type(sportsframe,frame).
part(standardframe).  price(standardframe,14). type(frame,frame).
part(fancysaddle).    price(fancysaddle,6).    type(fancysaddle,saddle). 
part(standardsaddle). price(standardsaddle,5). type(standardsaddle,saddle). 

&sum{price(P)} = V :- price(P,V).

maxlimit(14).

&max{price(P) :: selected(P) : part(P)} <= X :- maxlimit(X).
:- selected(P), selected(P'), P<P', 
   type(P,T),   type(P',T).
:- type(_,T), { selected(P) : type(P,T) }0.

#show selected/1.
&show{}.