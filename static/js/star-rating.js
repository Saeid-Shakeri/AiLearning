
const one = document.getElementById('first')
const two =  document.getElementById('second')
const three =  document.getElementById('third')
const four =  document.getElementById('fourth')
const five =  document.getElementById('fifth')

const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// optimized
const handleStarSelect = (size) => {
  const children = form.children
  console.log(children)
  for (let i=0; i < children.length; i++){
    if(i <= size){
      children[i].classList.add('checked')
    }
    else{
      children[i].classList.remove('checked')

    }
  }
}

// not optimized
const handleSelect = (selection) => {
  switch (selection) {
    case 'first' : {
      //one.classList.add('checked')
      //two.classList.remove('checked')
      //three.classList.remove('checked')
      //four.classList.remove('checked')
      //five.classList.remove('checked')
      handleStarSelect(1)
      return
    }
    case 'second' : {
    //   one.classList.add('checked')
    //   two.classList.add('checked')
    //   three.classList.remove('checked')
    //   four.classList.remove('checked')
    //   five.classList.remove('checked')
      handleStarSelect(2)
      return
    } 
    case 'third' : {
    //   one.classList.add('checked')
    //   two.classList.add('checked')
    //   three.classList.add('checked')
    //   four.classList.remove('checked')
    //   five.classList.remove('checked')
      handleStarSelect(3)
      return
    } 
    case 'fourth' : {
    //   one.classList.add('checked')
    //   two.classList.add('checked')
    //   three.classList.add('checked')
    //   four.classList.add('checked')
    //   five.classList.remove('checked')
      handleStarSelect(4)
      return
    } 
    case 'fifth' : {
    //   one.classList.add('checked')
    //   two.classList.add('checked')
    //   three.classList.add('checked')
    //   four.classList.add('checked')
    //   five.classList.add('checked')
      handleStarSelect(5)
      return
    }
  }

}

const getNumericValue = (stringValue)=> {
    let numericValue;
    if ( stringValue === 'first'){
        numericValue = 1
    }
    else if ( stringValue === 'second'){
        numericValue = 2
    }
    else if ( stringValue === 'third'){
        numericValue = 3
    }
    else if ( stringValue === 'fourth'){
        numericValue = 4
    }
    else if ( stringValue === 'fifth'){
        numericValue = 5
    }
    else {
        numericValue = 0
    }
    return numericValue
}

if ( one ){
    const arr = [one, two, three, four, five]

    arr.forEach(item=> item.addEventListener('mouseover',(event)=>{
        handleSelect(event.target.id)
    }))
    arr.forEach(item=> item.addEventListener('click', (event)=>{
        const val = event.target.id
        form.addEventListener('submit',e=>{
            e.preventDefault()
            const id = e.target.id
            const val_num = getNumericValue(val)
            $.ajax({
                type:'POST',
                url:'/course/rate-course/',
                data:{
                    'csrfmiddlewaretoken':csrf[0].value,
                    'el_id':id,
                    'val': val_num

                },
                success: function(response){
                    if ( response.success === 'false'){
                        confirmBox.innerHTML = '<h3>  قبلا امتیاز داده اید.! </h3>'
  
                     }
                      else{
                       confirmBox.innerHTML = '<h3> امتیاز شما ثبت شد! </h3>'
                      }
                },
                error:function(error){
                    confirmBox.innerHTML = '<h3> مشکلی پیش آمد! </h3>'
                }
            })

        })
    
    }))
}