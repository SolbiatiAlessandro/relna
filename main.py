# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import relna.db
import uuid
from relna.tensorflow.trainers.utils import jobAPIwrapper as job_wrapper

from flask import Flask, render_template, request

# [START create_app]
app = Flask(__name__)
# [END create_app]


@app.route('/')
def index():
    # later jobs will be first put inside DB and then queried
    # imitation_learning_jobs = relna.db.get_imitation_learning_jobs()

    # uncomment following line for permissions if flask server is run locally
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpkey.json"
    imitation_learning_jobs = job_wrapper.list()
    return render_template('index.html', 
            len_imitation_learning_jobs=len(imitation_learning_jobs))

@app.route('/imitation_learning/')
def imitation_learning():
    # look for jobs

    # later jobs will be first put inside DB and then queried
    # jobs = relna.db.get_imitation_learning_jobs()
    jobs = job_wrapper.list()
    return render_template('imitation_learning.html', jobs=jobs)

@app.route('/ship_trainer', methods=['GET', 'POST'])
def ship_trainer(
        trainer_folder_name='imitation_learning',
        data_file_name='RoboschoolHumanoid-v1.pkl'
        ):
    """
    Args:
        trainer_folder_name: (str) 
            -> relna/tensorflow/trainers/trainer_folder_name
            e.g. 'imitation_learning'
        data_file_name: (str) 
            -> gs://relna-mlengine/data/data_file_name
            e.g. 'RoboschoolHumanoid-v1.pkl'

    trainer_folder_name/
    - setup.py
    - trainer/
        - main.py
        - task.py

    ships trainer to Google AI Platform:
    1. build trainer package
    2. submit job to Google Cloud
    """
    print(request)

    #generete job uuid
    job_id = uuid.uuid4()
    job_name = ("relna_"+trainer_folder_name+"_"+str(job_id)).replace('-','_')
    print("[relna:ship_trainer] generated job {}".format(job_name))

    #build job package
    trainer_address = os.path.join(
            '.',
            'relna',
            'tensorflow',
            'trainers',
            trainer_folder_name)
    pkg_destination_folder = os.path.join("pkgs",job_name)
    # copying setup.py and trainer to current folder
    # (package will not be built correctly otherwise
    os.system("cp {} .".format(os.path.join(trainer_address, 'setup.py')))
    os.system("cp -r {} .".format(os.path.join(trainer_address, 'trainer')))
    # following commands builds the package
    os.system("python setup.py\
            sdist -d {}".format(pkg_destination_folder))
    logging.warning("[relna:ship_trainer] generated pakage {}".format(
        pkg_destination_folder))

    #clean local folder
    os.system("rm ./setup.py")
    os.system("rm -r ./trainer")
    os.system("rm -r ./trainer.egg-info")

    #submit job
    wrapper = job_wrapper(
            job_name,
            trainer_package_address = os.path.join(pkg_destination_folder,
                "trainer-0.1.tar.gz"),
            train_files = "gs://relna-mlengine/data/"+data_file_name,
            eval_files = "gs://relna-mlengine/data/"+data_file_name
            )
    wrapper.submit()
    logging.warning("[relna:ship_trainer] submitted job {}".format(
        job_name))

    return '[relna:ship_trainer] trainer shipped succesfully'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
