from modules.imagem import Imagem
from modules.download import Download
import connection
from webImageHandling import file_sended,url_sended
import requests
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import uuid
import os
import zipfile
from io import BytesIO
import shutil

def iniciar_sessão(seccao): 
    if 'user_id' not in seccao:
            seccao['user_id'] = str(uuid.uuid4())
    user_id = seccao['user_id']
    return user_id

def diretorio_unico(id_usuario:str) -> str:
    upload_folder = f'static/uploads/{id_usuario}'
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder


def listar_diretorio(path: str) -> list[str]:
    if not os.path.exists(path):
        return []
    return os.listdir(path)

app = Flask(__name__)

app.secret_key = 'vitinhoseulindo'

@app.route('/', methods=["GET", "POST"])
def home():
    placeholder = ""
    if request.method == "POST":
        user_id = iniciar_sessão(seccao=session)
        upload_folder = diretorio_unico(id_usuario=user_id) # Cria o diretório onde a imagem será salva

        submit_type = request.form.get("submit_type")
        if submit_type == "file":
            uploaded_file = request.files['imagem']
            
            if not uploaded_file:
                return render_template('index.html', error_message="Nenhuma Arquivo foi provido")

            if uploaded_file and uploaded_file.filename == '':
                return render_template('index.html', error_message="Arquivo não selecionado")
            
            try:
                imagem,filename = file_sended(uploaded_file=uploaded_file, upload_folder=upload_folder)
            except Exception:
                return render_template('index.html', error_message="Arquivo não é uma imagem ou não possui extensão suportada")
            
            
                
            
            

        elif submit_type == "url":
            try:
                url = request.form.get('link')  # Obtenha a URL ou arquivo enviado
                imagem,filename = url_sended(url=url,upload_folder=upload_folder) # aqui, a funcao que lança a excecao de valor é usada e funciona com seus excepts especificos
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    return render_template('index.html', error_message="URL não encontrada")
                elif e.response.status_code == 403:
                    return render_template('index.html', error_message="URL de acesso proibido")
            except requests.exceptions.MissingSchema:
                return render_template('index.html', error_message="URL inválida")
            except AttributeError:
                return render_template('index.html', error_message="Ocorreu um erro de Atributte, verifique a URL")
            except ValueError:
                return render_template('index.html', error_message="Imagem indefinida ou protegida, verifique a URL")
            
            
            
                
        for opcao in ["escala", "pretoBranco", "cartoon", "negativa", "contorno", "blurred"]:
            imagem_processada = connection.aplicar_filtro(opcao=opcao,imagem=imagem)
            image_path = os.path.join(upload_folder, f'{opcao}-{filename}')
            imagem_processada.save(image_path)

        # Passa o caminho da imagem para o template
        return render_template("imagem.html", imagem=image_path)
    
    return render_template('index.html',placeholder=placeholder)


@app.route('/listar', methods=["GET","POST"])
def listar():
    user_id = iniciar_sessão(seccao=session)
    upload_folder = diretorio_unico(id_usuario=user_id)
    imagens = listar_diretorio(upload_folder)
    if not imagens:
        return render_template("diretoriovazio.html")
    return render_template("lista.html", imagens=imagens)

@app.route('/escolha', methods=["POST"])
def escolha():
    imagem = request.form.get('imagem')
    imagem_name = imagem.split('-')[0]  # Extract only the image name
    return render_template("imagem.html", imagem=imagem_name)  # Pass the image name to the template

@app.route('/salvar', methods=["GET", "POST"])
def salvar():
    # Verifica se o botão foi pressionado
    button = request.form.get('discard_save_button')
    imagem = request.form.get('imagem')
    arquivo = os.path.basename(imagem)
    #return render_template('error.html', mensagem="URL inválida")
    if imagem is None:
        return "Imagem não foi enviada", 400  # Retorna erro se imagem não foi fornecida
    
    print(arquivo)
    tipo, imagem_name = arquivo.split('-', 1)
    print(imagem_name)

    user_id = session.get("user_id")  # Certifique-se de que session["user_id"] existe
    if not user_id:
        return "Usuário não autenticado", 403  # Se o usuário não estiver logado
    
    upload_folder = f'static/uploads/{user_id}'
        
    # if button == "save":
    # Itera sobre as opções e remove as imagens que não são do tipo selecionado
    for opcao in ['',"escala", "pretoBranco", "cartoon", "negativa", "contorno", "blurred"]:
        imagem_path = upload_folder + "/" + opcao + "-" + imagem_name
        if opcao=='':
            imagem_path = upload_folder + "/" + imagem_name
        print(f"{tipo} e {opcao}")
        if tipo == opcao and button == "save":
            continue
        if opcao == '' and button == "descartar":
            imagem_path = upload_folder + "/" + imagem_name
        os.remove(imagem_path)
    return render_template('index.html')           

      
@app.route('/download', methods=["POST"])
def download():
    user_id = iniciar_sessão(seccao=session)
    upload_folder = diretorio_unico(user_id) # Caminho do diretório onde as imagens estão armazenadas
    imagens = listar_diretorio(upload_folder)
    
    # Criação do arquivo zip em memória
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for imagem in imagens:
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
