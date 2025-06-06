from dis import Instruction

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
        "Put the <span class=\"argument\">argument value</span> onto <span class=\"stack\">the stack</span>."
    ],
    CommandType.POP: [
        "Take the top of <span class=\"stack\">the stack</span> and place on the discard pile."
    ],
    CommandType.ADD: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "<strong>Add</strong> these two values together and put this answer on a card.",
        "Place the answer on top of <span class=\"stack\">the stack</span>.",
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
    CommandType.OR:[
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "If <strong>either</strong> of these values are truthy (True, a non-zero value, or a non-empty set), place 'True' onto <span class=\"stack\">the stack</span>."
        "Otherwise, place 'False' onto <span class=\"stack\">the stack</span>.",
        "Discard A and B."
    ],
    CommandType.AND:[
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "If and only if <strong>both</strong> of these values are truthy (True, a non-zero value, or a non-empty set), place 'True' onto <span class=\"stack\">the stack</span>."
        "Otherwise, place 'False' onto <span class=\"stack\">the stack</span>.",
        "Discard A and B."
    ],
    CommandType.PRINT: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Shout the value of the card on A at an appropriately load volume.",
        "Discard A"
    ],
    CommandType.NOT: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Negate the value. True becomes false and false becomes true.",
        "Place this negated value on the top of <span class=\"stack\">the stack</span>.",
        "Discard A."
    ],
    CommandType.CMP: [
        "Take the top of <span class=\"stack\">the stack</span> and place on A.",
        "Take the top of <span class=\"stack\">the stack</span> and place on B.",
        "Compare A and B using the <span class=\"argument\">provided operation</span>. A is to the left and B is to the right.",
        "Take the result (which should be 'True' or 'False') and place on the top of <span class=\"stack\">the stack</span>."
        "Discard A and B."
    ],
    CommandType.JMP: [
        "Instead of flipping to the next instruction, flip to the instruction at the <span class=\"argument\">provided number</span>. Do that instruction next."
    ],
    CommandType.JF: [
        "Take the top of <span class=\"stack\">the stack</span> and place it on A.",
        "If this value is <strong>True</strong>, a non-zero value, or a non-empty set, discard the value and continue.",
        "If this value is <strong>False</strong>, <strong>None</strong>, or <strong>0</strong>, flip to the instruction at the <span class=\"argument\">provided number</span>. Do that instruction next.",
        "Discard the tested value on A, if you have not already.",
    ],
    CommandType.ROUND:[
        "Take the top of <span class=\"stack\">the stack</span> and place it on A.",
        "Round the value to the nearest whole number.",
        "Place this new value on top of the stack."
    ],
    CommandType.ENTERFRAME:[
        "Write down the next instruction number (this one plus one) in the scratch area."
        "Add a new Frame on top and slightly to the right of the current one. Note the <span class=\"argument\">name of the function</span> on the frame.",
        "Find the instruction booklet for the <span class=\"argument\">above name</span>.",
        "Begin following those instructions at instruction 1."
    ],
    CommandType.LOADFRAME: [
        "For the above number of times, move the top item of the (now previous) <span class=\"stack\">stack</span> onto the next available position in locals.",
    ],
    CommandType.PUSHLOCAL:[
        "Copy the value at the provided <span class=\"argument\">local position number</span> and put it onto <span class=\"stack\">the stack</span>."
    ],
    CommandType.SETLOCAL:[
        "If there is a local at the <span class=\"argument\">provided position number</span>, discard it.",
       "Take the top of <span class=\"stack\">the stack</span> and place it on the <span class=\"argument\">provided position number</span>.",
    ],
    CommandType.PUSHGLOBAL:[
        "Copy the value at the provided <span class=\"argument\">global position</span> from the heap and put it onto <span class=\"stack\">the stack</span>."
    ],
    CommandType.SETGLOBAL:[
        "If the global at the provided positon has a value, discard it.",
        "Put the top value of <span class=\"stack\">the stack</span> and place it on the heap, on the above <span class=\"argument\">global position</span>."
    ],
    CommandType.UNLOADFRAME:[
        "For the  <span class=\"argument\">provided number of times</span>, move the top item of the stack onto the previous stack.",
    ],
    CommandType.EXITFRAME:[
        "Discard all cards on this frames stack and locals.",
        "Remove the frame and place to the side."
        "Continue the previous frame's instructions at the (noted) instruction number."
    ],
    CommandType.ABORT:[
        "Uh Oh, something has gone wrong! This command means something invalid happened.",
        "We can't know what to do next. Abort!"
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

    uses_globals = any([ins
                        for r in ir.routines.values()
                        for ins in r.instructions
                        if ins.command == CommandType.PUSHGLOBAL or ins.command == CommandType.PUSHLOCAL])

    if "only_used_instructions" not in options:
        options["only_used_instructions"] = True

    if options["only_used_instructions"]:
        out["instructions"] = sorted([get_pretty_instruction(ct) for ct in ir.used_instructions], key=lambda k: k["name"])
    else:
        out["instructions"] = sorted([get_pretty_instruction(ct) for ct in CommandType], key=lambda x: x["name"])

    # scan IR for checks
    if uses_globals:
        options["ir_has_globals"] = True

    #turn on and off output settings
    if options:
        if options["inc_frames"] is not None and options["inc_frames"]:
            out["frames"] = []
            for option in range(options["frameCount"]):
                out["frames"].append("frame")

        out["globals"] = []
        if "ir_has_globals" in options and options["ir_has_globals"]:
            out["globals"].append("global")
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

def get_pretty_instruction(command_type: CommandType):
    return {"name": command_name_lookup[command_type],
           "details": details[command_type]
           }


def get_pretty_argument(command, argument):
    if command == CommandType.CMP:
        return argumentLookup[argument]
    elif command == CommandType.PUSH:
        if isinstance(argument, str):
            return '"' + argument + '"'
        return str(argument)
    elif command == CommandType.JMP or command == CommandType.JF:
        return argument+1 # commands start counting at 1 so we have to offset the internal (0 index) to the visual (counting). also: lol, lmao
    elif isinstance(argument, int):
        # prevent 0 from being falsey
        return str(argument)
    else:
        return argument
