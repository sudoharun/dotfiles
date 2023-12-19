import os
import subprocess
from time import sleep

packages = [
    "hyprland",
    "qt5-wayland",
    "qt6-wayland",
    "linux-headers",
    "reflector-simple",
    "ccache",
    "brillo",
    "iw",
    "wireless_tools",
    "zip",
    "unzip",
    "unrar",
    "p7zip",
    "upower",
    "udisks2",
    "zsh",
    "neovim",
    "polkit-gnome",
    "xdg-desktop-portal",
    "xdg-desktop-portal-hyprland",
    "xdg-desktop-portal-gtk",
    "grim",
    "slurp",
    "socat",
    "bc",
    "sysstat",
    "watchexec",
    "jq",
    "wev",
    "alacritty",
    "noto-fonts",
    "noto-fonts-cjk",
    "ttf-ibm-plex",
    "ttf-ibmplex-mono-nerd",
    "ttf-iosevka-nerd",
    "ttf-iosevkaterm-nerd",
    "ttf-apple-emoji",
    "dunst",
    "ranger",
    "dragon-drop",
    "ueberzugpp",
    "wofi",
    "wofi-emoji",
    "pfetch",
    "btop",
    "eww-wayland",
    "python-pywal",
    "swaybg",
    "waypaper-git",
    "firefox-developer-edition",
    "mpv",
    "capitaine-cursors",
    "papirus-icon-theme",
    "swaylock-effects-git",
    "nwg-look-bin",
    "imv",
    "rustup"
]

audio = [
    "pipewire",
    "sof-firmware",
    "pavucontrol",
    "pamixer",
    "alsa-firmware",
    "alsa-ucm-conf"
]

optional = [
    "dosfstools",
    "filezilla",
    "pinta",
    "deluge-gtk",
    "armcord-bin"
]

# Warning
os.system("clear")
print("This script is designed to run after a fresh, minimal install of Arch Linux.\nRun at your own risk!\nYou should also make sure your system is updated.")
sleep(10)
print("Continuing...")
sleep(2)

os.system("cd ~")

# Update pacman databases
print("Updating databases...")
os.system("sudo pacman -Syy &>> /dev/null")
sleep(1)
print("Done.\n\n")

# Install yay AUR helper
print("Installing yay...")
is_yay = int(subprocess.run("pacman -Q | grep yay | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
if is_yay != 0:
    print("'yay' already installed. Skipping...\n\n")
    sleep(2)
else:
    os.system("git clone https://aur.archlinux.org/yay.git &>> /dev/null")
    os.system("cd yay")
    os.system("makepkg -si --noconfirm &>> /dev/null")
    sleep(1)
    print("Done.\n\n")

# Install packages
print("Installing required packages (this may take a while)...")
for pkg in packages:
    try:
        is_pkg = int(subprocess.run(f"yay -Q | grep {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
        if is_pkg != 0:
            print(f"'{pkg}' already installed. Skipping...")
            sleep(1)
        else:
            os.system(f"yay -S --noconfirm {pkg} &>> /dev/null")
            sleep(0.5)
            print(f"Successfully installed '{pkg}'!")
    except:
        print(f"There was an error installing '{pkg}'!")
        print("Continuing...")

# Installing audio tools
while True:
    audio_opt = input("\n\nWould you like to install audio tools? [Y]es | [N]o | [S]ee what they are | [O]mit a package").lower()
    if audio_opt == "y":
        for pkg in audio:
            try:
                is_pkg = int(subprocess.run(f"yay -Q | grep {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
                if is_pkg != 0:
                    print(f"'{pkg}' already installed. Skipping...")
                    sleep(2)
                else:
                    os.system(f"yay -S --noconfirm {pkg} &>> /dev/null")
                    sleep(0.5)
                    print(f"Successfully installed '{pkg}'!")
            except:
                print(f"There was an error installing '{pkg}'!")
                print("Continuing...")
                sleep(2)
        break
    elif audio_opt == "n":
        print("Continuing...\n")
        sleep(2)
        break
    elif audio_opt == "s":
        print("The audio tools include:")
        for pkg in audio:
            print(f" - {pkg}")
        sleep(5)
    elif audio_opt == "o":
        print("Please enter 1 package to omit:")
        i = 1
        for pkg in audio:
            print(f" - {i}: {pkg}")
            i+=1
        try:
            om_audio_opt = input(">> ")
            audio.pop(om_audio_opt-1)
        except:
            print("Something went wrong!")
            print("Continuing...")
            sleep(2)
    else:
        print("Please enter a valid answer.\n")
        sleep(2)

# Installing optional packages
while True:
    optional_opt = input("\n\nWould you like to install optional packages? [Y]es | [N]o | [S]ee what they are | [O]mit a package").lower()
    if optional_opt == "y":
        for pkg in optional:
            try:
                is_pkg = int(subprocess.run(f"yay -Q | grep {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
                if is_pkg != 0:
                    print(f"'{pkg}' already installed. Skipping...")
                    sleep(2)
                else:
                    os.system(f"yay -S --noconfirm {pkg} &>> /dev/null")
                    sleep(0.5)
                    print(f"Successfully installed '{pkg}'!")
            except:
                print(f"There was an error installing '{pkg}'!")
                print("Continuing...")
                sleep(2)
        break
    elif optional_opt == "n":
        print("Continuing...\n")
        sleep(2)
        break
    elif optional_opt == "s":
        print("The optional packages include:")
        for pkg in optional:
            print(f" - {pkg}")
        sleep(5)
    elif optional_opt == "o":
        print("Please enter 1 package to omit:")
        i = 1
        for pkg in optional:
            print(f" - {i}: {pkg}")
            i+=1
        try:
            om_optional_opt = input(">> ")
            optional.pop(om_optional_opt-1)
        except:
            print("Something went wrong!")
            print("Continuing...")
            sleep(2)
    else:
        print("Please enter a valid answer.\n")
        sleep(2)

# Gtk theme
print("\nMaking Gtk themes folder...")
os.system("mkdir -p ~/.local/share/themes")
sleep(2)
print("Installing and copying mantis Gtk theme to themes folder...")
os.system("cd ~")
os.system("git clone git clone https://github.com/mantissa-/mantis-theme.git &>> /dev/null")
os.system("cd mantis-theme")
os.system("cp -r Manti* ~/.local/share/themes &>> /dev/null")
os.system("cd ~")
sleep(2)
print("Removing mantis theme folder from home directory...")
os.system("rm -rf mantis-theme")
sleep(2)

# Copying dotfiles
print("\nCopying dotfiles...")
os.system("mkdir ~/.config")
os.system("cd ~/dotfiles/config")
os.system("cp -r * ~/.config &>> /dev/null")
sleep(2)

# Enabling script execution permissions
print("\nEnabling script execution permissions...")
os.system("cd ~")
os.system("chmod +x dotfiles/wine.sh")
os.system("chmod +x dotfiles/post-install.sh")
os.system("cd ~/.config")
os.system("chmod +x dunst/dunstrc")
os.system("chmod +x dunst/alert")
os.system("chmod +x ranger/scope.sh")
os.system("chmod +x scripts/ffmpeg.sh")
os.system("chmod +x scripts/brightness.sh")
os.system("chmod +x scripts/powermenu.sh")
os.system("chmod +x eww/scripts/alacritty")
os.system("chmod +x eww/scripts/battery")
os.system("chmod +x eww/scripts/brightness")
os.system("chmod +x eww/scripts/emptyworkspaces")
os.system("chmod +x eww/scripts/kanjiworkspaces")
os.system("chmod +x eww/scripts/numworkspaces")
os.system("chmod +x eww/scripts/volume")
os.system("chmod +x eww/scripts/wifi")
sleep(2)

# Removing unnecessary/unused dependencies
print("\nRemoving unnecessary/unused dependencies...")
os.system("yay -Rns $(pacman -Qdtq) &>> /dev/null")
sleep(2)

# Setup ohmyzsh
print("\nThis last step will set up ohmyzsh. Follow the onscreen instructions if any appear.")
print("Please reboot once this step has completed.")
sleep(8)
os.system('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
