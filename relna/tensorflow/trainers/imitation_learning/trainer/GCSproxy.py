import os
from google.cloud import storage

class GCSproxy():
    """basic proxy to handle gcs APIs"""

    def __init__(self, mode="prod-cloud"):
        if mode != "prod-cloud": # means I am testing GCS from local machine and not from mlengine: dev-cloud
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../../../../../gcpkey.json'
        self.client = storage.Client()
        BUCKET_NAME = "relna-mlengine"
        self.bucket = self.client.get_bucket(BUCKET_NAME)

    def gcs_load(self, filename):
        """
        loads cards from gcs
        args:
            filename [cards.pkl, logs.csv]

        need key in ../gcskey.json
        
        returns: name of the file object was saved to
        """
        print("[GCSproxy.gcs_load] interacting with Google Cloud Storage to retrieve data: {}".format(filename))
        blob = self.bucket.get_blob(filename)
        
        clean_filename = filename[-filename[::-1].find('/')] 
        # this clean file name like asd/asd/asd.asd -> asd.asd
        # to be saved locally
        # otherwise rase error "no directory like asd" in the next line
        blob.download_to_filename(clean_filename)
        return clean_filename

    def gcs_write(self, source_file_name, destination_file_name):
        """
        write cards to gcs
        args:
            filename [cards.pkl, logs.csv]

        need key in ../gcskey.json
        """
        print("[GCSproxy.gcs_load] interacting with Google Cloud Storage to upload data: {}".format(source_file_name))
        blob = self.bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_name)
        