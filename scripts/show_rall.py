#!/usr/bin/env python3
# File:  show_rall.py
# Author:  mikolas
# Created on:  Thu Jul 3 12:40:15 PM UTC 2025
# Copyright (C) 2025, Mikolas Janota
import argparse

from run_all import Res, ResultInfo, Results, SolverCfg, load_results


def show_files():
    """Show stats about res files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_files", nargs="*", default=["results.pkl"])
    args = parser.parse_args()
    for pkl_file in args.pkl_files:
        show(pkl_file)


def show(pkl_file):
    """Show stats about res file."""
    results = load_results(pkl_file)
    methods = results.methods
    for met in methods:
        print(met, methods[met])
    dat = results.values
    true_eqs = 0
    false_eqs = 0
    for k in dat:
        # print(k, dat[k])
        ri: ResultInfo = dat[k]
        val: Res = ri.value
        if val == Res.IMPL_FALSE:
            true_eqs += 1
        if val == Res.IMPL_TRUE:
            false_eqs += 1
    print("===", pkl_file)
    print(f"total: {len(dat):,}")
    print(f"trues: {true_eqs:,}")
    print(f"falses: {false_eqs:,}")
    print(f"unknown: {(len(dat) - true_eqs - false_eqs):,}")


if __name__ == "__main__":
    show_files()
