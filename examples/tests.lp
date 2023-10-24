%*
% Standard GZ unsat
&clc{x}=1 :- &clc{ 1 : a }>= 0.
a :- &clc{x}=1.



% TODO: Weird conditional minimum body example (1 or no stable models?)
&clc{x} = 1.
a :- &min{3; x:a} > 2.


#show a/0.
*%

% Assignment fact
&clc{1} =: x.
&clc{z} =: y.

%*
% Conditional assignment fact

{a}.
&clc{z : a; 1} =: x.
&clc{x} =: y.

#show __def/1.

% Assignment head, body check
{a}.
&clc{1} =: x :- a.
b :- &clc{x} > 0.

% In assignment
&in{0..2} =: x.

% In assignment, vars undef
&in{y..z} =: x.

% In assignment, vars def, unsat

&clc{z} = 1.
&clc{y} = 2.
&in{y..z} =: x.

% In assignment, vars def, sat
&clc{z} = 2.
&clc{y} = 1.
&in{y..z} =: x.

% In assignment, vars def conditional, sat
{a}.
&clc{z} = 2 :- a.
&clc{y} = 1.
&in{y..z} =: x.

% Conditional linear constraint, head
{a}.
&clc{1:a} = x.

% Conditional linear constraint, body
{a}.
&clc{1} = x.
b :- &clc{1:a} < x.

% Minimum assignment fact
&min{3;2;1}=:x.

% Minimum body
&clc{x} = 1.
a :- &min{3;x} < 2.

% Conditional minimum assignment fact
{a}.
&min{3;2;1:a}=:x.

% Conditional minimum body
{b}.
&clc{x} = 1.
a :- &min{3; x:b} < 2.

% Maximum assignment fact
&max{3;2;1}=:x.

% Maximum body
&clc{x} = 3.
a :- &max{1;x} > 2.

% Conditional maximum assignment fact
{a}.
&max{3;2;4:a}=:x.

% Conditional maximum body
{b}.
&clc{x} = 2.
a :- &max{1; x:b} <= 1.

*%
