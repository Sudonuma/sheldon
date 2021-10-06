#!/usr/bin/env python
"""
this step allows you to download the latest version of the dataset used in the crack detection segmentation pipeline
"""
import argparse
import logging
import wandb
import yaml
import os
import gdown
# Get url from DVC
import dvc.api
from dvc.repo import Repo

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    if args.download_new == 'True':
        logger.info("Downloading_dataset")
        file_id = args.data_url.split('/')[-2]
        local_directory = os.path.join("/home/sheldon/data/raw/" + args.new_dataset_name + '.zip')
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.cached_download(url, local_directory, postprocess=gdown.extractall)
    else:
        logger.info("pulling data with DVC")
        repo = Repo(".")
        repo.pull()
        logger.info("Finished pulling data with dvc, check data folder")

        data_url = dvc.api.get_url(
            path=args.data_path,
            repo=args.repo,
            rev=args.version
        )


    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
        with wandb.init(job_type="get_data") as run:
            with dvc.api.open('./data.dvc') as fd:
                dataconfig = yaml.safe_load(fd)

                logger.info("Creating artifact")
                artifact = wandb.Artifact(
                    name=args.artifact_name,
                    type=args.artifact_type,
                    description=args.artifact_description,
                    metadata={'original_url': data_url, 'version': args.version}
                )
                artifact.add_file(fd.name, name='data.dvc')

                logger.info("Logging artifact")
                run.log_artifact(artifact)

                artifact.wait()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="this step allows you to download the dataset")


    parser.add_argument(
        "--new_dataset_name", 
        type=str,
        help="Set your new dataset name",
    )

    parser.add_argument(
        "--download_new", 
        type=str,
        help="Set this to True if you will not pull the dataset and will use a new different one",
        default='False',
        required=True
    )
    
    parser.add_argument(
        "--data_path", 
        type=str,
        help="path to local data",
        required=False,
        default="./data"
    )

    parser.add_argument(
        "--repo", type=str, help="repository", required=False, default="https://github.com/Sudonuma/sheldon.git" 
    )


    parser.add_argument(
        "--data_url", 
        type=str,
        help="URL of the dataset of your choice.",
        required=False
    )


    parser.add_argument(
        "--version", type=str, help="version", required=False, default="971b6cae3f36007ea3df3e0c43c8a139ae6a9dbd"
    )

    parser.add_argument(
        "--artifact_name", 
        type=str,
        help="Name for the artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_type", 
        type=str,
        help="Type for the artifact: .dvc file, .csv file",
        required=True
    )

    parser.add_argument(
        "--artifact_description", 
        type=str,
        help="Dataset used for crack detection project.",
        required=True
    )

    args = parser.parse_args()

    go(args)
