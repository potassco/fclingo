#theory csp {
    var_term  { };
    sum_term {
        #($\cdots$#)
    };
    dom_term {
        #($\cdots$#)
    };
    #(\alert<2->{\&sum/1 : sum\_term, \{<=,=,!=,<,>,>=\}, sum\_term, any;} #)
    &diff/1 : sum_term, {<=}, sum_term, any;
    &minimize/0 : sum_term, directive;
    &maximize/0 : sum_term, directive;
    &show/0 : sum_term, directive;
    &distinct/0 : sum_term, head;
    &dom/0 : dom_term, {=}, var_term, head
}.
