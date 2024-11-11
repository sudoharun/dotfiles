#!/bin/bash

while [[ $(astal -l | grep "bar" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/bar.py &
done

while [[ $(astal -l | grep "apps" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/apps.py &
done

while [[ $(astal -l | grep "notifications" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/notifications.py &
done

echo done
