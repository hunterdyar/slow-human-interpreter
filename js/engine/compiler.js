import {parse} from "acorn";
import {recursive} from "acorn-walk";

export function Compile(source)
{
    let tree = parse(source);
    let state = {instructions: [], globals: []};
    recursive(tree, state, {
        Literal: function (node, st, c) {
            st.instructions.push(`push: ${node.value}`);
        },
        BinaryExpression: function (node, st, c) {
            switch (node.operator) {
                case "+":
                    c(node.left, st);
                    c(node.right, st);
                    st.instructions.push("Pop two values from stack. Add them together. Push result to stack.");
                    break;
                case "-":
                    c(node.left, st);
                    c(node.right, st);
                    st.instructions.push("Pop two values from stack. Subtract the top from the second-from-top. Push result to stack.");
                    break;
                case "*":
                    c(node.left, st);
                    c(node.right, st);
                    st.instructions.push("Pop two values from the stack. Multiply them together. Push result onto the stack.");
                    break;
            }
        },
        Identifier: function (node, st, c) {
            let g = st.globals.indexOf(node.name);
            if (g < 0) {
                //Unknown Identifier!
            }
            st.instructions.push("get value of global " + g + ". Push it onto the stack.")
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
            st.instructions.push("pop and set global " + g + " to this value.")
        }

    })

    return state;
}
//console.log(state.instructions)


