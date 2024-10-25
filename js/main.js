console.log("main");
import {Compile} from "./engine/compiler.js"
import anime from "animejs"

const codeTextarea = document.getElementById("code");
const submitButton = document.getElementById("submit");
const instructionList = document.getElementById("instructionList");


submitButton.addEventListener("click", function(e) {
    e.preventDefault();
    let c = Compile(codeTextarea.value);
    instructionList.innerHTML = "";
    var timeline = anime.timeline({})
    c.instructions.forEach((x)=>{
        instructionList.innerHTML += "<li">"+x+"</li>"

        //pass the instruction over to an animation thing that runs each animation ...as the runtime, basically.
        //timeline.add({})
    })
})
