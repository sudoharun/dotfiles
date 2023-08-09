#!/bin/bash

if [[ $1 == increase ]]; then
  command=`brillo -A 10`
elif [[ $1 == decrease ]]; then
  command=`brillo -U 10`
else
  command=""
fi

declare -i inc=`eww get br-num`
$command
declare -i vol=`brillo -G | awk -F"." '{ print $1 }'`

while [[ $inc != $vol ]]; do
  declare -i inc=`eww get br-num`
  declare -i vol=`brillo -G | awk -F"." '{ print $1 }'`
  eww update br-rev=true
  if [[ $inc != $vol ]]; then
    sleep 3
    declare -i inc=`eww get br-num`
    declare -i vol=`brillo -G | awk -F"." '{ print $1 }'`
  else
    sleep 3
    if [[ $vol == $inc ]]; then
      sleep 3
      break 
    else
      declare -i inc=`eww get br-num`
      declare -i vol=`brillo -G | awk -F"." '{ print $1 }'`
      continue
    fi
  fi
done

eww update br-rev=false


