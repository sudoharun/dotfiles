#!/bin/bash

cd ~/dotfiles
mv config/wezterm.lua ~/.wezterm.lua

# Installing yay
cd ~
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# Installing other packages
cd ~
yay -S hyprland qt5-wayland qt6-wayland linux-headers wezterm zsh neovim firefox-developer-edition udisks2 unrar unzip ttf-jetbrains-mono-nerd sof-firmware rofi rofi-emoji dunst polkit-gnome ranger reflector-simple playerctl pavucontrol pamixer p7zip noto-fonts noto-fonts-cjk noto-fonts-emoji-apple neofetch mpv iw htop gimp dragon-drop deluge-gtk webcord ccache brillo alsa-firmware alsa-ucm-conf bluez capitaine-cursors zip upower ttf-roboto filezilla xdg-desktop-portal xdg-desktop-portal-gtk xdg-desktop-portal-hyprland-git papirus-icon-theme swaylock wireless_tools wev nwg-look-bin openshot imv hyprpaper hyprshot dosfstools

# Installing mantis gtk theme
cd ~
mkdir ~/.themes
git clone https://github.com/mantissa-/mantis-theme.git
cd mantis-theme
mv Manti* ~/.themes
cd ~
rm -rf mantis-theme

# Setup dotfiles
mkdir ~/.config
cd ~/dotfiles/config
mv * ~/.config/

# Enabling execution permissions
cd ~
chmod +x dotfiles/wine.sh
chmod +x dotfiles/post-install.sh
cd ~/.config
chmod +x hypr/autostart.sh
chmod +x dunst/dunstrc
chmod +x ranger/scope.sh
chmod +x scripts/ffmpeg.sh
chmod +x eww/scripts/activewindowname
chmod +x eww/scripts/bluetooth
chmod +x eww/scripts/battery
chmod +x eww/scripts/brightness
chmod +x eww/scripts/cpu
chmod +x eww/scripts/wezterm
chmod +x eww/scripts/memory
chmod +x eww/scripts/vertical-battery
chmod +x eww/scripts/vertical-workspaces
chmod +x eww/scripts/volume
chmod +x eww/scripts/wifi
chmod +x eww/scripts/workspaces

# Installing eww and rust using rustup
cd ~
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup install nightly
cd ~
yay -S eww-wayland-git

# Setup ohmyzsh
cd ~
cd ~
echo "Last step is setting up ohmyzsh"
sleep 3
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
