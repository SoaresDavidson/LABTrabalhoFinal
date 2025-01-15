import requests
class Download:
    def baixar(link):
        resposta = requests.get(link)
        if resposta.status_code == 200:
            with open ('imagemBaixada.jpg', 'wb') as arqv:
                arqv.write(resposta.content)
                print ("Imagem baixada pai!")
        else:
            print('o download nÃ£o foi realizado.')
        
if __name__ == '__main__':
   url = input("Digite o link da imagem que deseja baixar: ")
   Download.baixar(url)
   