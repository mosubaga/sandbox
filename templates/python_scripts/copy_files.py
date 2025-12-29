import sys
import shutil
from pathlib import Path

################################################################################
ROOT_DIR = "<rootDir>"
################################################################################

EURO_LANGS = {"german", "french", "spanish", "italian", "swedish", "finnish"}
TARGET_EXTS = {".xxx", ".yyy"}


def normalize_language(lang):
    print(f"Copying for language: {lang}")
    return "euro" if lang in EURO_LANGS else lang


def list_files(root_dir, lang):
    root_path = Path(root_dir)
    matches = []

    for path in root_path.rglob("*"):
        if path.is_file() and path.suffix in TARGET_EXTS:
            if lang in str(path):
                matches.append(path)

    return matches


def copy_files(files, root_dir):
    root_path = Path(root_dir)

    for src in files:
        tgt = root_path / src.name
        if tgt.is_file():
            tgt.unlink()
        print(f"Copying {src} to {tgt} ... ")
        shutil.copy(src, tgt)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: copy_files.py <language>")

    lang = normalize_language(sys.argv[1])
    files = list_files(ROOT_DIR, lang)
    copy_files(files, ROOT_DIR)
    print("Finish copying ...\n")


if __name__ == "__main__":
    main()
