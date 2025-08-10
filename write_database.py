"""Write data from a Bresser weather station to a sqlite3 database"""

import logging
from types import SimpleNamespace
import datetime
import sqlite3
import pathlib
import paho.mqtt.enums as enums
import paho.mqtt.client as mqtt 
from common import DBPATH, DBFIELDS, DBVALUES


logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s", level=logging.INFO)
LOGGER = logging.getLogger()


QOS = 0
TOPIC = [(f"rtl_433/46672/{key}", QOS) for key in DBFIELDS]

BROKER_ADDRESS = "127.0.0.1" 
PORT = 1883 
LENGTH = 10


def on_message(client, userdata, message): 
    msg = str(message.payload.decode("utf-8")) 
    key = message.topic.split("/")[-1]
    if key == "time":
        userdata.count += 1
    LOGGER.info(f"message {userdata.count}/{LENGTH} received: {msg!r}, topic: {message.topic}") 
    userdata.data[key].append(DBFIELDS[key]["cfn"](msg))
    #
    if all([len(item) >= LENGTH for item in userdata.data.values()]):
        for key in userdata.data:
            if key == "time":
                userdata.data["time"] = userdata.data["time"][-1]
                # find the time 1 day before
                twentyfour_before = userdata.data["time"] - 24 * 60 * 60
                userdata.cursor.execute(f"SELECT rain_mm FROM weather WHERE time <= ? ORDER BY time DESC LIMIT 1", (twentyfour_before, ))
                userdata.rain_mm_reference = cursor.fetchone()[0]
                LOGGER.critical(f"rain reference -> {userdata.rain_mm_reference}")
            else:
                userdata.data[key] = sum(userdata.data[key][:LENGTH]) / LENGTH
                if key == "rain_mm" and userdata.rain_mm_reference is not None:
                    rain_per_day_mm = userdata.data[key] - userdata.rain_mm_reference
                    LOGGER.critical(f"rain per day -> {rain_per_day_mm}")
                    userdata.cursor.execute("UPDATE rain_per_day SET rain_per_day_mm = ? WHERE idx = 0", (rain_per_day_mm, ))
        LOGGER.critical(f"db <- {userdata.data}")
        userdata.cursor.execute(f"INSERT OR IGNORE INTO weather VALUES ({DBVALUES})", userdata.data)
        userdata.connection.commit()
        for key in userdata.data:
            userdata.data[key] = [] 
        userdata.count = 0
    
    
def on_connect(client, userdata, flags, rc, properties): 
    LOGGER.info(f"Connected to MQTT Broker {BROKER_ADDRESS}") 
    client.subscribe(TOPIC) 
    
    
if __name__ == "__main__": 
    # sqlite stuff
    connection = sqlite3.connect(DBPATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    s = ",".join(f"{key} {DBFIELDS[key]['db']}" for key in DBFIELDS)    
    cursor.execute(f"CREATE TABLE IF NOT EXISTS weather ({s})")
    s = ",".join(DBFIELDS)
    # avoid writing duplicate items
    cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS uniquedata ON weather ({s})")
    # create trigger to delete items older than 1 year
    cursor.execute("""CREATE TRIGGER IF NOT EXISTS deletelastyear AFTER INSERT ON weather
                   BEGIN
                   DELETE FROM weather WHERE (julianday('now') - julianday(time, 'unixepoch')) > 365;
                   END
                   """)
    cursor.execute("CREATE TABLE IF NOT EXISTS rain_per_day (idx INT, rain_per_day_mm REAL)")
    connection.commit()
        
    # set userdata for paho client
    userdata = SimpleNamespace(cursor=cursor, connection=connection, data=dict((key, []) for key in DBFIELDS), rain_mm_reference=None, count=0)
    # mqtt stuff
    client = mqtt.Client(enums.CallbackAPIVersion(2), userdata=userdata) 
    client.on_connect = on_connect 
    client.on_message = on_message 
    client.connect(BROKER_ADDRESS, PORT) 
    client.loop_forever()