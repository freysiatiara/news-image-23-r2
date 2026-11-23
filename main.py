#!/usr/bin/env python3
"""Entrypoint (stdlib only): copy entry.png to the output location.

The PNG is rendered ahead of time by draw.py (which needs Pillow); the
grading environment is stdlib-only, so this entrypoint just verifies and
copies the committed image. Paths are resolved from this file's own
location, never from the working directory.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024  # 1 MiB
MAX_DIM = 1024


def png_size(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise ValueError("entry.png exceeds 1 MiB: %d bytes" % len(data))
    w, h = png_size(data)
    if w > MAX_DIM or h > MAX_DIM:
        raise ValueError("entry.png exceeds 1024x1024: %dx%d" % (w, h))

    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("OUTPUT_DIR")
               or ("/output" if os.path.isdir("/output") else os.getcwd()))
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dest) != os.path.abspath(SRC):
        shutil.copyfile(SRC, dest)
    print("entry.png -> %s (%d bytes, %dx%d)" % (dest, len(data), w, h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
