from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from modules import imagem, download, Filtros
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import requests
import uuid
import os
import io  # Para trabalhar com fluxos de bytes

class Filtro:
    def aplicar(self, imagem):
        pass

class EscalaCinza(Filtro):
    def aplicar(self, imagem):
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
    def aplicar(self, imagem):
        return ImageOps.invert(imagem)

class Contorno(Filtro):
    def aplicar(self, imagem):
        return imagem.filter(ImageFilter.CONTOUR)

class Blurred(Filtro):
    def aplicar(self, imagem):
        return imagem.filter(ImageFilter.BLUR)

# Flask setup
app = Flask(__name__)

app.secret_key = 'vitinhoseulindo'

class Download:
    def baixar(self, link):
        resposta = requests.get(link)
        if resposta.status_code == 200:
            # Aqui, transformamos o conteúdo da resposta (bytes) em uma imagem
            img = Image.open(io.BytesIO(resposta.content))  # Abre a imagem usando os bytes
            return img
        else:
            return False

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        user_id = session['user_id']
        
        # Cria o diretório onde a imagem será salva
        upload_folder = f'static/uploads/{user_id}'
        os.makedirs(upload_folder, exist_ok=True)
        
        # Obtenha a URL ou arquivo enviado
        url = request.form.get('link')
        imagem = request.files['imagem']
        
        if not imagem and not url:
            return "Nenhuma imagem foi provida", 400
        
        if imagem and imagem.filename == '':
            return "No selected file", 400
        
        elif imagem:
            filename = secure_filename(imagem.filename)
            imagem = Image.open(imagem)  # Abrindo a imagem enviada diretamente pelo formulário
        else:
            download = Download()
            imagem = download.baixar(url)  # Baixando e abrindo a imagem
            if imagem == False: 
                return "URL is not valid"
            filename = os.path.basename(url)
        
        # Aplica o filtro escolhido
        opcao = request.form['opcao']
        if opcao == 'escala':
            imagem = EscalaCinza().aplicar(imagem)
        elif opcao == 'pretobranco':
            imagem = PretoBranco().aplicar(imagem)
        elif opcao == 'cartoon':
            imagem = Cartoon().aplicar(imagem)
        elif opcao == 'negativa':
            imagem = FotoNegativa().aplicar(imagem)
        elif opcao == 'contorno':
            imagem = Contorno().aplicar(imagem)
        else:
            imagem = Blurred().aplicar(imagem)
        
        # Garante que a imagem salva tenha a extensão correta
        image_path = os.path.join(upload_folder, f"{filename}_{opcao}.png")
        imagem.save(image_path)
        
        # Passa o caminho da imagem para o template
        return render_template("imagem.html", imagem=image_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
