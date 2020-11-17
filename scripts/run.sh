#!/bin/bash
echo "Hostname: $1"
echo "Server port: $2"
host=$1
server_port=$2
ca_port=$3
run_server="python3 Server.py $server_port"
run_ca="python3 CA.py $ca_port"
run_bob="python3 Client.py $host $server_port $ca_port"
run_alice="python3 Client.py $host $server_port $ca_port"
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_server}; bash"
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_ca}; bash"
sleep 5
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_bob}; bash"
gnome-terminal --working-directory=$(pwd) -- bash -c "${run_alice}; bash"