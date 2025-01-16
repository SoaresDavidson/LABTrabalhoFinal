from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from modules import imagem, download, Filtros
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import requests
import uuid
import os


class Filtro:
    def aplicar(self, imagem):
        pass

class EscalaCinza(Filtro):
    def aplicar(imagem):
        return imagem.convert("L")

class PretoBranco(Filtro):
    def aplicar(self, imagem):
        imagemcinza = imagem.convert("L")
        limiar = 128
        return imagemcinza.point(lambda p: 255 if p > limiar else 0)

class Cartoon(Filtro):
    def aplicar(self, imagem):
        imagemCinza = imagem.convert("L")
        imagemSuavizada = imagemCinza.filter(ImageFilter.SMOOTH_MORE)
        bordas = imagem.filter(ImageFilter.FIND_EDGES)
        imagemCartoon = Image.blend(imagemSuavizada.convert("RGB"), bordas.convert("RGB"), alpha=0.3) 
        imagemCartoon = ImageEnhance.Contrast(imagemCartoon).enhance(1.5)  
        imagemCartoon = ImageEnhance.Brightness(imagemCartoon).enhance(1.2) 
        return imagemCartoon

class FotoNegativa(Filtro):
    def aplicar(imagem):
        return ImageOps.invert(imagem)

class Contorno(Filtro):
    def aplicar(imagem):
        return imagem.filter(ImageFilter.CONTOUR)

class Blurred(Filtro):
    def aplicar(imagem):
        return imagem.filter(ImageFilter.BLUR)


app = Flask(__name__)

class Download:
    def baixar(self, link):
        resposta = requests.get(link)
        if resposta.status_code == 200:
            with open (link, 'wb') as arqv:
                arqv.write(resposta.content)
                return arqv

        else:
            return False

# Configure the upload folder
#UPLOAD_FOLDER = 'static/uploads'
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        user_id = session['user_id']
        upload_folder = f'uploads/{user_id}'
        os.makedirs(upload_folder, exist_ok=True)
        # Check if an image file is uploaded
        url = request.form.get('link')
        imagem = request.files['imagem']
        if not imagem and not url:
            return "Nenhuma imagem foi provida", 400
        if imagem and imagem.filename == '':
            return "No selected file", 400
        elif imagem:
            filename = secure_filename(imagem.filename)
        else:
            download = Download()
            res = download.baixar(url)
            if res == False: return "URL is not valid"
            imagem = download
            filename = url
        opcao = request.form['opcao']
        if opcao == 'escala':
            imagem = EscalaCinza.aplicar(imagem=imagem)
        elif opcao == 'pretobranco':
            imagem = PretoBranco.aplicar(imagem=imagem)
        elif opcao == 'cartoon':
            imagem = Cartoon.aplicar(imagem=imagem)
        elif opcao == 'negativa':
            imagem = FotoNegativa.aplicar(imagem=imagem)
        elif opcao == 'contorno':
            imagem = Contorno.aplicar(imagem=imagem)
        else:
            imagem = Blurred.aplicar(imagem=imagem)
        image_path = os.path.join(upload_folder, filename + opcao)
        imagem.save(image_path)
 
        # Save the uploaded file
        #file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
        #imagem.save(file_path)
        # Pass the file path to the template
        return render_template("imagem.html", imagem=image_path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
