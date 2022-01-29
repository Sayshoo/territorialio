#!/bin/bash
echo "Trying to reach territorial.io"
# grep -Pzo "(?s)<script>.*<\/script>" script.js 
# tr -d '\000' < parsed.js | xxd | cut -c 10-50 
dateVar=$(date "+%d-%m-%y-%H-%M-%S")
archiveFileName="./scripts/${dateVar}-script.js"
curl https://territorial.io | grep -Pzo "(?s)<script>.*<\/script>" | \
 tr -d '\000' | grep -v "</script>" | grep -v "<script>" > $archiveFileName
cp $archiveFileName ./script.js
