#!/bin/bash

ls

echo Start?
read first_ep
echo End?
read last_ep

one=1

while (( $first_ep <= $last_ep )); do
  ffmpeg -i $first_ep.mp4 -vf scale=960:544 ep$first_ep.mp4
  rm $first_ep.mp4
  first_ep=$(($first_ep + $one))
  clear
done

ls
echo "Conversion Complete"
notify-send "convita is done"
mpv ~/.config/assets/notifications/sfx/retro-game-notification.wav
