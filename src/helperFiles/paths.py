import sys
from pathlib import Path
from platformdirs import user_data_dir


SOURCE_ROOT = Path(__file__).resolve().parents[1]

# This will default to the correct user data directory for your system:
# Windows: C:\Users\<User>\AppData\Local\PasswordKeeper
# macOS:   /Users/<User>/Library/Application Support/PasswordKeeper
# Linux:   /home/<User>/.local/share/PasswordKeeper
DATA_ROOT = Path(user_data_dir("PasswordKeeper", "zacianculovici")).resolve() / "data"
DATA_ROOT.mkdir(parents=True, exist_ok=True)


def resource_path(*parts):
    root = Path(getattr(sys, "_MEIPASS", SOURCE_ROOT))
    return root.joinpath(*parts)


def data_path(*parts):
    path = DATA_ROOT.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
