#!/bin/bash
echo "Starting webserver"
kill $(pgrep -f "python3 -m http.server") >/dev/null 2>&1
kill $(pgrep -f "python3 -u httpsServer.py") >/dev/null 2>&1
#python3 -u -m http.server >webserver.log 2>webserver.error &
python3 -u httpsServer.py >webserver.log 2>webserver.error &
echo "Retrieving game's javascript"
./getScript.sh >/dev/null 2>&1 
echo "Redirecting websocket connection to this container"
./ws_redirect_to_container.sh >/dev/null 2>&1

