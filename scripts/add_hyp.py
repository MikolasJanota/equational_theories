#!/usr/bin/env python3
# File:  add_hyp.py
# Author:  mikolas
# Created on:  Wed Sep 3 16:55:51 CEST 2025
# Copyright (C) 2025, Mikolas Janota
import argparse
import subprocess
import sys
import time

from generate_eqs_list import eqs
from generate_tptp import Converter
from run_all import Res, process_tptp_out


def msg(*args, **kwargs):
    """Report."""
    print("#", *args, **kwargs, flush=True)


def parse_args():
    """CLI opts parsing."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--solver",
        required=True,
        help="command to run the solver, may contain arguments separated by whitespace",
    )
    arg_parser.add_argument(
        "--timeout", help="timeout per call in seconds", type=float, default=5
    )
    return arg_parser.parse_args()


def mk_prob(left, right, c):
    tup_l = eqs[left]
    tup_r = eqs[right]
    tup_c = eqs[c]
    varnames = "XYZWUVRST"
    constnames = "abcdrstkv"
    convl = Converter("m", varnames)
    convr = Converter("m", constnames)
    left_eq = convl.tup_to_eq(tup_l, negate=False)
    right_eq = convr.tup_to_eq(tup_r, negate=True)
    c_eq = convl.tup_to_eq(tup_c, negate=False)
    return f"""\
cnf(left, axiom, {left_eq}).
cnf(add, axiom, {c_eq}).
cnf(right, negated_conjecture, {right_eq}).
"""


def run_vampire(external_command, timeout, prob):
    try:
        result = subprocess.run(
            external_command,
            input=prob,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return process_tptp_out(result.stdout)
    except subprocess.CalledProcessError:
        return Res.IMPL_UNKNOWN
    except subprocess.TimeoutExpired:
        return Res.IMPL_UNKNOWN


def test(external_command, timeout, a, b):
    varnames = "XYZWUVRST"
    conv = Converter("m", varnames)
    aix = a - 1
    bix = b - 1
    msg(f"testing {conv.tup_to_eq(eqs[aix])} {conv.tup_to_eq(eqs[bix])}")
    msg(f"testing {a} {b}")
    for cix, c in enumerate(eqs):
        if cix in {aix, bix}:
            continue
        msg(f"add {cix}: {conv.tup_to_eq(c, negate=False)}")
        prob = mk_prob(aix, bix, cix)
        start = time.perf_counter()
        prob_time = round(time.perf_counter() - start, 3)
        res = run_vampire(external_command, timeout, prob)
        msg(f"{res} tm:{prob_time}")
        if res is Res.IMPL_FALSE:
            msg("solution found")
            print("prob:\n", prob)
            break


def main():
    """Run the whole run."""
    args = parse_args()
    external_command = args.solver.split()
    for line in sys.stdin:
        line = line.rstrip()
        if not line:
            continue
        a, b = map(int, line.split(",")[:2])
        test(external_command, args.timeout, a, b)


if __name__ == "__main__":
    main()
