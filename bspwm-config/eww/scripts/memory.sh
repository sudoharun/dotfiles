#!/bin/bash
mem=`neofetch | grep Memory | awk -F":" '{ print $2 }' | awk -F"/" '{ print $1 }' | sed -e 's/\x1b\[[0-9;]*m//g' | xargs`
echo -e "$mem"
