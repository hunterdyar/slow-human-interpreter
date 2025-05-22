from enum import Enum

class IntermediateRep:
    def __init__(self):
        self.routines = []
        self.routines.append([])
    def add_command(self, command):
        self.routines[-1].append(command)

    # todo: make wrapper object for routine that gives routines names and threadability(?) status
    def push_routine(self):
        self.routines.append([])
    def get_top_routine_id(self) -> int:
        return len(self.routines)-1
    def pop_routine(self):
        self.routines.pop()

    def __str__(self):
        return str(self.routines[0])
    def __repr__(self):
        return str(self.routines[0])

class CommandType(Enum):
    PUSH = 1,
    POP = 2,
    ADD = 3,
    SUB = 4,
    MUL = 5,
    DIV = 6,
    AND = 7,
    OR = 8,
    PRINT = 7,

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