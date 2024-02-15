import os
from flask import Flask, request, g, render_template, jsonify
import marko
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from IPython.display import Markdown
import textwrap
import tempfile
from google.cloud import storage 


app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = "/images/"

config = {
  'temperature': 0,
  'top_k': 20,
  'top_p': 0.9,
  'max_output_tokens': 500
}

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

model = GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=config)

GCS_BUCKET_NAME = 'gemini-images-uploaded'  
storage_client = storage.Client()

def upload_to_gcs(temp_file, original_filename):  # Keep the filename parameter 
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    
    blob = bucket.blob(original_filename)
    blob.chunk_size = 1024 * 1024
    blob.upload_from_file(temp_file)
    
    print(f"Image uploaded successfully to gs://{GCS_BUCKET_NAME}/{original_filename}")

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('chat.html')

@app.route('/upload_image', methods=['GET','POST'])
def upload_image():           
        if 'file' not in request.files:
            return('No file part')
    
        file = request.files['file']

        upload_to_gcs(file, file.filename)

        # Construct GCS URI (using the original filename now)
        gcs_uri = f"gs://{GCS_BUCKET_NAME}/{file.filename}"
        
        # Prepare parts for Gemini 
        image = Part.from_uri(gcs_uri, mime_type="image/jpeg")
        print("created image part")
        prompt = """You need to analyze an input image which will show a person with a can of coke. 
            User will upload an image. Based on the image, identify the type of coke can (e.g. Coke Regular, Coke Zero and Diet Coke) and the emotion of the person in the picture. 
            The response should take the form of a JSON object with the following structure: 
            
            {"product": "Diet Coke", "emotion": "Happiness"}
            
            You should only return the JSON object and nothing else."""
        contents = [image, prompt]
        responses = model.generate_content(contents, stream=True)  
        print("generated model response") 
        full_response_text = ''  # Accumulate full output

        for chunk in responses:  # Iterate over generated chunks
            full_response_text += chunk.text  

        return jsonify({
            "response": marko.convert(full_response_text)  # Use aggregated text 
        })
        
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))