from memoize import memoized

from collections import namedtuple
from decimal import Decimal, InvalidOperation
from functools import partial
import operator as op

Branch = namedtuple('Branch', 'name, action, args')
def create_branch(name, action, *args):
    return Branch(name, action, list(args))
def print_branch(self):
    arg_list = reduce(lambda x, y: str(x) + ' ' + str(y), self.args)
    return '(' + self.name + ' ' + arg_list + ')'
Branch.__repr__ = print_branch

Rule = namedtuple('Rules', 'lhs, rhs')

Sub = partial(create_branch, '-', op.sub)
Add = partial(create_branch, '+', op.add)
Mul = partial(create_branch, '*', op.mul)
# Division is not performed, because I do not want to lose precision
# Using an exact representation like a fractions.Fraction would be
# essentially equivalent to leaving the operation unmodified
Div = partial(create_branch, '/', None)
Neg = partial(create_branch, '_', op.neg)

zero = '0'
one = '1'
any_identifier = '__any'
any = lambda name: any_identifier + str(name)

class TransformException(Exception): pass

def traverse_args(expr, rules):
    if type(expr) is str:
        return expr
    for idx, a in enumerate(expr.args):
        orig_expr = expr.args[idx]
        expr.args[idx] = apply_rules(orig_expr, rules)
    return expr

def update_history(history, new_expr):
    if new_expr in history:

def apply_rules(expr, rules):
    done = False
    prior_exprs = [expr]
    import ipdb;ipdb.set_trace()
    while not done:
        update_history(history, act(prior_exprs[-1]))
        update_history(history, match_and_transform(prior_exprs[-1], rules))
        update_history(history, traverse_args(prior_exprs[-1], rules))
        if prior_exprs[-1] in prior_exprs[:-3]:
            done = True
    return expr


def match_vars(var, template):
    split_template_name = template.split(any_identifier)
    if len(split_template_name) == 2:
        return True, {split_template_name[1]: var}
    if var != template:
        return False, {}
    return True, {}


def match_args(expr, template):
    if len(expr.args) != len(template.args):
        return False, {}
    any_list = dict()
    for expr_arg, template_arg in zip(expr.args, template.args):
        is_match, more_any = match(expr_arg, template_arg)
        if not is_match:
            return False, {}
        any_list.update(more_any)
    return True, any_list


def match(expr, template):
    if type(template) is str:
        return match_vars(expr, template)
    try:
        if expr.name != template.name:
            return False, {}
    except AttributeError:
        return False, {}
    return match_args(expr, template)


def transform_var(template, any_list):
    split_template_name = template.split(any_identifier)
    if len(split_template_name) != 2:
        return template
    if split_template_name[1] not in any_list:
        raise TransformException("Transforming improperly matched expression")
    return any_list[split_template_name[1]]


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


def to_decimal(args):
    decimal_args = []
    for arg in args:
        decimal_args.append(Decimal(arg))
    return decimal_args

@memoized
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
