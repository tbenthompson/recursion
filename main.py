from collections import namedtuple
from functools import partial

Branch = namedtuple('Branch', ['name', 'args'])
Rule = namedtuple('Rule', ['lhs', 'rhs'])

Minus = partial(Branch, '-')
Plus = partial(Branch, '+')
Mult = partial(Branch, '*')
Div = partial(Branch, '/')

zero = '0'
one = '1'
any_identifier = '__any'
any = lambda name: any_identifier + str(name)

rules = []
rules.append(Rule(Minus([any(0), zero]), any(0)))

class TransformException(Exception): pass

def traverse_args(expr, rules):
    if type(expr) is str:
        return expr
    for idx, a in enumerate(expr.args):
        orig_expr = expr.args[idx]
        expr.args[idx] = apply_rules(orig_expr, rules)
    return expr


def apply_rules(expr, rules):
    done = False
    while not done:
        orig_expr = expr
        expr = match_and_transform(orig_expr, rules)
        expr = traverse_args(expr, rules)
        if expr is orig_expr:
            done = True


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
    if type(expr) is str:
        return match_vars(expr, template)
    if expr.name != template.name:
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
    return Branch(template.name, new_args)


def match_and_transform(expr, rules):
    for r in rules:
        is_match, any_list = match(expr, r.lhs)
        if not is_match:
            continue
        is_match, any_list = match_args(r.lhs.args, expr.args)
    #     new_expr = r.rhs
    # return expr
