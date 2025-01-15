from modules import imagem, download, Filtros
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Check if an image file is uploaded
        if 'imagem' not in request.files:
            return "No file part", 400

        imagem = request.files['imagem']
        if imagem.filename == '':
            return "No selected file", 400

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
        imagem.save(file_path)

        # Pass the file path to the template
        return render_template("imagem.html", imagem=file_path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
