from interpreter.Interpreter import interpret
from printer.Printer import render
from humanSimulator.humanSimulator import HumanSimulator
from js import printHTMLPage, testResult
from pyscript import document

print("loaded!")

used_frame_count = 1
desired_frame_count = -1
source_field = document.querySelector("#source_field")

def do_compile(source: str) -> str:
    fc = desired_frame_count
    options = {}
    if desired_frame_count < 0:
        run_test()
        fc = used_frame_count
    options["frameCount"] = fc

    x = interpret(source)
    html = render(x,options)
    return html

def submit_form(e):
    res = do_compile(source_field.value)
    printHTMLPage(res)

def run_test():
    global used_frame_count
    x = interpret(source_field.value)
    sim = HumanSimulator(x, False)
    sim.execute()
    used_frame_count = sim.maxFameCount

    return sim
def test_form(event):
    try:
        sim = run_test()
        testResult(sim.output,True)
    except Exception as e:
        testResult(e,False)
        raise e
