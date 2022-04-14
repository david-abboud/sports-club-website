window.onload=function(){
    console.log("script loaded")
    var mod_button = document.getElementById("modify_button");
    mod_button.addEventListener("click", mod_func);


    console.log("log button", mod_button)
    
}

var SERVER_URL = "http://127.0.0.1:5000"

function mod_func() {
    console.log("log0")
    var username = document.getElementById("username").value;  
    var password = document.getElementById("password").value;
    var type = document.getElementById("select").value;
    var mdf = document.getElementById("modify").value;

    console.log("log1")

        const data = {  "user_name":username,
                        "password":password,
                        "type":type,
                        "modification":mdf
                        };
                        console.log("log2")

        fetch(`${SERVER_URL}/modify_customer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        console.log("log3")
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);

        })
        .catch((error) => {
            console.error('Error:', error);
        });
        console.log("log4")
        
}


