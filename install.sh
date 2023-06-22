#!/bin/bash

# Installing yay
cd ~
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# Installing other packages
cd ~
yay -S kitty zsh neovim firefox-developer-edition lightdm lightdm-webkit2-greeter lightdm-webkit-theme-litarvan lightdm-webkit2-theme-glorious ueberzug udisks2 unrar unzip ttf-jetbrains-mono-nerd ttf-iosevka-nerd ttf-iosevkaterm-nerd sof-firmware rofi rofi-emoji scrot dunst picom polkit-gnome ranger reflector-simple playerctl pavucontrol pamixer p7zip noto-fonts noto-fonts-cjk noto-fonts-emoji-apple neofetch mpv lxappearance-gtk3 iw htop gimp feh dragon-drop deluge-gtk discord ccache brillo alsa-firmware alsa-ucm-conf arandr bluez capitaine-cursors wmctrl zip upower ttf-roboto filezilla xdotool xorg-xprop xorg-xsetroot xdg-desktop-portal

# Helps with screen tearing
# Remove if this doesn't apply
yay -S xf86-video-intel

# Setup dotfiles
mkdir ~/.config
cd ~/dotfiles/bspwm-config
mv * ~/.config/

# Enabling execution permissions
cd ~/.config
chmod +x bspwm/bspwmrc
chmod +x bspwm/fullscreen.sh
chmod +x bspwm/scrot.sh
chmod +x sxhkd/sxhkdrc
chmod +x dunst/dunstrc
chmod +x ranger/scope.sh
chmod +x scripts/ffmpeg.sh
chmod +x scripts/scrot.sh
chmod +x wmstuff/minimizer.sh
chmod +x eww/scripts/battery.sh
chmod +x eww/scripts/bluetooth.sh
chmod +x eww/scripts/kitty.sh
chmod +x eww/scripts/toggle-cc.sh
chmod +x eww/scripts/toggle-wifi.sh
chmod +x eww/scripts/volume.sh
chmod +x eww/scripts/wifi.sh
chmod +x eww/scripts/window-name.sh
chmod +x eww/scripts/workspaces.sh

# Setup ohmyzsh
cd ~
echo "Last step is setting up ohmyzsh"
sleep 3
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
