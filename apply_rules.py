from memoize import memoized

from collections import namedtuple
from decimal import Decimal, InvalidOperation
from functools import partial
from itertools import combinations
import operator as op

Branch = namedtuple('Branch', 'name, action, args')
def create_branch(name, action, *args):
    return Branch(name, action, list(args))
def print_branch(self):
    arg_list = reduce(lambda x, y: str(x) + ' ' + str(y), self.args)
    return '(' + self.name + ' ' + str(arg_list) + ')'
Branch.__repr__ = print_branch
Branch.__str__ = print_branch

Rule = namedtuple('Rule', 'lhs, rhs')
def print_rule(self):
    return str(self.lhs) + "   --->   " + str(self.rhs)
Rule.__repr__ = print_rule
Rule.__str__ = print_rule

create_op = lambda name, under_op: partial(create_branch, name, under_op)

Sub = create_op('-', op.sub)
Add = create_op('+', op.add)
Mul = create_op('*', op.mul)
# Division is not performed, because I do not want to lose precision
# Using an exact representation like a fractions.Fraction would be
# essentially equivalent to leaving the operation unmodified
Div = create_op('/', None)
Neg = create_op('_', op.neg)

zero = '0'
one = '1'
special_identifier = '__'
any_identifier = special_identifier + 'any'
any = lambda name: any_identifier + str(name)
numeric_identifier = special_identifier + 'numeric'
numeric = lambda name: numeric_identifier + str(name)

class TransformException(Exception): pass

def traverse_args(expr, rules):
    if type(expr) is str:
        return expr
    for idx, a in enumerate(expr.args):
        orig_expr = expr.args[idx]
        expr.args[idx] = apply_rules(orig_expr, rules)
    return expr

def update_history(history, new_expr):
    if str(new_expr) not in history:
        history.append(str(new_expr))
    return new_expr

@memoized
def apply_rules(expr, rules):
    history = [expr]
    while True:
        init_history_size = len(history)
        expr = update_history(history, match_and_transform(expr, rules))
        expr = update_history(history, traverse_args(expr, rules))
        expr = update_history(history, act(expr))
        if len(history) == init_history_size:
            return expr

def match_vars(var, template, any_list):
    # CHECK any
    if template.startswith(any_identifier):
        if any_list.get(template, var) != var:
            return False, {}
        return True, {template: var}

    # Check numeric
    split_template_name = template.split(numeric_identifier)
    if template.startswith(numeric_identifier):
        if not is_number(var):
            return False, {}
        if any_list.get(template, var) != var:
            return False, {}
        return True, {template: var}

    if var != template:
        return False, {}
    return True, {}


def match_args(expr, template, any_list):
    if len(expr.args) != len(template.args):
        return False, {}
    local_any_list = any_list.copy()
    for expr_arg, template_arg in zip(expr.args, template.args):
        is_match, more_any = _match(expr_arg, template_arg, any_list)
        if not is_match:
            return False, {}
        any_list.update(more_any)
    return True, any_list


def _match(expr, template, any_list):
    if type(template) is str:
        return match_vars(expr, template, any_list)
    try:
        if expr.name != template.name:
            return False, {}
    except AttributeError:
        return False, {}
    return match_args(expr, template, any_list)

def match(expr, template):
    return _match(expr, template, {})


def transform_var(template, any_list):
    if not template.startswith(special_identifier):
        return template
    if template not in any_list:
        raise TransformException("Transforming improperly matched expression")
    return any_list[template]


def transform(template, any_list):
    if type(template) is str:
        return transform_var(template, any_list)
    new_args = []
    for template_arg in template.args:
        new_args.append(transform(template_arg, any_list))
    return template._replace(args = new_args)

def match_and_transform(expr, rules):
    for r in rules:
        is_match, any_list = match(expr, r.lhs)
        if not is_match:
            continue
        return transform(r.rhs, any_list)
    return expr

def is_number(val):
    try:
        Decimal(val)
    except (ValueError, InvalidOperation):
        return False
    else:
        return True

def to_decimal(args):
    decimal_args = []
    for arg in args:
        decimal_args.append(Decimal(arg))
    return decimal_args

def act(expr):
    if type(expr) is str:
        return expr
    if expr.action is None:
        return expr

    acted_args = []
    for arg in expr.args:
        acted_args.append(act(arg))

    try:
        decimal_args = to_decimal(acted_args)
    except (InvalidOperation, ValueError):
        return expr._replace(args = acted_args)
    else:
        return str(expr.action(*decimal_args))
