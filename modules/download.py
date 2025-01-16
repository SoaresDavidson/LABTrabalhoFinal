import requests
class Download:
    def baixar(link):
        resposta = requests.get(link)
        conteudo_resposta = resposta.headers.get('Content-Type')
        if 'image' in conteudo_resposta:
            if resposta.status_code == 200:
                with open ('imagemBaixada.jpg', 'wb') as arqv:
                    arqv.write(resposta.content)
                    print ("Imagem baixada com sucesso!")
            elif resposta.status_code == 404:
                print("O link fornecido não foi encontrado e o download não foi realizado.")
            elif resposta.status_code == 403:
                print("O link é de um conteúdo de acesso proibido.")
        else:
            print("O link fornecido não é uma imagem.")
        
        
if __name__ == '__main__':
   url = input("Digite o link da imagem que deseja baixar: ")
   Download.baixar(url)
   
   