# Deployment to CLoudrun 

cd ~/gemini-experiments/another_app_example

gcloud run deploy vision-coke-backend \
--region=us-central1 \
--no-allow-unauthenticated \
--source . \
--set-env-vars=BUCKET_NAME=gem-vison-cr-app-upload

#Sample Post Command 

cd ~/gemini-experiments/another_app_example/images

curl -X POST -F "file=@./coke.jpg" https://vision-coke-backend-ztskssd4ra-uc.a.run.app/upload_image -H "Authorization: Bearer $(gcloud auth print-identity-token)" 

curl -X POST -F "file=@./Selfie_David.JPG" https://vision-coke-backend-ztskssd4ra-uc.a.run.app/upload_image -H "Authorization: Bearer $(gcloud auth print-identity-token)" 

pip install -r requirements.txt 
export BUCKET_NAME="gem-vison-cr-app-upload"
export FLASK_APP="main"

