from PIL import Image, ImageFilter, ImageOps, ImageEnhance

class Filtro:
    def aplicar(imagem):
        pass

class EscalaCinza(Filtro):
    def aplicar(imagem):
        return imagem.convert("L")

class PretoBranco(Filtro):
    def aplicar(imagem):
        imagemcinza = imagem.convert("L")
        limiar = 128
        return imagemcinza.point(lambda p: 255 if p > limiar else 0)

class Cartoon(Filtro):
    def aplicar(imagem):
        imagemCinza = imagem.convert("L")
        imagemSuavizada = imagemCinza.filter(ImageFilter.SMOOTH_MORE)
        bordas = imagem.filter(ImageFilter.FIND_EDGES)
        imagemCartoon = Image.blend(imagemSuavizada.convert("RGB"), bordas.convert("RGB"), alpha=0.3) 
        imagemCartoon = ImageEnhance.Contrast(imagemCartoon).enhance(1.5)  
        imagemCartoon = ImageEnhance.Brightness(imagemCartoon).enhance(1.2) 
        return imagemCartoon

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

