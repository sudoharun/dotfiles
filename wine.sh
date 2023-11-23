#!/bin/bash

clear
echo "WARNING: This script is intended to run inside of a window manager or desktop environment (this will not work in a TTY!!)"
echo "If you are not in a window manager / desktop environment, please cancel by pressing Ctrl + c immediately"
sleep 10
clear
echo "Continuing..."
sleep 3
clear

cd ~
yay -S wine-staging winetricks dxvk-bin lib32-gnutls lib32-libxcomposite lib32-mesa lib32-vkd3d lib32-libva lib32-vulkan-icd-loader lib32-vulkan-intel lib32-vulkan-mesa-layers samba
sudo winetricks --self-update
winetricks -q --force dotnet48
winetricks -q d3dcompiler_47 corefonts
winetricks -q vcrun2005
winetricks -q d3dcompiler_43 d3dx11_42 d3dx11_43
winetricks -q gfw msasn1 physx
winetricks -q xact_x64 xact xinput
winetricks -q wmp11
WINEPREFIX=~/.wine setup_dxvk install
