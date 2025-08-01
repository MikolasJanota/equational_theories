#!/usr/bin/env python3
"""Check obtained results agains the databes."""

__author__ = "Mikolas Janota"
__copyright__ = "2025, Mikolas Janota"

# File:  check_res.py
# Author:  mikolas
# Created on:  Fri Aug 1 11:35:37 CEST 2025
import argparse
import json
import sys

from run_all import Res, ResultInfo, Results, SolverCfg, load_results


def get_num(eq: str):
    """Convert eqstr to id."""
    pre = "Equation"
    assert eq.startswith(pre)
    return int(eq[len(pre) :])


def read_json():
    """Read impls from json."""
    name = "general_implications_closure.json"
    imp_str = "implications"
    with open(name, "r", encoding="utf-8") as file:
        data = json.load(file)
    imps = data[imp_str]
    rv = set()
    for imp in imps:
        lhs = get_num(imp["lhs"])
        rhs = get_num(imp["rhs"])
        rv.add((lhs, rhs))
    return rv


def check_files():
    """Show stats about res files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_files", nargs="*", default=["results.pkl"])
    args = parser.parse_args()
    impls = read_json()
    print(f"read {len(impls):,} implications")
    for pkl_file in args.pkl_files:
        check_file(impls, pkl_file)


def check_file(impls, pkl_file):
    """Show stats about res file."""
    results = load_results(pkl_file)
    dat = results.values
    print(f"checking at most {len(dat)} results")
    checked = 0
    for k in dat:
        ri: ResultInfo = dat[k]
        val: Res = ri.value
        if val == Res.IMPL_UNKNOWN:
            continue
        # print(lhs, rhs, dat[k])
        if val == Res.IMPL_FALSE and k in impls:
            print(f"expected {k} but got false")
            sys.exit(1)
        elif val == Res.IMPL_TRUE and k not in impls:
            print(f"not expected {k} but got true")
            sys.exit(1)
        checked += 1
    print(f"checked {checked} results")


if __name__ == "__main__":
    check_files()
