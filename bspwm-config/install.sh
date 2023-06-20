#!/bin/bash

# Installing yay
cd ~
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# Installing other packages
cd ~
yay -S zsh wine-staging winetricks neovim lightdm lightdm-webkit2-greeter lightdm-webkit-theme-litarvan lightdm-webkit2-theme-glorious ueberzug udisks2 unrar unzip ttf-jetbrains-mono-nerd ttf-iosevka-nerd ttf-iosevkaterm-nerd steam sof-firmware rofi rofi-emoji scrot dunst picom-jonaburg-git polkit-gnome ranger reflector-simple playerctl pavucontrol pamixer p7zip noto-fonts noto-fonts-cjk noto-fonts-emoji-apple neofetch mpv lxappearance-gtk3 iw htop gimp feh dragon-drop deluge-gtk discord ccache brillo alsa-firmware alsa-ucm-conf arandr bluez capitaine-cursors wmctrl zip upower ttf-roboto filezilla xdotool xorg-xprop

# Setup dotfiles
cd ~/dotfiles/bspwm-config
mv * ~/.config/

# Enabling execution permissions
cd ~/.config
chmod +x bspwm/bspwmrc
chmod +x bspwm/eww-bar-fullscreen.sh
chmod +x bspwm/scrot.sh
chmod +x sxhkd/sxhkdrc
chmod +x dunst/dunstrc
chmod +x ranger/scope.sh
chmod +x scripts/ffmpeg.sh
chmod +x scripts/scrot.sh
chmod +x wmstuff/minimizer.sh

# Setup ohmyzsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Finish
mpv ~/.config/assets/notifications/sfx/retro-game-notification.wav
echo "Complete by setting up lightdm"
echo "and installing zsh"
sleep 3
echo "Rebooting..."
sleep 2
reboot
