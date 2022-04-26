window.onload=function(){
    console.log("script loaded")
    var mod_button = document.getElementById("email_button");
    mod_button.addEventListener("click", email_func());
}
var SERVER_URL = "http://127.0.0.1:5000"

async function email_func(){
    var email = document.getElementById("user_email").value;
    const data = {
        "email": email,
    };
    const response = await fetch(`${SERVER_URL}/forgot_password`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    
}