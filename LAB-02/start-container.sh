#!/bin/bash

# the default node number is 3
N=${1:-3}

sudo docker network create --driver=bridge hadoop

# start hadoop master container
sudo docker rm -f hadoop-master &> /dev/null
echo "start hadoop-master container..."
sudo docker run -itd \
                --network=hadoop \
                -p 9870:9870 \
                -p 8088:8088 \
                --name hadoop-master \
                --hostname hadoop-master \
                ducviet00/hadoop:1.0 &> /dev/null


# start hadoop worker container
i=1
while [ $i -lt $N ]
do
	sudo docker rm -f hadoop-worker$i &> /dev/null
	echo "start hadoop-worker$i container..."
	sudo docker run -itd \
	                --network=hadoop \
	                --name hadoop-worker$i \
	                --hostname hadoop-worker$i \
	                ducviet00/hadoop:1.0 &> /dev/null
	i=$(( $i + 1 ))
done 

# get into hadoop master container
sudo docker exec -it hadoop-master bash
