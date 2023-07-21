#!/bin/bash
pwr=`bluetoothctl show 6C:6A:77:DC:4B:B3 | grep "Powered" | awk -F":" '{ print $2 }' | xargs`

if [[ $pwr == "yes" ]]; then
  echo 󰂯
else
  echo 󰂲
fi
