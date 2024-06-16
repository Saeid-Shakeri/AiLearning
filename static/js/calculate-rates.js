window.onload = function exampleFunction() { 

    const one = document.getElementById('first')
    const two =  document.getElementById('second')
    const three =  document.getElementById('third')
    const four =  document.getElementById('fourth')
    const five =  document.getElementById('fifth')

    let score = $('input[name="score"]').val();
    score =  Math.round(Number(score));
    switch (score) {
        case 0 : {
            one.classList.add('checked')
            two.classList.remove('checked')
            three.classList.remove('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        }
        case 1 : {
            one.classList.add('checked')
            two.classList.remove('checked')
            three.classList.remove('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        }
        case '2' : {
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.remove('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        } 
        case 3 : {
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
            return
        } 
        case 4 : {
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.add('checked')
            five.classList.remove('checked')
            return
        } 
        case 5 : {
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.add('checked')
            five.classList.add('checked')
            return
        }
        default :{
            console.log('default is here........')
            one.classList.add('checked')
            two.classList.add('checked')
            three.classList.add('checked')
            four.classList.add('checked')
            five.classList.add('checked')
            return
        }
    }
} 