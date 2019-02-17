import argparse
from typing import Dict, List, Optional, Union
import warnings
import yaml


def add_common_args(parser):
    parser.add_argument(
        "--config-override",
        type=str,
        default="{}",
        help="A string following python dict syntax, specifying certain config arguments to "
             "override, useful for launching batch jobs through shel lscripts. The actual config "
             "will be updated and recorded in the checkpoint saving directory. Only argument "
             "names already present in config will be overriden, rest ignored."
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=0,
        help="Random seed for all devices, useful for doing multiple runs and reporting mean and "
             "variance."
    )

    parser.add_argument_group("CLEVR Data files.")
    parser.add_argument(
        "--tokens-train-h5",
        default="data/clevr_tokens_train.h5",
        help="Path to HDF file containing tokenized CLEVR v1.0 train split programs, questions "
             "and answers, and corresponding image indices."
    )
    parser.add_argument(
        "--tokens-val-h5",
        default="data/clevr_tokens_val.h5",
        help="Path to HDF file containing tokenized CLEVR v1.0 val split programs,"
             " questions and answers, and corresponding image indices."
    )
    parser.add_argument(
        "--features-train-h5",
        default="data/features_train.h5",
        help="Path to HDF file containing pre-extracted features from CLEVR v1.0 train images."
    )
    parser.add_argument(
        "--features-val-h5",
        default="data/features_val.h5",
        help="Path to HDF file containing pre-extracted features from CLEVR v1.0 val images."
    )
    parser.add_argument(
        "--vocab-dirpath",
        default="data/clevr_vocab",
        help="Path to directory containing vocabulary for programs, questions and"
             " answers."
    )

    parser.add_argument_group("Compute resource controlling arguments.")
    parser.add_argument(
        "--gpu-ids",
        nargs="+",
        type=int,
        help="List of ids of GPUs to use (-1 for CPU)."
    )
    parser.add_argument(
        "--num-val-examples",
        default=10000,
        type=int,
        help="Number of validation examples to use. CLEVR val is huge, this can be used to make "
             "the validation loop a bit faster, although might provide a noisy estimate of "
             "performance."
    )

    parser.add_argument_group("Checkpointing related arguments")
    parser.add_argument(
        "--save-dirpath",
        default="checkpoints/experiment",
        help="Path of directory to save checkpoints, this path is recommended to be empty or "
             "non-existent. Having previously saved checkpoints in this directory might overwrite "
             "them."
    )
    parser.add_argument(
        "--checkpoint-every",
        default=500,
        type=int,
        help="Save a checkpoint after every this many epochs/iterations."
    )


def read_config(config_ymlpath: str):
    config = yaml.load(open(config_ymlpath))
    return config


def override_config_from_opts(config: Dict[str, Union[int, float, str, List[int], List[float]]],
                              config_override: str):
    # Convert string to a python dict.
    config_override = eval(config_override)

    for config_key in config_override:
        if config_key in config:
            config[config_key] = config_override[config_key]
        else:
            warnings.warn(f"Config {config_key}, does not exist in provided config file.")
    return config


def print_config_and_args(config: Dict[str, Union[int, float, str, List[int], List[float]]],
                          args: argparse.Namespace):
    print(yaml.dump(config, default_flow_style=False))
    for arg in vars(args):
        print("{:<20}: {}".format(arg, getattr(args, arg)))


def cycle(iterable):
    # Using itertools.cycle with dataloader is harmful
    while True:
        for x in iterable:
            yield x