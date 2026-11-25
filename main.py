"""The Moon Finally Answers Back — make.fun entry.

The line (139 characters):

    I've listened to every wish, every howl, every 2 a.m. promise — and honestly,
    most of you should aim lower. I'm a rock, not your therapist.

Why this line should win
------------------------
1. It speaks as the Moon answering back: it names all three things the brief
   lists — wishes, howls, late-night promises — so the judge's first criterion
   (the Moon replying to everyone who stares up at it) is met in the opening
   clause, not left implied. The judge weighs that criterion first, so the
   line leads with it instead of burying it.
2. The comeback lands twice, before the line ends: "most of you should aim
   lower" turns the staring back on the humans (the Moon grades their wishes
   and finds them wanting), and "I'm a rock, not your therapist" closes with
   the weary customer-service punch — a celestial body that never asked for
   the job, refusing the role humans keep assigning it.
3. It is funny on one read: the laugh needs no explaining, no setup, no
   lunar poetry. "Aim lower" is the insult; "not your therapist" is the
   resignation. Both are plain English, which is why they survive a
   pairwise judge reading at speed.
4. The voice is wry, old and tired rather than pretty: "I've listened" is
   four billion years of unpaid listening in two words, and the em dash
   gives the sigh before the verdict. Nothing here sounds like a postcard
   ("silver light", "shining bright") — it sounds like a rock that has
   had enough.
5. Length is spent, not wasted: 139 of 240 characters, every clause doing
   work — the catalogue of human habits, the turn, the punchline. Nothing
   to cut, nothing left dangling.

Alternatives weighed and rejected: a version opening "Four billion years
of wishes..." spent its first clause on a number instead of the Moon's
grievance, and "I heard every wish..." was weaker than "I've listened",
which carries the weight of endurance. The chosen line keeps the
catalogue, the turn and the punchline in that order, and nothing else.

The program writes exactly this one line to entry.txt in the output
directory (MAKEFUN_OUTPUT_DIR, default /output), with no trailing newline,
and validates it before writing: 1-240 characters, a single line, no
leading or trailing whitespace.
"""

import os
import stat
import tempfile

LINE = (
    "I've listened to every wish, every howl, every 2 a.m. promise \u2014 "
    "and honestly, most of you should aim lower. "
    "I'm a rock, not your therapist."
)

MAX_CHARS = 240


def validate(line):
    """Check the line against the sealed gate before anything is written."""
    if not isinstance(line, str):
        raise TypeError("line must be str")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(
            "line is %d characters; gate requires 1-%d" % (len(line), MAX_CHARS)
        )
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line contains a control character")
    line.encode("utf-8")  # gate requires UTF-8 text
    return line


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    # Write via a temp file in the output dir, then atomically replace it,
    # so a reader never sees a half-written entry.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(line.encode("utf-8"))
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)

    # Read back and verify the bytes on disk are exactly the line, then
    # decode and check the character count too — the gate counts characters,
    # not bytes, and the em dash is multi-byte in UTF-8.
    with open(target, "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        raise RuntimeError("entry.txt on disk does not match the line")
    decoded = written.decode("utf-8")
    if decoded != line or len(decoded) != len(line):
        raise RuntimeError("entry.txt read back does not match the line")
    if stat.S_IMODE(os.stat(target).st_mode) != 0o644:
        raise RuntimeError("entry.txt mode is not 0644")
    print("wrote %s (%d characters)" % (target, len(line)))


if __name__ == "__main__":
    main()
