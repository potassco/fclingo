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
1. `&sus{lt1 : c1;...;ltn : cn} <> l0` 
2. `&sum{lt1 : c1;...;ltn : cn} <> l0`
3. `&in{lb..ub} =: x`
4. `&max{lt1 : c1;...;ltn : cn} <> l0`
4. `&min{lt1 : c1;...;ltn : cn} <> l0`

where `lti`, `lb`, and `ub` are linear terms,
`ci` is either a conjunction of literals for `i` between 0 and `n`, `x` is the name of a variable and `<>` is either `<=`,`=`,`!=`,`<`,`>`, or `>=`.

To hide and show assignments of specific variables, one can use the directive:
`&show{v1/a1;...;vn/an}`, where `vi` is the name of the function and `ai` is the arity of the function. For instance, the term `x/0` shows the variable named `x` while `price/1` shows all variables of the form `price(<argument>)`. Absence of this directive shows all variables, and `&show{}` hides all variables.

### 1. Sum under strict semantics

The atom in 1. sums up the linear terms for the conditions that are true. If any of the terms is undefined, resulting from a variable being undefined that is contained within, the sum is undefined as well. This results in the atom being false. The atom may be used in the head or in the body.

For example,
```
price(standardframe,15).
price(saddlebag,5).

  selected(standardframe).
{ selected(saddlebag) }.

&sus{price(P)} = V :- selected(P), price(P,V).
&sus{price(P) : selected(P)} = price(total).

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

To see the behavior in presence of undefined variables, consider following example:
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
Now, the price information for the saddlebag is omitted and instead of calculating the total price, we restrict the price to 14.

The call
```
fclingo examples/config_pricelimit_sus.lp 0
```
returns
```
Answer: 1
selected(standardframe) selected(saddlebag) val(price(standardframe),15)
```
The answer with only the standard frame is removed because its price alone is higher than the limit.
However, when the saddlebag is selected, its price value is undefined and therefore the sum under strict semantics returns undefined as well and the price limit is disregarded.

### 2. Aggregates under clingo semantics
The atom 2. also sums up all linear terms in the set, but it removes undefined elements, and therefore always returns a value. It can be used in the head and in the body.

The example `examples/config_optional.lp` behaves identically when we replace `sus` with `sum`.

But the following program:
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
with call
```
fclingo examples/config_pricelimit_sum.lp 0
```
returns
```
UNSATISFIABLE
```
because the undefined variable for the price of the saddlebag is removed, we can detect that the limit is reached, even when it is selected.
## Development

To improve code quality, we run linters, type checkers, and unit tests. The
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

Furthermore, we auto format code using [black]. We provide a [pre-commit][pre]
config to automate this process. It can be set up using the following commands:

```bash
python -m pipx install pre-commit
pre-commit install
```

This blackens the source code whenever `git commit` is used.

There is also a format session for nox. It can be run as follows:

```bash
nox -rs format
nox -rs format -- check
```

The latter command can be used to inspect changes before applying them.

[doc]: https://potassco.org/clingo/python-api/current/
[nox]: https://nox.thea.codes/en/stable/index.html
[pipx]: https://pypa.github.io/pipx/
[pre]: https://pre-commit.com/
[black]: https://black.readthedocs.io/en/stable/
