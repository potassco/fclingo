#theory htc {
    sum_term {
    -  : 3, unary;
    ** : 2, binary, right;
    *  : 1, binary, left;
    /  : 1, binary, left;
    \\ : 1, binary, left;
    +  : 0, binary, left;
    -  : 0, binary, left
    };
    dom_term {
        #($\cdots$#)
    .. : 0, binary, left
    };
    &sum/1 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, any;
    &min/1 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, any;
    &max/1 : sum_term, {<=,=,!=,<,>,>=,=:}, sum_term, any;
    &in/1 : dom_term, {=:}, sum_term, head
}.
