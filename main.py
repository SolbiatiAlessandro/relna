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
from relna.tensorflow.trainers.gcloud_job_shipper import jobAPIwrapper as job_wrapper
from relna.tensorflow.trainers.gcloud_job_shipper import GCSproxy

from flask import Flask, render_template, request

# [START create_app]
app = Flask(__name__)
# [END create_app]


@app.route('/')
def index():
    # later jobs will be first put inside DB and then queried
    imitation_learning_jobs = relna.db.get_imitation_learning_jobs()

    # uncomment following line for permissions if flask server is run locally
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpkey.json"
    # imitation_learning_jobs = job_wrapper.list()
    return render_template('index.html', 
            len_imitation_learning_jobs=len(imitation_learning_jobs))

@app.route('/imitation_learning/')
def imitation_learning():
    """
    look for jobs from postgresql
    """

    relna_jobs = relna.db.get_imitation_learning_jobs()
    # ('RoboschoolHumanoid', 'v1', 'hw1', 5, <memory at 0x108ebe4c8>, <memory at 0x109174288>)

    # query Google Cloud AI Platform job lists
    gcloud_jobs = job_wrapper.list()
    relna_jobs_state = {}
    # always record the state of the last gcloud job
    # gcloud doesn't guarantee they are time ordered tough
    for job in gcloud_jobs[::-1]:
        # this is the relna_job id without the gcloud uuid 
        relna_job_id = job['jobId'][:-36] 
        relna_jobs_state[relna_job_id] = {
                'state' : job['state'],
                'gcloud_id' : job['jobId']
                }

    data = []
    logging.warning("[DEBUGGING:jobs] trainerID, job_status, gcloud_job_id")
    for job in relna_jobs:
        trainerID = job[3]
        relna_job_id = "relna_imitation_learning__"+str(trainerID)+"__"
        job_status = relna_jobs_state[relna_job_id]['state']
        job_dict = {
                'trainerID':trainerID,
                'gym':job[0],
                'expert_policy':job[1],
                'model':job[2][:30],
                'status':job_status
            }
        logging.warning("[DEBBUGING:jobs] {} {} {}".format(
            trainerID,
            job_status,
            relna_jobs_state[relna_job_id]['gcloud_id']
            )
        )
        data.append(job_dict)

    return render_template('imitation_learning.html', jobs=data)

@app.route('/ship_trainer', methods=['GET', 'POST'])
def ship_trainer(
        trainer_folder_name='imitation_learning',
        data_file_name='RoboschoolHumanoid-v1.pkl',
        job_id=5
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
    1. download trainer package from postgresql
    2. upload trainer package as bytes to GCS
    3. submit job to Google Cloud with address to trainer package
    """
    print(request)
    shipping_id = str(job_id)+"__"+str(uuid.uuid4())
    job_name = ("relna_"+trainer_folder_name+"__"+str(shipping_id)).replace('-','_')
    print("[relna:ship_trainer] generated job {}".format(job_name))

    #####
    # get trainer from postgre
    # upload trainer to GCS
    #####
    pkg_destination_folder = os.path.join("pkgs",job_name)
    trainer_package_address = os.path.join(pkg_destination_folder,
                "trainer-0.1.tar.gz")

    #this is a <memoryview> object
    trainer_pkg = relna.db.get_imitation_learning_job_pkg(job_id)
    trainer_pkg_bytes = bytes(trainer_pkg)
    proxy = GCSproxy()
    proxy.gcs_write_bytes(trainer_pkg_bytes, 
            os.path.join("trainers", trainer_package_address))

    #####
    # submit job to GC ML
    #####
    wrapper = job_wrapper(
            job_name,
            trainer_package_address = trainer_package_address,
            train_files = "gs://relna-mlengine/data/"+data_file_name,
            eval_files = "gs://relna-mlengine/data/"+data_file_name
            )
    wrapper.submit()
    logging.warning("[relna:ship_trainer] submitted job {}".format(
        job_name))

    return '[relna:ship_trainer] trainer shipped succesfully'

@app.route('/fork', methods=['POST'])
def fork():
    """
    POST
    args: trainerID (int)
    """
    print(request.values)
    zipped_code = relna.db.get_imitation_learning_job_code(
            request.values['trainerID'])
    zipped_code_bytes = bytes(zipped_code)
    return zipped_code_bytes

@app.route('/ship', methods=['POST'])
def ship():
    """
    POST
    """
    logging.warning("relna:main:ship - recieved ship request")
    print(request.values)
    zipped_code_binary = bytes(request.values['zipped_code_binary'], 'utf8')
    trainer_pkg_binary = bytes(request.values['trainer_pkg_binary'], 'utf8')
    python_model = request.values['python_model']
    gym = request.values['gym']
    expert_policy = request.values['expert_policy']

    query_result = relna.db.insert_imitation_learning_job_bytes(
            gym,
            expert_policy,
            python_model,
            zipped_code_binary,
            trainer_pkg_binary
            )
    logging.warning("relna:main:ship - ship request executed")
    return "ship request executed"

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
