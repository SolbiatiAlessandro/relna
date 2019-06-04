"""programmatically launch job to Google Cloud AI Platform"""
from googleapiclient import discovery
from google.cloud import storage
import os

class jobAPIwrapper():
    """
    wrapper for ml-engine python API library:
    https://cloud.google.com/ml-engine/docs/tensorflow/python-client-library
    """
    def __init__(
        self,
        job_name,
        trainer_package_address = "template/dist/trainer-0.1.tar.gz",
        train_files = "gs://relna-mlengine/data/trainer_template/adult.data.csv",
        eval_files = "gs://relna-mlengine/data/trainer_template/adult.data.csv",
        train_steps = "1000",
        eval_steps = "100",
        verbosity="DEBUG"
        ):
        """
        trainer_address will be uploaded to GCS
        the rest will be sent thorugh gc mlengine APIS
        """
        self.job_name = job_name
        self.trainer_package_address = trainer_package_address
        training_inputs = {
            'packageUris': os.path.join("gs://relna-mlengine/trainers", self.trainer_package_address),
            'pythonModule': 'trainer.task',
             # args are the args that will be fed to trainer.task.__main__
            'args': [
                 '--mode','prod-cloud',
                 '--input-files', train_files,
                 '--train-files', train_files,
                 '--eval-files', eval_files,
                 '--train-steps', train_steps,
                 '--eval-setps', eval_steps,
                 '--verbosity', verbosity,
                 '--cloud-job-dir', os.path.join('outputs/imitation_learning/',
                     job_name),
                 '--local-job-dir', os.path.join('/tmp/imitation_learning/',
                     job_name)
                 ],
            'region': 'europe-west1',
            'jobDir': "gs://relna-mlengine/outputs/"+str(job_name),
            'runtimeVersion': '1.13',
            'pythonVersion': '3.5'}
        self.job_spec = {'jobId': job_name, 'trainingInput': training_inputs}

    def upload_trainer(self):
        """
        trainer folder need to be on GCS
        """
        proxy = GCSproxy()
        proxy.gcs_write(self.trainer_package_address, "trainers/")
        print("[utils.py] APIwrapper: trainer uploaded succesfully")


    def submit(self):
        """
        to run this locally you need to 
        export GOOGLE_APPLICATION_CREDENTIALS="/Users/alex/Desktop/Coding/AI/relna/gcpkey.json"
        """
        print("[utils.py] APIwrapper: submitting job ({})".format(self.job_name))
        project_name = 'relna-241818'
        project_id = 'projects/{}'.format(project_name)
        cloudml = discovery.build('ml', 'v1')
        request = cloudml.projects().jobs().create(body=self.job_spec,
                              parent=project_id)
        self.upload_trainer()
        try:
            print("[utils.py] APIwrapper.submit: executing request..")
            response = request.execute()
            print("\n[utils.py] APIwrapper.submit: SUCCESS, job submitted")
            print(response)
            print("[utils.py] you can monitor jobs at https://console.cloud.google.com/mlengine/jobs?project=relna-241818")
        except Exception as e:
            print("\n##### HTTP Error (from GCP ml-engine) in submitting job #####")
            
            print(e)

    @staticmethod
    def list():
        print("[utils.py] APIwrapper: listing jobs")
        project_name = 'relna-241818'
        project_id = 'projects/{}'.format(project_name)
        cloudml = discovery.build('ml', 'v1')
        request = cloudml.projects().jobs().list(parent=project_id)
        try:
            print("[utils.py] APIwrapper.submit: executing request..")
            response = request.execute()
            print("\n[utils.py] APIwrapper.submit: SUCCESS, job listed")
            jobs = list(response.values())[0]
            return jobs
        except Exception as e:
            print("\n##### HTTP Error (from GCP ml-engine) in submitting job #####")
            print(e)
            return None

class GCSproxy():
    """basic proxy to handle gcs APIs"""

    def __init__(self):
        """
        since this will be used mainly from google app engine, if you want to run locally (only for testing!) you need to 
        export GOOGLE_APPLICATION_CREDENTIALS="/Users/alex/Desktop/Coding/AI/relna/gcpkey.json"
        """
        self.client = storage.Client()
        BUCKET_NAME = "relna-mlengine"
        self.bucket = self.client.get_bucket(BUCKET_NAME)

    def gcs_load(self, filename):
        """
        loads cards from gcs
        args:
            filename [cards.pkl, logs.csv]
        """
        print("[GCSproxy.gcs_load] interacting with Google Cloud Storage to retrieve data: {}".format(filename))
        blob = self.bucket.get_blob(filename)
        blob.download_to_filename(filename)

    def gcs_write(self, filename, prefix=""):
        """
        write cards to gcs
        args:
            filename [cards.pkl, logs.csv]
        """
        print("[GCSproxy.gcs_load] interacting with Google Cloud Storage to upload data: {}".format(filename))
        blob = self.bucket.blob(prefix+filename)
        blob.upload_from_filename(filename)

if __name__ == "__main__":
    # this currently have permissions problems if run locally

    ### this is for testing template, currently working
    # jobs_wrapper = jobAPIwrapper('census_test_from_relna_local_04')
    # jobs_wrapper.submit()

    ### this is for testing imitiation_learning
    jobs_wrapper = jobAPIwrapper(
           'imitation_learning_from_local_test_007',
            trainer_package_address = "imitation_learning/dist/trainer-0.1.tar.gz",
            train_files = "gs://relna-mlengine/data/RoboschoolHumanoid-v1.pkl",
            eval_files = "gs://relna-mlengine/data/RoboschoolHumanoid-v1.pkl",
            )
    jobs_wrapper.submit()
