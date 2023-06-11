#!/bin/bash
wfstr() {
  wifi=`iwconfig wlan0 | grep "Link Quality" | awk -F'=' '{ print $2 }' | awk -F'/' '{ print $1 }'`
  wf=`echo "$wifi*100/70" | bc`
  echo "$wf%"
}

while [[ true ]]; do
  wfstr
  sleep 5
done
