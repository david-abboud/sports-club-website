window.onload = function () {
    var reg_button = document.getElementById("register_button");
    reg_button.addEventListener("click", reg_func);
}

var SERVER_URL = "http://127.0.0.1:5000"

async function reg_func() {
    if (document.getElementById("username").value != '' && document.getElementById("first_name").value != '' && document.getElementById("last_name").value != '' && document.getElementById("email").value != '' && document.getElementById("phone").value != '' && document.getElementById("password").value != '' && document.getElementById("confirm_password").value != '' && document.getElementById("password").value == document.getElementById("confirm_password").value) {
        var first_name = document.getElementById("first_name").value;
        var last_name = document.getElementById("last_name").value;
        var email = document.getElementById("email").value;
        var phone = document.getElementById("phone").value;
        var password = document.getElementById("password").value;
        var username = document.getElementById("username").value;

        const data = {
            "user_name": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone,
        };

        window.alert("If you have provided the correct information, an email was sent to your inbox. Please open your inbox in order to confirm your account.")

        const response = await fetch(`${SERVER_URL}/customer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        console.log('status code: ', response.status); // 👉️ 200

     

        if (response.ok) {
            console.log(response);
            console.log("User created successfully", data);
            window.open("http://127.0.0.1:5000/signin","_self")
        }
        else {
            console.log("error");
            window.alert("An account with that information already exists, or the formatting of one of the fields is incorrect. Please try again.");
        }
    }
}




