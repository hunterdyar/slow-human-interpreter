from enum import Enum

class Routine:
    def __init__(self, name):
        self.name = name
        self.instructions = []
        self.argumentCount = 0
        self.locals = {}
    def has_local(self, id) -> (bool, int):
        if self.locals.keys().__contains__(id):
            return self.locals[id]
        else:
            return False
    def add_local(self, local_id):
        self.locals[local_id] = len(self.locals)
        return self.locals[local_id]

    def get_local_index(self, local_id):
        return self.locals[local_id]

    def get_or_set_local_index(self, local_id):
        if local_id in self.locals:
            return self.locals[local_id]
        else:
            return self.add_local(local_id)

    def __str__(self):
        return "Routine(%s)" % self.name + "\n" + str(len(self.instructions))
    def __repr__(self):
        return str(self)

class IntermediateRep:
    def __init__(self):
        self.routines = {}
        self.routine_stack = []
        self.routine_stack.append(Routine("main"))

    def add_command(self, command):
        self.routine_stack[-1].instructions.append(command)
        return len(self.routine_stack[-1].instructions) - 1

    def update_argument(self, command_index, new_argument):
        self.routine_stack[-1].instructions[command_index].argument = new_argument

    def get_top_index(self):
        return len(self.routine_stack[-1].instructions) - 1

    # todo: make wrapper object for routine that gives routines names and threadability(?) status
    def push_routine(self, routine_id):
        self.routine_stack.append(Routine(routine_id))

    def get_top_routine_id(self) -> int:
        return len(self.routine_stack) - 1

    def pop_routine(self):
        # save our defined temp area stack of definitions to a lookup table.
        # todo: this odd code is a reflection of how i wrote this, and could be refactored such that IntermediateRep doens't have any temporary objects floating around.
        # like how the break and local stuff is over in Interpreter...
        r = self.routine_stack.pop()
        self.routines[r.name] = r

    def get_routine(self, routine_id):
        for r in self.routine_stack:
            if r.routine_id == routine_id:
                return r
        raise Exception("Routine "+ routine_id +" not found")

    def __str__(self):
        if len(self.routine_stack) == 0:
            return str(self.routines["main"])
        else:
            return str(self.routine_stack[0])

    def __repr__(self):
        return str(self)

    def get_global_index(self, id):
        return self.routine_stack[0].get_local_index(id)
    def get_local_index(self, id):
        # python uses globals, not punch-through locals...right?
        if id in self.routine_stack[-1].locals:
            return self.routine_stack[-1].locals[id]

        raise Exception("Variable name "+ id +" not found")

    def get_or_set_global_index(self, id):
        return self.routine_stack[0].get_or_set_local_index(id)

    def get_or_set_local_index(self, id):
        # python uses globals, not punch-through locals...right?
        return self.routine_stack[-1].get_or_set_local_index(id)


class CommandType(Enum):

    PRINT = 0,
    PUSH = 1,
    POP = 2,
    ADD = 3,
    SUB = 4,
    MUL = 5,
    DIV = 6,
    AND = 7,
    OR = 8,
    CMP = 9
    NOT = 10
    JMP = 11,
    JF = 12,
    ROUND = 13
    ENTERFRAME = 14
    LOADFRAME = 15
    PUSHLOCAL = 16
    SETLOCAL = 17
    PUSHGLOBAL = 18
    SETGLOBAL = 19
    EXITFRAME = 20
    UNLOADFRAME = 21
    ABORT = 22
    #JT = 13,
    #JZ = 14,



class Command:
    def __init__(self, command: CommandType, argument=None):
        self.command = command
        self.argument = argument

    def __str__(self):
        if self.argument is None:
            return str(self.command)
        else:
            return str(self.command) + str(self.argument)

    def __repr__(self):
        return str(self.command)


