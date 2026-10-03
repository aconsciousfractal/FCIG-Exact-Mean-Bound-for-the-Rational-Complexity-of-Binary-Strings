"""Directed arithmetic and reader-package failure controls; no full bridge resummation."""
from copy import deepcopy
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

mean = load("mean", ROOT/"companion/verify_mean.py")
manifest = load("manifest", ROOT/"scripts/check_manifest.py")

class ArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT/"companion/finite_certificates.json").read_text())

    def test_directed_log_bounds_independent_decimal(self):
        with localcontext() as ctx:
            ctx.prec = 75
            for num, den in [(1,1),(1001,1000),(3,2),(2,1)]:
                exact = (Decimal(num)/Decimal(den)).ln()*mean.SCALE
                self.assertLessEqual(Decimal(mean.unit_log(num,den,False)), exact)
                self.assertGreaterEqual(Decimal(mean.unit_log(num,den,True)), exact)
            for num, den in [(7,2),(1024,1),(1000001,3)]:
                exact = (Decimal(num)/Decimal(den)).ln()*mean.SCALE
                self.assertGreaterEqual(Decimal(mean.log_upper(num,den)),exact)

    def test_invalid_log_domains(self):
        for num, den in [(0,1),(1,0),(1,2),(3,1),(True,1)]:
            with self.assertRaises(ValueError):
                mean.unit_log(num,den,True)
        for num, den in [(0,1),(1,0),(1,2)]:
            with self.assertRaises(ValueError):
                mean.log_upper(num,den)

    def test_missing_levels_and_invalid_witness(self):
        d = deepcopy(self.data); d["small"].pop()
        with self.assertRaisesRegex(ValueError,"coverage"):
            mean.small_check(d)
        d = deepcopy(self.data); d["small"][0]["witnesses"][0][1] = 2
        with self.assertRaisesRegex(ValueError,"witness"):
            mean.small_check(d)
        d = deepcopy(self.data); d["bridge"].pop()
        with self.assertRaisesRegex(ValueError,"coverage"):
            mean.bridge_shape(d)

    def test_quick_cli_output(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)/"quick.json"
            flags = ["-B"] + (["-O"] if sys.flags.optimize else [])
            result = subprocess.run([sys.executable,*flags,str(ROOT/"scripts/reproduce.py"),
                                     "--quick","--output",str(out)],check=True,capture_output=True,text=True)
            d = json.loads(out.read_text())
            self.assertEqual(d,json.loads(result.stdout))
            self.assertEqual(d["status"],"PASS_QUICK_STRUCTURAL_ONLY")
            self.assertEqual(d["small"]["minima"],8190)
            self.assertIsNone(d["bridge"])
            self.assertFalse(d["all_N_proved_by_checker_alone"])

class ManifestTests(unittest.TestCase):
    def fixture(self, root):
        (root/"reader.txt").write_bytes(b"reader")
        row = hashlib.sha256(b"reader").hexdigest()+"  reader.txt\n"
        (root/manifest.MANIFEST).write_text(row)
        return row

    def test_normal_clone_and_build_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.fixture(root)
            (root/".git").mkdir(); (root/".git/config").write_text("local Git metadata")
            (root/"build").mkdir(); (root/"build/replay.json").write_text("generated")
            self.assertEqual(manifest.verify(root)["status"],"MANIFEST_PASS")

    def test_malformed_duplicate_escape_and_self_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); row=self.fixture(root)
            for text in ["bad\n",row+row,"0"*64+"  ../reader.txt\n",
                         "0"*64+"  MANIFEST_SHA256.txt\n","0"*64+"  C:/reader.txt\n"]:
                (root/manifest.MANIFEST).write_text(text)
                with self.assertRaises(ValueError): manifest.verify(root)

    def test_missing_tampered_and_unexpected_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.fixture(root)
            (root/"reader.txt").unlink()
            with self.assertRaisesRegex(ValueError,"file-set"): manifest.verify(root)
            (root/"reader.txt").write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError,"hash mismatch"): manifest.verify(root)
            self.fixture(root); (root/"extra.txt").write_text("extra")
            with self.assertRaisesRegex(ValueError,"file-set"): manifest.verify(root)

if __name__ == "__main__":
    unittest.main()
