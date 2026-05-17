"""
ar_UpdateScriptsCollection

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: Update Scripts Collection
Version: 1.3.0
Description-US: Updates the JSON-file, that contains information about the scripts..

Written for Blackmagic Design Fusion Studio 21.0 beata build 31.
Python version 3.13.7 (64-bit).

Installation path: Appdata/Roaming/Blackmagic Design/Fusion/Scripts/Comp

Changelog:
1.0.0 (17.05.2026) - Initial realease.
"""
# Libraries
import inspect
from pathlib import Path
import json
from typing import Any


# Global variables
script_dir  = Path(inspect.getfile(lambda: None)).resolve().parent.parent
icon_folder = script_dir / "Icons"


# Functions
def extract_metadata(py_file: Path) -> dict[str, str]:
    """."""

    name: str | None = None
    desc: str | None = None

    try:
        with py_file.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()

                if stripped.startswith("Name-US:"):
                    name = stripped.removeprefix("Name-US:").strip()

                elif stripped.startswith("Description-US:"):
                    desc = stripped.removeprefix("Description-US:").strip()

                if name and desc:
                    break

    except Exception as e:
        print(f"Virhe luettaessa tiedostoa {py_file}: {e}")

    return {
        "name": name if name else py_file.stem,
        "desc": desc or "",
    }


def build_icon_map(icon_root: Path) -> tuple[dict[str, Path], Path | None]:
    """."""

    icon_map: dict[str, Path] = {}
    default_icon: Path | None = None

    for icon_path in icon_root.rglob("*.png"):
        resolved = icon_path.resolve()

        if icon_path.name == "default_script.png":
            default_icon = resolved
        else:
            icon_map[icon_path.stem] = resolved

    return icon_map, default_icon


def scan_folder(root_folder: Path, icon_folder: Path) -> list[dict[str, str]]:
    """."""

    data: list[dict[str, str]] = []

    icon_map, default_icon = build_icon_map(icon_folder)

    for py_file in root_folder.rglob("*.py"):
        metadata = extract_metadata(py_file)

        icon_path = icon_map.get(py_file.stem)
        if icon_path is None:
            icon_path = default_icon

        entry = {
            "name": metadata["name"],
            "desc": metadata["desc"],
            "path": str(py_file.resolve()),
            "icon": str(icon_path) if icon_path else "",
        }

        data.append(entry)

    return data


def main() -> None:
    """The main function."""

    output_file = Path(script_dir / "scripts_collection.json")
    if not output_file.exists():
        output_file.touch()

    result = scan_folder(script_dir, icon_folder)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"JSON luotu: {output_file}")


if __name__ == "__main__":
    main()