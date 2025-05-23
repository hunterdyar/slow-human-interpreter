from enum import Enum


class IntermediateRep:
    def __init__(self):
        self.routines = []
        self.routines.append([])

    def add_command(self, command):
        self.routines[-1].append(command)
        return len(self.routines[-1]) - 1

    def update_argument(self, command_index, new_argument):
        self.routines[-1][command_index].argument = new_argument

    def get_top_index(self):
        return len(self.routines[-1]) - 1

    # todo: make wrapper object for routine that gives routines names and threadability(?) status
    def push_routine(self):
        self.routines.append([])

    def get_top_routine_id(self) -> int:
        return len(self.routines) - 1

    def pop_routine(self):
        self.routines.pop()

    def __str__(self):
        return str(self.routines[0])

    def __repr__(self):
        return str(self.routines[0])

    def get_pretty_object(self):
        out = {"instructions": []}
        num = 1
        for command in self.routines[0]:
            out["instructions"].append(command.get_pretty_object(num))
            num += 1

        return out


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
}
details = {
    CommandType.PUSH: [
        "Put the above value onto the stack."
    ],
    CommandType.POP: [
        "Take the top of the stack and place on the discard pile."
    ],
    CommandType.ADD: [
        "Take the top of the stack and place on A.",
        "Take the top of the stack and place on B.",
        "Add these two values together and note the answer.",
        "Place this answer on a card, and put on the stack.",
        "Discard A and B."
    ],
    CommandType.SUB: [
        "Take the top of the stack and place on A.",
        "Take the top of the stack and place on B.",
        "Subtract these two values together and note the answer.",
        "Place this answer on a card, and put on the stack.",
        "Discard A and B."
    ],
    CommandType.MUL: [
        "Take the top of the stack and place on A.",
        "Take the top of the stack and place on B.",
        "Multiply these two values together and note the answer.",
        "Place this answer on a card, and put on the stack.",
        "Discard A and B."
    ],
    CommandType.DIV: [
        "Take the top of the stack and place on A.",
        "Take the top of the stack and place on B.",
        "<strong>Divide</strong> these two values together and note the answer.",
        "Place this answer on a card, and put on the stack.",
        "Discard A and B."
    ],
    CommandType.PRINT: [
        "Take the top of the stack and place on A.",
        "Scream the value of the card on A as loudly as you can.",
        "Discard A"
    ],
    CommandType.NOT: [
        "Take the top of the stack and place on A.",
        "Negate the value. True becomes false and false becomes true.",
        "Place this negated value on the top of the stack.",
        "You will have replaced the top of the stack with it's opposite."
    ],
    CommandType.CMP: [
        "Take the top of the stack and place on A.",
        "Take the top of the stack and place on B.",
        "Compare A and B using the above operator. A is to the left and B is to the right.",
        "Take the result (which should be 'True' or 'False') and place on the top of the stack."
    ],
    CommandType.JMP: [
        "Turn the instructions to the above instruction number. (You will do that instruction next)."
    ],
    CommandType.JF: [
        "Take the top of the stack and place it on A.",
        "If this value is True, discard the value and continue.",
        "If this value is False, None, or 0, turn the instructions to the above instruction number. Do that instruction next.",
        "Discard the tested value on A, if you have not already.",
    ]
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

    def get_pretty_object(self, num: int):
        out = {"name": command_name_lookup[self.command],
               "argument": self.get_pretty_argument(self.command, self.argument),
               "number": num,
               "details": details[self.command]
               }
        return out

    @staticmethod
    def get_pretty_argument(command, argument):
        if command == CommandType.CMP:
            return argumentLookup[argument]
        if command == CommandType.PUSH:
            if isinstance(argument, str):
                return '"' + argument + '"'
            return str(argument)
        else:
            return argument
