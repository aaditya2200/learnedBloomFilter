#!/bin/bash

curl --location 'http://127.0.0.1:5001/consume' &
curl --location 'http://127.0.0.1:5001/produce/prime/1000' &
sleep 20
curl --location 'http://127.0.0.1:5001/attack/1000'
curl --location 'http://127.0.0.1:5001/attack-normal/1000'
curl --location 'http://127.0.0.1:5001/report'
