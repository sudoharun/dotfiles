import os
import subprocess
from time import sleep, perf_counter

home = str(subprocess.run("echo $HOME", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout).strip()
dots_dir = os.getcwd().strip()

packages = [
    "qt5-wayland",
    "qt6-wayland",
    "linux-headers",
    "reflector-simple",
    "bash-completion",
    "ccache",
    "brightnessctl",
    "iw",
    "wireless_tools",
    "zip",
    "unzip",
    "unrar",
    "p7zip",
    "upower",
    "udisks2",
    "neovim",
    "polkit-gnome",
    "xdg-desktop-portal-gtk",
    "grim",
    "slurp",
    "wev",
    "foot",
    "foot-terminfo",
    "noto-fonts",
    "noto-fonts-cjk",
    "ttf-roboto",
    "ttf-ibm-plex",
    "ttf-fantasque-nerd",
    "ttf-iosevka-term",
    "ttf-apple-emoji",
    "wofi",
    "wofi-emoji",
    "cliphist",
    "wl-clipboard",
    "pfetch",
    "btop",
    "rustup",
    "aylurs-gtk-shell", # Removing soon since moving to libastal
    "libastal-git",
    "libastal-io-git",
    "libastal-meta",
    "waypaper",
    "firefox",
    "mpv",
    "bibata-cursor-theme-bin",
    "papirus-icon-theme",
    "hyprlang",
    "hyprcursor",
    "hyprland",
    "xdg-desktop-portal-wlr",
    "hyprlock",
    "hypridle",
    "nwg-look",
    "qt5ct",
    "swww",
    "imv",
    "wl-clipboard",
    "zed",
    "meson",
    "cpio",
    "cmake"
]

audio = [
    "pipewire",
    "pipewire-pulse",
    "pipewire-jack",
    "pipewire-alsa",
    "sof-firmware",
    "pavucontrol",
    "pamixer",
    "alsa-firmware",
    "alsa-ucm-conf"
]

power_management = [
    # "powertop",
    "auto-cpufreq"
    # "tlp"
]

optional = [
    "downgrade",
    "dosfstools",
    "filezilla",
    "gimp",
    "deluge-gtk",
    "handbrake",
    "steam",
    "legcord"
]

start_time = int(perf_counter())

os.chdir(home)

# Update pacman databases
print("\n\nUpdating databases...")
os.system("sudo pacman -Syy")
sleep(1)
print("Done.\n\n")

# Install yay AUR helper
print("Installing yay...")
is_yay = int(subprocess.run("pacman -Q | grep -w yay | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
if is_yay != 0:
    print("'yay' already installed. Skipping...\n\n")
else:
    os.system("git clone https://aur.archlinux.org/yay.git")
    os.chdir("yay")
    os.system("makepkg -si --noconfirm")
    os.system("rm -rf ~/yay")
    print("Done.\n\n")

os.chdir(home)

packages_to_install = ""

for pkg in packages:
    packages_to_install = packages_to_install + " " + pkg

for pkg in power_management:
    packages_to_install = packages_to_install + " " + pkg

for pkg in audio:
    packages_to_install = packages_to_install + " " + pkg

for pkg in optional:
    packages_to_install = packages_to_install + " " + pkg

subprocess.run(f"yay -S --noconfirm {packages_to_install}", shell=True)

# Bluetooth
bt_opt = input("Would you like to install Bluetooth tools (bluez)? [Y/n] ").lower()
if bt_opt != "n":
    os.system("yay -S --noconfirm bluez bluez-tools bluez-utils")
    os.system("sudo systemctl enable --now bluetooth")
    print("Done.")

# Gtk theme
print("\nMaking Gtk themes folder...")
os.system("mkdir -p ~/.local/share/themes")
os.chdir(home)
os.system("git clone https://github.com/sudoharun/Triple12.git")
os.chdir("Triple12")
os.system("cp -r gtk/* ~/.local/share/themes")
os.chdir(home)
os.system("rm -rf Triple12")
print("\nSetting theme...")
os.system("gsettings set org.gnome.desktop.interface gtk-theme \"Triple12\"")
print("\nSetting cursor theme...")
os.system("gsettings set org.gnome.desktop.interface cursor-theme 'Bibata-Modern-Classic'")
print("\nSetting icon theme...")
os.system("gsettings set org.gnome.desktop.interface icon-theme \"Papirus\"")
print("\nSettings fonts...")
os.system("gsettings set org.gnome.desktop.interface document-font-name \"IBM Plex Sans 11\"")
os.system("gsettings set org.gnome.desktop.interface font-name \"IBM Plex Sans 11\"")
os.system("gsettings set org.gnome.desktop.interface monospace-font-name \"IBM Plex Mono 11\"")
os.system("gsettings set org.gnome.nautilus.desktop font \"IBM Plex Sans 11\"")

# Copying dotfiles
print("\nCopying dotfiles...")
os.system("mkdir ~/.config")
os.system(f"cp {dots_dir}/config/chadrc.lua ~")
os.system(f"cp {dots_dir}/config/plugins.lua ~")
os.system(f"cp -r {dots_dir}/config/* ~/.config")

# Fix waypaper config
edited = []
with open(f"{home}/.config/waypaper/config.ini", "r") as f:
    for word in f.readlines():
        edited.append(word.replace("REPLACE",home))
    f.close()
with open(f"{home}/.config/waypaper/config.ini", "w") as f:
    for word in edited:
        f.write(word)
    f.close()

# Enabling script execution permissions
print("\nEnabling script execution permissions...")
os.chdir(home)
os.system("chmod +x dotfiles/wine.sh")
os.system("chmod +x .config/hypr/idler")
print("Done.")

# Removing unnecessary/unused dependencies
print("\nRemoving unnecessary/unused dependencies...")
os.system("yay -Rns --noconfirm $(yay -Qdtq)")
print("Done.")

# Bash stuff
with open(f"{home}/.bashrc", "a") as f:
    f.write("\n\nbind \"set completion-ignore-case on\"")
    f.write("\nbind \"set show-all-if-ambiguous on\"")
    f.write("\n\nbind '\"\\e[A\": history-search-backward'")
    f.write("\nbind '\"\\e[B\": history-search-forward'")
    f.write("\nbind '\"\\C-H\": shell-backward-kill-word'")
    f.write("\nbind '\"\\e[3;5~\": shell-kill-word'")
    f.write("\n\nexport HISTCONTROL=ignoreboth:erasedups")

os.system("clear")

nvchad_opt = input("\n\nWould you like to set up NVChad? [Y/n] ").lower()
if nvchad_opt != "n":
    print("\n\nThis next step will setup NVChad. Just press enter when the prompt shows up, then type ':q' to quit neovim.")
    sleep(2)
    os.system("git clone https://github.com/NvChad/starter ~/.config/nvim --depth 1 && nvim && echo 0")
    os.system("mv ~/chadrc.lua ~/.config/nvim/lua/chadrc.lua")
    os.system("mv ~/plugins.lua ~/.config/nvim/lua/plugins/init.lua")
    with open(f"{home}/.config/nvim/lua/plugins/init.lua", "w") as f:
        f.close()
else:
    os.system("rm -f ~/chadrc.lua")

os.system("clear")
end_time = int(perf_counter())

last_opt = input("Would you like to continue setup in TTY (recommended), reboot or start Hyprland? [C/r/h] ").lower()
if last_opt == "r":
    os.system("reboot")
elif last_opt == "r":
    os.system("Hyprland")
