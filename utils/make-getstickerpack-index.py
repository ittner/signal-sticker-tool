#!/usr/bin/env python3

#
# Utility script to generate yaml definitions for stickers downloaded
# from getstickerpack, so signal-sticker-tool can upload them to Signal.
#
# This tool is called automatically by convert-getstickerpack.sh
#

import os
import re
import yaml
import sys


VALID_IMAGE_TYPES = set(["png", "webp"])


def get_info_file(path, fname):
    fpath = os.path.join(path, fname)
    try:
        with open(fpath) as fp:
            s = fp.read()
        return s.strip()
    except:
        pass
    return None


def generate(path):

    files = os.listdir(path)
    image_files = [
        os.path.normpath(f)
        for f in files
        if f.split(".", 1)[-1].lower() in VALID_IMAGE_TYPES
    ]

    author = get_info_file(path, "author.txt") or "fill-author-name-here"
    title = get_info_file(path, "title.txt")
    if not title:
        # Try to get a placeholder title from path:
        # /home/user/path/to/my-sticker-set -> my-sticker-set
        elements = [e for e in path.split("/") if e.strip() != ""]
        if len(elements) > 0:
            title = elements[-1]
    if not title:
        title = "fill-title-here"

    # Find cover image (if any) and remove it from sticker list.
    cover_fname = "tray"
    sticker_files = []
    cover = None
    for tmp in image_files:
        if tmp.split(".", 1)[0] == cover_fname:
            # Can have more than a single cover, just pick the first one.
            if not cover:
                cover = tmp
        else:
            sticker_files.append(tmp)

    # Put stickers in some natural order so "sticker_9.webp" comes before
    # "sticker_10.webp". More than one file with the same prefix (e.g.
    # "sticker_42.webp" and "sticker_42.png") will mess up the order, but it
    # should not be a common thing.

    smap = dict()
    pending = []
    for tmp in sticker_files:
        m = re.match("sticker_([0-9]+)\.", tmp)
        if m:
            smap[int(m[1])] = tmp
        else:
            pending.append(tmp)
    sticker_list = [smap[k] for k in sorted(smap.keys())] + pending

    # That site gives no emoji list, assign numbers and letters sequentially.
    emojis = list("0123456789abcdefghijklmnopqrstuvwxyz")[0 : len(sticker_list)]
    if len(sticker_list) > len(emojis):  # That's a big pack ...
        emojis += (len(sticker_list) - len(emojis)) * ["put_emoji_here"]
    stickers = [{"chr": emojis.pop(0), "file": f} for f in sticker_list]

    base = {
        "meta": {
            "title": title,
            "author": author,
            "cover": cover,
        },
        "stickers": stickers,
    }

    dest_file = os.path.join(path, "stickers.yaml")
    try:
        with open(dest_file, "x") as fp:
            yaml.safe_dump(base, fp, allow_unicode=True, default_flow_style=False)
    except FileExistsError:
        raise Exception(
            "Sticker index %s already exists. Delete it if you "
            "want to generate a new one." % (dest_file)
        )


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            sys.stderr.write("Usage: %s <path>\n" % sys.argv[0])
            exit(1)
        generate(sys.argv[1])
        exit(0)
    except Exception as exc:
        sys.stderr.write("Error: %s\n" % str(exc))
    exit(1)
