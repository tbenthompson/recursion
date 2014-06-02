from apply_rules import *

D = create_op('derivative', lambda x: 0)
Dk = create_op('derivative_k', lambda x: 0)
Pow = create_op('pow', lambda x, n: x ** n)

sub_to_add = Rule(Sub(any(0), any(1)), Add(any(0), Neg(any(1))))
add_ident = Rule(Add(any(0), '0'), any(0))
add_numeric = Rule(Add(numeric(0), any(0)), Add(any(0), numeric(0)))
mult_ident = Rule(Mul(any(0), '1'), any(0))
mult_zero = Rule(Mul(any(0), '0'), '0')
mult_numeric = Rule(Mul(numeric(0), any(0)), Mul(any(0), numeric(0)))
mult_assoc = Rule(Mul(Mul(any(0), numeric(0)), numeric(1)),
                   Mul(Mul(numeric(0), numeric(1)), any(0)))
add_mult_assoc = Rule(Add(Mul(any(0), numeric(0)),
                          Mul(any(0), numeric(1))),
                      Mul(any(0), Add(numeric(0), numeric(1))))
add_to_mult = Rule(Add(any(0), any(0)),
                   Mul('2', any(0)))

pow_to_1 = Rule(Pow(any(0), '0'), '1')
pow_to_null_op = Rule(Pow(any(0), '1'), any(0))
# pow_to_mul = Rule(Pow(any(0), numeric(0)), Mul(Pow(any(0), Sub(numeric(0), '1')), any(0)))

algebra_rules = [sub_to_add, add_ident, add_numeric,
                 mult_zero, mult_ident, mult_numeric, mult_assoc,
                 add_mult_assoc, add_to_mult,
                 pow_to_1, pow_to_null_op]

dk_to_d = Rule(Dk(any(0), any(1), numeric(0)), D(Dk(any(0), any(1), Sub(numeric(0), '1')), any(1)))
dk_to_d0 = Rule(Dk(any(0), any(1), '0'), any(0))

numeric_deriv = Rule(D(numeric(0), any(0)), '0')

self_deriv = Rule(D(any(0), any(0)), '1')

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

pow_rule = Rule(D(Pow(any(0), numeric(1)),
                  any(0)),
                Mul(numeric(1),
                    Pow(any(0),
                        Sub(numeric(1), '1'))))

deriv_rules = [dk_to_d0, dk_to_d, numeric_deriv, self_deriv, linear_deriv, product_rule, pow_rule]
