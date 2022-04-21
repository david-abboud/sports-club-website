window.onload = function () {
    console.log("script loaded")
    var fi_button = document.getElementById("field_button");
    fi_button.addEventListener("click", fi_func);

    var ev_button = document.getElementById("event_button");
    ev_button.addEventListener("click", ev_func);
}

var SERVER_URL = "http://127.0.0.1:5000"

async function fi_func() {
    console.log("log0")
    userToken = getUserToken();
    var field;
    var field_name = document.getElementById("field_select").value;
    var date = document.getElementById("Test_DatetimeLocal").value;

    if (field_name == "basketball") {
        field = 1;
    }
    if (field_name == "tennis") {
        field = 2;
    }
    if (field_name == "boxing") {
        field = 3;
    }
    if (field_name == "volleyball") {
        field = 4;
    }
    if (field_name == "football") {
        field = 5;
    }


    console.log(date);
    console.log(field_name);
    console.log(field);

    console.log("log1")

    const data = {
        "type": 1,
        "field_id": field,
        "event_id": null,
        "reservation_time": date
    };
    console.log("log2")
    if (field_name != "" && date != "") {
        const response = await fetch(`${SERVER_URL}/reservation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify(data),
        })
        console.log('status code: ', response.status); // 👉️ 200

        if (response.ok) {
            console.log(response);
            window.alert("Field Booked.");
        }
    }



}
async function ev_func() {
    console.log("log0")
    userToken = getUserToken();
    var event;
    var event_name = document.getElementById("event_select").value;

    if (event_name == "By the pool with sax") {
        event = 0;
    }
    if (event_name == "Mega vs speed (Football game)") {
        event = 1;
    }
    if (event_name == "Basketball workshop") {
        event = 2;
    }
    if (event_name == "Zinedine zidane freestyle show") {
        event = 3;
    }
    if (event_name == "Mohammad Ali vs David Abboud (boxing match)") {
        event = 4;
    }

    console.log(event_name);
    console.log(event);

    console.log("log1")

    const data = {
        "type": 0,
        "field_id": null,
        "event_id": event,
        "reservation_time": null
    };
    console.log("log2")
    if (event_name != "") {
        const response = await fetch(`${SERVER_URL}/reservation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify(data),
        })
        console.log('status code: ', response.status); // 👉️ 200

        if (response.ok) {
            console.log(response);
            window.alert("Event Booked.");
        }
    }



}
function getUserToken() {
    return localStorage.getItem("TOKEN");
  }


