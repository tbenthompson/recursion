from derivatives import *

def test_derivatives():
    expr = Dk(Pow('x', '4'), 'x', '2')
    deriv_rules.extend(algebra_rules)
    assert(str(apply_rules(expr, deriv_rules)) == '(* (pow x 2) 12)')
