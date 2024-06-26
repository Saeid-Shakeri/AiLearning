
function validateForm(name) {
    // signup_login.html
    if (name == 'login'){
        let x = document.forms[name]["email_username"].value;
        if (x == "") {
        alert("ایمیل یا نام کاربری نمیتواند خالی باشد!");
        return false;
        }
        x = document.forms[name]["password"].value;
        if (x == "") {
        alert("رمز عبور نمیتواند خالی باشد!");
        return false;
        }  
    }
    // signup_login.html
    else if (name == 'signup'){
        let x = document.forms[name]["username"].value;
        if (x == "") {
        alert("ایمیل یا نام کاربری نمیتواند خالی باشد!");
        return false;
        }
        x = document.forms[name]["email"].value;
        if (x == "") {
        alert("ایمیل نمیتواند خالی باشد!");
        return false;
        }  
        x = document.forms[name]["password1"].value;
        if (x == "") {
        alert("رمز عبور نمیتواند خالی باشد!");
        return false;
        }  	
        x = document.forms[name]["password2"].value;
        if (x == "") {
        alert("تکرار رمز عبور نمیتواند خالی باشد!");
        return false;
        }
    }
    // change_password.html
    else if(name == 'change_pass'){
        let x = document.forms[name]["oldpassword"].value;
        if (x == "") {
            alert("رمز قبلی نمی تواند خالی باشد!");
            return false;
            }
            x = document.forms[name]["password1"].value;
            if (x == "") {
            alert("رمز جدید نمیتواند خالی باشد!");
            return false;
            }  
            x = document.forms[name]["password2"].value;
            if (x == "") {
            alert("تکرار رمز نمیتواند خالی باشد!");
            return false;
            }
    }
    // support.html
    else if(name == 'support'){
        let x = document.forms[name]["cat"].value;
        if (x == "") {
            alert(" موضوع نمی تواند خالی باشد!");
            return false;
            }
            x = document.forms[name]["title"].value;
            if (x == "") {
            alert(" عنوان پیام نمیتواند خالی باشد!");
            return false;
            }  
            x = document.forms[name]["message"].value;
            if (x == "") {
            alert(" متن پیام نمیتواند خالی باشد!");
            return false;
            }
    }
    // lesson - course_details - article_details
    else if (name == 'lesson' || name == 'course' || name == 'article'){
        let x = document.forms[name]["name"].value;
        if (x == "") {
            alert(" نام نمی تواند خالی باشد!");
            return false;
            }
            x = document.forms[name]["email"].value;
            if (x == "") {
            alert("ایمیل نمیتواند خالی باشد!");
            return false;
            }  
            x = document.forms[name]["comment"].value;
            if (x == "") {
            alert(" متن نظر نمیتواند خالی باشد!");
            return false;
            }
    }

} 