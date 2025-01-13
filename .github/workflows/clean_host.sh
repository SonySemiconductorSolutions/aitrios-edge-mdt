#!/bin/bash

# Enable debugging for transparency
set -o xtrace

echo "Starting cleanup..."
echo "df -h before cleanup"
df -h

# Function to remove a directory or file with a check
remove_path() {
  local path=$1
  if [ -e "$path" ]; then
    sudo rm -rf "$path"
    echo "Removed: $path"
  else
    echo "Error: $path does not exist." >&2
  fi
}

# List of directories and files to clean up
paths=(
  /opt/hostedtoolcache/Ruby
  /opt/hostedtoolcache/CodeQL
  /opt/hostedtoolcache/go
  /usr/share/dotnet
  /usr/share/swift
  /usr/share/az*
  /usr/share/php*
  /usr/share/R
  /usr/share/mono*
  /usr/share/mysql
  /usr/share/mozilla
  /usr/local/julia*
  /usr/lib/mono
  /usr/local/lib/heroku
  /usr/lib/firefox
  /usr/include/php
  /home/linuxbrew
  /home/runneradmin/.dotnet
  /usr/local/share/powershell
  /usr/local/.ghcup/ghc/
  /usr/local/graalvm
  /home/runner/.rustup
  /home/runner/.cargo
  /home/runner/.dotnet
  /home/runner/perflog
  /home/runneradmin/.rustup
  /home/runneradmin/.cargo
  /opt/microsoft
  /etc/skel/.dotnet
  /etc/skel/.rustup
  /etc/skel/.cargo
  /usr/local/share/chromium
  /usr/lib/llvm-*
  /opt/google
  /opt/hhvm
  /usr/local/share/chromium
  /usr/bin/php*
  /var/lib/mysql
  /usr/local/aws-cli
  /usr/local/aws-sam-cli
  /usr/lib/erlang
  /usr/local/sqlpackage
  /usr/bin/mongod
)

# Iterate over the paths and attempt to remove them
for path in "${paths[@]}"; do
  remove_path "$path"
done

echo "cleanup completed."
echo "df -h after cleanup"
df -h