"""programmatically launch job to Google Cloud AI Platform"""
from googleapiclient import discovery


class APIwrapper():
    """
    wrapper for ml-engine python API library:
    https://cloud.google.com/ml-engine/docs/tensorflow/python-client-library
    """
    def __init__(
        self,
        job_name,
        train_files = "gs://relna-mlengine/data/adult.data.csv",
        eval_files = "gs://relna-mlengine/data/adult.data.csv",
        train_steps = "1000",
        eval_steps = "100",
        verbosity="DEBUG"
        ):
        training_inputs = {
            'packageUris': 'trainer/',
            'pythonModule': 'trainer.task',
            # args are the args that will be fed to trainer.task.__main__
             'args': [
                 '--train-files', train_files,
                 '--eval-files', eval_files,
                 '--train-steps', train_steps,
                 '--eval-setps', eval_steps,
                 '--verbosity', verbosity
                 ],
            'region': 'europe-west1',
            'jobDir': "gs://relna-mlengine/"+str(job_name),
            'runtimeVersion': '1.13',
            'pythonVersion': '3.5'}
        self.job_spec = {'jobId': job_name, 'trainingInput': training_inputs}

    def submit(self):
        """
        to run this locally you need to 
        export GOOGLE_APPLICATION_CREDENTIALS="/Users/alex/Desktop/Coding/AI/relna/gcpkey.json"
        """
        project_name = 'relna'
        project_id = 'projects/{}'.format(project_name)
        cloudml = discovery.build('ml', 'v1')
        request = cloudml.projects().jobs().create(body=self.job_spec,
                              parent=project_id)
        try:
            response = request.execute()
        except Exception as e:
            print("\n##### HTTP Error (from GCP ml-engine) in submitting job #####")
            
            print(e)

if __name__ == "__main__":
    # this currently have persmission problems if run locally
    jobs_wrapper = APIwrapper('census_test')
    jobs_wrapper.submit()
