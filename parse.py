import ast
import sys
import re

def mkstr(s):
    esc = s.translate({ord('\\'): r'\\', ord('"'): r'\"'})
    return f'"{esc}"'

def string_of_sexp(sexp):
    if type(sexp) is str:
        return sexp

    if type(sexp) is list:
        s = '('
        sep = False
        for child in sexp:
            if sep:
                s += ' '
            s += string_of_sexp(child)
            sep = True
        s += ')'
        return s

    return '#<error>'

def convert_node(node):
    t = type(node)

    if t is str:
        return mkstr(node)

    if t is list:
        return [convert_node(child) for child in node]

    if node is None:
        return 'nil'

    tname = t.__qualname__
    l = [tname]

    if t not in schema:
        return f'#<{tname}>'

    for name in schema[t]:
        l.append(':' + name)
        l.append(convert_node(getattr(node, name)))
    return l

# https://docs.python.org/3/library/ast.html#abstract-grammar
schema = \
    {
        # mod
        ast.Module: ['body'],
        ast.Interactive: ['body'],
        ast.Expression: ['body'],
        ast.Suite: ['body'],

        # stmt
        ast.FunctionDef: ['name', 'args', 'body', 'decorator_list', 'returns'],
        ast.AsyncFunctionDef: ['name', 'args', 'body', 'decorator_list', 'returns'],
        ast.ClassDef: ['name', 'bases', 'keywords', 'body', 'decorator_list'],
        ast.Return: ['value'],
        ast.Delete: ['targets'],
        ast.Assign: ['targets', 'value'],
        ast.AugAssign: ['target', 'op', 'value'],
        ast.AnnAssign: ['target', 'annotation', 'value', 'simple'],
        ast.For: ['target', 'iter', 'body', 'orelse'],
        ast.AsyncFor: ['target', 'iter', 'body', 'orelse'],
        ast.While: ['test', 'body', 'orelse'],
        ast.If: ['test', 'body', 'orelse'],
        ast.With: ['items', 'body'],
        ast.AsyncWith: ['items', 'body'],
        ast.Raise: ['exc', 'cause'],
        ast.Try: ['body', 'handlers', 'orelse', 'finalbody'],
        ast.Assert: ['test', 'msg'],
        ast.Import: ['names'],
        ast.ImportFrom: ['module', 'names', 'level'],
        ast.Global: ['names'],
        ast.Nonlocal: ['names'],
        ast.Expr: ['value'],
        ast.Pass: [],
        ast.Break: [],
        ast.Continue: [],

        # expr
        ast.BoolOp: ['op', 'values'],
        ast.BinOp: ['left', 'op', 'right'],
        ast.UnaryOp: ['op', 'operand'],
        ast.Lambda: ['args', 'body'],
        ast.IfExp: ['test', 'body', 'orelse'],
        ast.Dict: ['keys', 'values'],
        ast.Set: ['elts'],
        ast.ListComp: ['elt', 'generators'],
        ast.SetComp: ['elt', 'generators'],
        ast.DictComp: ['key', 'value', 'generators'],
        ast.GeneratorExp: ['elt', 'generators'],
        ast.Await: ['value'],
        ast.Yield: ['value'],
        ast.YieldFrom: ['value'],
        ast.Compare: ['left', 'ops', 'comparators'],
        ast.Call: ['func', 'args', 'keywords'],
        ast.Num: ['n'],
        ast.Str: ['s'],
        ast.FormattedValue: ['value', 'conversion', 'format_spec'],
        ast.JoinedStr: ['values'],
        ast.Bytes: ['s'],
        ast.NameConstant: ['value'],
        ast.Ellipsis: [],
        ast.Constant: ['value'],
        ast.Attribute: ['value', 'attr', 'ctx'],
        ast.Subscript: ['value', 'slice', 'ctx'],
        ast.Starred: ['value', 'ctx'],
        ast.Name: ['id', 'ctx'],
        ast.List: ['elts', 'ctx'],
        ast.Tuple: ['elts', 'ctx'],

        # expr_context
        ast.Load: [],
        ast.Store: [],
        ast.Del: [],
        ast.AugLoad: [],
        ast.AugStore: [],
        ast.Param: [],

        # slice
        ast.Slice: ['lower', 'upper', 'step'],
        ast.ExtSlice: ['dims'],
        ast.Index: ['value'],

        # boolop
        ast.And: [],
        ast.Or: [],

        # operator
        ast.Sub: [],
        ast.Mult: [],
        ast.MatMult: [],
        ast.Div: [],
        ast.Mod: [],
        ast.Pow: [],
        ast.LShift: [],
        ast.RShift: [],
        ast.BitOr: [],
        ast.BitXor: [],
        ast.BitAnd: [],
        ast.FloorDiv: [],

        # unaryop
        ast.Invert: [],
        ast.Not: [],
        ast.UAdd: [],
        ast.USub: [],

        # cmpop
        ast.Eq: [],
        ast.NotEq: [],
        ast.Lt: [],
        ast.LtE: [],
        ast.Gt: [],
        ast.GtE: [],
        ast.Is: [],
        ast.IsNot: [],
        ast.In: [],
        ast.NotIn: [],

        # comprehension
        ast.comprehension: ['target', 'iter', 'ifs', 'is_async'],

        # excepthandler
        ast.ExceptHandler: ['type', 'name', 'body'],

        # arguments
        ast.arguments: ['args', 'vararg', 'kwonlyargs', 'kw_defaults', 'kwarg',
                        'defaults'],

        # arg
        ast.arg: ['arg', 'annotation'],

        # keyword
        ast.keyword: ['arg', 'value'],

        # alias
        ast.alias: ['name', 'asname'],

        # withitem
        ast.withitem: ['context_expr', 'optional_vars']
    }

def main():
    path = sys.argv[1]
    with open(path) as f:
        text = f.read()
        tree = ast.parse(text, filename=path)
        print(string_of_sexp(convert_node(tree)))

if __name__ == '__main__':
    main()
