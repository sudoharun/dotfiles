#!/bin/bash

hour=`date "+%H"`

echo "$hour"
if [[ $hour -gt 6 && $hour -lt 20 ]]; then
  echo "Day"
else
  echo "Night"
fi
