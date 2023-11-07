# fclingo

fclingo is a solver for ASP modulo conditional linear constraints with founded variables.

## Installation

```shell
pip install . -r requirements.txt
```

## Usage

fclingo accepts as input [clingo](https://github.com/potassco/clingo) rules enriched with founded conditional linear constraints. It relies on the constraint answer set programming (CASP) solver [clingcon](https://github.com/potassco/clingo) into whose language a fclingo program is translated. fclingo's two main advantages are foundedness of the integer variables and aggregates over integer variables. The former allows variables to be undefined and only assume a value if a reason for that value can be derived. This differs to the behavior of CASP, where variables are always defined and in absence of any constraint to a variable, all possible values are enumerated. The latter generalizes ASP aggregates to contain integer variables that are not subject to grounding.
The answer sets to fclingo programs contain atoms `val(x,v)`, where `x` is a variable occurring in the program and `v` is the integer value of the variable in the answer set. The absence of such an atom means the variable is undefined.

Atoms representing the constraints may have the following form:
1. `&sum{lt1 : c1;...;ltn : cn} <> l0`
2. `&sus{lt1 : c1;...;ltn : cn} <> l0` 
3. `&in{lb..ub} =: x`
4. `&df{x}`
5. `&min{lt1 : c1;...;ltn : cn} <> l0`
6. `&max{lt1 : c1;...;ltn : cn} <> l0`

where `lti`, `lb`, and `ub` are linear terms,
`ci` is a conjunction of literals for `i` between 0 and `n`, `x` is the name of a variable and `<>` is either `<=`,`=`,`!=`,`<`,`>`, or `>=`.

To hide and show assignments of specific variables, one can use the directive `&show{v1/a1;...;vn/an}`, where `vi` is the name of the function and `ai` is the arity of the function. For instance, the term `x/0` shows the variable named `x` while `price/1` shows all variables of the form `price(<argument>)`. Absence of this directive shows all variables, and `&show{}` hides all variables.

### 1. Sum under clingo semantics
The atom in 1. sums up all linear terms in the set. It can be seen as a generalization of clingo sum aggregates as it similarly removes undefined elements, and therefore always returns a value. It can be used in the head and in the body.

For example,
```
price(standardframe,15).
price(saddlebag,5).

  selected(standardframe).
{ selected(saddlebag) }.

&sum{price(P)} = V :- selected(P), price(P,V).
&sum{price(P) : selected(P)} = price(total).

#show selected/1.
&show{price/1}.
```
This program configures a bike with a standard frame that has an optional saddlebag. For both the standard frame and the optional saddlebag prices are provided, stored in integer variables and then summed up to get the total price.

Executing 
```shell
fclingo examples/config_optional.lp
```
yields the answer sets
```
Answer: 1
selected(standardframe) val(price(total),15) val(price(standardframe),15)
Answer: 2
selected(standardframe) selected(saddlebag) val(price(saddlebag),5) val(price(total),20) val(price(standardframe),15)
```
As expected, we have two answer sets. The first does not select the optional saddlebag and calculates the total price as 15, same as the price of the standard frame. The second selects the saddlebag and increases the total price to 20.

To see the behavior in presence of undefined variables, consider following example
```
price(standardframe,15).

pricelimit(14).

  selected(standardframe).
{ selected(saddlebag) }.

&sum{price(P)} = V :- selected(P), price(P,V).
:- &sum { price(P) : selected(P)  } >= L,
   pricelimit(L).

#show selected/1.
&show{price/1}.
```
Now, the price of the saddlebag is omitted and instead of calculating the total price, we restrict the sum over the individual prices to be 14.
The call
```
fclingo examples/config_pricelimit_sum.lp 0
```
returns
```
UNSATISFIABLE
```
Even if the price for the saddlebag is undefined, the constraint detects that the price limit is breached since the undefined variable is removed from the set.

### 2. Sum under strict semantics

The atom in 2. sums up the linear terms for the conditions that are true. In contrast to 1., if any of the terms is undefined, resulting from a variable being undefined that is contained within, the sum is undefined as well. This results in the atom being false. The atom may be used in the head or in the body.

The example `examples/config_optional.lp` behaves identically when we replace `sus` with `sum`.

Different behavior arises for the price limit.
```
price(standardframe,15).

pricelimit(14).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V :- selected(P), price(P,V).
:- &sus { price(P) : selected(P)  } >= L,
   pricelimit(L).

#show selected/1.
&show{price/1}.
```

The call
```
fclingo examples/config_pricelimit_sus.lp 0
```
now returns
```
Answer: 1
selected(standardframe) selected(saddlebag) val(price(standardframe),15)
```
The answer with only the standard frame is removed because its price alone is higher than the limit.
However, when the saddlebag is selected, its price value is undefined and therefore the sum under strict semantics returns undefined as well and the price limit is disregarded.

### 3. Assignments

The atom in 3. is a directional assignment of a value between linear terms `lb` and `ub` to the variable `x`. It may only be used in the head of a rule. Only if `lb` and `ub` are defined, `x` will receive a value in between `lb` and `ub`. Note that this is different from using equality to assign a value. For instance, the fact `&sus{y}=x.` would allow `y` as well as `x` to be defined and take on arbitrary values such that `x` and `y` are equal, while `&in{y..y}=:x.` requires some other rule to define `y` and if that is not the case, `x` remains undefined. If no range is required, one can also use the strict sum and write `&sus{lt}=:x`, where `lt` is a linear term and `x` an integer variable.

For instance, take program
```
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
```

Here, we assign selected parts that are missing the price information a default within a certain range. 
Calling 

```
fclingo examples/config_default_in.lp 0
```
results in
```
Answer: 1
selected(standardframe) val(price(total),15) val(price(standardframe),15)
Answer: 2
selected(standardframe) selected(saddlebag) val(price(total),16) val(price(standardframe),15) val(price(saddlebag),1)
Answer: 3
selected(standardframe) selected(saddlebag) val(price(total),17) val(price(standardframe),15) val(price(saddlebag),2)
```
were in answers 2 and 3, the two possible defaults for the missing price information of the selected saddlebag is used.

### 4. Defined

The atom in 4. may be used in the body to reason about whether a given variable `x` is defined or not. This is useful for instance to provide defaults or detect errors if a certain variable does not have a value but should.

For instance, program
```
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
```
first tries to calculate the price, and if this calculation has a defined outcome, it is assigned to the total price. If not, a default price is used.

Calling
```
fclingo examples/config_default_in.lp 0
```
yields the intended two answer sets
```
Answer: 1
selected(standardframe) selected(saddlebag) val(price(standardframe),15) val(price(total),20)
Answer: 2
selected(standardframe) val(price(standardframe),15) val(price(total),15)
```
where Answer 1 makes use of the default because the price of the saddlebag is missing and therefore the total price may not be calculated.

### 5./6. Minimum and maximum aggregates

Atoms in 5. and 6. determine the minimum and maximum among linear terms in the set that have a defined value, respectively. They may be used in the head as well as in the body.

```
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
```
Here, atoms `min_price/1` and `max_price/1` query what selected part has the minimum and the maximum value, respectively. 

The call
```
fclingo config_minmax_price.lp 0
```
yields
```
Answer: 1
selected(standardframe) min_price(standardframe) max_price(standardframe) val(price(total),15) val(price(standardframe),15)
Answer: 2
selected(standardframe) selected(saddlebag) min_price(saddlebag) max_price(standardframe) val(price(total),20) val(price(standardframe),15) val(price(saddlebag),5)
```
When the saddlebag is not selected, the standard frame has the minimum and maximum price. In the second answer, we see that the saddlebag has the minimum price among selected parts, while the standard frame's price is the maximum.

### Choices
Similarly to the language of clingo, fclingo allows for choice rules in the head of a rule. Choices have the following form:
```
&fun{ lt1 :: ca1 : c1;...ltn :: can : cn} <> lt0
```
where `fun` is either `sum`, `sus`, `min`, or `max`,
`lti` are linear terms, `cai` are regular atoms that may be chosen, and
`ci` are conjunctions of literals for `i` between 0 and `n`,
and `<>` is either `<=`,`=`,`!=`,`<`,`>`, or `>=`.

As an example program
```
part(sportsframe).    price(sportsframe,15).   type(sportsframe,frame).
part(standardframe).  price(standardframe,14). type(standardframe,frame).
part(fancysaddle).    price(fancysaddle,6).    type(fancysaddle,saddle). 
part(standardsaddle). price(standardsaddle,5). type(standardsaddle,saddle). 

&sum{price(P)} = V :- price(P,V).

pricelimit(20).

&sum{price(P) :: selected(P) : part(P)} <= X :- pricelimit(X).
:- selected(P), selected(P'), P<P', 
   type(P,T),   type(P',T).
:- type(_,T), { selected(P) : type(P,T) }0.

#show selected/1.
&show{}.
```
Our parts database for the bike is now more involved. Each part has a price and a type. It contains two choices for the frame, either standard or sports, and two choices for the saddle, either standard or fancy. As before, we store the prices in integer values and we have a price limit. 

Using a choice, we can now express in one line, that we may freely select parts such that the price limit is respected. We further restrict solutions such that every type has something selected and there is only one option per type selected.

Calling
```
fclingo examples/config_pricelimit_choice.lp 0
```
outputs the three possible answers
```
Answer: 1
selected(standardframe) selected(fancysaddle)
Answer: 2
selected(standardframe) selected(standardsaddle)
Answer: 3
selected(sportsframe) selected(standardsaddle)
```
One has enough money to either combine the standard frame with the fancy saddle or the standard one, but if one opts for the sportsframe, the only viable choice is the standard saddle.

For another example, we replace from the program above the choice rule and the price limit with
```
maxlimit(14).

&max{price(P) :: selected(P) : part(P)} <= X :- maxlimit(X).
```
Now we restrict the maximum price an individual part may have.

Calling
```
fclingo examples/config_pricelimit_choice.lp 0
```
gives us
```
Answer: 1
selected(standardframe) selected(standardsaddle)
Answer: 2
selected(standardframe) selected(fancysaddle)
```
The new program removes all combinations using the sports frame since this part violates the maximum allowed spending for one part.

## Development

To improve code quality, we run linters, and unit tests. The
tools can be run using [nox]. We recommend installing nox using [pipx] to have
it available globally:

```bash
python -m pip install pipx
python -m pipx install nox
nox
```

Note that `nox --no-install -r` can be used to speed up subsequent runs. It
avoids recreating virtual environments. For example, to run the unit tests
without recreating the corresponding environment and installing packages each
time, you can use

```bash
nox --no-install -rs test
```
There is also a format session for nox. It can be run as follows:

```bash
nox -rs format
nox -rs format -- check
```

The latter command can be used to inspect changes before applying them.

[doc]: https://potassco.org/clingo/python-api/current/
[nox]: https://nox.thea.codes/en/stable/index.html
[pipx]: https://pypa.github.io/pipx/
