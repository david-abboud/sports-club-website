window.onload=function(){
    var log_button = document.getElementById("login_button");
    log_button.addEventListener("click", log_func)

    console.log("script loaded")
    console.log("log button", log_button)
    
}

var SERVER_URL = "http://127.0.0.1:5000"

async function log_func(username, password) {
    console.log("login called")
    var bool = true
    var username = document.getElementById("username_login").value;  
    var password = document.getElementById("password_login").value;
        const data = {  "user_name":username,
                        "password":password,
                        };
    const response = await fetch(`${SERVER_URL}/signin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then((response) => response.json())
        .then((body) => {
            console.log("TOKEN:");
            console.log(body.token);
            saveUserToken(body.token);
            token1 = body.token;
        });
// 👉️ 200
    if (token1 != "") {
      console.log(response);

      window.open("http://127.0.0.1:5000/home_si","_self")
    }

    //     .then((response) => {
    //     if (response.status === 200) {
    //         window.open("http://127.0.0.1:5000/home","_self")
    //     }
    // })
        // .then(response =>{response.json(),
        //     window.open("http://127.0.0.1:5000/home","_self")})
        // .then(data => {
        //     console.log('Success:', data);
            
        // })
        // .catch((error) => {
        //     console.error('Error:', error);
            
        // });
        
}

 function saveUserToken(userToken) {
    localStorage.setItem("TOKEN", userToken);
  }
   function getUserToken() {
    return localStorage.getItem("TOKEN");
  }
   function clearUserToken() {
    return localStorage.removeItem("TOKEN");
  }

