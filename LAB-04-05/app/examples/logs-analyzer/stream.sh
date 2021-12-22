#!/bin/sh
set -o nounset
set -o errexit
test $# -eq 1 || ( echo "Incorrect number of arguments" ; exit 1 )
file="$1"

network_port=9999
lines_in_batch=100
interval_sec=10

n_lines=$(cat $file | wc -l) 
cursor=1

while test $cursor -le $n_lines 
do
    tail -n +$cursor $file | head -$lines_in_batch | nc -l -p $network_port -q 0
    cursor=$(($cursor + $lines_in_batch))
    sleep $interval_sec 
done