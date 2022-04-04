var register_button = document.getElementById("register_button");
addButton.addEventListener("click", register_button);

var SERVER_URL = "http://127.0.0.1:5000"

function register_button() {
    if (document.getElementById("username").value != '' && document.getElementById("first_name").value != '' && document.getElementById("last_name").value != '' && document.getElementById("email").value != '' && document.getElementById("phone").value != '' && document.getElementById("password").value != '' && document.getElementById("confirm_password").value != '' && document.getElementById("password").value == document.getElementById("confirm_password").values) {
        var first_name = document.getElementById("first_name").value;
        var last_name = document.getElementById("last_name").value;
        var email = document.getElementById("email").value;
        var phone = document.getElementById("phone").value;
        var password = document.getElementById("password").value;
        var username = document.getElementById("username").value;

            
            const data = {  "user_name":username,
                            "password":password,
                            "first_name":first_name,
                            "last_name":last_name,
                            "email":email,
                            "phone_number":phone,
                            };

            fetch(`${SERVER_URL}/customer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}