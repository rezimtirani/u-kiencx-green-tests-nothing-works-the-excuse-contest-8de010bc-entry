"""Green Tests, Nothing Works — make.fun entry.

Writes one line — the excuse for a codebase whose tests are all green
while the app itself is broken — to $MAKEFUN_OUTPUT_DIR/entry.txt.
Only the Python standard library is used.
"""

import os
import sys

EXCUSE = "All 412 tests pass. The app still crashes on login — but the tests never logged in, so technically, nothing failed."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 140 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 140


def check_excuse(text):
    """Return the excuse once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line of 1 to 140 characters, not only white space, with no
    trailing newline in the output file.
    """
    if not isinstance(text, str):
        raise TypeError("excuse must be text")
    if not text.strip():
        raise ValueError("excuse must not be only white space")
    if len(text) > MAX_CHARS:
        raise ValueError("excuse is {} chars, over the {}-char gate".format(len(text), MAX_CHARS))
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    return text


def describe_result(line):
    """Return a one-line summary of the written entry for the console.

    Reports the entry in characters and in UTF-8 bytes, so a wide
    character (like the em dash) shows up as a byte/character gap
    instead of silently changing the count.
    """
    return "entry is {} characters, {} UTF-8 bytes".format(
        len(line), len(line.encode("utf-8")))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        raise SystemExit(2)
    os.makedirs(out_dir, exist_ok=True)
    line = check_excuse(EXCUSE)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print("wrote {} ({})".format(target, describe_result(line)))


if __name__ == "__main__":
    main()
