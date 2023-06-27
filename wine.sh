#!/bin/bash

clear
echo "WARNING: This script is intended to run inside a GUI (e.g. a window manager or desktop environment)"
echo "If you are not in a GUI, please cancel by pressing Ctrl + c immediately"
sleep 10
clear
echo "Continuing..."
sleep 3
clear

cd ~
yay -S wine-staging winetricks dxvk-bin
sudo winetricks --self-update
winetricks -q --force dotnet48
winetricks -q d3dcompiler_47 corefonts
winetricks -q vcrun2005
winetricks -q d3dcompiler_43 d3dx11_42 d3dx11_43
winetricks -q gfw msasn1 physx
winetricks -q xact_x64 xact xinput
winetricks -q wmp11
WINEPREFIX=~/.wine setup_dxvk install
