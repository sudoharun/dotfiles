#!/bin/bash
cpu=`grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}' | awk -F"." '{ print $1 }'`
echo "$cpu%"
