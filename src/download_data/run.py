#!/usr/bin/env python
"""
this step allows you to download the latest version of the dataset used in the crack detection segmentation pipeline
"""
import argparse
import logging
import wandb

# Get url from DVC
import dvc.api
from dvc.repo import Repo

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go():

    data_url = dvc.api.get_url(
        path='/home/sheldon/data',
        repo="https://github.com/Sudonuma/sheldon.git"
    )
    print(data_url)

    # run = wandb.init(job_type="download_data")
    # run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################


if __name__ == "__main__":

    # parser = argparse.ArgumentParser(description="this step allows you to download the dataset")

    # parser.add_argument(
    #     "--data_path", 
    #     type=str,
    #     help="path to local data",
    #     required=True,
    #     default="/home/sheldon/data"
    # )

    # parser.add_argument(
    #     "--repo", type=str, help="repository",  default="https://github.com/Sudonuma/sheldon.git" 
    # )


    # parser.add_argument(
    #     "--data_url", 
    #     type=str,
    #     help="URL of the dataset",
    #     required=True
    # )


    # parser.add_argument(
    #     "--version", type=str, help="version",  default="v1"
    # )

    # parser.add_argument(
    #     "--artifact_name", 
    #     type=str,
    #     help="Name for the artifact",
    #     required=True
    # )

    # parser.add_argument(
    #     "--artifact_type", 
    #     type=str,
    #     help="Type for the artifact: .dvc file, .csv file",
    #     required=True
    # )

    # parser.add_argument(
    #     "--artifact_description", 
    #     type=str,
    #     help="Description for the artifact",
    #     required=True
    # )


    # args = parser.parse_args()

    go()
