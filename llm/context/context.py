"""Download package documentation into llm/context/<name>/ folders."""

import shutil
import subprocess
import tempfile
from pathlib import Path

# key: folder name under llm/context/
# value: {"repo": git clone URL, "path": subdirectory to extract (e.g. "docs")}
SOURCES = {
    "streamlit": {
        "repo": "https://github.com/streamlit/docs.git",
        "path": "content",
    },
    "pynite": {
        "repo": "https://github.com/JWock82/Pynite.git",
        "path": "docs",
    },
    "eurocodepy": {
        "repo": "https://github.com/pcachim/eurocodepy.git",
        "path": "mkdocs/docs",
    },
}

CONTEXT_DIR = Path(__file__).parent


def download_source(name: str, source: dict) -> None:
    target = CONTEXT_DIR / name
    repo = source["repo"]
    sub_path = source.get("path", "docs")

    print(f"[{name}] Cloning {repo} ...")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        clone_cmd = [
            "git",
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            repo,
            "repo",
        ]
        subprocess.run(clone_cmd, cwd=tmp_path, check=True)
        repo_dir = tmp_path / "repo"
        subprocess.run(
            ["git", "sparse-checkout", "set", sub_path],
            cwd=repo_dir,
            check=True,
        )

        src = repo_dir / sub_path
        if not src.exists():
            print(f"[{name}] Warning: path '{sub_path}' not found in repo, skipping.")
            return

        # Remove existing and copy fresh
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(src, target)

    print(f"[{name}] Done -> {target}")


def main() -> None:
    for name, source in SOURCES.items():
        download_source(name, source)


if __name__ == "__main__":
    main()
