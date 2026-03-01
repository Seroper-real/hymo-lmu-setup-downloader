from pathlib import Path
import sys

def get_base_dir() -> Path:
    # Case exe (PyInstaller)
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR = get_base_dir()

def get_path(value: str | Path) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (BASE_DIR / p).resolve()
