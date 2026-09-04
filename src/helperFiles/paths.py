import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path(sys.executable).resolve().parent / "data" if getattr(sys, "frozen", False) else SOURCE_ROOT / "data"
DATA_ROOT.mkdir(parents=True, exist_ok=True)


def resource_path(*parts):
    root = Path(getattr(sys, "_MEIPASS", SOURCE_ROOT))
    return root.joinpath(*parts)


def data_path(*parts):
    path = DATA_ROOT.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
