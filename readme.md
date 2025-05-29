# Slow Human Interpreter

## What Is This?
Slow Human Interpreter is a tool that compiles python into instructions that can be printed out and executed by humans.
It supports a subset of the python language.

It's only slow for certain definitions of slow.

## Why Is This?
This is a teaching tool designed to get students to really experience how a simple stack-based virtual machine works from the inside out.
It was created to be used in a slightly-past-introductory computer science course.

Plus, it's kind of absurd. I love that.

## How Does It Work?

1. Python is parsed by the [ast](https://docs.python.org/3/library/ast.html) module that python provides.
2. We compile the supported subset of the language to an intermediate representation (IR).
3. A human simulator (also called a virtual machine) can execute this for testing purposes.
4. The IR is passed to a converter, which generates HTML+CSS using [mustache](https://mustache.github.io/) (and the [chevron](https://github.com/noahmorrison/chevron) python package) for templating.
5. The HTML is converted to a pdf by your web browser in a pop-up window, and the print() method is called.
6. All of this is served as a webpage using [PyScript](https://pyscript.net/). So technically the human simulator is a VM running inside of a python VM that's been compiled to WASM and is running in your browser. So that's neat.
