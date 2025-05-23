from interpreter.IntermediateRep import IntermediateRep, CommandType

class HumanSimulator(IntermediateRep):
    def __init__(self, intermediate):
        self.ir = intermediate
        self.frames = [Frame(self,self.ir.routines[0])]
        self.output = ""
    def execute(self):
        return self.frames[-1].execute()


class Frame:
    def __init__(self, sim, routine):
        self.sim = sim
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

            self.instr += 1

        # executing done?
        if len(self.stack) == 0:
            return None
        else:
            top = self.stack.pop()
            return top


