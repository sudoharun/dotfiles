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
    "xdg-desktop-portal-gnome"
    "wev"
    "foot"
    "foot-terminfo"
    "noto-fonts"
    "noto-fonts-cjk"
    "ttf-nerd-fonts-symbols"
    "ttf-fantasque-nerd"
    "ttf-iosevka-term"
    "ttf-apple-emoji"
    "xwayland-satellite"
    "cliphist"
    "wl-clipboard"
    "btop"
    "python"
    "dart-sass"
    "waypaper"
    "firefox"
    "mpv"
    "bibata-cursor-theme-bin"
    "papirus-icon-theme"
    "hyprlock"
    "hypridle"
    "nwg-look"
    "qt5ct"
    "qt6ct"
    "swww"
    "imv"
    "wl-clipboard"
    "niri-git"
    "ignis-git"
    "adw-gtk-theme"
    "kvantum"
    "kvantum-qt5"
    "kvantum-theme-libadwaita-git"
    "morewaita-icon-theme"
    "thunar"
    "gvfs"
    "tumbler"
    "thunar-volman"
    "thunar-archive-plugin"
    "thunar-media-tags-plugin"
    "xarchiver",
    "python-rapidfuzz"
)

audio=(
    "pipewire"
    "pipewire-pulse"
    # "pipewire-jack"
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
    "zed"
    "gimp"
    "deluge-gtk"
    "handbrake"
    "discord"
    "steam"
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

sudo pacman -Syyu

if [ ! -f "/usr/bin/yay" ]; then
    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si --noconfirm
    cd ..
    rm -r yay
fi

yay -S --noconfirm rustup
rustup default stable

yay -S --noconfirm $install_str
yay -Rnsc --noconfirm $(yay -Qdtq)
yay -Sc --noconfirm

cd $dots_dir
cp ./home/bashrc $HOME/.bashrc
cp -r ./config/* $HOME/.config/

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
gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'
# kvantummanager --set KvLibadwaitaDark

clear
echo "Installation complete. Reboot, set Kvantum theme, set qt6ct style to kvantum-dark"
