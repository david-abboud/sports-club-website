window.onload=function(){
    console.log("script loaded")
    var mod_button = document.getElementById("new_pass_button");
    mod_button.addEventListener("click", forg_func());
}
var SERVER_URL = "http://127.0.0.1:5000"

async function forg_func(){
    var new_password = document.getElementById("new_pass").value;
    var new_password_confirm = document.getElementById("confirm_new_pass").value;
    const data = {
        "new_password": new_password,
        "confirm_new_password": new_password_confirm,
    };
    const response = await fetch(`${SERVER_URL}/forgot_password_reset`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}