# Retro-esque, a Hyprland config

<div align="center">
  <img src="./assets/hyprland1.png">
  <img src="./assets/hyprland2.png">
  <img src="./assets/hyprland3.png">
</div>

## Keybindings

- `Super + [num]` = Switch to workspace [num]
- `Alt + [num]` = Move active window to workspace [num]
- `Super + Enter` = Open `foot` terminal
- `Super + B` = Open Floorp Web Browser
- `Super + Shift + B` = Open Floorp Private Window
- `Super + Q` = Kill active application
- `Super + R` = Open wofi (application launcher)
- `Super + E` = Open wofi-emoji (emoji selector)
- `Super + Tab` = Switch application
- `Super + Escape` = Toggle fullscreen for active application
- `Super + F` = Toggle floating
- `Super + S` = Toggle split
- `Super + M` = Exit Hyprland
- `Print` = Open screenshot menu in bar (arrow keys to change selection, `Enter` to enter selection, `Escape` to quit)
- `XF86PowerOff` = Open power menu in bar (arrow keys to change selection, `Enter` to enter selection, `Escape` to quit)

## How to install

You can either use `$ archinstall` and add `git` and `python` as additional packages, or follow the installation guide below.

### Arch Linux installation

NOTE: I made this guide using the Arch Linux Installation Guide and Artix Installation Guide.

After plugging in my usb with the Arch Linux ISO and booting into the Arch installer, I set my keyboard layout with `$ loadkeys`. In my case it's `$ loadkeys gb` since I have a British keyboard layout.

Next, I connect to wifi using `iwctl` (not necessary if on ethernet)
```
$ iwctl
[iwctl] station wlan0 scan
[iwctl] station wlan0 connect <essid>
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

Afterwards, I create my partition table on my NVME drive using `cfdisk`. In my case, I do `cfdisk /dev/nvme0n1`.
I delete all partitions and make 3 partitions:
- The first partition is going to be the EFI partition. I make it 500M in size, and the filesystem type is EFI
- The second partition is the swap partition. I make it half of my RAM size. I have 16G of RAM, so I make the swap partition 8G. The filesystem type is Linux Swap.
- The third and last partition is my root partition. I give it the remaining space and the filesystem type is Linux Filesystem.

Next, I make my partitions:
```
$ mkfs.fat -F 32 /dev/nvme0n1p1   # This is my EFI partition
$ mkswap /dev/nvme0n1p2           # This is my swap partition
$ mkfs.ext4 /dev/nvme0n1p3        # This is my root partition
```

After that, I mount my partitions:
```
$ mount /dev/nvme0n1p3 /mnt
$ mount --mkdir /dev/nvme0n1p1 /mnt/boot/efi
$ swapon /dev/nvme0n1p2
```

Time to `pacstrap` and install the base system:
```
$ pacstrap -K /mnt base base-devel linux linux-firmware networkmanager grub efibootmgr os-prober neovim git python
```

Now create your `fstab` file with `genfstab`:
```
$ genfstab -U /mnt >> /mnt/etc/fstab
```

Now, we can `chroot` into our system with `$ arch-chroot /mnt`.

Add your timezone by symlinking it to `/etc/localtime`. In my case, my timezone is London:
```
$ ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime
```

And synchronize to your hardware clock:
```
$ hwclock --systohc
```

Next, setting up locales:
- `$ nvim /etc/locale.gen` then uncomment your locale
- Then run `$ locale-gen` to generate them
- Finally `nvim /etc/locale.conf` and add `LANG=<locale>`. In my case it's `LANG=en_GB.UTF-8`.

Set up your TTY keymap with `$ nvim /etc/vconsole.conf` and add `KEYMAP=<your keymap>`. In my case it's `KEYMAP=gb`.

Create your hostname with `$ nvim /etc/hostname` and you can put in anything you want. Make sure it is unique or at least different to all computers on your LAN however.

Next, create your user(s) with 
```
$ useradd -m <username>
```

Give them some permissions like the ability to use `sudo` commands and the ability to change the brightness with `$ usermod -aG video wheel <username>`

When adding your user to the `wheel` group to give them access to `sudo` commands, you need to give the `wheel` group the ability to perform `sudo` commands. Edit `/etc/sudoers` with `$ visudo` (recommended, but you need `vi` installed), or `$ nvim /etc/sudoers` (not recommended). Then go down to this line: `## Uncomment to allow members of group wheel to execute any command` and uncomment the line below it, then save and quit.

Next add passwords to your users with `$ passwd <username>`. Add a root password with `$ passwd`.

Next, install grub:
- If you want to dual-boot, first uncomment `#GRUB_DISABLE_OS_PROBER=false` from `/etc/default/grub` then do the following.
- If you are not interested in Secure Boot, you can install `grub` normally with ```$ grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=Grub```
- If you want to setup Secure Boot, do ```$ grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=Grub --modules="tpm" --disable-shim-lock```

Now finally run
```
$ grub-mkconfig -o /boot/grub/grub.cfg
```

Now exit `chroot` with `$ exit`, unmount all partitions with `$ umount -R /mnt` and finally reboot into your newly installed system!

### After Arch Linux installation

Connect to wifi with `$ nmtui` or plug in your ethernet cable.

Then update your system with `$ sudo pacman -Syu`

Then you can do the following:
```
$ git clone -b retroesque https://github.com/sudoharun/dotfiles.git
$ cd dotfiles
$ python install.py
```

To show the shutdown menu in the bar when pressing the power button, you need to edit `/etc/systemd/logind.conf`. You need to uncomment and edit the line `#HandlePowerKey=poweroff` to `HandlePowerKey=ignore`. The change will take effect after a reboot.

To show colours when using `yay` or `pacman` commands, you need to edit `/etc/pacman.conf`. Uncomment the line `#Color` to `Color`.

### Tips and tricks

- Do `$ yay [package]` to search for a package


Please report any bugs or errors in documentation using Github Issues, or you can contact me on Discord. My Discord username is `sudoharun`.
