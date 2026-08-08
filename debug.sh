value=$1
systemctlcommands=("status" "stop" "start")
helpcommands=("h" "help")
rtlcommands=("rtl")
debugcommands=("debug")

if [[ " ${helpcommands[*]} " =~ [[:space:]]${value}[[:space:]] ]]; then
    cat << EOF
$0 start | stop | status -> systemctl 
$0 rtl -> rtl_433 -f 868M -F json -c empty.conf
$0 debug -> python debug.py
EOF
fi

if [[ " ${systemctlcommands[*]} " =~ [[:space:]]${value}[[:space:]] ]]; then
    systemctl $1 weatherstation.service
    systemctl $1 rtl_433-mqtt.service
    systemctl $1 mosquitto.service
fi

if [[ " ${rtlcommands[*]} " =~ [[:space:]]${value}[[:space:]] ]]; then
touch empty.conf
rtl_433 -f 868M -F json -c empty.conf
fi

if [[ " ${debugcommands[*]} " =~ [[:space:]]${value}[[:space:]] ]]; then
source .venv/bin/activate
python debug.py
fi
