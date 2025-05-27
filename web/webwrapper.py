from interpreter.Interpreter import interpret
from printer.Printer import render
from humanSimulator.humanSimulator import HumanSimulator
from js import printHTMLPage, testResult
from pyscript import document

print("loaded!")

source_field = document.querySelector("#source_field")

def do_compile(source: str) -> str:
    x = interpret(source)
    html = render(x)
    return html

def submit_form(e) -> str:
    res = do_compile(source_field.value)
    printHTMLPage(res)
    return res

def test_form(e) -> str:
    try:
        x = interpret(source_field.value)
        sim = HumanSimulator(x, False)
        sim.execute()
        testResult(sim.output,True)
    except e:
        testResult(e,False)
