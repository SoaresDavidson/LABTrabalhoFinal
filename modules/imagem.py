from PIL import Image
class Imagem:
    def __init__(self, img):
        if isinstance(img,str):
            self.__img = Image.open(img)
        else:
            self.__img = img
            
    def mostrarImagem(self):
        self.__img.show()
    
    def retornaImagem(self):
        return self.__img
    
    def salvarImagem(self,nome,caminho=""):
        newImg = caminho + nome
        self.__img.save(newImg)
    
    def __getattr__(self, name):
        return getattr(self.__img ,name)

        

if __name__ == "__main__":
    p = Imagem("/home/davi/Imagens/Wallpapers/mistborn.jpeg")
    p.salvarImagem("imagemd.jpeg","uploads/")

