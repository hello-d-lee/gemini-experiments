import os
from flask import Flask, request, Response, g, render_template, jsonify
import marko
from vertexai.preview.generative_models import GenerativeModel, Part
import base64


app = Flask(__name__)
app.debug = True

config = {
  'temperature': 0,
  'top_k': 20,
  'top_p': 0.9,
  'max_output_tokens': 500
}

model = GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=config)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("chat.html")

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_image' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['user_image']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        image_data = file.read()
        image_parts = [
            {
                "mime_type": file.content_type,
                "data": image_data
            },
        ]

        prompt_parts = [
            "You are Sheldon Cooper. User will upload an image. Based on the image, you have to come up with a Sheldon Cooper style fun fact. Also give a funny, sarcastic note about the image. \n\nUser's image:\n\n",
            image_parts[0],
            "\n\nFun fact:\n",
        ]    

        response = model.generate_content(prompt_parts)

        return jsonify({
            "response": marko.convert(response.text)
        })
        
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))