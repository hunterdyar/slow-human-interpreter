import unittest

from interpreter.Interpreter import interpret


class TestCompiler(unittest.TestCase):
    def test_empty(self):
        x = interpret("")
        self.assertNotEqual(x, None)

    def test_print(self):
        x = interpret("print(\"hi\")")
        self.assertNotEqual(x, None)

    def test_add(self):
        x = interpret("1+3")
        print(x)
        self.assertEqual(1, len(x.routine_stack))
        self.assertEqual(3, len(x.routine_stack[0]))
        # self.assertEqual(x.routines[0][0].command,CommandType.PUSH)
