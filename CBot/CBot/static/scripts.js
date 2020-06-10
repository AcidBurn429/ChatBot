function startConnection() {
    var xmlhttp;

    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    return xmlhttp;
}

function playSound(id) {
    var element = document.getElementById(id);
    element.play();
    setTimeout(element.pause(), 4000);
}

function start(tok) {
    var conn = startConnection();

    conn.onreadystatechange = function get_start() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            if (this.responseText == 'TRUE') {
                window.location.replace("/1");
            }
        }
    };

    conn.open("POST", "/0", true);
    conn.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    conn.send("instruction=FIRST&token=" + tok);
}