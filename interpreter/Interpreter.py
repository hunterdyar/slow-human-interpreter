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
        command_type = get_command_type(node.op)
        self.ir.add_command(Command(command_type))
    def visit_BoolOp(self, node):
        if(len(node.values) != 2):
            raise Exception("Boolean Op (and/or) with more/less than 2 arguments not currently supported.")
        self.visit(node.values[0])
        self.visit(node.values[1])
        command_type = get_command_type(node.op)
        self.ir.add_command(Command(command_type))

    def visit_Name(self, node):
        # determine if this is a local or a global
        print(node.id)
        self.generic_visit(node)

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

def get_command_type(op: ast.operator | ast.boolop) -> CommandType:
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
    else:
        raise Exception("Unsupported command "+str(op))
