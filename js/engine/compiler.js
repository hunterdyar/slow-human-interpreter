import {parse} from "acorn";
import {recursive} from "acorn-walk";

export function Compile(source)
{
    let tree = parse(source, {ecmaVersion: 2020});
    let state = {instructions: [], globals: []};
    recursive(tree, state, {
        Literal: function (node, st, c) {
            st.instructions.push({t:`push: ${node.value}`,o:"push",operand:node.value});
        },
        BinaryExpression: function (node, st, c) {
            switch (node.operator) {
                case "+":
                    c(node.left, st);
                    c(node.right, st);
                    st.instructions.push({t:"pop from stack twice. Add values together. Push this sum onto to stack.",op:"+"});
                    break;
                case "-":
                    c(node.left, st);
                    c(node.right, st);
                    st.instructions.push({t:"pop two values from stack. Subtract the top from the second-from-top. Push result to stack.",op:"-"});
                    break;
                case "*":
                    c(node.left, st);
                    c(node.right, st);
                    st.instructions.push({t:"pop from the stack twice. Multiply them together. Push result onto the stack.",op:"*"});
                    break;
            }
        },
        Identifier: function (node, st, c) {
            let g = st.globals.indexOf(node.name);
            if (g < 0) {
                //Unknown Identifier!
            }
            st.instructions.push({t:"get value of global " + g + ". Push it onto the stack.",op:"push_g",operand:g})
        },
        AssignmentExpression: function (node, st, c) {
            let id = "";
            if (node.left.type === "Identifier") {
                id = node.left.name;
            } else {
                console.log("Compiler Error: Cannot Assign to "+node.type)
                return;
            }
            let g = st.globals.indexOf(id);
            if (g < 0) {
                console.log("Compiler Error: Unknown Variable "+id)
                return;
                // g = st.globals.length;
                // st.globals.push(id);
            }
            c(node.right, st);
            st.instructions.push({t:"pop and set global " + g + " to this value.",op:"set_g",operand:g})
        }
    })

    for (let i = 0;i<state.instructions.length;i++) {
        state.instructions[i].id = "ins-"+i;
    }
    return state;
}
//console.log(state.instructions)


