# Perceiver IO Recommender
This repository includes a sample implementation of Perceiver-IO recommender for a news recommendation task on MIND dataset, along with [NAML](https://www.ijcai.org/proceedings/2019/536) and [NRMS](https://aclanthology.org/D19-1671/) baseline implementations.

## System Requirements
This code can be run from Docker on Linux environment. We confirmed that it runs under below environment.

* Linux (Ubuntu 20.04 LTS)
* Docker: version 20.10.6, build 370c289
* docker-compose: 1.29.1, build c34c88b2
* nvidia-container-toolkit: 1.5.1-1 amd64
* GPU: NVIDIA GeForce RTX 2080 Ti 


## Setting up
### 1. Clone the repository branch
```
git clone --recursive https://github.com/stockmarkteam/perceiver_io_recommender.git
```

### 2. Setup environment parameters

Environment parameters need to be written in `.env` file. You can simply copy it from `.env.sample` to work with default parameters.

```
cd perceiver_io_recommender
cp .env.sample .env
```

These are the necessary parameters written in `.env` file, you can edit it if necessary.

* `COMPOSE_PROJECT_NAME`:
    * Needed for docker-compose. For details please [refer](https://docs.docker.com/compose/reference/envvars/#compose_project_name).
* `DEVICE`（Default: `gpu`）: 
    * Device setting for docker. Parameters can be set to `gpu` or `cpu`, but we tested the code only with `gpu` parameter.
* `DATASET_PATH`Default: `$(PWD)/dataset`）:
    * Host directory for MIND dataset. It is mounted to `dataset/` directory from the container.
* `MODEL_PATH`（Default: `$(PWD)/models`）:
    * Host directory for pretrained models for GloVe and Transformer. It is mounted to `models/` directory from the container.
* `LOG_PATH` （Default: `$(PWD)/logs`）:
    * Host directory for training logs. It is mounted to `logs/` folder from the container.
* `VENV_PATH`:
    * Host directory for python virtual environment. It is mounted `.venv/` folder from the container.
* `JUPYTER_PORT`:（Default: `8888`）
    * The port number binded for the host OS access to the jupyter notebook that is launched in the container.
* `TENSORBOARD_PORT`: （Default: `6006`）
    * The port number binded for the host OS access to the tensorboard that is launched in the container.

### 3. Setup Docker Environment
```bash
make setup
```

### 4. Download dataset

Download [MIND dataset](https://msnews.github.io/) and put the zip file to a directory which is visible from the container. You can put it to the same folder with README.

### 5. Enter the container
```bash
make sh
```

## News Recommendation with MIND Dataset

## Preprocessing
Run below command in container to do all necessary preprocessing.
```bash
pipenv run preprocess-all data_path.train_zip=<path/to/MINDxxx_train.zip> data_path.valid_zip=<path/to/MINDxxx_dev.zip>
```
If you are working with the large dataset, please add this parameter to above command:

`params.dataset_type=large`


## Training
Run below command in container for training the perceiver-io model.
```bash
pipenv run train
```

Some of the optional parameters are listed below.

* `model`: 
    * `naml` or `nrms` (default: `nrms`)
* `embedding_layer`:
    *  `word_embedding` or `transformer` (default: word_embedding)
* `hparams.article_attributes`:
    *  Can be selected from [title,body,category,subcategory]（default: `[title,body,category,subcategory]`)
* `hparams.n_epochs`: 
    * default: 3
* `hparams.max_title_length`:
    *  Max. number of tokens from article titles（default: `30`)
* `hparams.max_body_length`:
    *  Max. number of tokens from article bodies（default: `128`）
* `hparams.batch_size.train`:
* `hparams.batch_size.valid`:
    * (Default batch sizes are different depending on the selected embedding layer）
* `hparams.accumulate_grad_batches`: 
    * Training batch size becomes `hparams.batch_size.train` * `hparams.accumulate_grad_batches`
* `dataset`:
    * If it is set to `precomputed`, it reads from serialized article text data hence fetching data during training can be speeded up.
* `num_workers`:
    * For dataLoader（default: `4`）

This library uses [hydra](https://github.com/facebookresearch/hydra) as config manager and  everything in [config](src/train/config) can be overwritten from the command line.

## Product Recommendation with Amazon Dataset

## Preprocessing
In the paper, we compared results with [DIEN](https://github.com/YafeiWu/DIEN), so we are going to convert data from their repository in order to make apple-to-apple comparison.

First, download meta_Books.json from `http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/` and put it under `dataset/amazon/books`.
Then, download `local_train_splitByUser` and `local_test_splitByUser` from [DIEN](https://github.com/YafeiWu/DIEN) and put it under `dataset/amazon/books`.

Finally, run below command: 
```bash
sh src/preprocess/scripts/amazon/preprocess_amazon.sh
```
## Training
Training can be done in the same way as we do for news recommendation on MIND dataset:

```bash
pipenv run python3 -m src.train.main  dataset_name=amazon dataset_type=books hparams.n_negatives=1 model=perceiver_io hparams.word_pos_emb=True hparams.feat_type_emb=True dataset=precomputed hparams.article_attributes=[title,body,category]
```

## Category Recommendation with MIND Dataset

If you already did preprocessing for news recommendation for MIND dataset, there is no extra preprocessing needed. To run training, please run below command:

```bash
pipenv run python3 -m src.train.main model=perceiver_io_category_prediction hparams_model=perceiver_io embedding_layer=word_embedding hparams.article_attributes=[title,body] hparams.classify_attr=category dataset=precomputed
```

## Check training results
```
pipenv run tensorboard
```
You can browse results from this link `localhost:${TENSORBOARD_PORT}` in the host.
