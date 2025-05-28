import pathlib
import chevron
from PrintObjectFactory import get_pretty_ir
from interpreter.IntermediateRep import IntermediateRep

def render(ir: IntermediateRep,options=None):
    element = get_pretty_ir(ir)
    dir = pathlib.Path(__file__).parent.resolve()
    ipf = dir.joinpath("../templates/instructionpages.mustache")
    with open(ipf, 'r') as instruction_pages_template:
        args={
            'template': instruction_pages_template,
            'data': element,
        }
        return chevron.render(**args)

def create_html_file(ir: IntermediateRep):
    rendered = render(ir)
    with open('output.html', 'w') as output_html:
        output_html.write(rendered)



