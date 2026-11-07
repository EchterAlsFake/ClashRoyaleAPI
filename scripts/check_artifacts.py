"""Install wheel and sdist in independent environments and verify the public package."""

import subprocess
import tempfile
from pathlib import Path


def main():
    artifacts = sorted([*Path("dist").glob("*.whl"), *Path("dist").glob("*.tar.gz")])
    assert len(artifacts) == 2, "Expected exactly one wheel and one sdist"
    for artifact in artifacts:
        with tempfile.TemporaryDirectory(prefix="clashroyale-install-") as directory:
            env = Path(directory) / "venv"
            subprocess.run(["uv", "venv", str(env)], check=True)
            python = env / ("Scripts/python.exe" if (env / "Scripts").exists() else "bin/python")
            subprocess.run(
                ["uv", "pip", "install", "--python", str(python), str(artifact.resolve())],
                check=True,
            )
            subprocess.run(
                [
                    str(python),
                    "-c",
                    "from clashroyaleapi import Client, Player, __version__; "
                    "from importlib.resources import files; "
                    'assert __version__ == "1.0.1"; '
                    'assert files("clashroyaleapi").joinpath("py.typed").is_file(); '
                    'assert Player.model_validate({"collectionLevel": 42}).collection_level == 42; '
                    'print("Clean installation verified")',
                ],
                cwd=directory,
                check=True,
            )


if __name__ == "__main__":
    main()
