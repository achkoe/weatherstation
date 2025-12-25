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

  sudo cp weatherstation.service /etc/systemd/system/

  sudo systemctl start weatherstation.service
  sudo systemctl enable weatherstation.service
  sudo systemctl status weatherstation.service

from https://grafana.com/tutorials/install-grafana-on-raspberry-pi/

  sudo mkdir -p /etc/apt/keyrings/
  wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

  echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

  sudo apt-get update
  sudo apt-get install -y grafana

  sudo /bin/systemctl enable grafana-server
  sudo /bin/systemctl start grafana-server

now

  http://<ip address>:3000

  grafana-cli plugins install frser-sqlite-datasource  
  sudo /bin/systemctl restart grafana-server

now configure database at Home / Connections / Data sources / frser-sqlite-datasource