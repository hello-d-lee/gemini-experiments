# Deployment to CLoudrun 

cd ~/gemini-experiments/another_app_example

#Deployment Command (Updated GCS Bucket)
gcloud run deploy vision-coke-backend \
--region=us-central1 \
--no-allow-unauthenticated \
--source . \
--set-env-vars=BUCKET_NAME=gem-vison-cr-app-upload

#Sample Post Command 

cd ~/gemini-experiments/another_app_example/images

#Test back end file upload
curl -X POST -F "file=@./coke.jpg" https://vision-coke-backend-ztskssd4ra-uc.a.run.app/upload_image -H "Authorization: Bearer $(gcloud auth print-identity-token)" 


#Local Testing
curl -X POST -F "file=@./coke.jpg" http:/127.0.0.1:5000/upload_image
curl -X POST -F "file=@./Selfie_David.JPG" https://vision-coke-backend-ztskssd4ra-uc.a.run.app/upload_image -H "Authorization: Bearer $(gcloud auth print-identity-token)" 

pip install -r requirements.txt 
export BUCKET_NAME="gem-vison-cr-app-upload"
export FLASK_APP="main"
gcloud auth print-identity-token

