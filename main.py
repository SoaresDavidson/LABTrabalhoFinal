from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from modules.Filtros import EscalaCinza,PretoBranco,Cartoon,Contorno,Blurred,FotoNegativa
from modules.imagem import Imagem
from modules.download import Download
import connection
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import requests
import uuid
import os
import zipfile
import io  # Para trabalhar com fluxos de bytes
from io import BytesIO
import shutil

def file_sended(uploaded_file, upload_folder:str):
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(upload_folder, filename)
        uploaded_file.save(file_path)  # Save the uploaded file
        imagem = Imagem(file_path) # Abrindo a imagem enviada diretamente pelo formulário
        return imagem, filename

def url_sended(url):
    download = Download()
    imagem = Imagem(download.baixar(url))  # Baixando e abrindo a imagem
    if imagem == False: 
        return render_template('error.html', mensagem="URL inválida")
    filename = os.path.basename(url)
    return imagem, filename

app = Flask(__name__)

app.secret_key = 'vitinhoseulindo'

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        user_id = session['user_id']
        submit_type = request.form.get("submit_type")
        # Cria o diretório onde a imagem será salva
        upload_folder = f'static/uploads/{user_id}'
        os.makedirs(upload_folder, exist_ok=True)
    
        if submit_type == "file":
            uploaded_file = request.files['imagem']

            if not uploaded_file:
                return render_template('index.html', error_message="Nenhuma Arquivo foi provido")

            if uploaded_file and uploaded_file.filename == '':
                return render_template('index.html', error_message="Arquivo não selecionado")
            imagem,filename = file_sended(uploaded_file=uploaded_file, upload_folder=upload_folder)

        elif submit_type == "url":
            try:
                url = request.form.get('link')  # Obtenha a URL ou arquivo enviado
                imagem,filename = url_sended(url=url)
            except Exception:
                return render_template('index.html', error_message="URL inválida")    
        opcao = request.form['opcao']
        imagem_processada = connection.aplicar_filtro(opcao=opcao,imagem=imagem)
        image_path = os.path.join(upload_folder, filename)
        imagem_processada.save(image_path)
        
        # Passa o caminho da imagem para o template
        return render_template("imagem.html", imagem=image_path)
    
    return render_template('index.html')


@app.route('/listar', methods=["GET"])
def listar():
    if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
    user_id = session['user_id']
        # Cria o diretório onde a imagem será salva
    upload_folder = f'static/uploads/{user_id}'
    os.makedirs(upload_folder, exist_ok=True)
    diretorio = os.listdir(upload_folder)
    imagens = []
    for imagem in diretorio:
        imagens.append(imagem)
    if len(imagens) == 0:
        return render_template("diretoriovazio.html")
    return render_template("lista.html", imagens=imagens)

@app.route('/download', methods=["POST"])
def download():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    
    # Caminho do diretório onde as imagens estão armazenadas
    upload_folder = f'static/uploads/{user_id}'
    os.makedirs(upload_folder, exist_ok=True)
    diretorio = os.listdir(upload_folder)
    
    # Criação do arquivo zip em memória
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for imagem in diretorio:
            imagem_path = os.path.join(upload_folder, imagem)
            if os.path.exists(imagem_path):
                zipf.write(imagem_path, arcname=imagem)
            else:
                print(f"Imagem não encontrada: {imagem}")
    
    # Fazendo o buffer voltar ao início para ser lido e enviado
    zip_buffer.seek(0)

    shutil.rmtree(upload_folder)
    
    # Retorna o arquivo zip para o navegador
    return send_file(zip_buffer, as_attachment=True, download_name="imagens.zip", mimetype="application/zip")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


