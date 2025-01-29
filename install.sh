#!/bin/bash

dots_dir=`dirname $(realpath $0)`

dependencies=(
    "qt5-wayland"
    "qt6-wayland"
    "linux-headers"
    "reflector-simple"
    "bash-completion"
    "ccache"
    "brightnessctl"
    "iw"
    "wireless_tools"
    "zip"
    "unzip"
    "unrar"
    "p7zip"
    "upower"
    "udisks2"
    "neovim"
    "polkit-gnome"
    "xdg-desktop-portal-gtk"
    "grim"
    "slurp"
    "wev"
    "foot"
    "foot-terminfo"
    "noto-fonts"
    "noto-fonts-cjk"
    "ttf-roboto"
    "ttf-ibm-plex"
    "ttf-fantasque-nerd"
    "ttf-iosevka-term"
    "ttf-apple-emoji"
    "wofi"
    "wofi-emoji"
    "cliphist"
    "wl-clipboard"
    "btop"
    "python",
    "git",
    "rustup"
    "libastal-git"
    "libastal-io-git"
    "libastal-meta"
    "dart-sass"
    "waypaper"
    "firefox"
    "mpv"
    "bibata-cursor-theme-bin"
    "papirus-icon-theme"
    "hyprlang"
    "hyprcursor"
    "hyprland"
    "xdg-desktop-portal-hyprland"
    "hyprlock"
    "hypridle"
    "nwg-look"
    "qt5ct"
    "swww"
    "imv"
    "wl-clipboard"
    "zed"
    "meson"
    "cpio"
    "cmake"
    "adw-gtk-theme"
    "kvantum-theme-libadwaita-git"
    "morewaita-icon-theme"
)

audio=(
    "pipewire"
    "pipewire-pulse"
    #"pipewire-jack"
    "pipewire-alsa"
    "sof-firmware"
    "pavucontrol"
    "pamixer"
    "alsa-firmware"
    "alsa-ucm-conf"
)

power_management=(
    "power-profiles-daemon"
)

optional=(
    "downgrade"
    "dosfstools"
    "filezilla"
    "gimp"
    "deluge-gtk"
    "handbrake"
    # "vesktop-bin"
)

cd $HOME

for i in ${!optional[@]}; do
    echo "Would you like to install '${optional[i]}'? [Y/n]"
    read answer
    if [[ "$answer" == "n" ]]; then
        unset 'optional[i]'
    fi
done

install_str=""

for pkg in ${dependencies[@]}; do
    install_str+="$pkg "
done

for pkg in ${audio[@]}; do
    install_str+="$pkg "
done

for pkg in ${power_management[@]}; do
    install_str+="$pkg "
done

for pkg in ${optional[@]}; do
    install_str+="$pkg "
done

cd $HOME
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..
rm -r yay

yay -S --noconfirm install_str
yay -Rnsc --noconfirm $(yay -Qdtq)
yay -Sc --noconfirm

cd $dots_dir
cp -r ./config/* $HOME/.config/
chmod u+x $HOME/.config/hypr/start_astal.sh

cd $HOME

if [ ! -d "$HOME/.local/share/fonts/Rubik" ]; then
    mkdir -p $HOME/.local/share/fonts/Rubik
fi

git clone https://github.com/googlefonts/rubik.git
cd rubik
cp fonts/variable/Rubik*.ttf $HOME/.local/share/fonts/Rubik
fc-cache -fv
gsettings set org.gnome.desktop.interface font-name 'Rubik 11'
cd ..
rm -rf rubik

gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3-dark'
gsettings set org.gnome.desktop.interface icon-theme 'MoreWaita'
kvantummanager --set KvLibadwaitaDark
