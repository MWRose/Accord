#!/bin/bash
echo "Hostname: $1"
echo "Server port: $2"
host=$1
port=$2
run_server="python3 Server.py $port"
run_bob="python3 Client.py $host $port"
run_alice="python3 Client.py $host $port"
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_server}; bash"
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_bob}; bash"
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_alice}; bash"
