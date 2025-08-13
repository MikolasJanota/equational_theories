#!/usr/bin/env python3
# File:  show_stats.py
# Author:  mikolas
# Created on:  Wed Aug 13 16:01:16 BST 2025
# Copyright (C) 2025, Mikolas Janota
import argparse
from collections import defaultdict

from run_all import Res, ResultInfo, Results, SolverCfg, load_results


def msg(*args, **kwargs):
    """Report."""
    print("#", *args, **kwargs, flush=True)


def mk_stats(pkl_file):
    """Calculate stats per method."""
    results = load_results(pkl_file)
    dat = results.values
    msg(f"loaded {len(dat)} values")
    stats = defaultdict(int)
    for _k, ri in dat.items():
        if ri.value == Res.IMPL_UNKNOWN:
            continue
        stats[(ri.method_id, ri.value)] += 1
    print("Methods", "&", "Refuted", "&", "Proven\\\\")
    for m in results.methods:
        print(
            m,
            "&",
            f"\\numprint{{{stats[(m, Res.IMPL_FALSE)]}}}",
            "&",
            f"\\numprint{{{stats[(m, Res.IMPL_TRUE)]}}}",
            "\\\\",
        )


def main():
    """Run the whole thing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", type=str)
    args = parser.parse_args()
    mk_stats(args.pkl_file)


if __name__ == "__main__":
    main()
