#!/usr/bin/env python3
"""Exact rational evaluation of the limiting logarithmic moments; stdlib only."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import json
from pathlib import Path

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def exact_fraction(value):
    if type(value) is int or isinstance(value,F):
        return F(value)
    raise ValueError("exact int or Fraction required, excluding bool")


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self):
        object.__setattr__(self, "lo", exact_fraction(self.lo))
        object.__setattr__(self, "hi", exact_fraction(self.hi))
        require(self.lo <= self.hi, "reversed interval")
    @staticmethod
    def lift(x):
        return x if isinstance(x, Interval) else Interval(exact_fraction(x),exact_fraction(x))
    def __add__(self, x):
        x=self.lift(x); return Interval(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self): return Interval(-self.hi,-self.lo)
    def __sub__(self,x): return self + (-self.lift(x))
    def __rsub__(self,x): return self.lift(x)+(-self)
    def __mul__(self,x):
        x=self.lift(x)
        vals=[self.lo*x.lo,self.lo*x.hi,self.hi*x.lo,self.hi*x.hi]
        return Interval(min(vals),max(vals))
    __rmul__=__mul__
    def reciprocal(self):
        require(self.lo>0 or self.hi<0,"interval division through zero")
        return Interval(1/self.hi,1/self.lo)
    def __truediv__(self,x): return self*self.lift(x).reciprocal()
    def __rtruediv__(self,x): return self.lift(x)*self.reciprocal()
    def __pow__(self,n):
        require(type(n) is int and n>=0,"nonnegative integer power required")
        if n==0: return self.lift(1)
        if n%2:
            return Interval(self.lo**n,self.hi**n)
        low=F(0) if self.lo<=0<=self.hi else min(self.lo**n,self.hi**n)
        return Interval(low,max(self.lo**n,self.hi**n))

def zeta_interval(p: int, K: int) -> Interval:
    require(type(p) is int and p>=2 and type(K) is int and K>=1,"zeta series domain")
    table=[F(1,(j+1)**p) for j in range(K)]
    eta=F(0)
    for k in range(K):
        require(0<table[0]<=1,"Euler finite difference outside proved bound")
        eta+=table[0]/(2**(k+1))
        table=[table[j]-table[j+1] for j in range(len(table)-1)]
    factor=1-F(1,2**(p-1))
    return Interval(eta/factor,(eta+F(1,2**K))/factor)

def ln2_interval(K: int) -> Interval:
    require(type(K) is int and K>=1,"positive exact series length required")
    total=2*sum((F(1,(2*j+1)*3**(2*j+1)) for j in range(K)),F(0))
    rem=F(9,4*(2*K+1)*3**(2*K+1))
    return Interval(total,total+rem)

def li4_interval(K: int) -> Interval:
    require(type(K) is int and K>=1,"positive exact series length required")
    total=sum((F(1,2**j*j**4) for j in range(1,K+1)),F(0))
    return Interval(total,total+F(1,2**K*(K+1)**4))

def outward_decimal(x: F, places: int, up: bool) -> str:
    require(type(places) is int and places>=1 and type(up) is bool,"decimal rounding domain")
    x=exact_fraction(x)
    scale=10**places
    value=-((-x.numerator*scale)//x.denominator) if up else (x.numerator*scale)//x.denominator
    sign="-" if value<0 else ""
    value=abs(value)
    return f"{sign}{value//scale}.{value%scale:0{places}d}"

def encode(x: Interval) -> dict:
    return {"lower":str(x.lo),"upper":str(x.hi),
            "decimal_lower":outward_decimal(x.lo,24,False),
            "decimal_upper":outward_decimal(x.hi,24,True),
            "width":str(x.hi-x.lo)}

def evaluate() -> dict:
    K=96
    z2,z3,z4=(zeta_interval(p,K) for p in (2,3,4))
    ell=ln2_interval(40); li4=li4_interval(96)
    pi2=6*z2
    Q=(4*z4+3*z2-F(7,4)*z3+z2*ell**2/2
       -F(7,4)*ell*z3-ell**4/12-2*li4)
    m1=7*z3/(2*pi2)-1
    m2=4*Q/pi2
    center=m1/(2*ell)
    variance=(m2-m1**2)/(4*ell**2)
    require(variance.lo>0,"positive limiting variance required")
    require(variance.hi-variance.lo<F(1,10**20),"certificate width too large")
    negative_controls=0
    for f in (lambda: Interval(1,0),lambda: Interval(-1,1).reciprocal()):
        try: f()
        except ValueError: negative_controls+=1
        else: raise ValueError("hostile input was accepted")
    result={"status":"PASS_EXACT_RATIONAL_EVALUATION",
            "parameters":{"zeta_euler_K":K,"ln2_K":40,"li4_K":96,"decimal_places":24},
            "inputs":{"zeta2":encode(z2),"zeta3":encode(z3),"zeta4":encode(z4),
                      "ln2":encode(ell),"Li4_half":encode(li4)},
            "natural_lambda_mean":encode(m1),
            "natural_lambda_second":encode(m2),
            "centered_mean_base2_R":encode(center),
            "limiting_variance_base2_R":encode(variance),
            "negative_controls":negative_controls,
            "floating_arithmetic_used":False,
            "assumptions":["The manuscript limiting-law identification and logarithmic moment formula",
                           "Euler zeta(2)=pi^2/6",
                           "proved Euler-transform/positive-series remainder bounds"],
            "formal_proof":False,"finite_N_variance_formula":False}
    require(center.lo<=F(-413852654438430019863270,10**24) and
            center.hi>=F(-413852654438430019863271,10**24),"mean offset enclosure")
    require(outward_decimal(center.lo,24,False)=="-0.413852654438430019863271" and
            outward_decimal(center.hi,24,True)=="-0.413852654438430019863270","stated mean endpoints")
    require(outward_decimal(variance.lo,24,False)=="0.892302571204274625294755" and
            outward_decimal(variance.hi,24,True)=="0.892302571204274625294756","stated variance endpoints")
    return result


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=evaluate()
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        require(args.output.parent.is_dir(),"output parent must exist")
        args.output.write_text(payload,encoding="utf-8",newline="\n")
    print(payload,end="")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
