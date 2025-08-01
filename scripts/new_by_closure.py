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
    dat = res.values
    msg("loaded")
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
    msg("unknown", len(dat) - len(non_impl) - len(impl))
    new_impl, new_non_impl = closure.close_implications(True, impl, non_impl)
    msg("impl", len(new_impl))
    msg("non-impl", len(new_non_impl))
    msg("unknown", len(dat) - len(new_non_impl) - len(new_impl))

    for k in new_non_impl:
        assert (
            dat[k] != Res.IMPL_TRUE
        ), f"{k} had value {dat[k]} but now it's marked as non-impl"
        dat[k] = Res.IMPL_FALSE
    for k in new_impl:
        assert (
            dat[k] != Res.IMPL_FALSE
        ), f"{k} had value {dat[k]} but now it's marked as impl"
        dat[k] = Res.IMPL_TRUE
    save_results(Results(res.methods, dat), f"closure_{file_name}")


def run():
    """Run the whole program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", default="results.pkl")
    args = parser.parse_args()
    cl(args.pkl_file)


if __name__ == "__main__":
    run()
