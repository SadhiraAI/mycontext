"""Minimal unified-diff parser (offline, dependency-free).

Just enough to support ``trace(..., diff=...)``: per changed file, the added and
removed lines. We don't try to be a full patch engine — we only need the text of
the change so we can keyword-match it against requirement IDs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class FileDiff:
    path: str
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)


def parse_diff(text: str) -> list[FileDiff]:
    """Parse unified-diff ``text`` into a list of :class:`FileDiff`."""
    files: list[FileDiff] = []
    current: FileDiff | None = None

    for line in (text or "").splitlines():
        # New file header: prefer the "+++ b/path" form, fall back to "diff --git".
        m = re.match(r"^\+\+\+ [ab]/(.+)$", line)
        if m:
            path = m.group(1).strip()
            if current is None or current.path != path:
                current = FileDiff(path=path)
                files.append(current)
            continue
        m = re.match(r"^diff --git a/(\S+) b/(\S+)", line)
        if m:
            current = FileDiff(path=m.group(2))
            files.append(current)
            continue
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if current is None:
            continue
        if line.startswith("+"):
            current.added.append(line[1:].strip())
        elif line.startswith("-"):
            current.removed.append(line[1:].strip())

    # Drop entries that captured no real path.
    return [f for f in files if f.path and f.path != "/dev/null"]
