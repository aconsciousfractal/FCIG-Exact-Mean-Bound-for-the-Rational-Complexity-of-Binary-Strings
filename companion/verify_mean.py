"""Exact finite premises for the dyadic mean theorem. Python standard library only."""
import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

SCALE = 1 << 40
TERMS = 12
BASE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ceildiv(a, b):
    return -((-a) // b)


def unit_log(num, den, upper):
    require(type(num) is int and type(den) is int and 0 < den <= num <= 2*den,
            "unit logarithm domain")
    if num == den:
        return 0
    z = ceildiv(SCALE*(num-den), num+den) if upper else SCALE*(num-den)//(num+den)
    square = ceildiv(z*z, SCALE) if upper else z*z//SCALE
    power = z
    total = 0
    for j in range(TERMS):
        total += ceildiv(power, 2*j+1) if upper else power//(2*j+1)
        power = ceildiv(power*square, SCALE) if upper else power*square//SCALE
    tail = ceildiv(8*SCALE, 3*25*(1 << 25)) if upper else 0
    return 2*total + tail


LN2_LO = unit_log(2, 1, False)
LN2_HI = unit_log(2, 1, True)


def log_upper(num, den):
    require(0 < den <= num, "logarithm domain")
    k = num.bit_length()-den.bit_length()
    if num < den << k:
        k -= 1
    require(k >= 0 and (den << k) <= num < (den << (k+1)), "range reduction")
    return k*LN2_HI + unit_log(num, den << k, True)


def primitive_box(t):
    require(type(t) is int and t >= 1, "primitive box domain")
    mu = [0]*(t+1)
    mu[1] = 1
    primes = []
    composite = [False]*(t+1)
    for i in range(2, t+1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i*p > t:
                break
            composite[i*p] = True
            if i % p == 0:
                mu[i*p] = 0
                break
            mu[i*p] = -mu[i]
    return sum(mu[g]*(2*(t//g)+1)*((t//g+1)//2) for g in range(1, t+1, 2))


def small_check(data):
    rows = data["small"]
    require([x["N"] for x in rows] == list(range(1, 13)), "small level coverage")
    population = excluded = 0
    for row in rows:
        n = row["N"]
        m = 1 << n
        hs, ws, cert = row["heights"], row["witnesses"], row["products"]
        require(row["M"] == m and len(hs) == len(ws) == m, "small population")
        for r, (h, w) in enumerate(zip(hs, ws, strict=True)):
            require(type(h) is int and 1 <= h <= m//2, "height domain")
            require(len(w) == 2 and all(type(v) is int for v in w), "witness shape")
            a, b = w
            require(b > 0 and b % 2 == 1 and (a-r*b) % m == 0
                    and math.gcd(a, b) == 1 and max(abs(a), b) == h, "witness")
            for odd in range(1, h, 2):
                v = r*odd % m
                require(min(v, m-v) >= h, "nonminimal height")
                excluded += 1
            population += 1
        large = [h for h in hs if 2*h*h > m]
        vals = {
            "target_product_squared_hex": math.prod(hs)**2,
            "target_rhs_hex": m**m,
            "K_product_squared_hex": math.prod(large)**2,
            "K_rhs_hex": 1 << (m+(n-1)*len(large)),
        }
        require(vals["target_product_squared_hex"] <= vals["target_rhs_hex"]
                and vals["K_product_squared_hex"] <= vals["K_rhs_hex"], "target or K product")
        require(cert["K_large_count"] == len(large), "large population")
        for key, value in vals.items():
            require(int(cert[key], 16) == value, "certificate product")
        require(cert["K_sufficient_finite_pass"] is True
                and cert["original_target_finite_pass"] is True, "false small flag")
    require(population == sum(1 << n for n in range(1, 13)), "derived small population")
    return {"parent_levels": len(rows), "minima": population, "excluded_denominators": excluded}


def bridge_shape(data):
    rows = data["bridge"]
    require([r["parent_n"] for r in rows] == list(range(13, 26)), "bridge level coverage")
    for row in rows:
        n = row["parent_n"]
        m = 1 << n
        t0 = math.isqrt(m//2)
        ds = [1 << j for j in range(1, n//2+1)]
        require(row["M"] == m and row["T0"] == t0, "bridge domain")
        require([c["D"] for c in row["cells"]] == ds, "content coverage")
        a = primitive_box(t0)
        v2 = sum((1 << (n-k-1))*(2*k-n) for k in range(n//2+1, n))
        require(row["A_exact"] == a and row["V2_exact"] == v2 and a > v2, "central-axis budget")
        pair_count = raw_count = total = 0
        for cell in row["cells"]:
            d = cell["D"]
            t = math.isqrt(m)//d
            require(cell["T"] == t, "cell radius")
            count = (primitive_box(t)-1)//2
            require(cell["positive_primitive_pairs"] == count, "cell population")
            require(type(cell["scaled_log_sum_upper"]) is int and cell["scaled_log_sum_upper"] >= 0,
                    "cell sum domain")
            pair_count += count
            raw_count += t*((t+1)//2)
            total += cell["scaled_log_sum_upper"]
        rhs = (a-v2)*LN2_LO
        require(row["positive_primitive_pairs"] == pair_count and row["raw_pairs"] == raw_count,
                "bridge population")
        require(row["twice_M_U_scaled_upper"] == total
                and row["central_minus_axis_scaled_lower"] == rhs
                and row["integer_margin"] == rhs-total and total <= rhs, "bridge margin")
        require(row["sufficient_K_finite_pass"] is True, "false bridge flag")
    return rows


def bridge_recompute(rows):
    all_pairs = all_raw = 0
    for row in rows:
        m = row["M"]
        total = pairs = raw = 0
        for cell in row["cells"]:
            d, t = cell["D"], cell["T"]
            subtotal = count = 0
            raw += t*((t+1)//2)
            for a in range(1, t+1):
                for b in range(1, t+1, 2):
                    if math.gcd(a, b) != 1:
                        continue
                    subtotal += d*log_upper((m+d*d*a*b)**2, m*d*d*(a+b)**2)
                    count += 1
            require(count == cell["positive_primitive_pairs"]
                    and subtotal == cell["scaled_log_sum_upper"], "recomputed cell")
            pairs += count
            total += subtotal
        require(total == row["twice_M_U_scaled_upper"]
                and pairs == row["positive_primitive_pairs"] and raw == row["raw_pairs"],
                "recomputed bridge")
        all_pairs += pairs
        all_raw += raw
    return {"parent_levels": len(rows), "positive_primitive_pairs": all_pairs,
            "raw_pairs": all_raw, "all_margins_positive": all(r["integer_margin"] > 0 for r in rows)}


def cutoff():
    delta = Fraction(1372, 9801)-Fraction(304, 2205)
    error = (Fraction(109, 120)*13+Fraction(47, 12))/2**13+Fraction(1, 8*2**26)
    require(delta > Fraction(1, 500) > error, "rational cutoff")
    # (a(J+1)+b)/2 < aJ+b iff a < aJ+b; this holds for all J>=13.
    require(Fraction(109, 120) < Fraction(109, 120)*13+Fraction(47, 12), "monotonicity criterion")
    return {"parent_n_min": 26, "delta_lower": str(delta), "error_at_J13_upper": str(error),
            "scope": "rational comparisons only; analytic estimates require manuscript proof"}


def negative_controls(data):
    def missing(x):
        x["small"].pop()
    def duplicate(x):
        x["small"].append(deepcopy(x["small"][-1]))
    def witness(x):
        x["small"][0]["witnesses"][0][1] = 2
    def height(x):
        x["small"][0]["heights"][0] = 2
    def margin(x):
        x["bridge"][0]["integer_margin"] += 1
    def population(x):
        x["bridge"][0]["positive_primitive_pairs"] -= 1
    def flag(x):
        x["small"][0]["products"]["K_sufficient_finite_pass"] = False
    rejected = []
    for mutate in [missing, duplicate, witness, height, margin, population, flag]:
        altered = deepcopy(data)
        mutate(altered)
        try:
            small_check(altered)
            bridge_shape(altered)
        except (ValueError, KeyError, TypeError):
            rejected.append(mutate.__name__)
        else:
            raise ValueError("negative control accepted: "+mutate.__name__)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="No bridge resummation: NOT a full finite proof replay.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    path = BASE/"finite_certificates.json"
    data = json.loads(path.read_text(encoding="utf8"))
    require(data["schema"] == "finite_rational_mean_certificates_v1", "certificate schema")
    require(data["scale"] == SCALE and data["terms"] == TERMS, "log parameters")
    small = small_check(data)
    rows = bridge_shape(data)
    controls = negative_controls(data)
    bridge = None if args.quick else bridge_recompute(rows)
    result = dict(status="PASS_QUICK_STRUCTURAL_ONLY" if args.quick else "PASS_FINITE_PREMISES",
                  certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  small=small, bridge=bridge, cutoff=cutoff(), negative_controls_rejected=controls,
                  all_N_proved_by_checker_alone=False, novelty_certified=False)
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(payload, encoding="utf8")
    print(payload, end="")


if __name__ == "__main__":
    main()

