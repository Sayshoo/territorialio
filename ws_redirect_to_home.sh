#!/bin/bash
#ipaddr=$(echo $SSH_CLIENT | awk '{ print $1}')
ipaddr="localhost"
#port=27000
port=8080
#proto="wss"
proto="ws"
echo "ipaddr is $ipaddr"
cp ./scripts/$(ls ./scripts/ -t | head -1) script.js
sed -i "s/wss:\/\/territorial.io\/socket/${proto}:\/\/${ipaddr}:${port}/" script.js
