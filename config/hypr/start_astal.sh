#!/bin/bash

while [[ $(astal -l | grep "bar" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/bar/app.py &
done

while [[ $(astal -l | grep "apps" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/apps/app.py &
done

while [[ $(astal -l | grep "notifications" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/notifications/app.py &
done

while [[ $(astal -l | grep "network" | wc -l) < 1 ]]; do
  sleep 0.5
  python $HOME/.config/astal/network/app.py &
done

echo done
