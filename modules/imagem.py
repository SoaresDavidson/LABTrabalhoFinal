from PIL import Image

class imagem:
    def __init__(self, img):
        if isinstance(img,str):
            self.__img = Image.open(img)
        else:
            self.__img = img
            

    def mostarImagem(self):
        self.__img.show()
    
    def retornaImagem(self):
        return self.__img

if __name__ == "__main__":
    p = imagem("/home/davi/Imagens/Wallpapers/mistborn.jpeg")
    p.mostarImagem()