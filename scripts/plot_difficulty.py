#!/usr/bin/env python3
# File:  plot_difficulty.py
# Author:  mikolas
# Created on:  Tue Aug 5 10:33:56 CEST 2025
# Copyright (C) 2025, Mikolas Janota
import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

import generate_eqs_list
from run_all import Res, ResultInfo, Results, SolverCfg, load_results

# from matplotlib.colors import ListedColormap

# Sample data with more realistic values
sample_data = {
    (1, 2): 1,
    (1, 3): 2,
    (2, 3): 4,
    (3, 2): 10,
}


def plot_pair_times(
    pair_times_dict,
    n=None,
    title="Pair Processing Times Heatmap",
    save_pdf=None,
    show_plot=True,
):
    """Create a heatmap visualization of pair processing times.

    Parameters:
    pair_times_dict: dict - Dictionary mapping (x, y) tuples to time values
    n: int - Size of the grid (if None, inferred from data)
    title: str - Title for the plot
    save_pdf: str - Path to save PDF file (if None, no file is saved)
    show_plot: bool - Whether to display the plot (default True)
    """

    # Determine n if not provided
    if n is None:
        if pair_times_dict:
            max_coord = max(max(pair) for pair in pair_times_dict.keys())
            n = max_coord
        else:
            n = 10  # default size

    # Create matrix to hold time values
    # Use np.nan for missing pairs, which we'll handle specially
    time_matrix = np.full((n, n), np.nan)

    # Fill in the time values
    for (x, y), time_val in pair_times_dict.items():
        if 1 <= x <= n and 1 <= y <= n:  # Ensure coordinates are within bounds
            time_matrix[y - 1, x - 1] = time_val  # Note: y-1, x-1 for matrix indexing

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create a mask for missing values
    mask = np.isnan(time_matrix)

    # Get the range of time values for colormap
    valid_times = time_matrix[~mask]
    if len(valid_times) > 0:
        vmin, vmax = valid_times.min(), valid_times.max()

        # Create the main heatmap for valid time values
        im = ax.imshow(
            time_matrix,
            cmap="viridis",
            vmin=vmin,
            vmax=vmax,
            origin="lower",
            extent=[0.5, n + 0.5, 0.5, n + 0.5],
        )

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label("Solving Time", rotation=270, labelpad=20)

        # Overlay black squares for missing pairs
        for i in range(n):
            for j in range(n):
                if mask[i, j]:
                    rect = patches.Rectangle(
                        (j + 0.5, i + 0.5), 1, 1, linewidth=0, facecolor="black"
                    )
                    ax.add_patch(rect)
    else:
        # If no valid time values, just show black squares
        ax.imshow(
            np.zeros((n, n)),
            cmap="gray",
            origin="lower",
            extent=[0.5, n + 0.5, 0.5, n + 0.5],
        )

    # Customize the plot
    ax.set_xlim(0.5, n + 0.5)
    ax.set_ylim(0.5, n + 0.5)
    ax.set_xlabel("Equation x")
    ax.set_ylabel("Equation y")
    ax.set_title(title)

    # Set ticks to show element numbers
    ax.set_xticks(range(1, n + 1))
    ax.set_yticks(range(1, n + 1))

    # Add grid
    ax.grid(True, alpha=0.3)

    # Add text annotation for black squares
    if np.any(mask):
        ax.text(
            0.02,
            0.98,
            "Black: No time data",
            transform=ax.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.tight_layout()

    # Save to PDF if path is provided
    if save_pdf:
        fig.savefig(save_pdf, format="pdf", bbox_inches="tight", dpi=300)
        print(f"Plot saved to: {save_pdf}")

    # Show plot if requested
    if show_plot:
        plt.show()

    return fig, ax


def test_run():
    """Example usage."""
    # Example data: dictionary mapping (x, y) pairs to processing times
    example_data = {
        (1, 1): 2.5,
        (1, 2): 1.8,
        (1, 3): 3.2,
        (2, 1): 4.1,
        (2, 2): 0.9,
        (2, 4): 2.7,
        (3, 1): 1.5,
        (3, 3): 5.2,
        (3, 5): 1.1,
        (4, 2): 3.8,
        (4, 4): 2.3,
        (5, 1): 4.5,
        (5, 3): 1.9,
        (5, 5): 3.6,
    }

    # Create the plot
    plot_pair_times(
        example_data,
        n=5,
        title="Example: Pair Processing Times",
        save_pdf="pair_times_example.pdf",
    )

    # Example with larger grid and more sparse data
    sparse_data = {
        (1, 8): 10.2,
        (3, 5): 7.8,
        (5, 2): 12.5,
        (7, 7): 5.3,
        (8, 1): 15.1,
        (10, 10): 8.7,
    }

    plot_pair_times(
        sparse_data,
        n=10,
        title="Example: Sparse Pair Data",
        save_pdf="sparse_pair_data.pdf",
        show_plot=False,
    )  # Don't show, just save

    print("Both plots have been saved as PDF files!")


def mk_plot_dat(pkl_file):
    """Debugging data."""
    results = load_results(pkl_file)
    dat = results.values
    plot_data = dict()
    for k in dat:
        ri: ResultInfo = dat[k]
        if ri.value == Res.IMPL_UNKNOWN:
            continue
        assert ri.value in {Res.IMPL_TRUE, Res.IMPL_FALSE}
        plot_data[k] = ri.time
    return plot_data


DEBUG = False


def read_and_plot(pkl_file):
    """Read pkl file and plot it."""
    if DEBUG:
        plot_data = sample_data
    else:
        plot_data = mk_plot_dat(pkl_file)

    print(f"loaded {len(plot_data)} data points")
    max_eq = len(generate_eqs_list.eqs)
    # Create the plot
    plot_pair_times(
        plot_data,
        n=None if DEBUG else max_eq,
        title="Solving Times x=>y",
        save_pdf="difficulty.pdf",
        show_plot=DEBUG,
    )


def main():
    """Run the whole thing."""
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", nargs="?", type=str, default="results.pkl")
    parser.add_argument("-d", "--debug", action="store_true")

    args = parser.parse_args()
    DEBUG = args.debug
    read_and_plot(args.pkl_file)


if __name__ == "__main__":
    main()
