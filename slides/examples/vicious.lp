&sum{x} = 1 :- &sum{ 1 : a } >= 0.
a :- &sum{x} = 1.
&sum(head){x} = 1 :- &sum(body){ 1 : a } >= 0.
a :- '&sum(body){x} = 1'.

def(x) :- &sum(head){x} = 1.
'&sum(body){x} = 1' :- def(x), &sum(body){x} = 1.
{&sum(body){x} = 1}.

&sum(head){aux(0)} = 1 :- a.
def(aux(0)) :- &sum(head){aux(0)} = 1.
&sum(head){aux(0)} = 0 :- not a.
def(aux(0)) :- &sum(head){aux(0)} = 0.
{a} :- def(aux(0)).
'&sum(body){aux(0)} >= 0' :- &sum(body){ 1 : a } >= 0.
&sum(body){ 1 : a } >=0   :- '&sum(body){aux(0)} >= 0'.
'&sum(body){aux(0)} >= 0' :- def(aux(0)), &sum(body){aux(0)} >= 0.
{&sum(body){aux(0)} >= 0}.

&sum(head){x} = 0      :- not def(x).
&sum(head){aux(0)} = 0 :- not def(aux(0)).

&sum(head){x} = 1   :- &sum(body){ 1 : a } >= 0.
def(x)              :- &sum(head){x} = 1.
'&sum(body){x} = 1' :- def(x), &sum(body){x} = 1.
a :- '&sum(body){x} = 1'.
&sum(head){aux(0)} = 1    :- a.
'&sum(body){aux(0)} >= 0' :- def(aux(0)), &sum(body){aux(0)} >= 0.
&sum(body){ 1 : a } >=0   :- '&sum(body){aux(0)} >= 0'.

&sum(head){aux(0)} = 1 :- a.
def(aux(0))            :- &sum(head){aux(0)} = 1.
{a} :- def(aux(0)).
 a  :- '&sum(body){x} = 1'.
