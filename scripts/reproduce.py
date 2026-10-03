"""Replay the exact finite premises; forward all CLI arguments to the companion."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1]/"companion"/"verify_mean.py"), run_name="__main__")
