import unittest

from humanSimulator.humanSimulator import HumanSimulator
from interpreter.Interpreter import interpret

def execute(code: str) -> object:
    x = interpret(code)
    sim = HumanSimulator(x, True)
    return sim.execute()
def execute_get_output(code: str) -> object:
    x = interpret(code)
    sim = HumanSimulator(x, False)
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
print("cake")
""")
        self.assertEqual("cake", result)

        result = execute_get_output("""
if False:
    print("banana")
else:
    print("cheese")
print("cake")
""")
        self.assertEqual("cheesecake", result)

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

    def test_assign(self):
        result = execute_get_output("""
i = 5
j = 10
i = 20 + i
k = i + j
print(k+i)
""")
        self.assertEqual("60", result)

# this will fail until I get variable assignment done, lol.
    def test_while(self):
        result = execute_get_output("""
i = 5
print("-")
while i>0:
    print(i)
    i = i-1
print("-")
    """)
        self.assertEqual("-54321-", result)

    def test_while_break(self):
        result = execute_get_output("""
i = 5
print("-")
while i > 0:
    print(i)
    if i == 3:
        break
    i = i-1
print("-")
            """)
        self.assertEqual("-543-", result)

    def test_while_continue(self):
        result = execute_get_output("""
i = 5
print("-")
while i > 0:
    i = i-1
    if i == 3:
        continue
    print(i)
print("-")
                """)
        self.assertEqual("-4210-", result)

    def test_simple_function_call(self):
        result = execute_get_output("""
do_something_awesome(0,1,2)

def do_something_awesome(a,b,c):
    print(a)
    print(b)
    print(c)
print(3)

do_something_awesome(4,5,6)

print(7)
    """)
        self.assertEqual("01234567", result)

    def test_globals(self):
        result = execute_get_output("""
c = 100
def no_glob(a,b):
    c = a+b

no_glob(4,5)

print(c)
""")
        self.assertEqual("100", result)
        result = execute_get_output("""
c = 100
def glob(a,b):
    global c
    c = a+b

glob(4,5)

print(c)
""")
        self.assertEqual("9", result)

    def test_return(self):
        result = execute_get_output("""
def addup(a,b,c):
    return a+b+c
print(addup(1,2,3))
    """)
        self.assertEqual("6", result)

    def test_list_1(self):
        result = execute_get_output("""
a = [1,2,3]
print(a)
    """)
        self.assertEqual("6", result)

