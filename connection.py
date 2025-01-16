from modules.Filtros import EscalaCinza,PretoBranco,Cartoon,Contorno,FotoNegativa,Blurred
from modules.imagem import Imagem
import PIL

opcoes = {"escala":EscalaCinza(), 
          "pretoBranco":PretoBranco(), 
          "cartoon":Cartoon(),
          "negativa":FotoNegativa(),
          "contorno":Contorno(),
          "blurred":Blurred()
        }

def aplicar_filtro(opcao:str,imagem:Imagem):
    if opcao in opcoes:
        filtro = opcoes[opcao]
        return filtro.aplicar(imagem=imagem)
    else:
        raise ValueError(f"Filtro '{opcao}' não encontrado. Opções disponíveis: {list(opcoes.keys())}")
    
def baixar_imagem(url):
    pass

if __name__ == "__main__":
    imagem = PIL.Image.open("/home/davi/Imagens/Wallpapers/mistborn.jpeg")
    aplicar_filtro("escala",imagem).show()