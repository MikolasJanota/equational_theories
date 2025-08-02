#!/usr/bin/env python3
import argparse
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from run_all import Res, ResultInfo, Results, SolverCfg, load_results

# Sample data with more realistic values - replace this with your actual data
sample_data = [
    ("A", True, 1.2, "method1"),
    ("A", False, 1.5, "method1"),
    ("B", True, 2.1, "method2"),
    ("A", True, 1.8, "method1"),
    ("C", False, 3.2, "method3"),
    ("B", False, 2.5, "method2"),
    ("A", False, 1.1, "method2"),
    ("C", True, 3.8, "method3"),
    ("B", True, 2.3, "method1"),
    ("A", True, 1.9, "method3"),
    ("D", True, 0.8, "method1"),
    ("D", False, 0.9, "method2"),
    ("E", True, 4.1, "method3"),
    ("F", False, 2.8, "method1"),
    ("G", True, 1.6, "method2"),
]


def plot_histogram(data, bins=10, figsize=(12, 8), save_path=None):
    """Plot histogram of time data with colors distinguishing different
    combinations of key, holds, and method.

    Parameters:
    data: list of tuples (key, holds, time, method)
    bins: number of bins for histogram
    figsize: figure size tuple
    save_path: path to save the plot as PDF (optional)
    """

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data, columns=["key", "holds", "time", "method"])

    # Data validation and cleaning
    print(f"Original data points: {len(df)}")
    print(f"Time range: {df['time'].min():.3f} to {df['time'].max():.3f}")

    # Check for negative times
    negative_times = df[df["time"] < 0]
    if len(negative_times) > 0:
        print(f"WARNING: Found {len(negative_times)} negative time values!")
        print("Negative time entries:")
        print(negative_times[["key", "holds", "time", "method"]])
        print("Removing negative times from analysis...")
        df = df[df["time"] >= 0]

    if len(df) == 0:
        print("ERROR: No valid data points remaining after cleaning!")
        return

    # Create a combined category for coloring (excluding key from display)
    df["category"] = df["holds"].astype(str) + "_" + df["method"]

    # Get unique categories and assign colors
    unique_categories = df["category"].unique()
    print(f"Categories found: {unique_categories}")

    # Use a better color palette for better visibility
    if len(unique_categories) <= 10:
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_categories)))
    else:
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_categories)))
    color_map = dict(zip(unique_categories, colors))

    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)

    # Determine appropriate bin range and count
    time_min, time_max = df["time"].min(), df["time"].max()
    time_range = time_max - time_min

    # Adjust bins if data range is very small
    if time_range < 1e-6:
        print("WARNING: Very small time range detected. Using single bin.")
        bins = 1
    elif isinstance(bins, int) and time_range > 0:
        # Create explicit bin edges for better control
        bin_edges = np.linspace(time_min, time_max, bins + 1)
    else:
        bin_edges = bins

    print(f"Using {bins} bins for time range {time_min:.3f} to {time_max:.3f}")

    # Plot histogram for each category with explicit alpha and edge colors
    for i, category in enumerate(unique_categories):
        category_data = df[df["category"] == category]["time"]
        print(f"Category '{category}': {len(category_data)} data points")

        n, bins_used, patches = ax.hist(
            category_data,
            bins=bin_edges,
            alpha=0.7,
            color=color_map[category],
            label=category,
            edgecolor="black",
            linewidth=0.8,
        )

        # Print histogram info for debugging
        print(f"  Histogram counts: {n}")

    # Customize the plot
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Number of Data Points", fontsize=12)
    ax.set_title("Histogram of Time Data by Holds and Method", fontsize=14)
    ax.set_yscale("log", base=10)

    # Improve legend positioning
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


def plot_stacked_histogram(data, bins=10, figsize=(12, 8), save_path=None):
    """
    Alternative: Plot stacked histogram for better visualization when categories overlap
    """
    df = pd.DataFrame(data, columns=["key", "holds", "time", "method"])
    df["category"] = df["holds"].astype(str) + "_" + df["method"]

    # Prepare data for stacked histogram
    categories = df["category"].unique()
    time_data = [df[df["category"] == cat]["time"].values for cat in categories]

    fig, ax = plt.subplots(figsize=figsize)

    # Create stacked histogram
    ax.hist(
        time_data,
        bins=bins,
        label=categories,
        alpha=0.8,
        edgecolor="black",
        linewidth=0.5,
        stacked=True,
    )

    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Number of Data Points", fontsize=12)
    ax.set_title("Stacked Histogram of Time Data by Holds and Method", fontsize=14)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save as PDF if path provided
    if save_path:
        plt.savefig(save_path, format="pdf", bbox_inches="tight", dpi=300)
        print(f"Stacked plot saved as PDF: {save_path}")

    plt.show()


def plot_separate_subplots(data, bins=10, figsize=(15, 10), save_path=None):
    """
    Alternative: Separate subplots for each unique combination of holds and method
    """
    df = pd.DataFrame(data, columns=["key", "holds", "time", "method"])

    # Get unique combinations for holds and method (excluding key from display)
    unique_holds = df["holds"].unique()
    unique_methods = df["method"].unique()

    # Create subplots
    n_plots = len(unique_holds) * len(unique_methods)
    n_cols = min(3, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_plots == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)

    plot_idx = 0
    for holds in unique_holds:
        for method in unique_methods:
            subset = df[(df["holds"] == holds) & (df["method"] == method)]

            if len(subset) > 0:
                row = plot_idx // n_cols
                col = plot_idx % n_cols

                if n_rows > 1:
                    ax = axes[row, col]
                else:
                    ax = axes[col]

                ax.hist(
                    subset["time"],
                    bins=bins,
                    alpha=0.7,
                    edgecolor="black",
                    linewidth=0.5,
                )
                ax.set_title(f"Holds: {holds}, Method: {method}")
                ax.set_xlabel("Time")
                ax.set_ylabel("Count")
                ax.grid(True, alpha=0.3)

                plot_idx += 1

    # Hide empty subplots
    for i in range(plot_idx, n_rows * n_cols):
        row = i // n_cols
        col = i % n_cols
        if n_rows > 1:
            axes[row, col].set_visible(False)
        else:
            axes[col].set_visible(False)

    plt.tight_layout()

    # Save as PDF if path provided
    if save_path:
        plt.savefig(save_path, format="pdf", bbox_inches="tight", dpi=300)
        print(f"Subplots saved as PDF: {save_path}")

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


def read_and_plot(pkl_file):
    """Read pkl file and plot it."""
    print("Plotting overlapping histogram...")
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

    inspect_data(plot_data)
    plot_histogram(plot_data, bins=3, save_path="overlapping_histogram.pdf")

    # print("\nPlotting stacked histogram...")
    # plot_stacked_histogram(sample_data, save_path="stacked_histogram.pdf")

    # print("\nPlotting separate subplots...")
    # plot_separate_subplots(sample_data, save_path="separate_subplots.pdf")


def main():
    """Run the whole thing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", type=str, default="results.pkl")
    args = parser.parse_args()
    read_and_plot(args.pkl_file)


# Usage example:
if __name__ == "__main__":
    main()
