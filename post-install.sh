#!/bin/bash

echo "exec bspwm" >> ~/.xinitrc

# If terminal does not open in home directory
echo "cd ~" >> ~/.zshrc

# Adding custom aliases


# Prevent looooong application loading times
systemctl mask --user --now xdg-desktop-portal.service
systemctl mask --user --now xdg-desktop-portal-gtk.service
systemctl mask --now xdg-desktop-portal.service
systemctl mask --now xdg-desktop-portal-gtk.service

# Bluetooth
yay -S bluez bluez-tools bluez-utils
systemctl enable bluetooth

# Installing custom rofi launchers
cd ~
git clone https://github.com/adi1090x/rofi.git
~/rofi/setup.sh
rm -r ~/rofi

startx
