# Deployment to CLoudrun 

gcloud run deploy / 
--no-allow-unauthenticated /
--region us-central1 /
--set-env-vars [BUCKET_NAME=gem-vison-cr-app-upload] /
--source .
