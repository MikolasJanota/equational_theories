#!/usr/bin/env python3
# File:  show_rall.py
# Author:  mikolas
# Created on:  Thu Jul 3 12:40:15 PM UTC 2025
# Copyright (C) 2025, Mikolas Janota
import closure
from rall2 import load_dictionary

dat = load_dictionary("results.pkl")
print("# loaded")
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
print("total", len(dat))
print("sat", sat)
print("unsat", unsat)
print("unknown", len(dat) - sat - unsat)
impl = set()
nimpl = set()
for x, y in dat:
    val = dat[(x, y)]
    if val is False:
        impl.add((x, y))
    if val is True:
        nimpl.add((x, y))
new_impl, new_nimpl = closure.close_implications(impl, nimpl)
print(len(new_impl), len(new_nimpl))
