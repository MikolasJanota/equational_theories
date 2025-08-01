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
    solved_by_method = {
        m: {v: 0 for v in {Res.IMPL_FALSE, Res.IMPL_TRUE}} for m in methods
    }
    for met in methods:
        print(met, methods[met])
    dat = results.values
    true_eqs = 0
    false_eqs = 0
    for k in dat:
        # print(k, dat[k])
        ri: ResultInfo = dat[k]
        val: Res = ri.value
        if val == Res.IMPL_UNKNOWN:
            continue
        solved_by_method[ri.method_id][val] += 1
        if val == Res.IMPL_FALSE:
            false_eqs += 1
        if val == Res.IMPL_TRUE:
            true_eqs += 1
    print("===", pkl_file)
    print(f"total: {len(dat):,}")
    print(f"trues: {true_eqs:,}")
    print(f"falses: {false_eqs:,}")
    print(f"unknown: {(len(dat) - true_eqs - false_eqs):,}")
    for m in methods:
        fs, ts = solved_by_method[m][Res.IMPL_FALSE], solved_by_method[m][Res.IMPL_TRUE]
        print(f"{m}: {fs+ts:,} = F:{fs:,} T:{ts:,}")


if __name__ == "__main__":
    show_files()
