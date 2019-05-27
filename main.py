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
import relna.db
from relna.tensorflow.trainers.utils import jobAPIwrapper as job_wrapper

from flask import Flask, render_template, request

# [START create_app]
app = Flask(__name__)
# [END create_app]


@app.route('/')
def index():
    imitation_learning_jobs = relna.db.get_imitation_learning_jobs()
    return render_template('index.html', 
            len_imitation_learning_jobs=len(imitation_learning_jobs))

@app.route('/imitation_learning/')
def imitation_learning():
    # look for jobs

    # later jobs will be first put inside DB and then queried
    # jobs = relna.db.get_imitation_learning_jobs()
    jobs = job_wrapper.list()
    return render_template('imitation_learning.html', jobs=jobs)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
