from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKSUMS = ROOT / "checksums.json"
TEXT_SUFFIXES = {".ablock", ".json", ".macro", ".md", ".py", ".js"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitkeep":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def update_remote_manifests() -> int:
    count = 0
    for path in sorted(ROOT.rglob("remote_manifest.json")):
        manifest = load(path)
        for item in manifest.get("files", []):
            target = ROOT / item["path"]
            if not target.is_file():
                raise FileNotFoundError(
                    f"{path.relative_to(ROOT)} referencia arquivo ausente: {item['path']}"
                )
            item["checksum_sha256"] = sha256(target)
        write(path, manifest)
        count += 1
    return count


def update_complete_map() -> int:
    current = load(CHECKSUMS)
    current["text_normalization"] = "lf"
    files = {
        path.relative_to(ROOT).as_posix(): sha256(path)
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path != CHECKSUMS
    }
    current["scope"] = "complete_src_tree_except_checksums_json"
    current["files"] = files
    write(CHECKSUMS, current)
    return len(files)


def main() -> None:
    manifests = update_remote_manifests()
    files = update_complete_map()
    print(f"Distribution metadata: OK (remote_manifests={manifests}, files={files})")


if __name__ == "__main__":
    main()
