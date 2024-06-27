function show_answer(name) {
    let x = document.forms[name]["answer"].value;
    alert(x)
    return false
}

function show_question(name){
    let x = document.forms[name]["question"].value;
    alert(x)
    return false
}
