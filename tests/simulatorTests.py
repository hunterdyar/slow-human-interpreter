import unittest

from humansimulator.humanSimulator import HumanSimulator
from interpreter.Interpreter import interpret

def execute(code: str) -> object:
    x = interpret(code)
    sim = HumanSimulator(x)
    return sim.execute()
def execute_get_output(code: str) -> object:
    x = interpret(code)
    sim = HumanSimulator(x)
    sim.execute()
    return sim.output

class TestSimulator(unittest.TestCase):
    def test_add(self):
        result = execute("1+3")
        self.assertEqual(4,result)

    def test_sub(self):
        result = execute("4-5")
        self.assertEqual(-1,result)

    def test_mult(self):
        result = execute("2*3*7")
        self.assertEqual(42,result)

    def test_div(self):
        result = execute("100/25")
        self.assertEqual(4,result)

    def test_math(self):
        result = execute("(2+3*2)/4")
        self.assertEqual(2,result)

    def test_and(self):
        result = execute("True and False")
        self.assertEqual(False, result)
        result = execute("True and True")
        self.assertEqual(True, result)
        result = execute("False and False")
        self.assertEqual(False, result)
        result = execute("False and True")
        self.assertEqual(False, result)

    def test_or(self):
        result = execute("True or False")
        self.assertEqual(True, result)
        result = execute("True or True")
        self.assertEqual(True, result)
        result = execute("False or False")
        self.assertEqual(False, result)
        result = execute("False or True")
        self.assertEqual(True, result)

    def test_compare(self):
        result = execute("False == True")
        self.assertEqual(False, result)

    def test_not(self):
        result = execute("not True")
        self.assertEqual(False, result)
        result = execute("not False")
        self.assertEqual(True, result)

    def test_print(self):
        result = execute_get_output("print(True)")
        self.assertEqual("True", result)
        result = execute_get_output("print(1, 2)")
        self.assertEqual("12", result)

    def test_if(self):
        result = execute_get_output("""
if False:
  print("banana")
""")
        self.assertEqual("", result)

        result = execute_get_output("""
if False:
          print("banana")
else:
    print("cheese")
""")
        self.assertEqual("cheese", result)

        result = execute_get_output("""
if True:
    print("banana")
else:
    print("cheese")
""")
        self.assertEqual("banana", result)

    def test_if_elif(self):
        result = execute_get_output("""
if False:
    print("banana")
elif False:
    print("cheese")
elif False:
    print("cheese")
else:
    print("cake")
""")
        self.assertEqual("cake", result)

# this will fail until I get variable assignment done, lol.
    def test_while(self):
            result = execute_get_output("""
i = 5
print("-")
while i>0:
    print(i)
    i = i-1
    """)
            self.assertEqual("-54321", result)
