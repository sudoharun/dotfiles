#!/bin/bash

# Install rustup with the following command
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

cd ~
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup install nightly
git clone https://github.com/elkowar/eww
mv ~/eww ~/.eww
cd ~/.eww
cargo build --release --no-default-features --features x11
cd target/release
chmod +x ./eww
mkdir -p ~/.local/bin
cp eww ~/.local/bin/
