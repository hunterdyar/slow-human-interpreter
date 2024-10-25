import {Compile} from "./engine/compiler.js"
import { SVG } from '@svgdotjs/svg.js'

const codeTextarea = document.getElementById("code");
const submitButton = document.getElementById("submit");
const instructionList = document.getElementById("instructionList");
let draw = null;

submitButton.addEventListener("click", function(e) {
    draw = SVG().addTo('#machine').size(800, 700);

    e.preventDefault();
    let c = Compile(codeTextarea.value);
    instructionList.innerHTML = "";
 //   var stack_bg = draw.rect(800, 100).attr({ fill: '#f06' })
    var stack = draw.group().addClass("stack")

    c.instructions.forEach((x)=>{
        var item = document.createElement("li")
        stack.rect(20, 100).attr({fill: '#091'}).animate().move(stack.children().length*25,0);
        instructionList.appendChild(item);
        item.id = x.id;
        item.innerText =x.t;
    })
})
