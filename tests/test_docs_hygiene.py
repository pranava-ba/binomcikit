"""Guards for the Markdown sources: encoding damage and MyST constructs that render wrongly.

None of these fail a ``sphinx -W`` build, so they were only ever found by reading the rendered pages.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "_build", "node_modules", ".venv", "paper-explorer", "previous-work"}
MD_FILES = sorted(p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts))
# UTF-8 text decoded as cp1252 and saved again: "â€”" for an em dash, "Ã©" for "é", ...
MOJIBAKE = re.compile("â€|Ã[\u0080-¿]|Â[ -¿]")
# Characters a "\theta"/"\alpha"/"\beta"/"\frac" typed through an escape-processing writer turns into.
BAD_CONTROL = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _ids(paths):
    return [str(p.relative_to(ROOT)) for p in paths]


def test_markdown_files_were_found():
    assert len(MD_FILES) > 50


@pytest.mark.parametrize("path", MD_FILES, ids=_ids(MD_FILES))
def test_markdown_encoding_is_clean(path):
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM"
    text = raw.decode("utf-8")  # raises on invalid UTF-8
    assert "�" not in text, "U+FFFD replacement character"
    assert not BAD_CONTROL.search(text), "control character (an eaten backslash escape?)"
    assert not MOJIBAKE.search(text), "double-encoded text (mojibake)"
    assert not (b"\r\n" in raw and re.search(rb"(?<!\r)\n", raw)), "mixed CRLF/LF line endings"


@pytest.mark.parametrize("path", MD_FILES, ids=_ids(MD_FILES))
def test_no_tab_inside_inline_math(path):
    """A TAB inside ``$...$`` is a ``\\t`` that ate the backslash of ``\\theta``/``\\times``."""
    in_fence = False
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
        if in_fence:
            continue
        for m in re.finditer(r"(?<!\\)\$([^$\n]+)\$", line):
            assert "\t" not in m.group(1), f"{path.name}:{n}: tab inside math"


DOCS = [
    p for p in MD_FILES if "docs" in p.relative_to(ROOT).parts[:1] and "reference" not in p.parts
]


@pytest.mark.parametrize("path", DOCS, ids=_ids(DOCS))
def test_display_math_is_not_glued_to_text_below(path):
    """``$$...$$`` on one line with prose directly above *and* below it is read by MyST as inline math."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    in_fence = False
    for i, line in enumerate(lines):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
        s = line.strip()
        if in_fence or not (s.startswith("$$") and s.endswith("$$") and len(s) > 4):
            continue
        above = lines[i - 1].strip() if i else ""
        below = lines[i + 1].strip() if i + 1 < len(lines) else ""
        assert not (above and below), f"{path.name}:{i + 1}: add a blank line above and below"


@pytest.mark.parametrize("path", DOCS, ids=_ids(DOCS))
def test_roles_do_not_contain_math(path):
    """MyST roles such as {doc}`...` take plain text; ``$x$`` in the link text is shown literally."""
    text = path.read_text(encoding="utf-8-sig")
    for m in re.finditer(r"\{(?:doc|ref|term)\}`([^`]*)`", text):
        assert "$" not in m.group(1), f"{path.name}: math inside role: {m.group(0)}"
