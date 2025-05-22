import ast
from interpreter.IntermediateRep import IntermediateRep, CommandType, Command


def interpret(source: str) -> IntermediateRep:
    ir = IntermediateRep()
    tree = ast.parse(source)
    visitor = Visitor(ir)
    visitor.visit(tree)
    return ir

class Visitor(ast.NodeVisitor):
    def __init__(self, ir: IntermediateRep):
        self.ir = ir

    def visit_Constant(self, node):
        v = node.value
        self.ir.add_command(Command(CommandType.PUSH, v))

    def visit_FunctionDef(self,node):
        self.generic_visit(node)

    # noinspection PyTypeChecker
    def visit_BinOp(self, node):
        self.visit(node.right)
        self.visit(node.left)
        command_type = operator_type_to_command_type(node.op)
        self.ir.add_command(Command(command_type))
    def visit_BoolOp(self, node):
        if len(node.values) != 2:
            raise Exception("Boolean Op (and/or) with more/less than 2 arguments not currently supported.")
        self.visit(node.values[0])
        self.visit(node.values[1])
        command_type = operator_type_to_command_type(node.op)
        self.ir.add_command(Command(command_type))
    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        # only NOT is supported. Invert (~), UAdd, and USub are not currently supported.
        command_type = operator_type_to_command_type(node.op)
        self.ir.add_command(Command(command_type))

    def visit_Name(self, node):
        # determine if this is a local or a global
        print(node.id)
        self.generic_visit(node)

    def visit_Compare(self, node):
        if len(node.comparators) != 1:
            raise Exception("Compare with more/less than 2 arguments (e.g. 1 < 2 < 3) not currently supported.")
        self.visit(node.comparators[0])
        self.visit(node.left)
        cmp_name = operator_to_compare_name(node.ops[0])
        self.ir.add_command(Command(CommandType.CMP, cmp_name))

    # throwing down some exceptions so we can start to connect the dots on what subset of python we will want to support.
    # function calls and conditionals before I start worrying about this lol.

    def visit_NamedExpr(self, node):
        raise Exception("Named Expr not currently supported.")
    def visit_Lambda(self, node):
        raise Exception("Lambda function is not currently supported.")
    def visit_Dict(self, node):
        raise Exception("Dict is not currently supported.")
    def visit_DictComp(self, node):
        raise Exception("DictComp is not currently supported.")
    def visit_ListComp(self, node):
        raise Exception("ListComp is not currently supported.")
    def visit_SetComp(self, node):
        raise Exception("SetComp is not currently supported.")
    def visit_GeneratorExp(self, node):
        raise Exception("GeneratorExp is not currently supported.")
    def visit_Slice(self, node):
        raise Exception("You got to slice without going through subscript. uh oh.")
    def visit_ImportFrom(self, node):
        raise Exception("imports are not allowed! get out of here with that.")
    def visit_Import(self, node):
        raise Exception("imports are not allowed! get out of here with that.")
    def visit_Invert(self, node):
        raise Exception("bitwise invert (~) is not supported, because this machine does not use bits.")
    def visit_Call(self, node):
        func_name = node.func.id
        # put all args on stack
        node.args.reverse()
        for arg in node.args:
            self.visit(arg)
        count = len(node.args)
        if func_name == "print":
            self.ir.add_command(Command(CommandType.PRINT, count))
        #else.... uh...


def operator_type_to_command_type(op: ast.operator | ast.boolop) -> CommandType:
    if isinstance(op, ast.Add):
        return CommandType.ADD
    elif isinstance(op, ast.Sub):
        return CommandType.SUB
    elif isinstance(op, ast.Mult):
        return CommandType.MUL
    elif isinstance(op, ast.Div):
        return CommandType.DIV
    elif isinstance(op, ast.And):
        return CommandType.AND
    elif isinstance(op, ast.Or):
        return CommandType.OR
    elif isinstance(op, ast.Not):
        return CommandType.NOT
    elif isinstance(op, (ast.Invert, ast.UAdd, ast.USub)):
        raise Exception("Unary operators not currently supported.")
    elif isinstance(op, (ast.MatMult, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor, ast.FloorDiv)):
        raise Exception("Unsupported Command "+str(op))
    else:
        raise Exception("Unsupported command "+str(op))

def operator_to_compare_name(op: ast.cmpop) -> str:
    return str(op.__class__.__name__)
