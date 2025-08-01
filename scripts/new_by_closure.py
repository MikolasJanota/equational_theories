#!/usr/bin/env python3
# File:  new_by_closure.py
# Author:  mikolas
# Created on:  Thu Jul 3 12:40:15 PM UTC 2025
# Copyright (C) 2025, Mikolas Janota
import argparse

import closure
from rall2 import load_dictionary, save_dictionary


def msg(*args, **kwargs):
    print("#", *args, **kwargs, flush=True)


def cl(file_name):
    dat = load_dictionary(file_name)
    msg("loaded")
    impl = set()
    non_impl = set()
    for k in dat:
        val = dat[k]
        if val is None:
            continue
        if val is True:
            non_impl.add(k)
        if val is False:
            impl.add(k)
    msg("total", len(dat))
    msg("impl", len(impl))
    msg("non-impl", len(non_impl))
    msg("unknown", len(dat) - len(non_impl) - len(impl))
    new_impl, new_non_impl = closure.close_implications(True, impl, non_impl)
    msg("impl", len(new_impl))
    msg("non-impl", len(new_non_impl))
    msg("unknown", len(dat) - len(new_non_impl) - len(new_impl))

    def filled(val):
        return val is False or val is True

    for k in new_non_impl:
        assert (
            not filled(dat[k]) or dat[k] is True
        ), f"{k} had value {dat[k]} but now it's marked as non-impl"
        dat[k] = True
    for k in new_impl:
        assert (
            not filled(dat[k]) or dat[k] is False
        ), f"{k} had value {dat[k]} but now it's marked as impl"
        dat[k] = False
    save_dictionary(dat, f"closure_{file_name}")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", default="results.pkl")
    args = parser.parse_args()
    cl(args.pkl_file)


if __name__ == "__main__":
    run()
