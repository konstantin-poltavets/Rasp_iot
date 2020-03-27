
var tim_0 = Date.now();
function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    host = "82.144.207.13";
    port = "1884";

    // Print output for the user in the messages div
    document.getElementById("messages").innerHTML += '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
    document.getElementById("messages").innerHTML += '<span>Using the following client value: ' + clientID + '</span><br/>';

    // Initialize new Paho client connection
    client = new Paho.MQTT.Client(host, Number(port), clientID);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({onSuccess:onConnect,
                useSSL: false,
                keepAliveInterval: 100});
console.log("attempting to connect...");




}

// Called when the client connects
function onConnect() {

    topic = "home/orbitrack/impulse";

    client.subscribe(topic);
         $("#seven-seg-array").sevenSeg({ digits: 4, value: 0000 });
	$("#seven-seg-array_1").sevenSeg({ digits: 3, value: 0000, colorOff: "#003200",
		colorOn: "Lime",  });

}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    document.getElementById("messages").innerHTML += '<span>ERROR: Connection lost</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("messages").innerHTML += '<span>ERROR: ' + + responseObject.errorMessage + '</span><br/>';
    }
}

var t = 0;

// Called when a message arrives
function onMessageArrived(message) {
    console.log(message.payloadString);
    document.getElementById("messages").innerHTML += '<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '</span><br/>';
	t = message.payloadString;
	 $("#seven-seg-array").sevenSeg({ digits: 4, value: t });
var tim = Math.round((Date.now() - tim_0)/1000 );
var time_2 = tim.toString();
console.log(time_2);

	$("#seven-seg-array_1").sevenSeg({ digits: 4, value: time_2 , decimalPoint: true});
	}



// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}


function onConnect_g(value) {
	if (document.getElementById("switch_IR").value == "ON"){
		client.publish("inTopic/Living_Room/IR_strip", value, 0, false)
		document.getElementById("messages").innerHTML += '<span> Green colour </span><br/>';
		document.getElementById("switch_IR").style.backgroundColor = value;
		}}
		


//	setInterval('show()',1000);
	

