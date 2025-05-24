import ast
from interpreter.IntermediateRep import IntermediateRep, CommandType, Command


def interpret(source: str) -> IntermediateRep:
    ir = IntermediateRep()
    tree = ast.parse(source)
    visitor = Visitor(ir)
    visitor.visit(tree)
    ir.pop_routine()
    return ir

class Visitor(ast.NodeVisitor):
    use_globals_stack = []
    break_command_stack = []
    continue_command_stack = []
    def __init__(self, ir: IntermediateRep):
        self.ir = ir

    def visit_Constant(self, node):
        v = node.value
        self.ir.add_command(Command(CommandType.PUSH, v))

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
        if self.should_use_globals(node.id):
            # push global!
            global_index = self.ir.get_global_index(node.id)
            self.ir.add_command(Command(CommandType.PUSHGLOBAL, global_index))
        else:
            local_index = self.ir.get_local_index(node.id)
            self.ir.add_command(Command(CommandType.PUSHLOCAL, local_index))
        self.generic_visit(node)

    def visit_Assign(self, node):
        # leave value on stack
        self.visit(node.value)

        if len(node.targets) != 1:
            raise Exception("Assignment with more than one target not currently supported.")

        target_expression = node.targets[0]
        if isinstance(target_expression, ast.Name):
            target = target_expression.id
        else:
            raise Exception("Assignment with an unsupported assignee type.")

        if self.should_use_globals(target):
            # push global!
            global_index = self.ir.get_or_set_global_index(target)
            self.ir.add_command(Command(CommandType.SETGLOBAL, global_index))
        else:
            local_index = self.ir.get_or_set_local_index(target)
            self.ir.add_command(Command(CommandType.SETLOCAL, local_index))

    def visit_Compare(self, node):
        if len(node.comparators) != 1:
            raise Exception("Compare with more/less than 2 arguments (e.g. 1 < 2 < 3) not currently supported.")
        self.visit(node.comparators[0])
        self.visit(node.left)
        cmp_name = operator_to_compare_name(node.ops[0])
        self.ir.add_command(Command(CommandType.CMP, cmp_name))
    def visit_If(self, node):
        has_else = len(node.orelse) > 0
        self.visit(node.test)
        cond_jump_index = self.ir.add_command(Command(CommandType.JF, -1))
        skip_else_index = 0
        for expr in node.body:
            self.visit(expr)
        if has_else:
            skip_else_index = self.ir.add_command(Command(CommandType.JMP,-1))
        #set the conditional jump to jump to after the body.

        self.ir.update_argument(cond_jump_index, self.ir.get_top_index() + 1)

        if has_else:
            for expr in node.orelse:
                self.visit(expr)
            ##skip else should skip the else, go to here.
            self.ir.update_argument(skip_else_index, self.ir.get_top_index() + 1)

    def visit_While(self, node):
        self.break_command_stack.append([])
        self.continue_command_stack.append([])
        start_of_loop = self.ir.get_top_index() + 1
        #+1 ? so... this one we DON'T add the +1 to? i confused myself.
        self.visit(node.test)
        cond_jump_index = self.ir.add_command(Command(CommandType.JF, -1))
        for expr in node.body:
            #any break's will get put on the top stack.
            self.visit(expr)
        # and back to the top!
        self.ir.add_command(Command(CommandType.JMP, start_of_loop))
        # or, skip that and back up.
        exit_point = self.ir.get_top_index() + 1

        # update the breaks
        for break_command_index in self.break_command_stack[-1]:
            self.ir.update_argument(break_command_index, exit_point)
        self.break_command_stack.pop()

        # update any continues
        for continue_command_index in self.continue_command_stack[-1]:
            self.ir.update_argument(continue_command_index, start_of_loop)
        self.continue_command_stack.pop()

        self.ir.update_argument(cond_jump_index, exit_point)

    def visit_Break(self, node):
        if len(self.break_command_stack) == 0:
            raise Exception("not inside of a loop where we support break commands. (while?)")
        self.ir.add_command(Command(CommandType.JMP, -1))
        self.break_command_stack[-1].append(self.ir.get_top_index())

    def visit_Continue(self, node):
        if len(self.continue_command_stack) == 0:
            raise Exception("not inside of a loop where we support continue statements. (while?)")
        self.ir.add_command(Command(CommandType.JMP, -1))
        self.continue_command_stack[-1].append(self.ir.get_top_index())
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
    def visit_Global(self, node):
       for name in node.names:
           self.use_globals_stack[-1].add(name)
    ## not a pythonAST, just our own way to move builtins to their own place.
    ## returns true if the node is handled, false if it wasn't.
    def visit_builtin(self, node):
        func_name = node.func.id
        arg_count = len(node.args)
        if func_name == "print":
            node.args.reverse()
            for arg in node.args:
                self.visit(arg)
            self.ir.add_command(Command(CommandType.PRINT, arg_count))
            return True
        if func_name == "round":
            self.visit(node.args[0])
            self.ir.add_command(Command(CommandType.ROUND))
        return False
    def visit_arg(self, node):
        self.visit(node.arg)

    def visit_Call(self, node):
        if self.visit_builtin(node):
            return

        func_name = node.func.id

        # put all args on stack in reverse order.
        node.args.reverse()
        for arg in node.args:
            self.visit(arg)

        ## push a frame of name (get other instruction booklet)
        self.ir.add_command(Command(CommandType.ENTERFRAME, func_name))
        # move from old stack to locals.

    def visit_FunctionDef(self, node):
        self.use_globals_stack.append(set())
        self.ir.push_routine(node.name)

        # read this one out loud! (node.args contains args, defaults, kw_defaults, posonlyargs, etc). normal args, args, contains args objects with annotations and such
        if len(node.args.args) >0:
            for arg in node.args.args:
                self.ir.routine_stack[-1].add_local(arg.arg)
            self.ir.add_command(Command(CommandType.LOADFRAME, len(node.args.args)))
        # python function calls are complicated.
        if node.args.vararg:
            raise Exception("Var argnot supported.")
        if node.args.kwarg:
            raise Exception("Keyword args not supported.")
        if len(node.args.defaults) > 0:
            raise Exception("Default args not supported.")
        if len(node.args.posonlyargs) > 0:
            raise Exception("position only arguments not supported.")

        for expr in node.body:
            self.visit(expr)

        # how do we handle returns? i guess we... don't? returns just pop the frame...
        # can we check if all branches are handled before appending the "leave frame" command if it will never be hit?
        self.ir.add_command(Command(CommandType.EXITFRAME))
        self.ir.pop_routine()
        self.use_globals_stack.pop()

    def visit_Return(self, node):
        self.visit(node.value)
        self.ir.add_command(Command(CommandType.UNLOADFRAME,1))
        self.ir.add_command(Command(CommandType.EXITFRAME))

    def should_use_globals(self, id):
        if len(self.ir.routine_stack) == 1:
            return True
        for scopes in self.use_globals_stack:
            if id in scopes:
                return True
        return False


def operator_type_to_command_type(op: ast.operator | ast.boolop | ast.unaryop) -> CommandType:
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
