# weatherstation

Software to read and archive data from a Bresser weather station


## Requirements

- rtl_433, see https://triq.org/rtl_433/

- mosquitto

- Eclipse Paho™ MQTT Python Client, see https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html#eclipse-paho-mqtt-python-client


## Installation

  sudo apt install rtl-433

  sudo apt install mosquitto
  sudo systemctl enable mosquitto.service

  git clone git@github.com:achkoe/weatherstation.git
  cd weatherstation/

  python -m venv .venv
  . .venv/bin/activate
  
  pip install paho-mqtt

  sudo mkdir /etc/rtl_433
  sudo cp rtl_433.conf /etc/rtl_433/

  sudo systemctl start rtl_433-mqtt.service 
  sudo systemctl enable rtl_433-mqtt.service 
  sudo systemctl status rtl_433-mqtt.service 

  sudo mkdir /opt/weatherstation
  sudo chmod o=rwx /opt/weatherstation

For testing:
  python write_database.py