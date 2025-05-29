from interpreter.IntermediateRep import CommandType, Routine, Command, IntermediateRep

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
    CommandType.LOADFRAME: "Load Locals",
    CommandType.EXITFRAME: "Exit Procedure",
    CommandType.UNLOADFRAME: "Unload From Frame",
    CommandType.ABORT: "Abort",
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
        "Add a new Frame on top the current one. Note the <span class=\"argument\">name of the function</span> on the frame.",
        "Write down the current instruction number (this one) in the scratch area."
        "Find the instruction booklet for the <span class=\"argument\">above name</span>.",
        "Begin following those instructions at instruction 1."
    ],
    CommandType.LOADFRAME: [
        "For the above number of times, move the top item of the (now previous) stack onto the next available spot in locals.",
    ],
    CommandType.PUSHLOCAL:[
        "Copy the value at the above <span class=\"argument\">local number</span> and put it onto <span class=\"stack\">the stack</span>."
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
    CommandType.UNLOADFRAME:[
        "For the above number of times, move the top item of the stack onto the previous stack.",
    ],
    CommandType.EXITFRAME:[
        "Discard all cards on this frames stack and locals.",
        "Remove the frame and place to the side."
        "Continue the previous frame's instructions at the (noted) instruction number."
    ],
    CommandType.ABORT:[
        "Uh Oh, something has gone wrong! This command means something invalid happened.",
        "No clue what to do next. Abort!"
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


def get_pretty_ir(ir: IntermediateRep, options):
    out = {"routines": []}
    for routine in reversed(ir.routines.values()):
        out["routines"].append(get_pretty_routine(routine))

    if options:
        out["frames"] = []
        for option in range(options["frameCount"]):
            out["frames"].append("frame")
    else:
        out["frames"] = ["frame"]
    return out

def get_pretty_routine(routine: Routine, options=None):
    out = {"instructions": [],
            "name": routine.name,
            "localCount": len(routine.locals)}
    num = 1
    for command in routine.instructions:
        out["instructions"].append(get_pretty_command(command, num, routine.name))
        num += 1
    return out

def get_pretty_command(command: Command, num: int, routine_name: str):
    out = {"name": command_name_lookup[command.command],
               "argument": get_pretty_argument(command.command, command.argument),
               "number": num,
               "details": details[command.command],
               "routine": routine_name,
               }
    return out

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
