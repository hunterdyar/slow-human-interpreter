from interpreter.IntermediateRep import IntermediateRep, CommandType

frames = []
ir = None

class Frame:
    def __init__(self, routine):
        self.routine = routine
        self.instr = 0
        self.stack = []

    def execute(self):
        while self.instr < len(self.routine):
            instruction = self.routine[self.instr]
            if instruction.command == CommandType.PUSH:
                self.stack.append(self.routine[self.instr].argument)
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

            self.instr += 1

        # executing done?
        if len(self.stack) == 0:
            return None
        else:
            top = self.stack.pop()
            return top


def execute(intermediate: IntermediateRep):
    global frames,ir
    ir = intermediate
    # call the base frame.
    frames.append(Frame(ir.routines[0]))
    return frames[-1].execute()

