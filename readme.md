# relna -> Reinforcement Learning Arena

Relna is a platform to train Reinforcement Learning models and share them with other users, it's great for iterating quickily on different models and dataset in the Reinforcement Learning domain.

Similar platform out there are [Kaggle](www.kaggle.com) and [AICrowd](https://www.aicrowd.com/). [relna](https://relna-241818.appspot.com) is focused specifically on Deep Reinforcement Learning.

Some Deep Reinforcement Learning resources that can be used along side with [relna](https://relna-241818.appspot.com)
- [CS294 Berkley - Deep Reinforcement Learning](http://rll.berkeley.edu/deeprlcourse/)
- [Google Dopamine- research framework for fast prototyping of reinforcement learning algorithms](https://github.com/google/dopamine)

## relna-docs

Relna is deployed with Google Cloud App Engine at [https://relna-241818.appspot.com](https://relna-241818.appspot.com)

Some useful GCP SDK commands

```
gcloud init # to initialize folder in the SDK

# you can't use dev_appserver since is doesn't support python3x (WTF?)
dev_appserver.py app.yaml 

# but you can run flask like
export FLASK_APP=main.py
flask run

# you need to create a app.yaml file with inside 'runtime: python37'
gcloud app deploy # to deploy
```

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
- [ ] Run tensorflow example from python
- [ ] Run imitation learning job from python

Integration
- [ ] Integrate Google App Engine and Google ML Engine
- [ ] Create command line upload-job features
- [ ] Train model from Google App
