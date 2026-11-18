"""Copy the bundled news image to the harness output path.

The repository holds entry.png (a front page summing up the world's news
of Tuesday 17 November 2026, drawn by build_image.py). The program just
copies it to /output/entry.png: deterministic, no network, same bytes
on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST = "/output/entry.png"


def main():
    # The harness gives us a writable /output; the repository itself is
    # read-only at run time, so copy the bundled image there.
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    assert os.path.getsize(DEST) == os.path.getsize(SOURCE)


if __name__ == "__main__":
    main()
