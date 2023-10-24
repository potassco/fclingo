%*
% Standard GZ unsat
&sus{x}=1 :- &sus{ 1 : a }>= 0.
a :- &sus{x}=1.



% TODO: Weird conditional minimum body example (1 or no stable models?)
&sus{x} = 1.
a :- &min{3; x:a} > 2.


#show a/0.
*%

% Assignment fact
&sus{1} =: x.
&sus{z} =: y.

%*
% Conditional assignment fact

{a}.
&sus{z : a; 1} =: x.
&sus{x} =: y.

#show __def/1.

% Assignment head, body check
{a}.
&sus{1} =: x :- a.
b :- &sus{x} > 0.

% In assignment
&in{0..2} =: x.

% In assignment, vars undef
&in{y..z} =: x.

% In assignment, vars def, unsat

&sus{z} = 1.
&sus{y} = 2.
&in{y..z} =: x.

% In assignment, vars def, sat
&sus{z} = 2.
&sus{y} = 1.
&in{y..z} =: x.

% In assignment, vars def conditional, sat
{a}.
&sus{z} = 2 :- a.
&sus{y} = 1.
&in{y..z} =: x.

% Conditional linear constraint, head
{a}.
&sus{1:a} = x.

% Conditional linear constraint, body
{a}.
&sus{1} = x.
b :- &sus{1:a} < x.

% Minimum assignment fact
&min{3;2;1}=:x.

% Minimum body
&sus{x} = 1.
a :- &min{3;x} < 2.

% Conditional minimum assignment fact
{a}.
&min{3;2;1:a}=:x.

% Conditional minimum body
{b}.
&sus{x} = 1.
a :- &min{3; x:b} < 2.

% Maximum assignment fact
&max{3;2;1}=:x.

% Maximum body
&sus{x} = 3.
a :- &max{1;x} > 2.

% Conditional maximum assignment fact
{a}.
&max{3;2;4:a}=:x.

% Conditional maximum body
{b}.
&sus{x} = 2.
a :- &max{1; x:b} <= 1.

*%
