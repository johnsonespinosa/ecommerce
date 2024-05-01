const socket = new WebSocket("ws://localhost:8000/ws/stock/");

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(data.message);
    // Updates the UI with the new stock information
};
