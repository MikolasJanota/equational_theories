#!/usr/bin/env python3
# File:  res2json.py
# Author:  mikolas
# Created on:  Mon Aug 11 11:36:27 BST 2025
# Copyright (C) 2025, Mikolas Janota
import argparse
import json
import sys

from run_all import (
    Res,
    ResultInfo,
    Results,
    SolverCfg,
    generate_combinations,
    load_results,
)


def msg(*args, **kwargs):
    """Report."""
    print("#", *args, **kwargs, flush=True, file=sys.stderr)


def dictify(t):
    if not isinstance(t, SolverCfg):
        t = t[0]
    assert isinstance(t, SolverCfg)
    return t._asdict()


def serialize_data(results_obj):
    """Converts a Results namedtuple object into a JSON-serializable
    dictionary.

    Args:
        results_obj (Results): The namedtuple instance to serialize.

    Returns:
        dict: A dictionary ready for JSON serialization.
    """
    serializable_dict = {}

    # Convert the 'methods' dictionary.
    # The values (SolverCfg) are namedtuples, which we convert to dicts using _asdict().
    serializable_dict["methods"] = {
        k: dictify(v) for k, v in results_obj.methods.items()
    }

    # Convert the 'values' dictionary.
    # Keys are tuples, which must be converted to strings for JSON.
    # Values are ResultInfo namedtuples, which we convert to dicts.
    serializable_values = {}
    for (pair1, pair2), result_info in results_obj.values.items():
        # Convert the tuple key to a string
        key_str = f"{pair1}_{pair2}"

        # Convert the ResultInfo namedtuple to a dictionary.
        # The 'value' field is an Enum, so we extract its integer value.
        result_info_dict = result_info._asdict()
        result_info_dict["value"] = result_info_dict["value"].value
        serializable_values[key_str] = result_info_dict

    serializable_dict["values"] = serializable_values

    return serializable_dict


def test():
    """--- Create sample data ---"""
    # First, create some instances of the namedtuples.
    solver_cfg_1 = SolverCfg(
        external_command="solver_a", use_smt2=True, timeout=60, method_id="solver_a_v1"
    )
    solver_cfg_2 = SolverCfg(
        external_command="solver_b",
        use_smt2=False,
        timeout=120,
        method_id="solver_b_v2",
    )

    result_info_1 = ResultInfo(value=Res.IMPL_TRUE, time=0.5, method_id="solver_a_v1")
    result_info_2 = ResultInfo(value=Res.IMPL_FALSE, time=1.2, method_id="solver_b_v2")
    result_info_3 = ResultInfo(
        value=Res.IMPL_UNKNOWN, time=10.1, method_id="solver_a_v1"
    )

    # Now, create the main Results object with the sample data.
    methods_dict = {"solver_a_v1": solver_cfg_1, "solver_b_v2": solver_cfg_2}

    values_dict = {(1, 2): result_info_1, (3, 4): result_info_2, (5, 6): result_info_3}

    data_to_serialize = Results(methods=methods_dict, values=values_dict)

    # --- Serialize the data and print the JSON string ---
    # Use the custom function to prepare the data for JSON.
    json_serializable_data = serialize_data(data_to_serialize)

    # Use json.dumps to get the formatted JSON string.
    json_output = json.dumps(json_serializable_data, indent=1)

    print(json_output)


def export(pkl_file):
    """Export pkl file."""
    data_to_serialize = load_results(pkl_file)
    results = load_results(pkl_file)
    msg(f"loaded {len(results.values)} values")
    # mets = data_to_serialize.methods
    # for m, d in mets.items():
    #     print(m, d, type(d), type(d[0]), d[0])

    # --- Serialize the data and print the JSON string ---
    # Use the custom function to prepare the data for JSON.
    json_serializable_data = serialize_data(data_to_serialize)

    # Use json.dumps to get the formatted JSON string.
    json_output = json.dumps(json_serializable_data)
    msg("printing")
    print(json_output)
    msg("printing done")


def main():
    """Run the whole thing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("pkl_file", type=str)
    args = parser.parse_args()
    export(args.pkl_file)


if __name__ == "__main__":
    # test()
    main()
