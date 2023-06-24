#!/bin/bash

cd ~
yay -S wine-staging winetricks dxvk-bin
sudo winetricks --self-update
winetricks -q --force dotnet48
winetricks -q d3dcompiler_47 corefonts
winetricks -q vcrun2005
winetricks -q d3dcompiler_43 d3dx11_42 d3dx11_43
winetricks -q gfw msasn1 physx
winetricks -q xact_x64 xact xinput
WINEPREFIX=~/.wine setup_dxvk install
