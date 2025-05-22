# Slow Human Interpreter

## What Is This?
Slow Human Interpreter is a tool that compiles python into instructions that can be printed out and executed by humans.
It supports a subset of the python language.

It's only slow for certain definitions of slow.

## Why Is This?
This is a teaching tool designed to get students to really experience how a simple stack-based virtual machine works from the inside out.
It was created to be used in a slightly-past-introductory computer science course.

Plus, it's kind of absurd. I love that.

## How Do I Use It?

#### Prerequisites
1. A printer and paper. 8.5" x 11" (aka '[normal printer paper](https://en.wikipedia.org/wiki/Letter_%28paper_size%29)')
2. A stack of Index Cards to use for data
3. A hole punch
4. Binder Rings

#### Compiling a program
*TBD*

#### Executing the program
*TBD, but just follow the instructions...*  

The standard memory is simply a table on a whiteboard.
The standard output is a drawing program; coloring 'pixels' in a grid.

## How Does It Work?

1. Python is parsed by the [ast](https://docs.python.org/3/library/ast.html) module that python provides.
2. We compile the supported subset of the language to an intermediate representation (IR).
3. A human simulator (also called a virtual machine) can execute this for testing purposes.
4. The IR is passed to a converter, which generates HTML+CSS
5. The HTML is converted to pdfs to be printed and executed by real humans.