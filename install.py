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
    #"ttf-apple-emoji",
    "wofi",
    "wofi-emoji",
    "cliphist",
    "wl-clipboard",
    "btop",
    "rustup",
    # "aylurs-gtk-shell", # Removing soon since moving to libastal
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
    "xdg-desktop-portal-hyprland",
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
    #"pipewire-jack",
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
    "vesktop-bin"
]

start_time = int(perf_counter())

os.chdir(home)

# Update pacman databases
print("\n\nUpdating databases...")
os.system("sudo pacman -Syy")
sleep(1)
print("Done.\n\n")

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
