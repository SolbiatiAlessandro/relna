import utils
import os
import logging

def prepare_payload(
        trainer_folder_name,
        payload_folder_name="payload"
        ):
    """
    zip python code and build package
    """
    logging.warning("relna:client:prepare_payload: preparing payload from {} to {}".format(trainer_folder_name, payload_folder_name))
    try: os.mkdir(payload_folder_name)
    except: pass
    utils.zip_trainer(
            trainer_folder_name,
            zip_name=os.path.join(payload_folder_name, "trainer.zip"))
    utils.build_package(
            trainer_folder_name,
            package_name=payload_folder_name)
    logging.warning("relna:client:prepare_payload: payload prepared succesfully at  {}".format(payload_folder_name))
