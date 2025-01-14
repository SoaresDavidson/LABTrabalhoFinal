from PIL import ImageFilter, ImageOps

class Filtro:
    def aplicar(self, imagem):
        pass

class EscalaCinza(Filtro):
    def aplicar(imagem):
        return imagem.convert("L")

class PretoBranco(Filtro):
    def aplicar(imagem):
        return imagem.convert("1")

class Cartoon(Filtro):
    def aplicar(imagem):
        return imagem.filter(ImageFilter.FIND_EDGES)

class FotoNegativa(Filtro):
    def aplicar(imagem):
        return ImageOps.invert(imagem)

class Contorno(Filtro):
    def aplicar(imagem):
        return imagem.filter(ImageFilter.CONTOUR)

class Blurred(Filtro):
    def aplicar(imagem):
        return imagem.filter(ImageFilter.BLUR)

# Usar from PIL import Image
# Usar Image.open("caminho") para instanciar uma imagem
# Instanciar o filtro desejado igualando uma variável a função do filtro
# Usar instancia do filtro.aplicar na imagem

if __name__ == "__main__":
    import PIL.Image
    import PIL

    imagem = PIL.Image.open("/home/davi/Imagens/Wallpapers/mistborn.jpeg")
    EscalaCinza.aplicar(imagem=imagem).show()
    PretoBranco.aplicar(imagem=imagem).show()
    Cartoon.aplicar(imagem=imagem).show()
    FotoNegativa.aplicar(imagem=imagem).show()
    Contorno.aplicar(imagem=imagem).show()
    Blurred.aplicar(imagem=imagem).show()

