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

    def visit_BinOp(self, node):
        self.visit(node.right)
        self.visit(node.left)
        ctpye = get_command_type(node.op)
        self.ir.add_command(Command(ctpye))

def get_command_type(op: ast.operator) -> CommandType:
    if isinstance(op, ast.Add): return CommandType.ADD
    elif isinstance(op, ast.Sub): return CommandType.SUB
    elif isinstance(op, ast.Mult): return CommandType.MUL
    elif isinstance(op, ast.Div): return CommandType.DIV
    else: raise Exception("Unsupported command "+str(op))
