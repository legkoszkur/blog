var clik = 0;

var clik = 0;
function submitUserForm() {
    
    if (clik == 0){
        document.getElementById("captcha").style.display = "block";
        clik++;
        return false;
    } else {
        var response = grecaptcha.getResponse();
            if(response.length == 0) {
                document.getElementById('g-recaptcha-error').innerHTML = '<span style="color:red;">To pole jest wymagane.</span>';
                return false;
            }
            return true;
    }  
}
 
function verifyCaptcha() {
    document.getElementById('g-recaptcha-error').innerHTML = '';
}
