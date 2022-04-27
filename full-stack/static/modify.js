window.onload=function(){
    console.log("script loaded")
    var mod_button = document.getElementById("modify_button");
    mod_button.addEventListener("click", mod_func);

    var del_button = document.getElementById("delete_button");
    del_button.addEventListener("click", del_func);

    getUserInfo();
}

var SERVER_URL = "http://127.0.0.1:5000"

async function del_func(){
    var username = document.getElementById("username").value;  
    var password = document.getElementById("password").value;
    var confirmation = document.getElementById("newpassword").value;

        const data = {  "user_name":username,
                        "password":password,
                        "confirmation":confirmation,
                       
                        };
                        console.log("log2")

        const response = await fetch(`${SERVER_URL}/delete_customer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
    })
    if (response.ok) {
        console.log(response);
        console.log("User deleted successfully", data);
        window.open("http://127.0.0.1:5000/home","_self")
    }
    else {
        console.log("error");
    }

}

async function getUserInfo(){
    userToken = getUserToken();

    console.log("log token", userToken)

    const response = await fetch(`${SERVER_URL}/getUserInfo`, {
        method: 'Get',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`
        },
    })
    const data = await response.json();

    document.getElementById("username_display").innerHTML = data.user_name;
    document.getElementById("firstname_display").innerHTML = data.first_name;
            document.getElementById("lastname_display").innerHTML =data.last_name ;
            document.getElementById("email_display").innerHTML =data.email ;
            document.getElementById("phone_display").innerHTML = data.phone_number;
    
}

function mod_func() {
    console.log("log0")
    var username = document.getElementById("username").value;  
    var password = document.getElementById("password").value;
    var type = document.getElementById("select").value;
    var mdf = document.getElementById("modify").value;
    var confirmation = document.getElementById("newpassword").value;

    if (confirmation != ""){
        if (password == confirmation){
            const data2 = {  "user_name":username,
                            "old_password":password,
                            "new_password1":mdf,
                            "new_password2":mdf,
                            };
                            console.log("log2")

            var response2 = fetch(`${SERVER_URL}/reset_password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data2),
            })
 
        }

            window.open("http://127.0.0.1:5000/signin","_self");
        
        
        return;
    }

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
        console.log("log3");
        window.open("http://127.0.0.1:5000/modify_si","_self");
        console.log("log4")
        
}

function getUserToken() {
    return localStorage.getItem("TOKEN");
  }


