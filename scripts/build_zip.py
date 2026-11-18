#!/usr/bin/env python3
"""Validate the skill and build the upload zip(s) into dist/. Standard library only.

    python scripts/build_zip.py

dist/<name>.zip       upload this to a Claude or ChatGPT account (200 files at most)
dist/<name>-full.zip  complete copy for Claude Code / Codex (only for skills with a lite build)
"""
import hashlib
import json
import os
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "packaging.json").read_text(encoding="utf-8"))
NAME = CFG["name"]
VERSION = CFG["version"]
SKILL = ROOT / "skills" / NAME
MAX_FILES = 200
MAX_DESCRIPTION = 1024
NEVER = {"sites.txt", ".env", ".DS_Store", "Thumbs.db"}
NEVER_DIRS = {"__pycache__", "node_modules", ".git", ".venv"}
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def fail(message):
    sys.exit("ERROR: " + message)


def frontmatter(text):
    match = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        fail("SKILL.md has no YAML frontmatter")
    fields, key = {}, None
    for line in match.group(1).replace("\r", "").split("\n"):
        found = re.match(r"([A-Za-z_-]+):\s*(.*)$", line)
        if found and not line.startswith(" "):
            key = found.group(1)
            fields[key] = found.group(2).strip()
        elif key:
            fields[key] += " " + line.strip()
    for key, value in fields.items():
        value = re.sub(r"^[>|][+-]?\s*", "", value).strip()
        fields[key] = value[1:-1] if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'" else value
    return fields


def validate():
    entry = SKILL / "SKILL.md"
    if not entry.is_file():
        fail("missing skills/%s/SKILL.md" % NAME)
    fields = frontmatter(entry.read_text(encoding="utf-8"))
    if fields.get("name") != NAME:
        fail("frontmatter name %r does not match %r" % (fields.get("name"), NAME))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", NAME) or len(NAME) > 64:
        fail("invalid skill name")
    if not fields.get("description"):
        fail("frontmatter description is empty")
    if len(fields["description"]) > MAX_DESCRIPTION:
        fail("description is %d characters; the limit is %d" % (len(fields["description"]), MAX_DESCRIPTION))
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if plugin["version"] != VERSION:
        fail("plugin.json version differs from packaging.json")
    if os.environ.get("GITHUB_REF_TYPE") == "tag" and os.environ.get("GITHUB_REF_NAME") != "v" + VERSION:
        fail("tag %s does not match version v%s" % (os.environ.get("GITHUB_REF_NAME"), VERSION))


def all_files():
    for path in sorted(SKILL.rglob("*")):
        rel = path.relative_to(SKILL)
        if path.is_file() and path.name not in NEVER and path.suffix != ".pyc" and not NEVER_DIRS & set(rel.parts):
            yield path, rel.as_posix()


def lite_keep(rel, lite):
    parts = rel.split("/")
    if set(parts[:-1]) & set(lite["exclude_dirs"]):
        return False
    return parts[-1] in lite["include_names"] or pathlib.PurePosixPath(rel).suffix.lower() in lite["include_suffixes"]


def write_zip(target, files, note=None):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, rel in files:
            data = path.read_bytes()
            if note and rel == "SKILL.md":
                text = data.decode("utf-8")
                end = re.match(r"---\r?\n.*?\r?\n---\r?\n", text, re.S).end()
                data = (text[:end] + "\n" + note.strip() + "\n" + text[end:]).encode("utf-8")
            info = zipfile.ZipInfo("%s/%s" % (NAME, rel), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    print("%s: %d files, %.2f MB" % (target.name, len(files), target.stat().st_size / 1e6))


def main():
    validate()
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    files = list(all_files())
    lite = CFG.get("lite")
    if lite:
        keep = [item for item in files if lite_keep(item[1], lite)]
        note = (ROOT / "packaging" / "lite-note.md").read_text(encoding="utf-8")
        write_zip(dist / (NAME + "-full.zip"), files)
    else:
        keep, note = files, None
    if len(keep) > MAX_FILES:
        fail("upload zip has %d files; the limit is %d" % (len(keep), MAX_FILES))
    write_zip(dist / (NAME + ".zip"), keep, note)
    sums = ["%s  %s" % (hashlib.sha256(z.read_bytes()).hexdigest(), z.name) for z in sorted(dist.glob("*.zip"))]
    (dist / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
