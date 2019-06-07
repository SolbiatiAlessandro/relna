# SHIP TRAINER

workflow

## 1. (relna-client) Prepare payload

1. zip trainer -> payload/trainer.zip
2. build package -> payload/trainer-01.tar.gz

## 2. (relna-client) Ship request

1. Open in memory trainer.zip and trainer-01.tar.gz
2. Send them over POST to relna server

## 3. (relna) /ship

1. Insert new relna-job in relna db
2. (gcloud_ship) upload trainer to GCS
3. (glcoud_job_shipper) submit job to Google Cloud AI PLatform:w
