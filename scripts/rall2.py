#!/usr/bin/env python3
import os
import pickle
import subprocess
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed

import z3

import generate_smt2


def print_file(x, y):
    generate_smt2.S = z3.DeclareSort("S")
    generate_smt2.m = z3.Function(
        "m", generate_smt2.S, generate_smt2.S, generate_smt2.S
    )
    return generate_smt2.print_smt2_file(x, y)


def process_combination(x, y, external_command):
    """Process a single x,y combination through external process."""
    try:
        # Generate the input string
        input_string = print_file(x, y)

        # Run the external process
        result = subprocess.run(
            external_command,
            input=input_string,
            text=True,
            capture_output=True,
            timeout=30,  # 30 second timeout per process
        )

        # Look for the line starting with '% SZS status'
        szs_line = None
        for line in result.stdout.split("\n"):
            if line.startswith("% SZS status"):
                szs_line = line
                break
        if szs_line and "Satisfiable" in szs_line:
            szs_line = True
        elif szs_line and "Unsatisfiable" in szs_line:
            szs_line = False

        return (x, y, szs_line)

    except subprocess.TimeoutExpired:
        return (x, y, "TIMEOUT")
    except Exception as e:
        return (x, y, f"ERROR: {str(e)}")


def save_dictionary(results_dict, filename="results.pkl"):
    """Save results dictionary to disk."""
    try:
        with open(filename, "wb") as f:
            pickle.dump(results_dict, f)
        print(f"Saved {len(results_dict)} results to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


def load_dictionary(filename="results.pkl"):
    """Load existing results dictionary from disk."""
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading existing results: {e}")
    return {}


def generate_combinations():
    """Generate all valid (x,y) combinations where x,y in 1..4694 and x !=
    y."""
    all = range(1, 4694)
    return [(x, y) for x in all for y in all if x != y]


def main():
    # Configuration
    EXTERNAL_COMMAND = "/home/mikolas/git/equational_theories/scripts/vam/bin/vampire_z3_rel_static_casc2023_6749 -t 1 -sa fmb --input_syntax smtlib2".split()
    MAX_WORKERS = 100
    BATCH_SIZE = 1000  # Process in batches to avoid overwhelming the system
    SAVE_INTERVAL = 100000
    RESULTS_FILE = "results.pkl"

    # Thread-safe dictionary access
    results_dict = load_dictionary(RESULTS_FILE)
    results_lock = threading.Lock()

    initial_count = len(results_dict)
    processed_count = 0

    print(f"Starting with {initial_count} existing results")
    print(f"Processing combinations with {MAX_WORKERS} parallel workers")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Saving every {SAVE_INTERVAL} new results")

    # Generate all combinations
    all_combinations = generate_combinations()
    total_combinations = len(all_combinations)

    # Filter out already processed combinations
    remaining_combinations = [
        (x, y)
        for x, y in all_combinations
        if (x, y) not in results_dict and results_dict[(x, y)] != Res.IMPL_UNKNOWN
    ]

    print(f"Total combinations: {total_combinations}")
    print(f"Remaining to process: {len(remaining_combinations)}")

    if not remaining_combinations:
        print("All combinations already processed!")
        return

    # Process combinations in batches
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        try:
            # Process in batches to avoid overwhelming the system
            for batch_start in range(0, len(remaining_combinations), BATCH_SIZE):
                batch_end = min(batch_start + BATCH_SIZE, len(remaining_combinations))
                batch = remaining_combinations[batch_start:batch_end]

                print(
                    f"Processing batch {batch_start//BATCH_SIZE + 1}/{(len(remaining_combinations) + BATCH_SIZE - 1)//BATCH_SIZE}"
                )

                # Submit batch jobs
                future_to_combination = {
                    executor.submit(process_combination, x, y, EXTERNAL_COMMAND): (x, y)
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
                        if processed_count % SAVE_INTERVAL == 0:
                            save_dictionary(results_dict.copy(), RESULTS_FILE)
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
                save_dictionary(results_dict, RESULTS_FILE)
            return

        except Exception as e:
            print(f"Error during processing: {e}")
            with results_lock:
                save_dictionary(results_dict, RESULTS_FILE)
            return

    # Final save
    with results_lock:
        save_dictionary(results_dict, RESULTS_FILE)
    print(f"Completed! Processed {processed_count} new combinations")
    print(f"Total results: {len(results_dict)}")


if __name__ == "__main__":
    main()
