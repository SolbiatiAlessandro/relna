import pickle as pkl
import argparse
import logging
from model import Model as ImitationTrainerModel
import uuid
import os
from GCSproxy import GCSproxy


def load_data(expert_data_filename, mode):
    """
    returns numpy arrays X, Y
    X.shape = (, 44)
    Y.shape = (, 17)
    """
    if type(expert_data_filename) == list:
        if len(expert_data_filename) > 1:
            raise NotImplemented("can just load from one file")
        expert_data_filename = expert_data_filename[0]
    if mode!="dev-local":
        proxy = GCSproxy(mode) 
        pkl_filename = proxy.gcs_load(expert_data_filename)
    else:
        pkl_filename = expert_data_filename

    expert_rollouts = pkl.load(open(pkl_filename,"rb"))  
    X = expert_rollouts['observations']
    Y = expert_rollouts['actions']
    assert len(X) == len(Y)
    return X, Y

def upload_model(source_model_dir, destination_model_dir, mode):
    """
    upload the whole model.ckpt. package (4 files)
    mode can be dev-cloud or prod-cloud, changes permission of GCSproxy
    """
    logging.warning("[task.py]:upload_model - uploading model from {} to {}".format(source_model_dir, destination_model_dir))
    proxy = GCSproxy(mode) 
    files = os.listdir(source_model_dir)
    for file in files:
        proxy.gcs_write(
            os.path.join(source_model_dir, file),
            os.path.join(destination_model_dir, file)
        )

def train_and_save(args):
    """
    routine for training and saving model

    note: to see how to predict look inside task.ipynb
    """
    X, Y = load_data(args.input_files, args.mode)
    model = ImitationTrainerModel()
    train_mse = model.train(
            X,
            Y, 
            steps=args.train_steps,
            batch_size=args.train_batch_size,
            save_folder=args.local_job_dir)

    # visualize mse
    if args.mode in ["dev-notebook"]:
        model.visualize_train_mse(train_mse)
    
    # test predictions (if model is being saved correctly)
    if args.mode in ["dev-local", "dev-cloud"]: 
        y = model.predict(X, save_folder=args.local_job_dir)
        score = model.evaluate_predictions(y, Y)
        logging.warning('[model.py]:predict - SUCCESS, score = {}'.format(score))
        
    if args.mode != "dev-local":
        upload_model(
                args.local_job_dir,
                args.cloud_job_dir,
                mode=args.mode)

if __name__=="__main__":
    job_id = uuid.uuid4()

    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--mode',
            type=str,
            help="1) dev-local 2) dev-cloud (triggers GCS) 3) prod-cloud",
            default="dev-local")
    parser.add_argument(
        '--input-files',
        nargs='+',
        help='Training files local or GCS',
        default="/Users/alex/Desktop/Coding/AI/CS294_DeepReinforcementLearning/homeworks/hw1/expert_data/RoboschoolHumanoid-v1.pkl")
    parser.add_argument(
        '--local-job-dir',
        type=str,
        help="""local dir for checkpoints, exports, and summaries.
          Use an existing directory to load a trained model, or a new directory
          to retrain""",
        default='/tmp/imitation-learning/'+str(job_id)+"/")
    parser.add_argument(
        '--cloud-job-dir',
        type=str,
        help="""GCS dir for checkpoints, exports, and summaries.
          Use an existing directory to load a trained model, or a new directory
          to retrain""",
        default='/outputs/imitation-learning/'+str(job_id)+"/")
    parser.add_argument(
        '--train-steps',
        type=int,
        help='Maximum number of training steps to perform.',
        default=3000)
    parser.add_argument(
        '--eval-steps',
        help="""Number of steps to run evalution for at each checkpoint.train_batch_size,
        If unspecified, will run for 1 full epoch over training data""",
        default=None,
        type=int)
    parser.add_argument(
        '--train-batch-size',
        type=int,
        default=40,
        help='Batch size for training steps')
    parser.add_argument(
        '--eval-batch-size',
        type=int,
        default=40,
        help='Batch size for evaluation steps')
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=0.003,
        help='Learning rate for SGD')


    args, _ = parser.parse_known_args()
    train_and_save(args)
