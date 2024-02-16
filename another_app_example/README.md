# Deployment to CLoudrun 

cd ~/gemini-experiments/another_app_example

gcloud run deploy vision-coke-backend \
--region=us-central1 \
--no-allow-unauthenticated \
--source . \
--set-env-vars=[BUCKET_NAME=gem-vison-cr-app-upload]
