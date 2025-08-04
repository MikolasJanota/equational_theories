#!/usr/bin/env python3
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from run_all import Res, ResultInfo, Results, SolverCfg, load_results

# Sample data with more realistic values - replace this with your actual data
sample_data = [
    ("1", True, 1, "method1"),
    ("1", True, 1.5, "method1"),
    ("2", False, 1, "method1"),
    ("3", True, 1, "method2"),
    ("4", True, 10, "method1"),
    ("5", False, 10, "method1"),
    ("6", True, 10, "method2"),
    ("8", False, 1.3, "method2"),
    ("7", False, 5, "method2"),
]

CB_color_cycle = [
    "#377eb8",
    "#ff7f00",
    "#4daf4a",
    "#f781bf",
    "#a65628",
    "#984ea3",
    "#999999",
    "#e41a1c",
    "#dede00",
]


def plot_stacked_histogram(data, bins=10, figsize=(12, 8), save_path=None):
    """
    Alternative: Plot stacked histogram for better visualization when categories overlap
    """
    df = pd.DataFrame(data, columns=["key", "holds", "time", "method"])

    # Data validation and cleaning (same as overlapping histogram)
    print(f"HISTOGRAM - Original data points: {len(df)}")
    print(f"Time range: {df['time'].min():.3f} to {df['time'].max():.3f}")

    # Check for negative times
    negative_times = df[df["time"] < 0]
    if len(negative_times) > 0:
        print(f"WARNING: Found {len(negative_times)} negative time values!")
        print("Removing negative times from analysis...")
        df = df[df["time"] >= 0]

    if len(df) == 0:
        print("ERROR: No valid data points remaining after cleaning!")
        return

    df["category"] = df["holds"].astype(str) + "_" + df["method"]

    # Prepare data for stacked histogram
    categories = df["category"].unique()
    print(f"Categories found: {categories}")

    # Create time data arrays and check for empty categories
    time_data = []
    valid_categories: list[str] = []

    for cat in categories:
        cat_data = df[df["category"] == cat]["time"].values
        print(f"Category '{cat}': {len(cat_data)} data points")
        if len(cat_data) > 0:
            time_data.append(cat_data)
            valid_categories.append(cat)
        else:
            print(f"WARNING: Category '{cat}' has no data points - excluding from plot")

    if len(time_data) == 0:
        print("ERROR: No categories with valid data!")
        return

    _fig, ax = plt.subplots(figsize=figsize)

    # Determine appropriate bin range
    time_min, time_max = df["time"].min(), df["time"].max()
    time_range = time_max - time_min

    if time_range < 1e-6:
        print("WARNING: Very small time range detected. Using single bin.")
        bins = 1
    elif isinstance(bins, int) and time_range > 0:
        bin_edges = np.linspace(time_min, time_max, bins + 1)
    else:
        bin_edges = bins

    print(f"Using {bins} bins for time range {time_min:.3f} to {time_max:.3f}")

    # Create histogram with better colors
    if len(valid_categories) <= len(CB_color_cycle):
        colors = CB_color_cycle[0 : len(valid_categories)]
    elif len(valid_categories) <= 10:
        colors = plt.cm.tab10(np.linspace(0, 1, len(valid_categories)))
    else:
        colors = plt.cm.Set3(np.linspace(0, 1, len(valid_categories)))

    # print(time_data)
    n, _bins_used, _patches = ax.hist(
        time_data,
        bins=bin_edges,
        label=[cat.replace("_", " ") for cat in valid_categories],
        alpha=0.8,
        edgecolor="black",
        linewidth=0.8,
        stacked=False,
        color=colors,
    )

    # Debug output for histogram
    print("Histogram results:")

    for i, ni in enumerate(n):
        print("cat bins", categories[i], ni)

    for cat, counts in zip(valid_categories, n):
        total_count = np.sum(counts)
        print(
            f"  Category '{cat}': total count = {total_count}, max bin = {np.max(counts)}"
        )
        if total_count == 0:
            print(f"  WARNING: Category '{cat}' shows zero counts in all bins!")

    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Number of Data Points", fontsize=12)
    ax.set_title("Time Data by True/False and Solving Method", fontsize=14)
    ax.set_yscale("log", base=10)

    # Improve legend
    legend = ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    for text in legend.get_texts():
        text.set_fontsize(10)

    ax.grid(True, alpha=0.3)

    # Set reasonable axis limits
    ax.set_xlim(time_min - 0.05 * time_range, time_max + 0.05 * time_range)

    plt.tight_layout()

    # Save as PDF if path provided
    if save_path:
        plt.savefig(save_path, format="pdf", bbox_inches="tight", dpi=300)
        print(f"Plot saved as PDF: {save_path}")
    else:
        plt.show()


# Additional utility function to inspect your data
def inspect_data(data):
    """Inspect the data for potential issues."""
    df = pd.DataFrame(data, columns=["key", "holds", "time", "method"])
    print("=== DATA INSPECTION ===")
    print(f"Total data points: {len(df)}")
    print("Time statistics:")
    print(f"  Min: {df['time'].min()}")
    print(f"  Max: {df['time'].max()}")
    print(f"  Mean: {df['time'].mean():.3f}")
    print(f"  Std: {df['time'].std():.3f}")

    # print(f"\nUnique values:")
    # print(f"  Keys: {sorted(df['key'].unique())}")
    # print(f"  Holds: {sorted(df['holds'].unique())}")
    # print(f"  Methods: {sorted(df['method'].unique())}")

    print(f"\nData range: {df['time'].max() - df['time'].min():.6f}")

    # Check for negative times
    negative_count = len(df[df["time"] < 0])
    if negative_count > 0:
        print(f"\nWARNING: {negative_count} negative time values found!")
        print("Negative entries:")
        print(df[df["time"] < 0])

    # Check for very small ranges
    if df["time"].max() - df["time"].min() < 1e-6:
        print(
            "\nWARNING: Time values have very small range - may cause visualization issues"
        )

    print("========================\n")
    return df


def mk_plot_dat(pkl_file):
    """Debugging data."""
    results = load_results(pkl_file)
    dat = results.values
    plot_data = []
    for k in dat:
        ri: ResultInfo = dat[k]
        if ri.value == Res.IMPL_UNKNOWN:
            continue
        assert ri.value in {Res.IMPL_TRUE, Res.IMPL_FALSE}
        met = ri.method_id
        if met.startswith("vm"):
            met = "vam_fmb"
        elif met.startswith("vs"):
            met = "vam_saturation"
        pt = (str(k), ri.value == Res.IMPL_TRUE, ri.time, met)
        plot_data.append(pt)
    return plot_data


DEBUG = False


def read_and_plot(pkl_file):
    """Read pkl file and plot it."""
    if DEBUG:
        plot_data = sample_data
    else:
        plot_data = mk_plot_dat(pkl_file)

    print(f"inspecting data {len(plot_data)}")
    inspect_data(plot_data)
    print("\nPlotting histogram...")
    plot_stacked_histogram(plot_data, bins=20, save_path="time_histogram.pdf")


def main():
    """Run the whole thing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", type=str, default="results.pkl")
    args = parser.parse_args()
    read_and_plot(args.pkl_file)


# Usage example:
if __name__ == "__main__":
    main()
