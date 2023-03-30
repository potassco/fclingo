def(#($\mathit{min}$#)) :- def(#($x_1$)#),#(\dots#),def(#($x_n$)#).
:- not &sum(body){$\mathit{min}$} <= $e_i$.
s :- sum(body){$\mathit{min}$} = $e_i$.
:- not s, def(#($\mathit{min}$#)).
&min$(l)\mathtt{\{}e_1,\dots,e_n\mathtt{\}} \prec k$ :- &sum$(l)\{\mathit{min}\} \prec k$, def(#($\mathit{min}$#)).
&min$(l)\mathtt{\{}e_1,\dots,e_n\mathtt{\}} \prec k$ :- &sum$(l)\{\mathit{min}\} \prec k$.
&sum$(l)\{\mathit{min}\} \prec k$ :- &min$(l)\mathtt{\{}e_1,\dots,e_n\mathtt{\}} \prec k$.
