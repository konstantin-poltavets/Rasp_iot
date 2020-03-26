
function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    host = "192.168.1.141";
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
console.log("attempting to connect...")
}

// Called when the client connects
function onConnect() {

    topic = "home/poliv/#";

    // Print output for the user in the messages div
 //   document.getElementById("messages").innerHTML += '<span>Subscribing taaaa: ' + topic + '</span><br/>';

    // Subscribe to the requested topic
    client.subscribe(topic);
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
    console.log("onMessageArrived: " + message.payloadString);
    document.getElementById("messages").innerHTML += '<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '</span><br/>';
}

// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}

function onConnect_1() {
	if (document.getElementById("switch").value == "OFF"){
		client.publish("home/bath/esp1/GPIO4_set", "1", 0, false)
		document.getElementById("switch").value = "ON"
		document.getElementById("messages").innerHTML += '<span> Switched ON </span><br/>';
		document.getElementById("switch").style.backgroundColor = "red";
		document.getElementById("switch").style.border = "none";
		}
else if (document.getElementById("switch").value == "ON") { 
		client.publish("home/bath/esp1/GPIO4_set", "0", 0, false)
		document.getElementById("switch").value = "OFF"
		document.getElementById("messages").innerHTML += '<span> Switched OFF </span><br/>';
		document.getElementById("switch").style.backgroundColor = "grey";
		}
}

function onConnect_2() {
	if (document.getElementById("switch_IR").value == "OFF"){
		client.publish("inTopic/Living_Room/IR_strip", "N", 0, false)
		document.getElementById("switch_IR").value = "ON"
		document.getElementById("messages").innerHTML += '<span> Switched ON </span><br/>';
		document.getElementById("switch_IR").style.backgroundColor = "red";
		document.getElementById("switch_IR").style.border = "none";
		}
	else if (document.getElementById("switch_IR").value == "ON") { 
		client.publish("inTopic/Living_Room/IR_strip", "F", 0, false)
		document.getElementById("switch_IR").value = "OFF"
		document.getElementById("messages").innerHTML += '<span> Switched OFF </span><br/>';
		document.getElementById("switch_IR").style.backgroundColor = "grey";
		}
}

function onConnect_g(value) {
	if (document.getElementById("switch_IR").value == "ON"){
		client.publish("inTopic/Living_Room/IR_strip", value, 0, false)
		document.getElementById("messages").innerHTML += '<span> Green colour </span><br/>';
		document.getElementById("switch_IR").style.backgroundColor = value;
		}}
		
		
function onConnect_3(value) {
	if (document.getElementById("switch_esp1").value == "ON"){
		client.publish("sonoff1", "0", 0, false)
		document.getElementById("switch_esp1").value = "OFF"
		document.getElementById("messages").innerHTML += '<span> Switched OFF </span><br/>';
		document.getElementById("switch_esp1").style.backgroundColor = "grey";
		}
else if (document.getElementById("switch_esp1").value == "OFF") { 
		client.publish("sonoff1", "1", 0, false)
		document.getElementById("switch_esp1").value = "ON"
		document.getElementById("messages").innerHTML += '<span> Switched ON </span><br/>';
		document.getElementById("switch_esp1").style.backgroundColor = "red";
		}
}

function onConnect_4(value) {
		client.publish("home/poliv/water", "1", 0, false)
		document.getElementById("messages").innerHTML += '<span> Green colour </span><br/>';
		document.getElementById("switch_water").style.backgroundColor = value;
		}


function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Temperature', 50],
          ['Humidity', 100]
       
        ]);

        var options = {
          width: 400, height: 120,
          redFrom: 90, redTo: 100,
          yellowFrom:75, yellowTo: 90,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

        chart.draw(data, options);

        setInterval(function() {
        //  data.setValue(0, 1, message.payloadString.substr(-5) );

          chart.draw(data, options);
        }, 13000);
        setInterval(function() {
          data.setValue(1, 1, 40 );
          chart.draw(data, options);
        }, 5000);

      }