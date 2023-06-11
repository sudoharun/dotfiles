#!/bin/bash
bat() {
  upower -d | grep "percentage" | awk -F":" 'NR==1{ print $2 }' | xargs
}

while [[ true ]]; do
  bat
  sleep 10
done
