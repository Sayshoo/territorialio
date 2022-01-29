#!/bin/bash
ipaddr=$(curl ifconfig.me 2>/dev/null)
port=27000
echo "ipaddr is $ipaddr"
cp ./scripts/$(ls ./scripts/ -t | head -1) script.js
sed -i "s/wss:\/\/territorial.io\/socket/wss:\/\/${ipaddr}:${port}/" script.js
