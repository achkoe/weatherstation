"""Write data from a Bresser weather station to a sqlite3 database"""

import logging
from types import SimpleNamespace
import datetime
import sqlite3
import pathlib
from dotenv import dotenv_values
import paho.mqtt.enums as enums
import paho.mqtt.client as mqtt 

DBFIELDS = ["time", "model", "id", "temperature_C", "humidity", "wind_max_m_s", "wind_avg_m_s", "wind_dir_deg", "rain_mm", "light_klx", "light_lux", "uv", "battery_ok", "mic"]

loglevel = logging.INFO
logging.basicConfig(format="%(levelname)s:%(asctime)s:%(lineno)d:%(message)s", level=loglevel)
LOGGER = logging.getLogger()


QOS = 0
TOPIC = [(f"rtl_433/46672/{key}", QOS) for key in DBFIELDS]

BROKER_ADDRESS = "127.0.0.1" 
PORT = 1883 
LENGTH = 10


def on_message(client, userdata, message): 
    msg = str(message.payload.decode("utf-8")) 
    key = message.topic.split("/")[-1]
    LOGGER.info(f"received  topic: {message.topic:30} -> {msg!r}") 
    
    
def on_connect(client, userdata, flags, rc, properties): 
    LOGGER.info(f"Connected to MQTT Broker {BROKER_ADDRESS}") 
    client.subscribe(TOPIC) 
    
    
if __name__ == "__main__": 
    # set userdata for paho client
    userdata = SimpleNamespace()
    # mqtt stuff
    client = mqtt.Client(enums.CallbackAPIVersion(2), userdata=userdata) 
    client.on_connect = on_connect 
    client.on_message = on_message 
    client.connect(BROKER_ADDRESS, PORT) 
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("terminated by Ctrl+C")