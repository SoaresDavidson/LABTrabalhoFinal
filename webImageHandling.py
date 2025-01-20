from werkzeug.utils import secure_filename
import os
from modules.imagem import Imagem
from PIL import Image
from modules.download import Download

def file_sended(uploaded_file, upload_folder:str) -> tuple[Imagem,str]:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(upload_folder,filename)
        uploaded_file.save(file_path)
        ext = ['.jpg', '.png', '.png', '.gif', '.bmp', '.heic', '.webp', '.jpeg']
        if not any(filename.lower().endswith(i) for i in ext): # verifica o final do nome dos arquivos de upload para ciencia da sua extensao
            raise ValueError
        try:
            imagem = Imagem(file_path) # Abrindo a imagem enviada diretamente pelo formulário
            
        except (IOError, SyntaxError): # A partir disto, é possível levantar exceções caso o arquivo não seja uma imagem, como na linha 72
            os.remove(file_path)
            raise ValueError
            
        
        return imagem, filename
        
            

def url_sended(url:str, upload_folder:str) -> tuple[Imagem,str]:
    download = Download()
    try:
        imagem = Imagem(download.baixar(url))
    except Image.UnidentifiedImageError: # verifica se o image.open lança uma excecao do tipo imagem indefinida, e lança uma excecao de valor
        raise ValueError
    
    filename = os.path.basename(url)
    imagem.salvarImagem(nome=filename,caminho=upload_folder+"/")
    return imagem, filename