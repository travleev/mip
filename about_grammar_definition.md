---
title: 
tags: [grammar, tatsu, MCNP input parser]
---

# Grammar for arithmetical expression with 2 operations
Description of cell geometry uses two binary operators, union and intersection
(the unitary complement operator can be avoided by transforming expression to
which it applies). Manual specifies explicitly order of operations and the use
of parentheses to control it. Thus, geometry description of a cell has the same
syntax as arithmetical expression consisting of two types of operators (the
only difference is that one of the operators, intersection, is implicit and
represented by a zero or more spaces). 

Example of a simple calculator parser implemented in `tatsu` refers to the
grammer defined in `yacc`. This reference does not provide explanations of how
the grammar is defined, whether this is the only grammar that describes
arithmetics expression and how it should be modified in case of additional
operations. 

To start with, consider an expression representing the sum of 3 elements,

```
    a + b + c        (1)
```

This expression is evaluated from left to right, which explicitly can be
written using parentheses:

```
    ((a + b) + c)
```
Here one can see that the original expression is split by the last operator,
whose left operand is another expression and the right operand is a value. The
left operand is an expression consting of the operand, whose left and right
operands are simple values.  The recursive grammar for this case can be:

```
    start = expr $; 

    expr = 
        | expr '+' value     # 1-st option
        | value;             # 2-nd option
```

This grammar stays that `expr` can be the '+' operation, which left operand
is another expression or a value, and the right operand is a value.

The fact that in the first option operands are of differnet type, `expr` and
`value`, allows to parse the original expression unambigouosly. If the
1-st option were ```expr = expr '+' expr```, it would match the sum in several
ways:

```
    a + b '+' c
    a '+' b + c
```

The second option in definition of `expr` simply states that a single value is
also an expression. This also provides the recursion terminal.

Now consider another expression, where both operations are used:

```
    a + b * c + d                  (2)
```
Since '*' is evalueated first, this expression is equal to

```
    a + (b*c) + d
```
Here we see that expression is again a sum of elements, but in this case, one
of operands can be the result of multiplication. Since the result of
multiplication can appear as the left of right operand of '*', the 1-st option
of the above grammar must be modified by introducing a new type, `mult`:

```
    expr = 
        | expr '+' mult
        | mult;

    mult = 
        | mult '*' value
        | value; 
```
When this grammar applied to expression (2):

```
    expr: 'a + b * c'          '+'  'd'
    expr: 'a' '+' 'b * c'
    mult:         'b' '*' 'c'
```

The order of operators, parsed with the grammar, depends on the first assumption
on the form of the expression. In the grammar above, it is first assumed that the
expression is a sum, '+', which operand is another expression. The operands
will be evaluated first, consequently, the '+' operator will be evaluated after
the others. 

Parentheses are added to the grammar by allowing `expr`, `mult` or `value` be
circumscribed with '(' and ')' and specifying that the obtained form is, again,
an expression `expr` (maybe not directly). Let consider the following expression:

```
    a + b * (c + d)                            (3)
```
This expression cannot be parsed with the above parser, since the right operand
of '+' does not match to the form ```mult '*' value```, since it contains ```(c
+ d)``` on the place of ```value```. Let us modify the ```value``` rule to have
two forms:


```
    value = 
        | '(' @:expr ')'
        | number;

    variable = /[a-z]/;
```

in this grammar, the value rule is not a terminal one (as it was considered
before),  but can be another expression in parentheses or a variable (which is
the terminal rule). Such modified grammar parses expression (3) in the
following steps:

```
    'a' '+' 'b * (c + d)'
    'b' '*' '(c + d)'
    'c' '+' 'd'
```

It is interesting to note that the parentheses in the expression (3) that we
considered to guess the grammar, are necessary. What happens if we would
consider another expression, where parentheses are optional? Let consider
expression 

```
    a + (b*c) + d                                (4)
```
This expression can be matched by the unmodified version of ```expr``` and
splitted into ```a + (b*c)```, ```+``` and ```d```.  The left operand does not
match to the original ```expr`` and we could assume another modification to
account for parentheses:

```
    mult = 
        | '(' @:expr ')'
        | mult '*' value
        | value;
```
where ```value``` is the terminal rule. Expression (4) is parsed into the
following chunks:

```
    'a + (b * c)' '+' 'd'
    'a' '+' '(b * c)'
    'b' '*' 'c'
``` 
While expression (3) cannot be parsed, while 'b * (c + d)' does not match to
any option of ```mult```. 

```
    'a' '+' 'b * (c + d)'
```
        
