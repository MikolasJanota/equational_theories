#!/usr/bin/env python3
# File:  closure.py
# Author:  mikolas
# Created on:  Thu Jul 10 11:57:03 CEST 2025
# Copyright (C) 2025, Mikolas Janota
from collections import defaultdict, deque


def msg(*args, **kwargs):
    """Resport."""
    print("#", *args, **kwargs, flush=True)


class Implications:
    def __init__(self, known_implies):
        self.implies = defaultdict(set)
        self.is_implied = defaultdict(set)
        for a, b in known_implies:
            self.add(a, b)

    def add(self, a, b):
        """Add edge a->b."""
        self.implies[a].add(b)
        self.is_implied[b].add(a)


def close_implications(known_implications, known_non_implications, neg_only):
    msg("closure start")
    implications = Implications(known_implications)
    not_implies = defaultdict(set)

    # Initialize non implications
    for a, b in known_non_implications:
        not_implies[a].add(b)

    # Initialize que
    worklist = deque()
    for a, b in known_implications:
        worklist.append((a, b))

    if neg_only:
        worklist = None
    while worklist:
        if len(worklist) % 1000 == 0:
            msg("todo pos:", len(worklist))
        a, b = worklist.popleft()
        assert b in implications.implies[a]

        # Rule: If A ⇒ B and B ⇒ C, then A ⇒ C
        for c in implications.implies[b]:
            if c != a and c not in implications.implies[a]:
                implications.add(a, c)
                worklist.append((a, c))
                msg(f"New positive {a} {c} from {a}=>{b},{b}=>{c}")
                assert c not in not_implies[a]

        # Rule: If D ⇒ A and A ⇒ B, then D ⇒ B
        for d in implications.is_implied[a]:
            if d != b and b not in implications.implies[d]:
                implications.add(d, b)
                worklist.append((d, b))
                msg(f"New positive {d} {b} from {d}=>{a},{a}=>{b}")
                assert b not in not_implies[d]
    msg("Positive closed")

    changed = True
    while changed:
        msg("New non round")
        new_non = set()
        for i, a in enumerate(implications.implies):
            if i % 100 == 0:
                msg("non prop1:", i, a)
            # if a => b and not (a => c) then not (b => c)
            for b in implications.implies[a]:
                for c in not_implies[a]:
                    if c not in not_implies[b]:
                        new_non.add((b, c))
                        msg(f"New negative {b} {c} from {a}=>{b}, not {a}=>{c}")

        for i, a in enumerate(not_implies):
            if i % 100 == 0:
                msg("non prop2:", i, a)
            # if not (a => c) and b => c then not (a => b)
            for c in not_implies[a]:
                for b in implications.is_implied[c]:
                    if b not in not_implies[a]:
                        new_non.add((a, b))
                        msg(f"New negative {a} {b} from {b}=>{c}, not {a}=>{c}")
        changed = len(new_non) != 0
        for x, y in new_non:
            not_implies[x].add(y)

    # print(implications.implies, not_implies)
    rv_implies = {(a, b) for a in implications.implies for b in implications.implies[a]}
    rv_not_implies = {(a, b) for a in not_implies for b in not_implies[a]}
    return rv_implies, rv_not_implies


def run_test():
    """Example usage."""
    known_implications = [(0, 1), (1, 3), (4, 5), (8, 9)]
    known_non_implications = {(4, 6), (7, 9)}

    implies, not_implies = close_implications(
        known_implications, known_non_implications, False
    )

    print("Implied Pairs:")
    for a, b in sorted(implies):
        print(f"{a} ⇒ {b}")

    print("\nNon-Implied Pairs:")
    for a, b in sorted(not_implies):
        print(f"{a} ⇏ {b}")


if __name__ == "__main__":
    run_test()
