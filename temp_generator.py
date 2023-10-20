import json
import paho.mqtt.client as mqtt
import random
import time

mqtt_broker = "localhost"
mqtt_port = 1883

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")

def generate_temperature():
    return round(random.uniform(20, 30), 2)

client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

while True:
    for device in config['devices']:
        temperature = generate_temperature()
        data = {
            "device_id": device["device_id"],
            "temperature": temperature,
        }
        message = json.dumps(data)

        client.publish(device["topic"], message)
        device["temperature"] = temperature

        print(message)

    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


    time.sleep(60)  


