from modules.imagem import Imagem
from modules.download import Download
import connection
import requests
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import uuid
import os
import zipfile
from io import BytesIO
import shutil

def file_sended(uploaded_file, upload_folder:str):
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(upload_folder, filename)
        uploaded_file.save(file_path)
        ext = ['.jpg', '.png', '.png', '.gif', '.bmp', '.heic', '.webp']
        if not any(filename.lower().endswith(i) for i in ext):
            raise ValueError
        try:
            imagem = Imagem(file_path) # Abrindo a imagem enviada diretamente pelo formulário
            
        except (IOError, SyntaxError): # A partir disto, é possível levantar exceções caso o arquivo não seja uma imagem, como na linha 72
            os.remove(file_path)
            raise ValueError
            
        
        return imagem, filename
        
            

def url_sended(url, upload_folder:str):
    download = Download()
    imagem = Imagem(download.baixar(url))
    
    
    
    filename = os.path.basename(url)
    imagem.salvarImagem(nome=filename,caminho=upload_folder+"/")
    return imagem, filename

def iniciar_sessão(seccao):
    if 'user_id' not in seccao:
            seccao['user_id'] = str(uuid.uuid4())
    user_id = seccao['user_id']
    return user_id

def diretorio_unico(id_usuario) -> str:
    upload_folder = f'static/uploads/{id_usuario}'
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

app = Flask(__name__)

app.secret_key = 'vitinhoseulindo'
""""""
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
                imagem,filename = url_sended(url=url,upload_folder=upload_folder)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    return render_template('index.html', error_message="URL não encontrada")
                elif e.response.status_code == 403:
                    return render_template('index.html', error_message="URL de acesso proibido")
            except requests.exceptions.MissingSchema:
                return render_template('index.html', error_message="URL inválida")
            except AttributeError:
                return render_template('index.html', error_message="Ocorreu um erro de Atributte, verifique a URL")
            
            
            
                
                
                    
                  
            
        for opcao in ["escala", "pretoBranco", "cartoon", "negativa", "contorno", "blurred"]:
            imagem_processada = connection.aplicar_filtro(opcao=opcao,imagem=imagem)
            image_path = os.path.join(upload_folder, f'{opcao}-{filename}')
            imagem_processada.save(image_path)

        # Passa o caminho da imagem para o template
        return render_template("imagem.html", imagem=image_path)
    
    return render_template('index.html',placeholder=placeholder)


@app.route('/listar', methods=["GET","POST"])
def listar():
    # if 'user_id' not in session:
    #         session['user_id'] = str(uuid.uuid4())
    # user_id = session['user_id']
    user_id = iniciar_sessão(seccao=session)
        # Cria o diretório onde a imagem será salva
    # upload_folder = f'static/uploads/{user_id}'
    # os.makedirs(upload_folder, exist_ok=True)
    upload_folder = diretorio_unico(id_usuario=user_id)
    diretorio = os.listdir(upload_folder)
    imagens = []
    for imagem in diretorio:
        imagens.append(imagem)
    if len(imagens) == 0:
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
    button = request.form.get('save_button')
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
        
    if button == "save":
        # Itera sobre as opções e remove as imagens que não são do tipo selecionado
        for opcao in ['',"escala", "pretoBranco", "cartoon", "negativa", "contorno", "blurred"]:
            imagem_path = upload_folder + "/" + opcao + "-" + imagem_name
            if opcao=='':
                imagem_path = upload_folder + "/" + imagem_name
            print(f"{tipo} e {opcao}")
            if tipo == opcao:
                continue
            os.remove(imagem_path)
    return render_template('index.html')        
     
@app.route('/deletar', methods=["GET", "POST"])
def deletar():
    button = request.form.get('discard_button')
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
        
    if button == "descartar":
        # Itera sobre as opções e remove as imagens que não são do tipo selecionado
        for opcao in ['',"escala", "pretoBranco", "cartoon", "negativa", "contorno", "blurred"]:
            imagem_path = upload_folder + "/" + opcao + "-" + imagem_name
            if opcao=='':
                imagem_path = upload_folder + "/" + imagem_name
            print(f"{tipo} e {opcao}")
            os.remove(imagem_path)
    return render_template('index.html')         

      
@app.route('/download', methods=["POST"])
def download():
    user_id = iniciar_sessão(seccao=session)
    upload_folder = diretorio_unico(user_id) # Caminho do diretório onde as imagens estão armazenadas
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
