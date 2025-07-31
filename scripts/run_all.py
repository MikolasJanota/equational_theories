#!/usr/bin/env python3
"""Run a given solver on the problems not so far."""

__author__ = "Mikolas Janota"
__copyright__ = "2025, Mikolas Janota"

# File:  run_all.py
# Author:  mikolas
# Created on:  Thu Jul 31 11:37:46 CEST 2025
# Copyright (C) 2025, Mikolas Janota

import argparse
import os
import pickle
import subprocess
import sys
import threading
import time
from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor, as_completed
from enum import Enum

import generate_smt2
import generate_tptp


class Res(Enum):
    """Possible result for single implication."""

    IMPL_FALSE = 0
    IMPL_TRUE = 1
    IMPL_UNKNOWN = 2


Results = namedtuple("Results", ["methods", "values"])
SolverCfg = namedtuple(
    "SolverCfg", ["external_command", "use_smt2", "timeout", "method_id"]
)
ResultInfo = namedtuple("ResultInfo", ["value", "time", "method_id"])


def get_program_version(program_name):
    """Run a program with --version flag and return the standard output.

    Args:
        program_name (str): Name of the program to check version for

    Returns:
        str: Standard output from the version command, or error message
    """
    try:
        # Run the program with --version flag
        result = subprocess.run(
            [program_name, "--version"],
            capture_output=True,
            text=True,
            timeout=10,  # 10 second timeout to prevent hanging
            check=True,
        )

        # Return stdout if command succeeded
        assert result.returncode == 0
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"non-zero output of solver on --version, {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(
            f"Timeout: {program_name} --version took too long to execute",
            file=sys.stderr,
        )
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Program '{program_name}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running {program_name}: {str(e)}", file=sys.stderr)
        sys.exit(1)


def process_tptp_out(out):
    """Take TPTP output and returns a Res."""
    szs_line = None
    for line in out.split("\n"):
        if line.startswith("% SZS status"):
            szs_line = line
            break
    if szs_line is None:
        return Res.IMPL_UNKNOWN
    if "Satisfiable" in szs_line:
        return Res.IMPL_FALSE
    if "Unsatisfiable" in szs_line:
        return Res.IMPL_TRUE
    print(f"Warning: unknown result from solver {szs_line}", file=sys.stderr)
    return Res.IMPL_UNKNOWN


def print_file_tptp(x, y):
    "Generate tptp input for equations x y."
    return generate_tptp.print_tptp_file(x, y)


def print_file_smt2(x, y):
    "Generate smt2 input for equations x y."
    sort, m = generate_smt2.mk_decls(use_ints=False)
    return generate_smt2.print_smt2_file(
        x, y, m=m, thesort=sort, skolemize=False, logic="UF"
    )


def process_combination(x, y, solver_cfg: SolverCfg):
    """Process a single x,y combination through external process."""
    try:
        input_string = (
            print_file_smt2(x, y) if solver_cfg.use_smt2 else print_file_tptp(x, y)
        )

        start = time.process_time()
        result = subprocess.run(
            solver_cfg.external_command,
            input=input_string,
            text=True,
            capture_output=True,
            timeout=solver_cfg.timeout,
            check=False,
        )
        cpu_time = round(time.process_time() - start, 3)
        res = process_tptp_out(result.stdout)
        return (x, y, ResultInfo(res, cpu_time, solver_cfg.method_id))

    except subprocess.TimeoutExpired:
        return (
            x,
            y,
            ResultInfo(Res.IMPL_UNKNOWN, solver_cfg.timeout, solver_cfg.method_id),
        )
    except Exception as e:
        print(f"Error on call: {e}", file=sys.stderr)
        return (x, y, ResultInfo(Res.IMPL_UNKNOWN, None, solver_cfg.method_id))


def save_results(results: Results, filename):
    """Save results dictionary to disk."""
    try:
        with open(filename, "wb") as f:
            pickle.dump(results, f)
        print(f"Saved {len(results)} results to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


def load_results(filename):
    """Load existing results dictionary from disk."""
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading existing results: {e}")
    return Results({}, {})


def generate_combinations():
    """Generate (x,y) combinations where x,y in 1..4694 and x != y."""
    # all_eqs = range(1, 4694)
    all_eqs = range(1, 5)
    return [(x, y) for x in all_eqs for y in all_eqs if x != y]


def parse_args():
    """CLI opts parsing."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--solver",
        required=True,
        help="command to run the solver, may contain arguments separated by whitespace",
    )
    arg_parser.add_argument(
        "--method_id",
        required=True,
        help="an id (e.g. integer) for the method being run, stored in the DB",
    )
    arg_parser.add_argument(
        "--resfile", help="where to store results", default="results.pkl"
    )
    arg_parser.add_argument(
        "--timeout", help="timeout per call in seconds", type=float, default=30
    )
    arg_parser.add_argument(
        "--smt2", help="use smt2 rather than tptp", action="store_true", default=False
    )
    arg_parser.add_argument("--max_workers", default=100, type=int)
    arg_parser.add_argument(
        "--batch_size",
        default=1000,
        help="Process in batches to avoid overwhelming the system",
    )
    arg_parser.add_argument(
        "--save_interval", help="how often save results", default=100000
    )
    return arg_parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    solver_cfg = SolverCfg(
        external_command=args.solver.split(),
        use_smt2=args.smt2,
        timeout=args.timeout,
        method_id=args.method_id,
    )
    batch_size = args.batch_size

    # Thread-safe dictionary access
    results = load_results(args.resfile)
    methods = results.methods
    version = get_program_version(solver_cfg.external_command[0])
    methods[solver_cfg.method_id] = (solver_cfg, version)
    results_dict = results.values
    results_lock = threading.Lock()

    initial_count = len(results_dict)
    processed_count = 0

    print(f"Starting with {initial_count} existing results")
    print(f"Processing combinations with {args.max_workers} parallel workers")
    print(f"Batch size: {batch_size}")
    print(f"Saving every {args.save_interval} new results")

    # Generate all combinations
    all_combinations = generate_combinations()
    total_combinations = len(all_combinations)

    # Filter out already processed combinations
    remaining_combinations = [
        k
        for k in all_combinations
        if k not in results_dict or results_dict[k].value == Res.IMPL_UNKNOWN
    ]

    print(f"Total combinations: {total_combinations}")
    print(f"Remaining to process: {len(remaining_combinations)}")

    if not remaining_combinations:
        print("All combinations already processed!")
        return

    # Process combinations in batches
    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        try:
            # Process in batches to avoid overwhelming the system
            for batch_start in range(0, len(remaining_combinations), batch_size):
                batch_end = min(batch_start + batch_size, len(remaining_combinations))
                batch = remaining_combinations[batch_start:batch_end]
                rembatches = (
                    len(remaining_combinations) + batch_size - 1
                ) // batch_size
                print(f"Processing batch {batch_start//batch_size + 1}/{rembatches}")

                # Submit batch jobs
                future_to_combination = {
                    executor.submit(
                        process_combination,
                        x,
                        y,
                        solver_cfg,
                    ): (x, y)
                    for x, y in batch
                }

                # Wait for batch to complete
                for future in as_completed(future_to_combination):
                    x, y, result = future.result()

                    # Thread-safe update of results dictionary
                    with results_lock:
                        results_dict[(x, y)] = result
                        processed_count += 1
                        current_processed = processed_count

                        # Save periodically (inside lock to ensure consistency)
                        if processed_count % args.save_interval == 0:
                            save_results(
                                Results(methods, results_dict.copy()), args.resfile
                            )
                            print(
                                f"Checkpoint: Saved after {processed_count} new results"
                            )

                    # Print progress (outside lock to avoid holding it too long)
                    if current_processed % 1000 == 0:
                        total_processed = initial_count + current_processed
                        print(
                            f"Processed {current_processed} new combinations "
                            f"(Total: {total_processed}/{total_combinations})"
                        )

        except KeyboardInterrupt:
            print("\nInterrupted by user. Saving current progress...")
            with results_lock:
                save_results(Results(methods, results_dict.copy()), args.resfile)
            return

        except Exception as e:
            print(f"Error during processing: {e}")
            with results_lock:
                save_results(Results(methods, results_dict.copy()), args.resfile)
            return

    # Final save
    with results_lock:
        save_results(Results(methods, results_dict), args.resfile)
    print(f"Completed! Processed {processed_count} new combinations")
    print(f"Total results: {len(results_dict)}")


if __name__ == "__main__":
    main()
