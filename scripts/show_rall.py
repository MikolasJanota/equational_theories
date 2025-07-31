#!/usr/bin/env python3
# File:  show_rall.py
# Author:  mikolas
# Created on:  Thu Jul 3 12:40:15 PM UTC 2025
# Copyright (C) 2025, Mikolas Janota
import argparse

from rall2 import load_dictionary


def show_files():
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_files", nargs="*", default=["results.pkl"])
    args = parser.parse_args()
    for pkl_file in args.pkl_files:
        show(pkl_file)


def show(pkl_file):
    dat = load_dictionary(pkl_file)
    sat = 0
    unsat = 0
    for k in dat:
        val = dat[k]
        if val is None:
            continue
        if val is True:
            sat += 1
        if val is False:
            unsat += 1
    print("===", pkl_file)
    print(f"total: {len(dat):,}")
    print(f"sat: {sat:,}")
    print(f"unsat: {unsat:,}")
    print(f"unknown: {(len(dat) - sat - unsat):,}")


if __name__ == "__main__":
    show_files()
