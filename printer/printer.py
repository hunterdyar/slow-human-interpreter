import pathlib

import chevron

from interpreter.IntermediateRep import IntermediateRep
from printer.PrintObjectFactory import get_pretty_ir

def render(ir: IntermediateRep):
    element = get_pretty_ir(ir)
    dir = pathlib.Path(__file__).parent.resolve()
    ipf = dir.joinpath("instructionpages.mustache")
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

