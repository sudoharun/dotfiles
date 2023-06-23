#!/bin/bash

echo "exec bspwm" >> ~/.xinitrc

# Adding custom aliases and environment variables
echo "# Custom Aliases" >> ~/.zshrc
echo "alias convita='~/.config/scripts/ffmpeg.sh'" >> ~/.zshrc
echo "alias myscrot='scrot ~/Pictures/Screenshots/%d%b::%H:%M:%S.png'" >> ~/.zshrc
echo " " >> ~/.zshrc
echo "# Adding stuff to path" >> ~/.zshrc
echo "path+=('/home/harun/.local/bin/')" >> ~/.zshrc # Edit this line for your user
echo "path+=('/usr/lib/ccache/bin/')" >> ~/.zshrc
echo "export PATH" >> ~/.zshrc
echo " " >> ~/.zshrc
echo "export TERMINAL='kitty'" >> ~/.zshrc
echo "export EDITOR='nvim'" >> ~/.zshrc
echo " " >> ~/.zshrc

# If terminal does not open in home directory
echo "cd ~" >> ~/.zshrc


# Prevent looooong application loading times
systemctl mask --user --now xdg-desktop-portal.service
systemctl mask --user --now xdg-desktop-portal-gtk.service
systemctl mask --now xdg-desktop-portal.service
systemctl mask --now xdg-desktop-portal-gtk.service

# Bluetooth
yay -S bluez bluez-tools bluez-utils
systemctl enable --now bluetooth

# Installing custom rofi launchers
cd ~
git clone https://github.com/adi1090x/rofi.git
~/rofi/setup.sh
rm -r ~/rofi

startx
