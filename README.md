# mirrorlist-service

A simple Python script and systemd setup to handle mirrorlist.pacnew files.

## What?

Arch Linux's package manager, pacman, works with a system of mirrors, so that
Arch Linux itself does not have to stand up to the traffic of the many millions
of Arch Linux users whenever they update. The mirrors are stored in a mirrorlist,
which is often updated.
Whenever it is updated, the file (`/etc/pacman.d/mirrorlist`) is not simply
overwritten, so as not to discard user changes. Instead, the newest version is
saved to `/etc/pacman.d/mirrorlist.pacnew`.

This little project is designed to notice whenever a `mirrorlist.pacnew` shows
up, and to then generate a new `mirrorlist` from it, and remove the `.pacnew`
file.

## Why?

Because every time I update I get a `mirrorlist.pacnew`, and I can't just let it
sit there, but I also don't want to replace my `mirrorlist` manually every time.

## How?

You can use the script as a standalone thing and run it whenever you need to.
```console
$ ./mirrorlist.py --help
```

To utilize the systemd service, and have your `mirrorlist.pacnew` taken care of
automatically whenever one is installed:

Edit `systemd/mirrorlist.service` and change the `mirrorlist.py` invocation to
suit your needs.

Then take a look at `install.sh`. If that looks like a change you would want to
make to your system, run:

```console
$ sudo ./install.h
$ sudo systemctl enable mirrorlist.path
$ sudo systemctl enable mirrorlist.service
$ sudo systemctl start mirrorlist.path
```
