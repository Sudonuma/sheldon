# sheldon
Torngat dev repository with wandb, mlflow, hydra and dvc

## Preliminary steps for development
### Clone sheldon repository

```
git clone https://github.com/Sudonuma/sheldon.git
```

Commit and push to the repository often while you make progress towards the solution.

### Create environment
Make sure to have conda installed and ready, then create a new environment using the ``environment.yml``
file provided in the root of the repository and activate it:

```bash
> conda env create -f environment.yml
> conda activate sheldon
```

### Get API key for Weights and Biases
Get your API key from W&B by going to 
[https://wandb.ai/authorize](https://wandb.ai/authorize) and click on the + icon (copy to clipboard), 
then paste your key into this command:

```bash
> wandb login [your API key]
```

You should see a message similar to:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[your username]/.netrc
```

### Cookie cutter
use cookie cutter template to create stubs for new pipeline components. It is not required that you use this, but it might save you from a bit of 
boilerplate code. Just run the cookiecutter and enter the required information, and a new component 
will be created including the `conda.yml` file, the `MLproject` file as well as the script. You can then modify these
as needed, instead of starting from scratch.
For example:

```bash
> cookiecutter cookie-mlflow-step -o src

step_name [step_name]: download_dataset
script_name [run.py]: run.py
job_type [my_step]: download_dataset
short_description [My step]: This steps downloads the data
long_description [Mlflow component]: Downloads the dataset used for this project and saves it in datasets folder. you can check your data version using DVC as explained further.
parameters [parameter1,parameter2]: parameter1,parameter2,parameter3
```

This will create a step called ``download_dataset`` under the directory ``src`` with the following structure:

```bash
> ls src/download_dataset/
conda.yml  MLproject  run.py
```

You can now modify the script (``run.py``), the conda environment (``conda.yml``) and the project definition 
(``MLproject``) as you please.

The script ``run.py`` will receive the input parameters ``parameter1``, ``parameter2``,
``parameter3`` and it will be called like:

```bash
> mlflow run src/step_name -P parameter1=1 -P parameter2=2 -P parameter3="test"
```

### The configuration
The parameters controlling the pipeline are defined in the ``config.yaml`` file defined in
the root folder. We will use Hydra to manage this configuration file. Remember: this file is only read by the ``main.py`` script 
(i.e., the pipeline) and its content is
available with the ``go`` function in ``main.py`` as the ``config`` dictionary. 

NOTE: do NOT hardcode any parameter when writing the pipeline. All the parameters should be 
accessed from the configuration file.

### Running the entire pipeline or just a selection of steps
In order to run the pipeline when you are developing, you need to be in the root of the starter kit, 
then you can execute as usual:

```bash
>  mlflow run .
```
This will run the entire pipeline.

When developing it is useful to be able to run one step at the time. Say you want to run only
the ``download_dataset`` step. The `main.py` is written so that the steps are defined at the top of the file, in the 
``_steps`` list, and can be selected by using the `steps` parameter on the command line:

```bash
> mlflow run . -P steps=download
```
If you want to run the ``download_dataset`` and another step let's say for instance ``train_model``, you can similarly do:
```bash
> mlflow run . -P steps=download_dataset,train_model
```
You can override any other parameter in the configuration file using the Hydra syntax, by
providing it as a ``hydra_options`` parameter. Example:

```bash
> mlflow run . \
  -P steps=download_dataset,train_model \
  -P hydra_options="modeling.network.lr=0.1 modeling.network.batch_size=8"
```

### Data version control config: DVC

## Components: 1/ Download_data 2/ second_component 3/ third_component
### Components: 1/ Download_data 

If you want to pull the latest version of the data, run:
```bash 
> mlflow run . -P steps=download_dataset
```
If you have a different data you will work on, run:
```bash 
> mlflow run . -P steps=download_data -P hydra_options="data.download_new='True'"
```

This will download your data in the data/raw path.
if you used your data for training and this data is the next version of the dataset please add it to be tracked and to be pulled by you collegues to do so please follow these steps:
```bash 
> dvc add data/
> git add data/.gitignore data.dvc
> git commit -m 'New data version ...'
create a tag:
> git tag -a 'v[version_number]' -m 'message'
> dvc push
```

