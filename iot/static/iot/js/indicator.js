function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    host = "82.144.207.13";
    port = "1884";

    // Print output for the user in the messages div
   document.getElementById("messages").innerHTML = '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
   document.getElementById("messages").innerHTML = '<span>Using the following client value: ' + clientID + '</span><br/>';

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
         $("#seven-seg-array_v").sevenSeg({ digits: 4, value: 0000 });

	$("#seven-seg-array_s").sevenSeg({ digits: 2, value: 00, colorOff: "#003200", colorOn: "Lime",  decimalPoint: true});
    $("#seven-seg-array_m").sevenSeg({ digits: 2, value: 00, colorOff: "#003200", colorOn: "Lime",  decimalPoint: true});
    $("#seven-seg-array_h").sevenSeg({ digits: 2, value: 00, colorOff: "#003200", colorOn: "Lime",  decimalPoint: true});
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    document.getElementById("messages").innerHTML += '<span>ERROR: Connection lost</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("messages").innerHTML += '<span>ERROR: ' + + responseObject.errorMessage + '</span><br/>';
    }
}

// Called when a message arrives
function onMessageArrived(message) {
let payload = JSON.parse(message.payloadString);

   // console.log(payload);
    document.getElementById("messages").innerHTML += '<span>Topic: ' + message.destinationName + '  '+ message.payloadString +'| '  + '</span><br/>';
//let t = payload["time"];


	 $("#seven-seg-array").sevenSeg({ digits: 4, value: payload["distance"] });
	 $("#seven-seg-array_v").sevenSeg({ digits: 4, value: payload["speed"], decimalPoint: true });

let time_s = 0;
let time_m = 0;

let  time_row = parseInt(payload["time"]);


if (time_row  > 59) { time_s = time_row % 60; }
else { time_s = time_row; }

if (time_s < 10 ){time_s = '0' + time_s.toString();}

let time_mm = Math.floor(time_row / 60);


if (time_mm  > 59) { time_m = time_mm % 60; }
else { time_m = time_mm; }


if (time_m < 10  ){time_m = '0' + time_m.toString();}

let time_h = Math.floor(time_row / 60/60);



	$("#seven-seg-array_h").sevenSeg({ digits: 2, value: time_h.toString() , decimalPoint: true});

	$("#seven-seg-array_m").sevenSeg({ digits: 2, value: time_m.toString() , decimalPoint: true});

	$("#seven-seg-array_s").sevenSeg({ digits: 2, value: time_s.toString() , decimalPoint: true});

document.getElementById('messages').scrollTop = 9999999;

	}



// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}



//	setInterval('show()',1000);


