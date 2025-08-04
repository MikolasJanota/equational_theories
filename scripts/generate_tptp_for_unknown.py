#!/usr/bin/env python3
# File:  generate_tptp_for_unknown.py
# Author:  mikolas
# Created on:  Fri Aug 1 21:43:10 CEST 2025
# Copyright (C) 2025, Mikolas Janota
import argparse
import os
from pathlib import Path

import check_res
from generate_tptp import print_tptp_file
from run_all import (
    Res,
    ResultInfo,
    Results,
    SolverCfg,
    generate_combinations,
    load_results,
)


def msg(*args, **kwargs):
    """Report."""
    print("#", *args, **kwargs, flush=True)


def main():
    """Run the whole thing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", type=str)
    parser.add_argument(
        "out_dir", help="name of the directory where to output files", type=str
    )
    parser.add_argument(
        "--res",
        help="add info about expected result obtained from general_implications_closure.json",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()
    export(args.pkl_file, args.out_dir, args.res)


def export(pkl_file, out_dir, res):
    """Export all they unknowns."""
    impls = check_res.read_json() if res else None
    results = load_results(pkl_file)
    dat = results.values
    msg(f"loaded {len(dat)} values")
    combinations = generate_combinations()
    msg(f"generating from {len(combinations)} combinations")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for k in combinations:
        if k in dat and dat[k].value != Res.IMPL_UNKNOWN:
            continue
        lhs, rhs = k
        msg(f"generate {lhs} {rhs}")
        out_file_name = Path(f"{lhs}_{rhs}.p")
        with open(
            os.path.join(out_dir, out_file_name), "w", encoding="ascii"
        ) as out_file:
            if impls is not None:
                out_file.write(f"% proven true: {(lhs, rhs) in impls}\n")
            out_file.write(print_tptp_file(lhs, rhs))


if __name__ == "__main__":
    main()
