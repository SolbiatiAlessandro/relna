This is the folder that contain the tensorflow files for training on Google Cloud AI Platform. You can read more in [the tutorial in how to train a tensorflow model](https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction) and [the tutorial on how to do it programmaticaly](https://cloud.google.com/ml-engine/docs/tensorflow/training-jobs).

The pricing for Google Cloud AI Platform = Consumed ML units * $0.49

## Run job locally
```
gcloud ai-platform local train    \
	--module-name trainer.task    \
    --package-path trainer/     \
    --job-dir $MODEL_DIR    \
    --     \
    --train-files $TRAIN_DATA    \
    --eval-files $EVAL_DATA    \
    --train-steps 1000    \
    --eval-steps 100
```
NOTE1: I am following cloudml-samples/census/tensorflowcore example, that didn't run in python3 runtime. I adapted the code and opened a pull request [here on the github page of GCP](https://github.com/GoogleCloudPlatform/cloudml-samples/pull/424)

NOTE2: For debugging purpose all the env variables in these example commands are inside ./tutorial.vars


## Run a job from gcloud with python3 runtime
```
gcloud ai-platform jobs submit training $JOB_NAME \
    --job-dir $OUTPUT_PATH \
    --runtime-version 1.13 \
    --python-version 3.5 \
    --module-name trainer.task \
    --package-path trainer/ \
    --region $REGION \
    -- \
    --train-files $TRAIN_DATA \
    --eval-files $EVAL_DATA \
    --train-steps 1000 \
    --eval-steps 100 \
    --verbosity DEBUG
```

To check the current jobs open the [jobs panel in GCP](https://console.cloud.google.com/mlengine/jobs?project=relna-241818).

If the jobs execute correctly on cloud you should have the file `gs://relna-mlengine/census_single_1/export/saved_model.pb`

## Run a job locally programmatically

An example of a full model is inside `trainers/template/`, you can read the README.md there
