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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpkey.json"
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

@app.route('/run_imitation_learning_job', methods=['GET', 'POST'])
def run_imitation_learning_job():
    print(request)

    #generete job uuid
    job_id = uuid.uuid4()
    job_name = ("relna_imitation_learning_"+str(job_id)).replace('-','_')
    print("[relna:run_imitation_learning_job] generated job {}".format(job_name))

    #build job package
    logging.warning("[relna:run_imitation_learning_job] generating job uuid")
    pkg_destination_folder = os.path.join("pkgs",job_name)
    os.system("python relna/tensorflow/trainers/imitation_learning/setup.py\
            sdist -d {}".format(pkg_destination_folder))
    logging.warning("[relna:run_imitation_learning_job] generated pakage {}".format(
        pkg_destination_folder))

    #submit job
    wrapper = job_wrapper(
            job_name,
            trainer_package_address = os.path.join(pkg_destination_folder,
                "trainer-0.1.tar.gz"),
            train_files = "gs://relna-mlengine/data/RoboschoolHumanoid-v1.pkl",
            eval_files = "gs://relna-mlengine/data/RoboschoolHumanoid-v1.pkl"
            )
    wrapper.submit()
    logging.warning("[relna:run_imitation_learning_job] submitted job {}".format(
        job_name))


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
