#!/bin/bash
sudo apt update
sudo apt install python3.11
python3.9 --version
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
python3.11 -m pip install --upgrade pip