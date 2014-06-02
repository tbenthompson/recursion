import pytest
from main import *

# ACTIONS:
def test_sub():
    expr = Sub('0', '1')
    assert(act(expr) == '-1')


def test_add_sub():
    expr = Add(Sub('0', '1'), '1')
    assert(act(expr) == '0')


def test_add_mult():
    expr = Add(Mul('10', '7.3'), '0.4')
    assert(act(expr) == '73.4')


def test_add_in_subexpr():
    expr = Add(Mul('5', '1.222'),'x')
    assert(act(expr) == Add('6.110','x'))

# MATCHING TESTS
def test_match_vars_true():
    assert(match_vars('a', 'a') == (True, {}))


def test_match_vars_false():
    assert(match_vars('a', 'b') == (False, {}))


def test_match_vars_any():
    assert(match_vars('a', any(1)) == (True, {'1': 'a'}))


def test_match_simple():
    expr = Branch('my_name', None, [])
    template = Branch('my_name2', None, [])
    assert(match(expr, template) == (False, {}))


def test_match_simple2():
    expr = Branch('my_name', None, [])
    template = Branch('my_name', None, [])
    assert(match(expr, template) == (True, {}))


def test_match_minus():
    expr = Sub('x', zero)
    template = Sub(any(1), zero)
    assert(match(expr, template) == (True, {'1': 'x'}))


def test_match_deeper():
    expr = Sub(Sub('x', zero), 'x')
    template = Sub(Sub(any(1), zero), any(2))
    assert(match(expr, template) == (True, {'1': 'x', '2': 'x'}))


def test_match_deeper2():
    expr = Sub(Sub('x', zero), 'x')
    template = Sub(Sub(any(1), zero), 'y')
    assert(match(expr, template) == (False, {}))

def test_match_any_expr():
    expr = Sub(Sub('x', zero), 'x')
    template = Sub(any(0), 'x')
    assert(match(expr, template) == (True, {'0':expr.args[0]}))


# REPLACEMENT TESTS
def test_transform0():
    assert(transform(any(0), {'0': 'y'}) == 'y')


def test_transform1():
    template = Sub(any(0), '0')
    assert(transform(template, {'0': 'x'}) == Sub('x', '0'))


def test_transform2():
    template = Sub(any(0), any(10))
    with pytest.raises(TransformException):
        transform(template, {'0': 'x'}) == Sub('x', '0')


def test_match_transform_identity():
    expr = Sub(Sub('x', zero), 'x')
    template = Sub(Sub(any(1), zero), any(2))
    matches, any_list = match(expr, template)
    result = transform(template, any_list)
    assert(match(result, expr) == (True, {}))

# MATCH AND TRANSFORM
def test_match_and_transform():
    expr = Sub('x', '0')
    rule = Rule(Sub(any(0), '0'), any(0))
    assert(match_and_transform(expr, [rule]) == 'x')


def test_match_and_transform1():
    expr = Sub(Mul('x', '0'), '1')
    rule = Rule(Mul(any(0), '0'), '0')
    # The match and transform is not top level, don't do it
    assert(match_and_transform(expr, [rule]) == expr)


# FULL SCALE!!! APPLY RULES!
def test_apply_rules():
    expr = Sub(Sub('0', 'x'), '1')
    rules = [Rule(Sub(any(0), any(1)), Add(any(0), Neg(any(1))))]
    result = apply_rules(expr, rules)
    print result
    assert(result == Add(Add('0', Neg('x')), Neg('1')))


def test_apply_infinite_stop():
    expr = Sub(Sub('0', 'x'), '1')
    rules = [Rule(Sub(any(0), any(1)), Add(any(0), Neg(any(1)))),
             Rule(Add(any(0), any(1)), Add(any(1), any(0)))]
    assert(apply_rules(expr, rules) == Add(Neg('1'), Add(Neg('x'), '0')))
