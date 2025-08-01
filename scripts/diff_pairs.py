#!/usr/bin/env python3
"""
File:  diff_pairs.py
Author:  mikolas
Created on:  Thu Jul 17 15:58:14 CEST 2025
Copyright (C) 2025, Mikolas Janota
"""

import argparse
import sys


def diff(s1, s2):
    d1 = s1 - s2
    d2 = s2 - s1
    print(f"1 but not 2 #{len(d1)}")
    for a, b in d1:
        print(a, b)
    print(f"2 but not 1 #{len(d2)}")
    for a, b in d2:
        print(a, b)


def read(f):
    rv = set()
    for line in f:
        p = line.split()
        assert len(p) == 2
        a, b = map(int, p)
        rv.add((a, b))
    return rv


def run_main():
    """Run the whole program."""
    parser = argparse.ArgumentParser(description="dp.")
    parser.add_argument("filename1")
    parser.add_argument("filename2")
    opts = parser.parse_args()
    with open(opts.filename1, "r", encoding="ascii") as f1:
        with open(opts.filename2, "r", encoding="ascii") as f2:
            ps1 = read(f1)
            ps2 = read(f2)
            diff(ps1, ps2)


if __name__ == "__main__":
    run_main()
    sys.exit(0)
