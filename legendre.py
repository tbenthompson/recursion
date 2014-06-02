from apply_rules import *
from derivatives import *

LegendreP = create_op('Pn', None)
Alpha = create_op('alpha', None)
Beta = create_op('beta', None)

# P_{n+1} = alpha_{n} * x * P_n - beta_{n} * P_{n - 1}
legendre_recursion = lambda n: Rule(LegendreP(Add(n, '1'), any(0)),
                          Add(Mul(Mul(Alpha(n), any(0)), LegendreP(n, any(0))),
                              Neg(Mul(Beta(n), LegendreP(Sub(n, '1'), any(0))))))

# (1 / alpha_{n}) * P_{n+1} + (beta_n / alpha_n) * P_{n - 1} = x * P_n
legendre_inv_recursion = \
    lambda n: Rule(Mul(any(0), LegendreP(n, any(0))),
                   Add(Mul(Div('1', Alpha(n)), LegendreP(Add(n, '1'), any(0))),
                       Mul(Div(Beta(n), Alpha(n)), LegendreP(Sub(n, '1'), any(0)))))
nice_form = lambda n: Rule(Mul(Mul(any(0), any(1)), LegendreP(n, any(1))),
                           Mul(any(0), Mul(any(1), LegendreP(n, any(1)))))

expr = LegendreP(Add('n', '1'), 'x')
recursed = apply_rules(expr, [legendre_recursion('n')])
print recursed
inv_recursed = apply_rules(recursed, [legendre_inv_recursion('n'), nice_form('n')])
print inv_recursed
inv_recursed_simplified = apply_rules(recursed, algebra_rules)
print inv_recursed_simplified


# # Integral from neg 1 to 1
# IntM11 = create_op('intm11', lambda x: 2 * x)
# int_leg_0 = Rule(IntM11(LegendreP('0', any(0)), any(0)), '2')
# int_leg_gt_0 = Rule(IntM11(LegendreP(any(0), any(1)), any(1)), '0')
#
# legendre_rules = [int_leg_0, int_leg_gt_0]
#
# print apply_rules(IntM11(LegendreP('n', 'x'), 'x'), legendre_rules)

# logxy = Log(Sub(x, y))
