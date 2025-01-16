from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from modules.Filtros import Filtro, EscalaCinza, PretoBranco, Cartoon, Blurred, Contorno, FotoNegativa
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import requests
import uuid
import os
import io

app = Flask(__name__)

app.secret_key = 'vitinhoseulindo'

class Download:
    def baixar(link):
        resposta = requests.get(link)
        conteudo_resposta = resposta.headers.get('Content-Type')
        if 'image' in conteudo_resposta:
            if resposta.status_code == 200:
                with open ('imagemBaixada.jpg', 'wb') as arqv:
                    arqv.write(resposta.content)
                    print ("Imagem baixada com sucesso!")
                    return arqv
            elif resposta.status_code == 404:
                print("O link fornecido não foi encontrado e o download não foi realizado.")
            elif resposta.status_code == 403:
                print("O link é de um conteúdo de acesso proibido.")
        else:
            print("O link fornecido não é uma imagem.")
        return False

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        user_id = session['user_id']
        try:
            upload_folder = os.path.join(os.getcwd(), 'static', 'uploads', user_id)
            os.makedirs(upload_folder, exist_ok=True)
        except: print("Erro ao criar diretório")
        # Check if an image file is uploaded
        url = request.form.get('link')
        imagem = request.files['imagem']
        if not imagem and not url:
            return "Nenhuma imagem foi provida", 400
        if imagem and imagem.filename == '':
            return "Nenhum arquivo selecionado", 400
        elif imagem:
            filename = secure_filename(imagem.filename)
            print(1)
        else:
            download = Download()
            res = download.baixar(url)
            if res == False: return "URL não é válida"
            imagem = res
            filename = imagem.filename
        ext = imagem.filename.split('.')[-1]
        if ext != 'jpeg' and ext != 'png':
            return f"Formato inválido (.{ext}). Por favor, envie arquivos '.jpeg' ou '.png'" 
        opcao = request.form['opcao']
        print(filename)
        #byte = imagem.read()
        #imagem = Image.open(io.BytesIO(byte)) 
        byte = imagem.read() if imagem else open(filename, 'rb').read()
        imagem = Image.open(io.BytesIO(byte))
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
        image_path = os.path.join(upload_folder, "Imagem_" + opcao + "." + ext)
        #print(image_path)
        imagem.save(image_path)
        path = os.path.join('uploads', user_id, 'Imagem_' + opcao + '.' + ext)
        print(path)
 
        # Save the uploaded file
        #file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
        #imagem.save(file_path)
        # Pass the file path to the template
        return render_template("imagem.html", imagem=path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
