"""Stage the server documentation builder, validate links, then install changed outputs only."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server", type=Path)
    args = parser.parse_args()
    target = args.server.resolve() / "docs"
    fragment = Path("docs/clashroyaleapi.html").resolve()
    with tempfile.TemporaryDirectory(prefix="clashroyale-docs-") as temporary:
        stage = Path(temporary) / "docs"
        shutil.copytree(target, stage, ignore=shutil.ignore_patterns("dist", "__pycache__"))
        shutil.copy2(fragment, stage / "content/clashroyaleapi.html")
        subprocess.run([sys.executable, str(stage / "build.py")], check=True)
        page = stage / "dist/clashroyaleapi/index.html"
        soup = BeautifulSoup(page.read_text(), "html.parser")
        ids = {t["id"] for t in soup.select("[id]")}
        missing = {
            a["href"][1:]
            for a in soup.select('a[href^="#"]')
            if a["href"] != "#" and a["href"][1:] not in ids
        }
        if missing:
            raise RuntimeError(f"Broken anchors: {missing}")
        if "clashroyaleapi" not in (stage / "dist/index.html").read_text():
            raise RuntimeError("Portal does not include ClashRoyaleAPI")
        outputs = [(fragment, target / "content/clashroyaleapi.html")]
        outputs += [
            (p, target / "dist" / p.relative_to(stage / "dist"))
            for p in (stage / "dist").rglob("*")
            if p.is_file()
        ]
        changed = []
        for source, destination in outputs:
            if destination.exists() and source.read_bytes() == destination.read_bytes():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as out:
                out.write(source.read_bytes())
                name = out.name
            os.chmod(name, 0o644)
            os.replace(name, destination)
            changed.append(str(destination))
        print("Installed changed files:\n" + "\n".join(changed))


if __name__ == "__main__":
    main()
