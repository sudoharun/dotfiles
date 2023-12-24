import os
import subprocess
from time import sleep

home = str(subprocess.run("echo $HOME", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout).strip()

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
    "rustup",
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
    "wl-clipboard"
]

audio = [
    "pipewire",
    "sof-firmware",
    "pavucontrol",
    "pamixer",
    "alsa-firmware",
    "alsa-ucm-conf"
]

power_management = [
    "powertop",
    "auto-cpufreq",
    "tlp"
]

optional = [
    "downgrade",
    "dosfstools",
    "filezilla",
    "pinta",
    "deluge-gtk",
    "armcord-bin"
]

# Warning
os.system("clear")
print("This script is designed to run after a fresh, minimal install of Arch Linux.\nRun at your own risk!\nYou should also make sure your system is updated.")
print("\n(Also, if a package takes long to install,\n don't worry, just be a bit patient.\n It's probably just a rust package compiling, such as eww.)")
start = input("\nContinue? [Y/n]: ")
if start == "n":
    exit()
sleep(2)

os.chdir(home)

# Update pacman databases
print("\n\nUpdating databases...")
os.system("sudo pacman -Syy &>> /dev/null")
sleep(1)
print("Done.\n\n")

# Install yay AUR helper
print("Installing yay...")
is_yay = int(subprocess.run("pacman -Q | grep -w yay | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
if is_yay != 0:
    print("'yay' already installed. Skipping...\n\n")
    sleep(2)
else:
    os.system("git clone https://aur.archlinux.org/yay.git &>> /dev/null")
    os.chdir("yay")
    os.system("makepkg -si --noconfirm &>> /dev/null")
    os.system("rm -rf ~/yay")
    sleep(1)
    print("Done.\n\n")

os.chdir(home)

# Install packages
print("Installing required packages (this may take a while)...")
sleep(2)
for pkg in packages:
    print(f"\nInstalling '{pkg}'...")
    try:
        is_pkg = int(subprocess.run(f"yay -Q | grep -w {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
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
    audio_opt = input("\n\nWould you like to install audio tools? [Y]es | [N]o | [S]ee what they are | [O]mit a package\n>> ").lower()
    print()
    if audio_opt == "y":
        print(f"Installing '{pkg}'...")
        for pkg in audio:
            try:
                is_pkg = int(subprocess.run(f"yay -Q | grep -w {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
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
        sleep(1)
    elif audio_opt == "o":
        print("Please enter 1 package to omit:")
        i = 1
        for pkg in audio:
            print(f" - {i}: {pkg}")
            i+=1
        try:
            om_audio_opt = int(input(">> "))
            audio.pop(om_audio_opt-1)
        except:
            print("Something went wrong!")
            print("Continuing...")
            sleep(2)
    else:
        print("Please enter a valid answer.\n")
        sleep(2)

# Installing (laptop) power management tools
while True:
    power_opt = input("\n\nWould you like to install (laptop) power management tools? [Y]es | [N]o | [S]ee what they are | [O]mit a package\n>> ").lower()
    print()
    if power_opt == "y":
        print(f"Installing '{pkg}'...")
        for pkg in power_management:
            try:
                is_pkg = int(subprocess.run(f"yay -Q | grep -w {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
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
    elif power_opt == "n":
        print("Continuing...\n")
        sleep(2)
        break
    elif power_opt == "s":
        print("The power management tools include:")
        for pkg in power_management:
            print(f" - {pkg}")
        sleep(1)
    elif power_opt == "o":
        print("Please enter 1 package to omit:")
        i = 1
        for pkg in power_management:
            print(f" - {i}: {pkg}")
            i+=1
        try:
            om_power_opt = int(input(">> "))
            power_management.pop(om_power_opt-1)
        except:
            print("Something went wrong!")
            print("Continuing...")
            sleep(2)
    else:
        print("Please enter a valid answer.\n")
        sleep(2)

# Installing optional packages
while True:
    optional_opt = input("\n\nWould you like to install optional packages? [Y]es | [N]o | [S]ee what they are | [O]mit a package\n>> ").lower()
    print()
    if optional_opt == "y":
        for pkg in optional:
            print(f"Installing '{pkg}'...")
            try:
                is_pkg = int(subprocess.run(f"yay -Q | grep -w {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
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
        sleep(1)
    elif optional_opt == "o":
        print("Please enter 1 package to omit:")
        i = 1
        for pkg in optional:
            print(f" - {i}: {pkg}")
            i+=1
        try:
            om_optional_opt = int(input(">> "))
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
os.chdir(home)
os.system("git clone https://github.com/mantissa-/mantis-theme.git &>> /dev/null")
os.chdir("mantis-theme")
os.system("cp -r Manti* ~/.local/share/themes &>> /dev/null")
os.chdir(home)
sleep(2)
print("Removing mantis theme folder from home directory...")
os.system("rm -rf mantis-theme")
sleep(2)

# Copying dotfiles
print("\nCopying dotfiles...")
os.system("mkdir ~/.config &>> /dev/null")
os.system("cp ~/dotfiles/config/zlogin ~")
os.system("cp ~/dotfiles/config/chadrc.lua ~")
os.system("cp -r ~/dotfiles/config/* ~/.config &>> /dev/null")
sleep(2)

# convita
convita_opt = input("\n\nWould you like to keep a script that converts mp4 files for PSVita consoles? [y/N] ").lower()
if convita_opt != "y":
    os.system("rm -r ~/.config/scripts/ffmpeg.sh")

# Enabling script execution permissions
print("\nEnabling script execution permissions...")
os.chdir(home)
os.system("chmod +x dotfiles/wine.sh")
os.system("chmod +x dotfiles/post-install.sh")
os.system("chmod +x .config/dunst/dunstrc")
os.system("chmod +x .config/dunst/alert")
os.system("chmod +x .config/ranger/scope.sh")
if convita_opt != "y":
    os.system("chmod +x .config/scripts/ffmpeg.sh")
os.system("chmod +x .config/scripts/brightness.sh")
os.system("chmod +x .config/scripts/powermenu.sh")
os.system("chmod +x .config/eww/scripts/alacritty")
os.system("chmod +x .config/eww/scripts/battery")
os.system("chmod +x .config/eww/scripts/brightness")
os.system("chmod +x .config/eww/scripts/emptyworkspaces")
os.system("chmod +x .config/eww/scripts/kanjiworkspaces")
os.system("chmod +x .config/eww/scripts/numworkspaces")
os.system("chmod +x .config/eww/scripts/volume")
os.system("chmod +x .config/eww/scripts/wifi")
sleep(1)
print("Done.")
sleep(2)

# Removing unnecessary/unused dependencies
print("\nRemoving unnecessary/unused dependencies...")
os.system("yay -Rns --noconfirm $(pacman -Qdtq) &>> /dev/null")
print("Done.")
sleep(2)

# Setup oh-my-zsh
zsh_opt = input("\n\nWould you like to set up oh-my-zsh? [Y/n] ").lower()
if zsh_opt != "n":
    print("\n\nThis next step will set up ohmyzsh. Follow the onscreen instructions if any appear.")
    input("(Press enter to continue)")
    os.system("clear")
    os.system('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended')
    os.system("mv ~/zlogin ~/.zlogin")
    
    # Append stuff to ~/.zshrc
    with open(f"{home}/.zshrc", "a") as f:
        f.write("")
        f.write("")
        f.write("# Custom Aliases")
        f.write("")
        if convita_opt != "y":
            f.write("alias convita='~/.config/scripts/ffmpeg.sh'")
            f.write("")
        f.write("")
        f.write("# Adding stuff to path")
        f.write("")
        f.write("path+=('$HOME/.local/bin/')")
        f.write("")
        f.write("path+=('/usr/lib/ccache/bin/')")
        f.write("")
        f.write("export PATH")
        f.write("")
        f.write("")
        f.write("export TERMINAL='alacritty'")
        f.write("")
        f.write("export editor='nvim'")
        f.write("")
        f.write("")
        f.write("cd ~")
        f.write("")
        f.write("pfetch")
else:
    os.system("rm -f ~/zlogin")

os.system("clear")

# Bluetooth
bt_opt = input("Would you like to install Bluetooth tools (bluez)? [Y/n] ").lower()
if bt_opt != "n":
    os.system("yay -S --noconfirm bluez bluez-tools bluez-utils &>> /dev/null")
    os.system("sudo systemctl enable --now bluetooth")
    print("Done.")

nvchad_opt = input("\n\nWould you like to set up NVChad? [Y/n] ").lower()
if nvchad_opt != "n":
    print("\n\nThis next step will setup NVChad. Just press enter when the prompt shows up, then type ':q' to quit neovim.")
    sleep(5)
    os.system("git clone https://github.com/NvChad/NvChad ~/.config/nvim --depth 1 && nvim")
    os.system("mv ~/chadrc.lua ~/.config/nvim/lua/custom/chadrc.lua")
else:
    os.system("rm -f ~/chadrc.lua")

# pywal
os.system(f'wal -b 121212 -i "{home}/.config/hypr/flowerz.jpg"')

# Add user to video group to be able to change brightness
os.system("sudo usermod -aG video $USER")

os.system("clear")

last_opt = input("Would you like to reboot (recommended) or start Hyprland? [R/h] ").lower()
print(f"Remember to manually set your wallpaper with waypaper when starting Hyprland! (Located in {home}/.config/hypr named flowerz.jpg)")
print("Also, you need to set Gtk theme to Mantis (any), icons to Papirus and font to IBM Plex Sans Regular manually with nwg-look-bin")
sleep(2)
input("(Press enter to continue)")
if last_opt != "r":
    os.system("Hyprland")
else:
    os.system("reboot")
