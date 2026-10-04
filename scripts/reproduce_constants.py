"""Evaluate the manuscript limiting constants with exact rational bounds."""
from pathlib import Path
import runpy

if __name__=="__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1]/"companion"/"limit_constants.py"),run_name="__main__")
