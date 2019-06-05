import zipfile
import logging
import os
def zip_trainer(
        trainer_folder_name,
        TRAINER_FILES = [
            'README.md',
            'setup.py',
            'trainer/model.py',
            'trainer/task.py'
            ]
        ):
    """
    a trainer must have

    - README.md
    - setup.py
    - trainer/
        - model.py
        - task.py
    """
    zip_name = "trainer.zip"
    logging.warning("relna:utils:zip_trainer: writing zipfile to {}".format(zip_name))
    zf = zipfile.ZipFile(zip_name, mode='w')
    for filename in TRAINER_FILES:
        zf.write(os.path.join(trainer_folder_name, filename),
                arcname=filename)
    zf.close()

def unzip_trainer(
        zipped_trainer_filename="trainer.zip", 
        destination_dir="./unzipped_trainer"):
    logging.warning("relna:utils:unzip_trainer: unzip trainer from {} to {}".format(
                zipped_trainer_filename, destination_dir))
    zip_ref = zipfile.ZipFile(zipped_trainer_filename, 'r')
    zip_ref.extractall(destination_dir)
    zip_ref.close()
