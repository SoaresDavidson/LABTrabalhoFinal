import requests
from PIL import Image
import io

class Download:
    @staticmethod
    def baixar(link):
        resposta = requests.get(link)
        if resposta.status_code == 200:
                # Abrir a imagem diretamente a partir dos bytes recebidos
                img = Image.open(io.BytesIO(resposta.content))  # Abre a imagem a partir do buffer de bytes
                return img
                # img.show()  # Exibe a imagem (opcional)
                # img.save('imagemBaixada.jpg')  # Salva a imagem
                #print("Imagem baixada com sucesso!")
           
        
          


    
