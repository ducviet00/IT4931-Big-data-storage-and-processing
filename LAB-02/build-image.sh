#!/bin/bash

echo ""

echo -e "\nbuild docker hadoop image\n"
sudo docker build -t ducviet00/hadoop:1.0 .

echo ""