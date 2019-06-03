# Imitation Learning Trainer basis

## MODES

You can run jobs in different modes:
1. DEV-LOCAL: the task is executed on the local machine, using local data
2. DEV-CLOUD: the task is executed locally using data from cloud, t, you need a `gcpkey.json`, 
3. PROD-CLOUD: the task is executed as a job on Google AI Platform (relna), it uses Google Cloud Storage input/output

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

NOTE: the models are uploaded to 
`Buckets/relna-mlengine/ /outputs/imitation-learning`

You can also launch dev-cloud job from Google Cloud SDK (locally)
```
cd ../
pwd
>> /Users/alex/Desktop/Coding/AI/relna/relna/tensorflow/trainers/imitation_learning

gcloud ai-platform local train    \
	--module-name trainer.task    \
    --package-path trainer/     \
    --     \
    --mode dev-cloud \
    --input-files data/RoboschoolHumanoid-v1.pkl \
    --train-steps 1000    \
```
you should get the same output as before

## running the trainer - PROD-CLOUD

PROD-CLOUD can be executed from Google Cloud SDK

```
gcloud ai-platform jobs submit training test000 \
    --job-dir gs://relna-mlengine/outputs/imitation-learning/mlengine000 \
    --runtime-version 1.13 \
    --python-version 3.5 \
    --module-name trainer.task \
    --package-path trainer/ \
    --region europe-west1 \
    -- \
    --mode prod-cloud \
    --input-files data/RoboschoolHumanoid-v1.pkl \
    --train-steps 2000 \
    --verbosity DEBUG
```

(RELNA) You can programmatically run the job on cloud on cloud locally with the `utils.py` script

Before running programmtically the job you need to build the package with

```
(venv) python setup.py sdist
cd ..
(FISH) set GOOGLE_APPLICATION_CREDENTIALS ../../../gcpkey.json
(venv) python utils.py
```
