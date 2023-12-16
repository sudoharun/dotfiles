#!/bin/zsh

# Adding custom aliases and environment variables
echo "# Custom Aliases" >> ~/.zshrc
echo "alias convita='~/.config/scripts/ffmpeg.sh'" >> ~/.zshrc
echo " " >> ~/.zshrc
echo "# Adding stuff to path" >> ~/.zshrc
echo "path+=('$HOME/.local/bin/')" >> ~/.zshrc # Edit this line for your user
echo "path+=('/usr/lib/ccache/bin/')" >> ~/.zshrc
echo "export PATH" >> ~/.zshrc
echo " " >> ~/.zshrc
echo "export TERMINAL='alacritty'" >> ~/.zshrc
echo "export EDITOR='nvim'" >> ~/.zshrc
echo " " >> ~/.zshrc

# If terminal does not open in home directory
echo "cd ~" >> ~/.zshrc

# Source zshrc for changes to take effect in current session
source ~/.zshrc

# ~/.zlogin for automatically starting Hyprland after TTY login
cd ~
mv dotfiles/.zlogin $HOME/

# Bluetooth
yay -S --noconfirm bluez bluez-tools bluez-utils
sudo systemctl enable --now bluetooth

# Pywal
wal -b 121212 -i "/home/$USER/.config/hypr/flowerz.jpg"
