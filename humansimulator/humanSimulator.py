from interpreter.IntermediateRep import IntermediateRep, CommandType

class HumanSimulator:
    def __init__(self, intermediate):
        self.ir = intermediate
        self.frames = [Frame(self, self.ir.routines["main"])]
        self.output = ""
        self.globals = []
    def execute(self):
        return self.frames[-1].execute()
    def execute_frame(self, frame):
        self.frames.append(frame)
        self.frames[-1].execute()

class Frame:
    def __init__(self, sim, routine):
        self.sim = sim
        self.routine = routine
        self.instr = 0
        self.stack = []
        self.locals = []

    def execute(self):
        while self.instr < len(self.routine.instructions):
            instruction = self.routine.instructions[self.instr]

            if instruction.command == CommandType.PUSH:
                self.stack.append(self.routine.instructions[self.instr].argument)
            elif instruction.command == CommandType.POP:
                self.stack.pop()
            elif instruction.command == CommandType.ADD:
                left = self.stack.pop()
                right = self.stack.pop()
                addition = left + right
                self.stack.append(addition)
            elif instruction.command == CommandType.SUB:
                left = self.stack.pop()
                right = self.stack.pop()
                sub = left - right
                self.stack.append(sub)
            elif instruction.command == CommandType.MUL:
                left = self.stack.pop()
                right = self.stack.pop()
                mul = left * right
                self.stack.append(mul)
            elif instruction.command == CommandType.DIV:
                left = self.stack.pop()
                right = self.stack.pop()
                division = left / right
                self.stack.append(division)
            elif instruction.command == CommandType.AND:
                left = self.stack.pop()
                right = self.stack.pop()
                division = left and right
                self.stack.append(division)
            elif instruction.command == CommandType.OR:
                left = self.stack.pop()
                right = self.stack.pop()
                division = left or right
                self.stack.append(division)
            elif instruction.command == CommandType.CMP:
                left = self.stack.pop()
                right = self.stack.pop()
                answer = False
                if instruction.argument == "Eq":
                    answer = left == right
                elif instruction.argument == "NotEq":
                    answer = left != right
                elif instruction.argument == "Lt":
                    answer = left < right
                elif instruction.argument == "LtE":
                    answer = left <= right
                elif instruction.argument == "Gt":
                    answer = left > right
                elif instruction.argument == "GtE":
                    answer = left >= right
                elif instruction.argument == "Is":
                    answer = left is right
                elif instruction.argument == "IsNot":
                    answer = left is not right
                elif instruction.argument == "NotIn":
                    answer = left not in right
                elif instruction.argument == "In":
                    answer = left in right
                self.stack.append(answer)
            elif instruction.command == CommandType.NOT:
                left = self.stack.pop()
                left = not left
                self.stack.append(left)
            elif instruction.command == CommandType.PRINT:
                n = int(instruction.argument)
                for i in range(n):
                     self.sim.output += str(self.stack.pop())
            elif instruction.command == CommandType.JMP:
                self.instr = int(instruction.argument)
            elif instruction.command == CommandType.JF:
                test = self.stack.pop()
                if not test:
                    self.instr = int(instruction.argument)
            elif instruction.command == CommandType.ROUND:
                val = self.stack.pop()
                val = round(val)
                self.stack.append(val)
            elif instruction.command == CommandType.ENTERFRAME:
                name = instruction.argument[0]
                local_count = int(instruction.argument[1])
                new_frame = Frame(self.sim,self.sim.ir.routines[name])
                for x in range(local_count):
                    new_frame.locals.append(self.stack.pop())
                self.sim.execute_frame(new_frame)
            elif instruction.command == CommandType.PUSHLOCAL:
                local_id = int(instruction.argument)
                if local_id >= len(self.locals):
                    raise Exception("Runtime (simulator) error. Global ID out of range")
                self.stack.append(self.locals[local_id])
            elif instruction.command == CommandType.SETLOCAL:
                local_id = int(instruction.argument)
                while len(self.locals) < local_id+1:
                    self.locals.append(None)
                self.locals[local_id] = self.stack.pop()
            elif instruction.command == CommandType.PUSHGLOBAL:
                global_id = int(instruction.argument)
                if global_id >= len(self.sim.globals):
                    raise Exception("Runtime (simulator) error. Global ID out of range")
                self.stack.append(self.sim.globals[global_id])
            elif instruction.command == CommandType.SETGLOBAL:
                global_id = int(instruction.argument)
                while len(self.sim.globals) < global_id+1:
                    self.sim.globals.append(None)
                self.sim.globals[global_id] = self.stack.pop()
            else:
                raise Exception("Runtime (simulator) error. Unknown command '" + instruction.command + "'")
            self.instr += 1


        # executing done?
        if len(self.stack) == 0:
            return None
        else:
            top = self.stack.pop()
            return top


