import paho.mqtt.client as mqtt
from poller import Poller
from players import VLCMediaPlayer


#DEVICE_ID = '2d4a563e-cbda-4a8e-b1bc-5e0f8a117918'
DEVICE_ID = '3de90b9e-f304-43b5-aa17-1544fe780a63'
DEVICE_TYPE = 3
TOPIC = f'digital-signage/event/{DEVICE_ID}'

vlc_player = VLCMediaPlayer()

def on_poller_done():
    vlc_player.refresh()
    vlc_player.play()

poller = Poller(DEVICE_TYPE)
poller.set_dir()
poller.set_media_player(on_poller_done)

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    poller.run()
    client.subscribe(TOPIC)  # Subscribe to the topic “digitest/test1”, receive any messages published on it

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    poller.run()
    #if str(msg.payload) == 'on_change_content': polling.main(DEVICE_TYPE)

import time

time.sleep(10)

vlc_player.play()

client = mqtt.Client("digital-signage")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect('ibncorp.co.id', 1883)
client.loop_forever()  # Start networking daemon
