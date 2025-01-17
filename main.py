from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from modules.Filtros import EscalaCinza,PretoBranco,Cartoon,Contorno,Blurred,FotoNegativa
from modules.imagem import Imagem
from modules.download import Download
import connection
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import requests
import uuid
import os
import io  # Para trabalhar com fluxos de bytes

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
        #imagem = request.files.get('imagem')
        uploaded_file = request.files['imagem']
        if not uploaded_file and not url:
            return render_template('error.html', mensagem="Nenhuma imagem foi provida")

        if uploaded_file and uploaded_file.filename == '':
            return render_template('error.html', mensagem="Arquivo não selecionado")
        
        elif uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(upload_folder, filename)
            uploaded_file.save(file_path)  # Save the uploaded file
            imagem = Image.open(file_path)  # Open the saved file # Abrindo a imagem enviada diretamente pelo formulário
            
        elif url:
            download = Download()
            imagem = download.baixar(url)  # Baixando e abrindo a imagem
            if imagem == False: 
                return render_template('error.html', mensagem="URL inválida")
            filename = os.path.basename(url)
        
        # Aplica o filtro escolhido
        opcao = request.form['opcao']
        imagem_processada = connection.aplicar_filtro(opcao=opcao,imagem=imagem)
        image_path = os.path.join(upload_folder, filename)
        imagem_processada.save(image_path)
        
        # Passa o caminho da imagem para o template
        return render_template("imagem.html", imagem=image_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
