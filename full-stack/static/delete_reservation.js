window.onload=function(){
    console.log("script loaded")
    var mod_button = document.getElementById("delete_id_button");
    mod_button.addEventListener("click", del_res_func);
}

var SERVER_URL = "http://127.0.0.1:5000"

async function del_res_func(){
    console.log("Func");
    var id = document.getElementById("reservation_id").value;

        const data = {  "id":id,
                        };
                        

        const response = await fetch(`${SERVER_URL}/delete_reservation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
    })
    if (response.ok) {
        window.alert("Reservation cancelled.");
        window.open("http://127.0.0.1:5000/reservations_si","_self");
    }
    else {
        console.log("error");
    }

}