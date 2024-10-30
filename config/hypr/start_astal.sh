#!/bin/bash

while [[ $(astal -l | grep "bar" | wc -l) < 1 ]]; do
  python $HOME/.config/astal/bar.py &
done

while [[ $(astal -l | grep "notifications" | wc -l) < 1 ]]; do
  python $HOME/.config/astal/notifications.py &
done

echo found
