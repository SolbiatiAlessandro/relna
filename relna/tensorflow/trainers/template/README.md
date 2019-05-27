# Trainer Template 

Before running programmtically the job you need to build the package with

```
(venv) python setup.py sdist
```

You can programmatically run the job locally with the `utils.py` script

```
cd ..
(venv) python utils.py
```

The jobs will take data from `gs://relna-mlengine/data/trainer_template/adult.data.csv`
