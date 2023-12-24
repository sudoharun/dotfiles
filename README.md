# Retro-esque, a Hyprland config

<div align="center">
  <img src="./assets/hyprland1.png">
  <img src="./assets/hyprland2.png">
  <img src="./assets/hyprland3.png">
</div>

## Keybindings

- `Super + Enter` = Open Alacritty terminal
- `Super + F` = Open Firefox Developer Edition
- `Super + Q` = Kill active application
- `Super + R` = Open wofi (application launcher)
- `Super + E` = Open wofi-emoji (emoji selector)
- `Super + Tab` = Switch application
- `Super + Escape` = Toggle fullscreen for active application
- `Alt + F` = Toggle floating
- `Super + M` = Exit Hyprland
- `Print` = Open screenshot menu in bar (arrow keys to change selection, `Enter` to enter selection, `Escape` to quit)
- `XF86PowerOff` = Open power menu in bar (arrow keys to change selection, `Enter` to enter selection, `Escape` to quit)

## How to install

Before starting, I would like to mention that `install.sh` and `post-install.sh` are deprecated in favour of `install.py`.

### Arch Linux installation
Because I am lazy, I just use the `archinstall` script. Here is how I do it on my laptop:

After plugging in my usb with the Arch Linux ISO and booting into the Arch installer, I connect to wifi using `iwctl`
```
$ iwctl
[iwctl] station wlan0 scan
[iwctl] station wlan0 connect essid
[iwctl] quit
```

Next, I do stuff with the keyring and keys
```
$ pacman-key --init
$ pacman-key --populate archlinux
$ pacman -Sy archlinux-keyring
```

If I get any errors with the above, I do the following then repeat the above:
```
$ killall gpg-agent
$ rm -rf /etc/pacman.d/gnupg
```

Now it is time for `archinstall`:
```
$ archinstall
```

In `archinstall`:
- Under profile I choose minimal
- Under optional packages, I enter `git`
- Under audio I choose `pipewire`
- I prefer to have a root user and my own user with sudo privileges enabled
- Under network configuration I choose `networkmanager`
- Under optional repositories, I like to enable `multilib`

The rest is easy to figure out on your own based on your preferences.

### After Arch Linux installation

First update your system:
```
$ sudo pacman -Syu
```

Then you can do the following:
```
$ sudo pacman -S python git
$ git clone -b retroesque https://github.com/sudo-harun/dotfiles.git
$ cd dotfiles
$ python install.py
```

To show the shutdown menu in the bar when pressing the power button, you need to edit `/etc/systemd/logind.conf`. You need to uncomment and edit the line `#HandlePowerKey=poweroff` to `HandlePowerKey=ignore`. The change will take effect after a reboot.

To show colours when using `yay` or `pacman` commands, you need to edit `/etc/pacman.conf`. Uncomment the line `#Color` to `Color`.
