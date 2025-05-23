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

    def get_pretty_routine(self):
        out = {"instructions": [],
                "name": self.name,
                "localCount": len(self.locals)}
        num = 1
        for command in self.instructions:
            out["instructions"].append(command.get_pretty_object(num, self.name))
            num += 1
        return out

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
        return str(self.routine_stack[0])

    def __repr__(self):
        return str(self.routine_stack[0])

    def get_pretty_object(self):
        out = {"routines": []}
        for routine in reversed(self.routines.values()):
            out["routines"].append(routine.get_pretty_routine())
        return out

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
    PUSHLOCAL = 15
    SETLOCAL = 16
    PUSHGLOBAL = 17
    SETGLOBAL = 18
    #JT = 13,
    #JZ = 14,


command_name_lookup = {
    CommandType.PUSH: "Push",
    CommandType.POP: "Pop",
    CommandType.ADD: "Add",
    CommandType.SUB: "Subtract",
    CommandType.MUL: "Multiply",
    CommandType.DIV: "Divide",
    CommandType.AND: "And",
    CommandType.OR: "Or",
    CommandType.CMP: "Compare",
    CommandType.NOT: "Not",
    CommandType.PRINT: "Print",
    CommandType.JMP: "Jump",
    CommandType.JF: "Jump If False",
    CommandType.ROUND: "Round",
    CommandType.ENTERFRAME: "Start Procedure",
    CommandType.PUSHLOCAL: "Get Local Variable",
    CommandType.SETLOCAL: "Set Local Variable",
    CommandType.PUSHGLOBAL: "Get Global Variable",
    CommandType.SETGLOBAL: "Set Global Variable",
}
details = {
    CommandType.PUSH: [
        "Put the <span class=\"argument\">above value</span> onto <span class=\"stack\">the stack</span>."
    ],
    CommandType.POP: [
        "Take the top of <span class=\"stack\">the stack</span> and place on the discard pile."
    ],
    CommandType.ADD: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "<strong>Add</strong> these two values together and note the answer.",
        "Place this answer on a card, and place on top of <span class=\"stack\">the stack</span>.",
        "Discard A and B."
    ],
    CommandType.SUB: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "<strong>Subtract</strong> these two values (a minus b) and note the answer.",
        "Place this answer on a card, and put on <span class=\"stack\">the stack</span>.",
        "Discard A and B."
    ],
    CommandType.MUL: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "<strong>Multiply</strong> these two values together and note the answer.",
        "Place this answer on a card, and put on <span class=\"stack\">the stack</span>.",
        "Discard A and B."
    ],
    CommandType.DIV: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "<strong>Divide</strong> these two values together and note the answer.",
        "Place this answer on a card, and put on <span class=\"stack\">the stack</span>.",
        "Discard A and B."
    ],
    CommandType.PRINT: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Scream the value of the card on A as loudly as you can.",
        "Discard A"
    ],
    CommandType.NOT: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Negate the value. True becomes false and false becomes true.",
        "Place this negated value on the top of <span class=\"stack\">the stack</span>.",
        "You will have replaced the top of <span class=\"stack\">the stack</span> with it's opposite."
    ],
    CommandType.CMP: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "Compare A and B using the above operator. A is to the left and B is to the right.",
        "Take the result (which should be 'True' or 'False') and place on the top of <span class=\"stack\">the stack</span>."
    ],
    CommandType.JMP: [
        "Instead of flipping to the next instruction. Instead, flip to the <span class=\"argument\">above instruction</span>."
    ],
    CommandType.JF: [
        "Take the top of <span class=\"stack\">the stack</span> and place it on A.",
        "If this value is <strong>True</strong>, a non-zero value, or a non-empty set, discard the value and continue.",
        "If this value is <strong>False</strong>, <strong>None</strong>, or <strong>0</strong>, flip to the  <span class=\"argument\">above instruction number</span>. Do that instruction next.",
        "Discard the tested value on A, if you have not already.",
    ],
    CommandType.ROUND:[
        "Take the top of <span class=\"stack\">the stack</span> and place it on A.",
        "Round the value to the nearest whole number.",
        "Place this new value on top of the stack."
    ],
    CommandType.ENTERFRAME:[
        "Add a new Frame on top the current one, slightly to the right, covering up the locals, but leaving the stack and scratch area visible.",
        "Write down the <span class=\"argument\">current instruction number</span> in the scratch area to remember it. Booklets may get reused and lose their place."
        "For the above number of times, move the top item of the (now previous) stack onto the next available spot in locals.",
        "Find the appropriate instruction booklet with the <span class=\"argument\">above name</span>. Write down the <span class=\"argument\">name</span> of the function in the new frame's scratch area to remember it.",
        "Start following these instructions at instruction 1."
    ],
    CommandType.PUSHLOCAL:[
        "Copy the value at the above <span class=\"argument\">local number</span> and put it onto  <span class=\"stack\">the stack</span>."
    ],
    CommandType.SETLOCAL:[
        "If the above numbered local has a value, discard it.",
       "Take the top of <span class=\"stack\">the stack</span> and place it on the above local value.",
    ],
    CommandType.PUSHGLOBAL:[
        "Copy the value at the above <span class=\"argument\">global number</span> from the heap and put it onto <span class=\"stack\">the stack</span>."
    ],
    CommandType.SETGLOBAL:[
        "If the above numbered global has a value, discard it.",
        "Put the top value of <span class=\"stack\">the stack</span> and place it on the heap, on the above <span class=\"argument\">global number</span>."
    ],
}
argumentLookup = {
    "Eq": "Is Equal To",
    "NotEQ": "Is Not Equal To",
    "Lt": "Less Than",
    "LtE": "Less Than or Equal To",
    "Gt": "Greater Than",
    "GtE": "Greater Than or Equal To",
    "In": "In",
    "NotIn": "Not In",
    "Is": "Is",
    "IsNot": "Is Not",
}


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

    def get_pretty_object(self, num: int, routine_name: str):
        out = {"name": command_name_lookup[self.command],
               "argument": self.get_pretty_argument(self.command, self.argument),
               "number": num,
               "details": details[self.command],
               "routine": routine_name,
               }
        return out

    @staticmethod
    def get_pretty_argument(command, argument):
        if command == CommandType.CMP:
            return argumentLookup[argument]
        elif command == CommandType.PUSH:
            if isinstance(argument, str):
                return '"' + argument + '"'
            return str(argument)
        elif command == CommandType.JMP or command == CommandType.JF:
            return argument+1 # commands start counting at 1 so we have to offset the internal (0 index) to the visual (counting). also: lol, lmao
        else:
            return argument
