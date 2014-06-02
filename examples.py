from functools import partial
from apply_rules import *

LegendreP = create_op('Pn', None)
Alpha = create_op('alpha', None)
Beta = create_op('beta', None)

# P_{n+1} = alpha_{n} * P_n - beta_{n} * P_{n - 1}
n = 'n'
n_plus_1 = Add(n, '1')
n_minus_1 = Sub(n, '1')
x = any(1)
term1 = Mul(Alpha(n), LegendreP(n, x))
term2 = Neg(Mul(Beta(n_minus_1), LegendreP(n_minus_1, x)))
rhs = Add(term1, term2)
lhs = LegendreP(n_plus_1, any(1))

legendre_recursion = Rule(lhs, rhs)

expr = LegendreP(n_plus_1, 'y')
print apply_rules(expr, [legendre_recursion])

# Multiplicative identity
mult_ident = Rule(Mul(any(0), '1'),
                  any(0))
mult_ident2 = Rule(Mul('1', any(0)),
                  any(0))

# Addition to Multiplication
add_to_mult = Rule(Add(any(0), any(0)),
                   Mul('2', any(0)))

# d/dx (x) = 1
D = create_op('derivative', lambda x: 0)
expr = D('x', 'x')
self_deriv = Rule(D(any(0), any(0)), '1')
print apply_rules(expr, [self_deriv])


Inde = create_op('independent', None)
inde_deriv = Rule(D(Inde(any(1), any(0)), any(0)), '0')
expr = D(Inde('y', 'x'), 'x')
print apply_rules(expr, [inde_deriv])

# Linearity of derivative
linear_deriv = Rule(D(Add(any(0), any(1)), any(2)),
                    Add(D(any(0), any(2)), D(any(1), any(2))))

# Product rule
product_rule = Rule(D(Mul(any(0), any(1)),
                      any(2)),
                    Add(Mul(any(0),
                            D(any(1), any(2))),
                        Mul(any(1),
                            D(any(0), any(2)))))
expr = D(D(Mul('x', Mul('x', 'x')), 'x'), 'x')
print apply_rules(expr, [product_rule,
                         linear_deriv,
                         self_deriv,
                         add_to_mult,
                         mult_ident,
                         mult_ident2])

