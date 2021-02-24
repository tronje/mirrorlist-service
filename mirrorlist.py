#!/usr/bin/env python3

import argparse
import time
import sys
import os


def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M")
    print(ts + " :: " + msg, file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create an up-to-date mirrorlist from mirrorlist.pacnew"
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Path to the directory in which the mirrorlist and mirrorlist.pacnew reside",
        default="/etc/pacman.d/",
    )
    parser.add_argument(
        "-c",
        "--country",
        help="The country for which to generate a mirrorlist",
    )
    parser.add_argument(
        "-s",
        "--https-only",
        help="Select only mirrors with HTTPS support",
        action="store_true",
    )
    return parser.parse_args()


def select_mirrors(filename, country):
    record = False
    mirrors = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if record:
                if len(line) == 0:
                    # end of country block
                    break
                else:
                    mirrors.append(line)
            else:
                if country in line:
                    # beginning of country block
                    record = True
    return mirrors


def prepare_mirrors(mirrors, https_only):
    cleaned_mirrors = []
    for mirror in mirrors:
        if https_only:
            if "https://" not in mirror:
                continue
        if mirror.startswith("#"):
            cleaned_mirrors.append(mirror[1:])
    return cleaned_mirrors


def main():
    args = parse_args()

    directory = args.directory
    infile = os.path.join(directory, "mirrorlist.pacnew")
    outfile = os.path.join(directory, "mirrorlist")
    country = args.country
    https_only = args.https_only

    if not os.path.isfile(infile):
        log("Nothing to do")
        return 0

    if not os.path.isfile(outfile):
        log(f"Output file {outfile} does not yet exist!")

    mirrors = select_mirrors(infile, country)
    if not mirrors:
        log(f"No mirrors available for country {country} in {infile}")
        return 1

    mirrors = prepare_mirrors(mirrors, https_only)
    with open(outfile, "w") as f:
        f.write(f"## Generated from {infile} with mirrorlist.py ##\n")
        f.write("\n".join(mirrors) + "\n")
        log(f"Wrote {len(mirrors)} mirrors for country {country} to {outfile}")

    try:
        os.remove(infile)
    except Exception as e:
        log(f"Failed to remove file {infile}: {e}")
        return 1

    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
