# relna -> Reinforcement Learning Arena

Relna is a platform to train Reinforcement Learning models and share them with other users, it's great for iterating quickily on different models and dataset in the Reinforcement Learning domain.

Similar platform out there are [Kaggle](www.kaggle.com) and [AICrowd](https://www.aicrowd.com/). [relna](https://relna-241818.appspot.com) is focused specifically on Deep Reinforcement Learning.

Some Deep Reinforcement Learning resources that can be used along side with [relna](https://relna-241818.appspot.com)
- [CS294 Berkley - Deep Reinforcement Learning](http://rll.berkeley.edu/deeprlcourse/)
- [Google Dopamine - research framework for fast prototyping of reinforcement learning algorithms](https://github.com/google/dopamine)
- [DeepTraffic - Deep Reinfrocement Learning competition](https://github.com/lexfridman/deeptraffic)

## relna-concepts

The value proposition of **relna** is to simplify the process of development and training of Deep Reinforcement Learning models, in an educational perspective. **relna** is not for research, but for learning and experiments.

The fundamental use-case for  **relna** is to be able to select any of the available gyms (virtually all the major ones available), upload just the minimal code necessary to describe your Reinforcemnt Learning agent and evaluate your model. 

How is this value proposition important?

1. Abstracting away any complexity regarding the implementation of Deep Reinforcemnt Learning algorithms
2. Abstracting away any complexity related to training infrastructure (relna uses Google Cloud AI Platform on the back-end to train models)
3. Benchmarking and comparing high number of models uploaded by high number of users, all using the same environment and infrastructure.

How is this value proposition implemented?

This is a proposed UX flow.
1. Landing
2. Select RL Domain (e.g. Imitation Learning)
3. Select Gym and other stuff (e.g. expert policy)
4. Upload code (ideally <100 lines) and Submit Training
5. Compare and rank result with other models

Under the hood **relna** (a *Google App Engine* instance) will collect all the information and build a python package and submit it to *Google AI Platform* for training. The python package (aka **trainers**) are standard templates for differents RL domains/gyms. Once the jon is finished **relna** ranks all the models and provide tool for training examination and model comparison.

## relna-docs

Relna is deployed with Google Cloud App Engine at [https://relna-241818.appspot.com](https://relna-241818.appspot.com)

Some useful GCP SDK commands

``` gcloud init # to initialize folder in the SDK

# you can't use dev_appserver since is doesn't support python3x (WTF?)
dev_appserver.py app.yaml 

# but you can run flask like
(fish) set -g -x FLASK_APP main.py
(bash) export FLASK_APP=main.py
flask run

# you need to create a app.yaml file with inside 'runtime: python37'
gcloud app deploy # to deploy
gcloud beta app deploy --verbosity=info
```
FIX: lib has 15k files in it, I can't deploy it. You can put in the yaml stuff like libraries: , should have a look later

The app runs a Google Cloud SQL database at 104.199.68.166

```
gcloud sql connect relna --user=postgres # connects with gcloud
gcloud sql instances describe relna # get info
# connect with psql (you need to whitelist your IP address in sql > instance > connections)
psql "sslmode=disable dbname=postgres user=postgres hostaddr=104.199.68.166" 
```

The app triggers jobs on Google Cloud AI Platform (ex Google Cloud ML Engine).
The best docs /w code examples I found so far are [in this repo](https://github.com/GoogleCloudPlatform/cloudml-samples/tree/master/census).

## Iteration I

Google App Engine
- [X] Create Google App Engine
- [X] Run flask
- [x] Create navigation features
- [X] Create model list page

Google ML Engine
- [X] Create Google ML Engine instance
- [X] Run tensorflow example from gcloud
- [X] Run tensorflow example from python
- [ ] Create trainer for imitation learning job

Integration
- [X] Integrate Google App Engine and Google ML Engine
- [ ] Create trainer shipping interface for template trainer
- [ ] Create command line upload-job features
- [ ] Create trainer shipping interface for imitation_learning trainer
