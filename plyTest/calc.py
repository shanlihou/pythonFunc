# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens, states


def p_add(p):
    'expression : expression PLUS term'
    print(p)
    p[0] = p[1] + p[3]


def p_sub(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_factor(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_fact_param(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors


def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    if s == 'q' or s == 'Q':
        break
    result = parser.parse(s)
    print(result)
