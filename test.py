import pytest
from main import *


# MATCHING TESTS
def test_match_vars_true():
    assert(match_vars('a', 'a') == (True, {}))


def test_match_vars_false():
    assert(match_vars('a', 'b') == (False, {}))


def test_match_vars_any():
    assert(match_vars('a', any(1)) == (True, {'1': 'a'}))


def test_match_simple():
    expr = Branch('my_name', [])
    template = Branch('my_name2', [])
    assert(match(expr, template) == (False, {}))


def test_match_simple2():
    expr = Branch('my_name', [])
    template = Branch('my_name', [])
    assert(match(expr, template) == (True, {}))


def test_match_minus():
    expr = Minus(['x', zero])
    template = Minus([any(1), zero])
    assert(match(expr, template) == (True, {'1': 'x'}))


def test_match_deeper():
    expr = Minus([Minus(['x', zero]), 'x'])
    template = Minus([Minus([any(1), zero]), any(2)])
    assert(match(expr, template) == (True, {'1': 'x', '2': 'x'}))


def test_match_deeper2():
    expr = Minus([Minus(['x', zero]), 'x'])
    template = Minus([Minus([any(1), zero]), 'y'])
    assert(match(expr, template) == (False, {}))


# REPLACEMENT TESTS
def test_transform0():
    assert(transform(any(0), {'0': 'y'}) == 'y')


def test_transform1():
    template = Minus([any(0), '0'])
    assert(transform(template, {'0': 'x'}) == Minus(['x', '0']))


def test_transform2():
    template = Minus([any(0), any(10)])
    with pytest.raises(TransformException):
        transform(template, {'0': 'x'}) == Minus(['x', '0'])


def test_match_transform_identity():
    expr = Minus([Minus(['x', zero]), 'x'])
    template = Minus([Minus([any(1), zero]), any(2)])
    matches, any_list = match(expr, template)
    result = transform(template, any_list)
    assert(match(result, expr) == (True, {}))

# APPLY RULES
def test_match_and_transform():
    expr = Minus(['x', '0'])
    rule = Rule(Minus([any(0), '0']), any(0))
    match_and_transform(expr, [rule])
