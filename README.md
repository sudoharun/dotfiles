# Retro-esque, a Hyprland config

<div align="center">
  <img src="./assets/hyprland1.png">
  <img src="./assets/hyprland2.png">
  <img src="./assets/hyprland3.png">
</div>

## How to install
First update your system:
```
sudo pacman -Syu
```

Then you can do the following:
```
sudo pacman -S python git
git clone -b retroesque https://github.com/sudo-harun/dotfiles.git
cd dotfiles
python install.py
```

To show the shutdown menu in the bar when pressing the power button, you need to edit `/etc/systemd/logind.conf`. You need to edit the line `#HandlePowerKey=poweroff` to `HandlePowerKey=ignore`. The change will take effect after a reboot.
