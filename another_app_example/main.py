import os
from flask import Flask, request, g, render_template, jsonify
import marko
from vertexai.preview.generative_models import GenerativeModel, Part, Image
# from IPython.display import Markdown
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

# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

model = GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=config)

GCS_BUCKET_NAME = os.environ['BUCKET_NAME'] 
storage_client = storage.Client()

image_coke_regular_uri = "gs://{GCS_BUCKET_NAME}/Selfie_India_7.png"
image_coke_zero_uri = "gs://{GCS_BUCKET_NAME}/Selfie_India_16.png"
image_coke_diet_uri = "gs://{GCS_BUCKET_NAME}/Selfie_David.JPG"
image_coke_regular = Part.from_uri(image_coke_regular_uri, mime_type="image/png")
image_coke_zero = Part.from_uri(image_coke_zero_uri, mime_type="image/png")
image_coke_diet = Part.from_uri(image_coke_diet_uri, mime_type="image/jpeg")

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
        responses = model.generate_content(
        [f"""Look at the coke in this person's hand in this selfie {image_coke_regular}, The type of coke is Regular Coke which has a full red package and Coca-Cola logo in white color and usually comes with Original Taste text under it.""",
         f"""Look at the coke in this person's hand in this selfie {image_coke_zero}, The type of coke is Coke Zero which is a full red package and Coca-Cola logo in black color and usually comes with Zero Sugar text under it.""",
         f"""Look at the coke in this person's hand in this selfie {image_coke_diet}, The type of coke is Diet Coke which has a full silver package and Coca-Cola logo in red color and usually comes with Diet text above it.""",
         f"""Extract the type of coke of three options of Regular Coke, Coke Zero, and Diet Coke as mentioned above and emotion from {image} and output them in JSON.""", image]
        )
        print("generated model response") 
        return jsonify({
            "response": marko.convert(responses.text)  # Use aggregated text 
        })
        
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))