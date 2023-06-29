let chatSocket = null;
function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/new-user/");

    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function () {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
    };

    chatSocket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();