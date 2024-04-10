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
    "xdg-desktop-portal-gtk",
    "grim",
    "slurp",
    "socat",
    "bc",
    "sysstat",
    "watchexec",
    "jq",
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
    "dunst",
    "ranger-git",
    "dragon-drop",
    "wofi",
    "wofi-emoji",
    "pfetch",
    "btop",
    "rustup",
    "eww",
    "python-pywal",
    "waypaper-git",
    "floorp-bin",
    "mpv",
    "bibata-cursor-theme-bin",
    "papirus-icon-theme",
    "hyprlang-git",
    "hyprcursor-git",
    "hyprland-git",
    "xdg-desktop-portal-wlr",
    "hyprlock-git",
    "hypridle-git",
    "nwg-look",
    "qt6ct",
    "imv",
    "wl-clipboard",
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
    "powertop",
    "auto-cpufreq",
    "tlp"
]

optional = [
    "downgrade",
    "dosfstools",
    "filezilla",
    "gimp",
    "deluge-gtk",
    "handbrake",
    "armcord-bin"
]

start_time = int(perf_counter())

# Warning
os.system("clear")
print("This script is designed to run after a fresh, minimal install of Arch Linux.\nRun at your own risk!\nYou should also make sure your system is updated.")
print("\n(Also, if a package takes long to install,\n don't worry, just be a bit patient.\n It's probably just a rust package compiling, such as eww.)")
start = input("\nContinue? [Y/n]: ")
if start == "n":
    exit()

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
    sleep(1)
    print("Done.\n\n")

os.chdir(home)

# Install packages
print("Installing required packages (this may take a while)...")
for pkg in packages:
    print(f"\nInstalling '{pkg}'...")
    try:
        is_pkg = int(subprocess.run(f"yay -Q | grep -w {pkg} | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
        if is_pkg != 0:
            print(f"'{pkg}' already installed. Skipping...")
            sleep(1)
        else:
            os.system(f"yay -S --noconfirm {pkg}")
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
                else:
                    os.system(f"yay -S --noconfirm {pkg}")
                    sleep(0.5)
                    print(f"Successfully installed '{pkg}'!")
            except:
                print(f"There was an error installing '{pkg}'!")
                print("Continuing...")
        break
    elif audio_opt == "n":
        print("Continuing...\n")
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
    else:
        print("Please enter a valid answer.\n")

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
                else:
                    os.system(f"yay -S --noconfirm {pkg}")
                    sleep(0.5)
                    print(f"Successfully installed '{pkg}'!")
            except:
                print(f"There was an error installing '{pkg}'!")
                print("Continuing...")
        break
    elif power_opt == "n":
        print("Continuing...\n")
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
    else:
        print("Please enter a valid answer.\n")

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
                else:
                    os.system(f"yay -S --noconfirm {pkg}")
                    sleep(0.5)
                    print(f"Successfully installed '{pkg}'!")
            except:
                print(f"There was an error installing '{pkg}'!")
                print("Continuing...")
        break
    elif optional_opt == "n":
        print("Continuing...\n")
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
    else:
        print("Please enter a valid answer.\n")

# Gtk theme
print("\nMaking Gtk themes folder...")
os.system("mkdir -p ~/.local/share/themes")
os.system("mkdir -p ~/.local/share/icons")
os.system(f"cp -r {dots_dir}/themes/* ~/.local/share/themes/")
os.system(f"cp -r {dots_dir}/icons/* ~/.local/share/icons/")
os.chdir(home)
print("\nSetting theme...")
os.system("gsettings set org.gnome.desktop.interface gtk-theme \"triple12\"")
print("\nSetting cursor theme...")
os.system("gsettings set org.gnome.desktop.interface cursor-theme 'Bibata-Modern-Classic'")
print("\nSetting icon theme...")
os.system("gsettings set org.gnome.desktop.interface icon-theme \"triple12\"")
print("\nSettings fonts...")
os.system("gsettings set org.gnome.desktop.interface document-font-name \"IBM Plex Sans 11\"")
os.system("gsettings set org.gnome.desktop.interface font-name \"IBM Plex Sans 11\"")
os.system("gsettings set org.gnome.desktop.interface monospace-font-name \"IBM Plex Mono 11\"")
os.system("gsettings set org.gnome.nautilus.desktop font \"IBM Plex Sans 11\"")

# Copying dotfiles
print("\nCopying dotfiles...")
os.system("mkdir ~/.config")
os.system(f"cp {dots_dir}/home/zlogin ~")
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
os.system("chmod +x .config/dunst/dunstrc")
os.system("chmod +x .config/dunst/alert")
os.system("chmod +x .config/ranger/scope.sh")
os.system("chmod +x .config/scripts/powermenu")
os.system("chmod +x .config/scripts/screenshooter")
os.system("chmod +x .config/eww/scripts/battery")
os.system("chmod +x .config/eww/scripts/brightness")
os.system("chmod +x .config/eww/scripts/workspaces")
os.system("chmod +x .config/eww/scripts/volume")
os.system("chmod +x .config/eww/scripts/wifi")
os.system("chmod +x .config/hypr/idler")
print("Done.")

# Removing unnecessary/unused dependencies
print("\nRemoving unnecessary/unused dependencies...")
os.system("yay -Rns --noconfirm $(yay -Qdtq)")
print("Done.")

# Setup oh-my-zsh
zsh_opt = input("\n\nWould you like to set up oh-my-zsh? [Y/n] ").lower()
if zsh_opt != "n":
    print("\n\nThis next step will set up ohmyzsh. Follow the onscreen instructions if any appear.")
    input("(Press enter to continue)")
    os.system("clear")
    os.system('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended')
    os.system("mv ~/zlogin ~/.zlogin")
    os.system("chsh -s /bin/zsh")
    
    # Append stuff to ~/.zshrc
    with open(f"{home}/.zshrc", "a") as f:
        f.write("\n\n# Custom Aliases")
        f.write("\nalias xtmapper='~/wayland-getevent/client | sudo waydroid shell -- sh /sdcard/Android/data/xtr.keymapper/files/xtMapper.sh --wayland-client'")
        f.write("\n\n# Adding stuff to path")
        f.write(f"\npath+=('{home}/.local/bin/')")
        f.write("\npath+=('/usr/lib/ccache/bin/')")
        f.write("\nexport PATH")
        f.write("\n\nexport TERMINAL='foot'")
        f.write("\nexport editor='nvim'")
        f.write("\n\ncd ~")
        f.write("\npfetch")
else:
    os.system("rm -f ~/zlogin")

os.system("clear")

# Bluetooth
bt_opt = input("Would you like to install Bluetooth tools (bluez)? [Y/n] ").lower()
if bt_opt != "n":
    os.system("yay -S --noconfirm bluez bluez-tools bluez-utils")
    os.system("sudo systemctl enable --now bluetooth")
    print("Done.")

nvchad_opt = input("\n\nWould you like to set up NVChad? [Y/n] ").lower()
if nvchad_opt != "n":
    print("\n\nThis next step will setup NVChad. Just press enter when the prompt shows up, then type ':q' to quit neovim.")
    sleep(5)
    os.system("git clone https://github.com/NvChad/starter ~/.config/nvim --depth 1 && nvim && echo 0")
    os.system("mv ~/chadrc.lua ~/.config/nvim/lua/chadrc.lua")
    os.system("mv ~/plugins.lua ~/.config/nvim/lua/plugins/init.lua")
    with open(f"{home}/.config/nvim/lua/plugins/init.lua", "a") as f:
        f.close()
else:
    os.system("rm -f ~/chadrc.lua")

# pywal
# os.system(f'wal -b 121212 -i "{home}/.config/hypr/flowerz.jpg"')

# Add user to video group to be able to change brightness
os.system("sudo usermod -aG video $USER")

os.system("clear")
end_time = int(perf_counter())

last_opt = input("Would you like to reboot (recommended) or start Hyprland? [R/h] ").lower()
# print(f"Remember to manually set your wallpaper with waypaper when starting Hyprland! (Located in {home}/.config/hypr named flowerz.jpg)")
# print(f"(By the way, the installation process took {end_time - start_time} seconds, or {(end_time - start_time)/60} minutes.)")
# input("(Press enter to continue)")
if last_opt == "h":
    os.system("Hyprland")
else:
    os.system("reboot")
