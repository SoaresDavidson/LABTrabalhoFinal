import requests
from PIL import Image
import io

class Download:
    @staticmethod
    def baixar(link):
        resposta = requests.get(link)
        conteudo_resposta = resposta.headers.get('Content-Type')
        
        if 'image' in conteudo_resposta:
            if resposta.status_code == 200:
                # Abrir a imagem diretamente a partir dos bytes recebidos
                img = Image.open(io.BytesIO(resposta.content))  # Abre a imagem a partir do buffer de bytes
                return img
                # img.show()  # Exibe a imagem (opcional)
                # img.save('imagemBaixada.jpg')  # Salva a imagem
                print("Imagem baixada com sucesso!")
            elif resposta.status_code == 404:
                print("O link fornecido não foi encontrado e o download não foi realizado.")
            elif resposta.status_code == 403:
                print("O link é de um conteúdo de acesso proibido.")
        else:
            print("O link fornecido não é uma imagem.")

if __name__ == '__main__':
    url = input("Digite o link da imagem que deseja baixar: ")
    Download.baixar(url)
