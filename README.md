# Triggering Cloud Function via Pub/Sub to store data in FireStore

Purpose - Sample project to trigger cloud function from pub/sub message and insert data into Firestore. Sample data is collected from http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/mondial/mondial-3.0.xml

Developer - K.Janarthanan

![alt text](https://github.com/kujalk/CF_To_FireStore/blob/main/Diagram/Architecture.png)

# Notes

1. New collection is created everytime with "country*{date}*{randomstring}" format

2. Data is inserted in batch wise to the above collection

# Method

## 1.A) To run locally

1. Create a Service account with Firebase.admin role and download it's key and use the script with in Local_Function/main.py

2. Update the JSON key location with in the Code.py

## 2.A) To run as Cloud Function

Use below commands,

gcloud auth login

gcloud projects list

gcloud config set project {project name}

gcloud pubsub topics create fetch-country-topic

gcloud pubsub topics list --filter="fetch-country-topic"

gcloud iam service-accounts create firestore-cf-access --display-name="Firestore access from CloudFunction to store country list"

gcloud iam service-accounts list --filter="Firestore access from CloudFunction to store country list"

gcloud projects add-iam-policy-binding {project name} --member='serviceAccount:{service account email from above output}' --role='roles/firebase.admin'

cd Upload_Function

gcloud functions deploy fetch-country-cf --gen2 --entry-point="main" --allow-unauthenticated --run-service-account={service account email} --runtime=python39 --source . --timeout 600 --trigger-topic fetch-country-topic --region asia-southeast1

gcloud pubsub topics publish fetch-country-topic --message 'MyMessage'
