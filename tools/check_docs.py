from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = {"README.md", "AGENTS.md"}
LINK = re.compile(r"!?\[[^]]*]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    documents = manifest.get("documents", [])
    ids = [document["id"] for document in documents]
    paths = [document["path"] for document in documents]

    if len(ids) != len(set(ids)):
        fail(errors, "manifest.json contains duplicate document ids")
    if len(paths) != len(set(paths)):
        fail(errors, "manifest.json contains duplicate document paths")

    markdown_paths = {
        path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.md")
    }
    registered = set(paths)
    unregistered = markdown_paths - registered - ENTRYPOINTS
    missing = registered - markdown_paths
    for path in sorted(unregistered):
        fail(errors, f"unregistered Markdown document: {path}")
    for path in sorted(missing):
        fail(errors, f"manifest path does not exist: {path}")

    hashes: dict[str, str] = {}
    for relative in sorted(markdown_paths):
        path = ROOT / relative
        content = path.read_text(encoding="utf-8")
        digest = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()
        if digest in hashes:
            fail(errors, f"duplicate Markdown content: {relative} and {hashes[digest]}")
        hashes[digest] = relative

        for raw_target in LINK.findall(content):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = unquote(target.split("#", 1)[0])
            resolved = (path.parent / target_path).resolve()
            if not resolved.is_relative_to(ROOT):
                fail(errors, f"link escapes repository: {relative} -> {target}")
            elif not resolved.exists():
                fail(errors, f"broken relative link: {relative} -> {target}")

    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(markdown_paths)} Markdown files and {len(documents)} manifest entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
