import unittest

from humansimulator.humanSimulator import execute
from interpreter.shInterpreter import interpret


class TestSimulator(unittest.TestCase):
    def test_add(self):
        x = interpret("1+3")
        result = execute(x)
        self.assertEqual(4,result)

    def test_sub(self):
        x = interpret("4-5")
        result = execute(x)
        self.assertEqual(-1,result)

    def test_mult(self):
        x = interpret("2*3*7")
        result = execute(x)
        self.assertEqual(42,result)

    def test_div(self):
        x = interpret("100/25")
        result = execute(x)
        self.assertEqual(4,result)


    def test_math(self):
        x = interpret("(2+3*2)/4")
        result = execute(x)
        self.assertEqual(2,result)