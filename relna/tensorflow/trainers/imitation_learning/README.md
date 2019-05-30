# Imitation Learning Trainer basis

## setup
Before running programmtically the job you need to build the package with

```
(venv) python setup.py sdist
```

## running the trainer - DEV-LOCAL

Locally, development mode
```
(venv) cd trainer
(venv) python task.py --mode dev-local
```

You should see something like
```
>>> WARNING:root:[model.py]:predict - SUCCESS, score = 0.3126386516517327
```
This means that the model is being trained and predicting succesfully.

## running the trainer - DEV-CLOUD

Cloud, development mode
```
(venv) cd trainer
(venv) python task.py --help
(venv) python task.py --mode dev-cloud --input-files data/RoboschoolHumanoid-v1.pkl
```

You should see something like this
```
[GCSproxy.gcs_load] interacting with Google Cloud Storage to retrieve data: data/RoboschoolHumanoid-v1.pkl
[GCSproxy.gcs_load] interacting with Google Cloud Storage to upload data: /tmp/imitation-learning/7e130c26-9513-4b90-bbbb-53926dae540f/model.ckpt.index
```
It means  the model is being trained and uploaded to cloud


## running the trainer - PROD-CLOUD

(RELNA) You can programmatically run the job on cloud on cloud locally with the `utils.py` script

```
cd ..
(venv) python utils.py
```
