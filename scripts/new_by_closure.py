#!/usr/bin/env python3
"""Stupid closure method."""
# File:  new_by_closure.py
# Author:  mikolas
# Created on:  Thu Jul 3 12:40:15 PM UTC 2025
# Copyright (C) 2025, Mikolas Janota
import argparse

import closure
from run_all import Res, ResultInfo, Results, SolverCfg, load_results, save_results


def msg(*args, **kwargs):
    """Report."""
    print("#", *args, **kwargs, flush=True)


def cl(file_name):
    """Run stupid closure method."""
    res = load_results(file_name)
    method_id = "clo"
    cfg = SolverCfg(
        external_command="new_by_closure.py",
        use_smt2=None,
        timeout=None,
        method_id=method_id,
    )
    res.methods[method_id] = cfg
    dat = res.values
    impl = set()
    non_impl = set()
    for k in dat:
        val: Res = dat[k].value
        if val == Res.IMPL_UNKNOWN:
            continue
        if val is Res.IMPL_FALSE:
            non_impl.add(k)
        if val is Res.IMPL_TRUE:
            impl.add(k)
    msg("total", len(dat))
    msg("impl", len(impl))
    msg("non-impl", len(non_impl))
    new_impl, new_non_impl = closure.close_implications(impl, non_impl, neg_only=False)
    msg("impl", len(new_impl), f"+{len(new_impl)-len(impl)}")
    msg("non-impl", len(new_non_impl), f"+{len(new_non_impl)-len(non_impl)}")

    def not_value(k, v):
        test = k not in dat or dat[k].value != v
        assert test, f"{k} had value {dat[k].value} but now it's marked as {v}"

    added_non = 0
    added_pos = 0
    for k in new_non_impl:
        not_value(k, Res.IMPL_TRUE)
        if k not in dat:
            r = ResultInfo(value=Res.IMPL_FALSE, time=0, method_id=method_id)
            dat[k] = r
            added_non += 1
    for k in new_impl:
        not_value(k, Res.IMPL_FALSE)
        if k not in dat:
            r = ResultInfo(value=Res.IMPL_TRUE, time=0, method_id=method_id)
            dat[k] = r
            added_pos += 1

    msg(f"added pos {added_pos}, added neg {added_non}, tot {added_non+added_pos}")
    save_results(Results(res.methods, dat), f"closure_{file_name}")


def run():
    """Run the whole program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", default="results.pkl")
    args = parser.parse_args()
    cl(args.pkl_file)


if __name__ == "__main__":
    run()
