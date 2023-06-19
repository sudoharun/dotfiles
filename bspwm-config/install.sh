#!/bin/bash

# Installing yay
cd ~
git clone https://github.com/Jguer/yay
cd yay
makepkg -si

# Installing other packages
cd ~
yay -S bspwm sxhkd xf86-video-intel wine-staging winetricks neovim lightdm lightdm-webkit2-greeter lightdm-webkit-theme-litarvan lightdm-webkit2-theme-glorious ueberzug udisks2 unrar unzip ttf-jetbrains-mono-nerd ttf-iosevka-nerd ttf-iosevkaterm-nerd steam sof-firmware rofi rofi-emoji scrot dunst picom-ftlabs-git polkit-gnome ranger reflector-simple playerctl pavucontrol pamixer p7zip noto-fonts noto-fonts-cjk noto-fonts-emoji-apple neofetch mpv lxappearance iw htop gimp eww feh dragon-drop deluge-gtk discord ccache brillo alsa-firmware alsa-ucm-conf arandr bluez capitaine-cursors wmctrl xdg-desktop-portal xdg-desktop-portal-gtk zip upower ttf-roboto filezilla

# Setup dotfiles
cd ~/dotfiles/bspwm-config
mv * ~/.config/

# Finish
clear
mpv ~/.config/assets/notifications/sfx/retro-game-notification.wav
echo "Complete by setting up lightdm"
echo "and installing zsh"
sleep 10
