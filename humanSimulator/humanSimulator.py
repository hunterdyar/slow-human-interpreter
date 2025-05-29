from interpreter.IntermediateRep import CommandType

class HumanSimulator:
    def __init__(self, intermediate, use_implicit_return = False):
        self.ir = intermediate
        self.stack = []
        self.globals = []
        self.output = ""
        self.maxFameCount = 0
        self.frames = [Frame(self, self.ir.routines["main"])]
        ## main frame should always return value
        self.frames[0].implicit_return = use_implicit_return
    def execute(self):
        self.maxFameCount = 1
        return self.frames[0].execute()
    def execute_frame(self, frame):
        self.frames.append(frame)
        if len(self.frames) > self.maxFameCount:
            self.maxFameCount = len(self.frames)
        res= self.frames[-1].execute()
        self.frames.pop()
        return res

class Frame:
    def __init__(self, sim, routine):
        self.sim = sim
        self.routine = routine
        self.instr = 0
        self.locals = []
        self.return_val = None
        # mark the position of the stack. The paper version does this by having the stack start to the side of the current stack, or by inserting a marker (that's what we will do for the sim)
        self.starting_stack_len = len(self.sim.stack)
        self.implicit_return = False

    def execute(self):
        loop_count = 0

        while self.instr < len(self.routine.instructions):
            instruction = self.routine.instructions[self.instr]
            loop_count += 1
            if len(self.sim.stack) > 512:
                raise Exception("Stack Overflow Exception")
            if loop_count > 100000:
                raise Exception("Execution limit exceeded (infinite loop?)")

            match instruction.command:
                case CommandType.PUSH:
                    self.sim.stack.append(self.routine.instructions[self.instr].argument)
                case CommandType.POP:
                    self.sim.stack.pop()
                case CommandType.ADD:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    addition = left + right
                    self.sim.stack.append(addition)
                case CommandType.SUB:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    sub = left - right
                    self.sim.stack.append(sub)
                case CommandType.MUL:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    mul = left * right
                    self.sim.stack.append(mul)
                case CommandType.DIV:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    division = left / right
                    self.sim.stack.append(division)
                case CommandType.AND:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    division = left and right
                    self.sim.stack.append(division)
                case CommandType.OR:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    division = left or right
                    self.sim.stack.append(division)
                case CommandType.CMP:
                    left = self.sim.stack.pop()
                    right = self.sim.stack.pop()
                    answer = False
                    match instruction.argument:
                        case "Eq":
                            answer = left == right
                        case "NotEq":
                            answer = left != right
                        case  "Lt":
                            answer = left < right
                        case  "LtE":
                            answer = left <= right
                        case  "Gt":
                            answer = left > right
                        case  "GtE":
                            answer = left >= right
                        case  "Is":
                            answer = left is right
                        case  "IsNot":
                            answer = left is not right
                        case  "NotIn":
                            answer = left not in right
                        case  "In":
                            answer = left in right
                    self.sim.stack.append(answer)
                case CommandType.NOT:
                    left = self.sim.stack.pop()
                    left = not left
                    self.sim.stack.append(left)
                case CommandType.PRINT:
                    n = int(instruction.argument)
                    for i in range(n):
                         self.sim.output += str(self.sim.stack.pop())
                case CommandType.JMP:
                    self.instr = int(instruction.argument)
                    continue
                case CommandType.JF:
                    test = self.sim.stack.pop()
                    if not test:
                        self.instr = int(instruction.argument)
                        continue
                case CommandType.ROUND:
                    val = self.sim.stack.pop()
                    val = round(val)
                    self.sim.stack.append(val)
                case CommandType.ENTERFRAME:
                    name = instruction.argument
                    new_frame = Frame(self.sim,self.sim.ir.routines[name])
                    res = self.sim.execute_frame(new_frame)
                    if res is not None:
                        self.sim.stack.append(res)
                case CommandType.LOADFRAME:
                    local_count = int(instruction.argument)
                    self.starting_stack_len -= local_count
                    for x in range(local_count):
                        s = self.sim.stack.pop()
                        self.locals.append(s)
                case CommandType.PUSHLOCAL:
                    local_id = int(instruction.argument)
                    if local_id >= len(self.locals):
                        raise Exception("Runtime (simulator) error. Global ID out of range")
                    self.sim.stack.append(self.locals[local_id])
                case CommandType.SETLOCAL:
                    local_id = int(instruction.argument)
                    while len(self.locals) < local_id+1:
                        self.locals.append(None)
                    self.locals[local_id] = self.sim.stack.pop()
                case CommandType.PUSHGLOBAL:
                    global_id = int(instruction.argument)
                    if global_id >= len(self.sim.globals):
                        raise Exception("Runtime (simulator) error. Global ID out of range")
                    self.sim.stack.append(self.sim.globals[global_id])
                case CommandType.SETGLOBAL:
                    global_id = int(instruction.argument)
                    while len(self.sim.globals) < global_id+1:
                        self.sim.globals.append(None)
                    self.sim.globals[global_id] = self.sim.stack.pop()
                case CommandType.UNLOADFRAME:
                    self.return_val = self.sim.stack.pop()
                case CommandType.EXITFRAME:
                    self.clean_stack()
                    return self.return_val
                case _:
                    raise Exception("Runtime (simulator) error. Unknown command '" + str(instruction.command) + "'")
            self.instr += 1

        if self.implicit_return:
            print("Using implicit return. This is a testing feature that will be removed for deployment.")
            if len(self.sim.stack) > 0:
                self.return_val = self.sim.stack.pop()

        self.clean_stack()
        return self.return_val

    def clean_stack(self):
        while len(self.sim.stack) > self.starting_stack_len:
            self.sim.stack.pop()
