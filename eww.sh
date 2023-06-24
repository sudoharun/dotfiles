#!/bin/bash
cd ~
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup install nightly
git clone https://github.com/elkowar/eww
mv ~/eww ~/.eww
cd ~/.eww
rustup default nightly
cargo build --release --no-default-features --features x11
cd target/release
chmod +x ./eww
mkdir -p ~/.local/bin
cp eww ~/.local/bin/
rustup default stable
