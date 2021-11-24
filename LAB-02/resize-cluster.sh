#!/bin/bash

# N is the node number of hadoop cluster
N=$1

if [ $# = 0 ]
then
	echo "Please specify the node number of hadoop cluster!"
	exit 1
fi

# change slaves file
i=1
rm config/workers
while [ $i -lt $N ]
do
	echo "hadoop-worker$i" >> config/workers
	((i++))
done 

echo ""

echo -e "\nbuild docker hadoop image\n"

# rebuild ducviet00/hadoop image
sudo docker build -t ducviet00/hadoop:1.0 .

echo ""
