import json

import mlflow
import tempfile
import os
import wandb
import hydra
from omegaconf import DictConfig

_steps = [
    "download_data",
    "check_data_quality",
    # check if you need data split step or not
    "data_split",
    "train_model",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
   # "test_model"
]

# This automatically reads in the configuration
@hydra.main(config_name='config')
def go(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # You can get the path at the root of the MLflow project with this:
    root_path = hydra.utils.get_original_cwd()

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "download_data" in active_steps:
            # Download file and load in W&B
            _ = mlflow.run(
                os.path.join(root_path, "src", "download_data"),
                "main",
                parameters={
                    "new_dataset_name": "CFD",
                    "download_new": config['data']['download_new'],
                    "data_path": "./data",
                    "repo": config['main']['repository'],
                    "data_url": config['data']['data_url'],
                    "version": config['data']['version'],
                    "artifact_name": "data.dvc",
                    "artifact_type": "dataset_dvc_file",
                    "artifact_description": "Dataset metadata and .dvc file: This is an artfact for data information and not the data itself"
                },
            )


if __name__ == "__main__":
    go()
