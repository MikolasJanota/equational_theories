#!/usr/bin/env python3
# File:  closure.py
# Author:  mikolas
# Created on:  Thu Jul 10 11:57:03 CEST 2025
# Copyright (C) 2025, Mikolas Janota
from collections import defaultdict, deque


def close_implications(known_implications, known_non_implications):
    print("closure start")
    implies = defaultdict(set)
    not_implies = defaultdict(set)

    # Initialize non implications
    for a, b in known_non_implications:
        if b not in not_implies[a]:
            not_implies[a].add(b)

    # Initialize implications
    worklist = deque()
    for a, b in known_implications:
        if b not in implies[a]:
            implies[a].add(b)
            worklist.append((a, b))

    while worklist:
        a, b = worklist.popleft()

        # Rule: If A ⇒ B and B ⇒ C, then A ⇒ C
        for c in implies[b]:
            if c != a and c not in implies[a]:
                implies[a].add(c)
                worklist.append((a, c))
                print(f"New positive {a} {c} from {a}=>{b},{b}=>{c}")
                assert c not in not_implies[a]

        # Rule: If D ⇒ A and A ⇒ B, then D ⇒ B
        for d in implies:
            if d != b and a in implies[d] and b not in implies[d]:
                implies[d].add(b)
                worklist.append((d, b))
                print(f"New positive {d} {b} from {d}=>{a},{a}=>{b}")
                assert b not in not_implies[d]
    print("Positive closed")

    changed = True
    while changed:
        print("New non round")
        new_non = set()
        for a in implies:
            for b in implies[a]:
                for c in not_implies[a]:
                    if c not in not_implies[b]:
                        new_non.add((b, c))
                        print(f"New negative {b} {c}")
        changed = len(new_non) != 0
        for x, y in new_non:
            not_implies[x].add(y)

    # Final set of derived implications (excluding reflexive)
    final_implies = set()
    for a in implies:
        for b in implies[a]:
            if a != b:
                final_implies.add((a, b))
    final_not_implies = set()
    for a in not_implies:
        for b in not_implies[a]:
            assert (a, b) not in final_implies
            final_not_implies.add((a, b))

    return final_implies, final_not_implies


def run_test():
    """Example usage."""
    known_implications = [(0, 1), (1, 3), (4, 5)]
    known_non_implications = {(4, 6)}

    implied, not_implied = close_implications(
        known_implications, known_non_implications
    )

    print("Implied Pairs:")
    for a, b in sorted(implied):
        print(f"{a} ⇒ {b}")

    print("\nNon-Implied Pairs:")
    for a, b in sorted(not_implied):
        print(f"{a} ⇏ {b}")


if __name__ == "__main__":
    run_test()
