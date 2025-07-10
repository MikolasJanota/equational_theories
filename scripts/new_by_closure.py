#!/usr/bin/env python3
# File:  new_by_closure.py
# Author:  mikolas
# Created on:  Thu Jul 3 12:40:15 PM UTC 2025
# Copyright (C) 2025, Mikolas Janota
import argparse

import closure
from rall2 import load_dictionary


def cl(file_name):
    dat = load_dictionary(file_name)
    print("# loaded")
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
    print("total", len(dat))
    print("impl", len(impl))
    print("non-impl", len(non_impl))
    print("unknown", len(dat) - len(non_impl) - len(non_impl))
    new_impl, new_non_impl = closure.close_implications(impl, non_impl)
    print("impl", len(new_impl))
    print("non-impl", len(new_non_impl))
    print("unknown", len(dat) - len(new_non_impl) - len(new_non_impl))


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", default="results.pkl")
    args = parser.parse_args()
    cl(args.pkl_file)


if __name__ == "__main__":
    run()
