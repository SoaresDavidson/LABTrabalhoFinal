from modules import imagem,Filtros

p = imagem.imagem("/home/davi/Imagens/Wallpapers/mistborn.jpeg")
#p.mostarImagem()
p2 = Filtros.EscalaCinza.aplicar(p.retornaImagem())
p3 = imagem.imagem(p2)
p3.mostarImagem()