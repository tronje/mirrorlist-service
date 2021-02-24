#!/bin/sh

set -e

install -m 0744 mirrorlist.py /usr/local/bin/mirrorlist.py
install -m 0644 systemd/mirrorlist.path /usr/lib/systemd/system/mirrorlist.path
install -m 0644 systemd/mirrorlist.service /usr/lib/systemd/system/mirrorlist.service
