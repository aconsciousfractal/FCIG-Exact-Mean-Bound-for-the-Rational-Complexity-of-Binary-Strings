"""Guard rational interval operations needed by the limiting-constant certificate."""
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"companion"))
from limit_constants import Interval,ln2_interval,zeta_interval,li4_interval,outward_decimal,evaluate


class ConstantTests(unittest.TestCase):
    def test_signs_powers_and_division(self):
        x=Interval(-2,3)
        self.assertEqual((x**2).lo,F(0))
        self.assertEqual((x**2).hi,F(9))
        self.assertEqual((x**3).lo,F(-8))
        self.assertEqual((x**3).hi,F(27))
        y=Interval(2,4)
        self.assertEqual(y.reciprocal(),Interval(F(1,4),F(1,2)))
        with self.assertRaises(ValueError):x.reciprocal()
        with self.assertRaises(ValueError):Interval(1,0)

    def test_exactness_and_domains(self):
        for value in (1.0,True,"1",complex(1)):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):Interval(value,value)
        for operation in (lambda:zeta_interval(2,0),lambda:zeta_interval(2,True),
                          lambda:zeta_interval(2.0,4),lambda:ln2_interval(0),
                          lambda:li4_interval(1.0),lambda:Interval(1,2)**True):
            with self.assertRaises(ValueError):operation()

    def test_signed_outward_rounding(self):
        self.assertEqual(outward_decimal(F(-1,3),2,False),"-0.34")
        self.assertEqual(outward_decimal(F(-1,3),2,True),"-0.33")
        self.assertEqual(outward_decimal(F(1,3),2,False),"0.33")
        self.assertEqual(outward_decimal(F(1,3),2,True),"0.34")

    def test_series_enclosures_nest(self):
        for function in (ln2_interval,li4_interval,lambda k:zeta_interval(2,k),
                         lambda k:zeta_interval(3,k),lambda k:zeta_interval(4,k)):
            wide=function(2);narrow=function(8)
            self.assertLessEqual(wide.lo,narrow.lo)
            self.assertGreaterEqual(wide.hi,narrow.hi)

    def test_stated_bounds(self):
        data=evaluate()
        self.assertEqual(data["limiting_variance_base2_R"]["decimal_lower"],"0.892302571204274625294755")
        self.assertEqual(data["limiting_variance_base2_R"]["decimal_upper"],"0.892302571204274625294756")
        self.assertFalse(data["floating_arithmetic_used"])

if __name__=="__main__":
    unittest.main()
