#!/bin/zsh

# Adding custom aliases and environment variables
echo "# Custom Aliases" >> ~/.zshrc
echo "alias convita='~/.config/scripts/ffmpeg.sh'" >> ~/.zshrc
echo " " >> ~/.zshrc
echo "# Adding stuff to path" >> ~/.zshrc
echo "path+=('/home/harun/.local/bin/')" >> ~/.zshrc # Edit this line for your user
echo "path+=('/usr/lib/ccache/bin/')" >> ~/.zshrc
echo "export PATH" >> ~/.zshrc
echo " " >> ~/.zshrc
echo "export TERMINAL='wezterm'" >> ~/.zshrc
echo "export EDITOR='nvim'" >> ~/.zshrc
echo " " >> ~/.zshrc

# If terminal does not open in home directory
echo "cd ~" >> ~/.zshrc

# Source zshrc for changes to take effect in current session
source ~/.zshrc

# Bluetooth
yay -S bluez bluez-tools bluez-utils
systemctl enable --now bluetooth

# Installing custom rofi launchers
cd ~
git clone https://github.com/adi1090x/rofi.git
cd ~/rofi
./setup.sh
rm -rf ~/rofi
