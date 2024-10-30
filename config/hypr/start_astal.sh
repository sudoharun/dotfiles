#!/bin/bash

while [[ $(astal -l | grep "bar" | wc -l) < 1 ]]; do
  python $HOME/.config/astal/bar.py &
  sleep 0.5
done

while [[ $(astal -l | grep "notifications" | wc -l) < 1 ]]; do
  python $HOME/.config/astal/notifications.py &
  sleep 0.5
done

echo done
