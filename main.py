from modules import imagem,download,Filtros
from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def home():
    if request.method == "POST":
        imagem = "static/imagem.jpeg"
        return render_template("imagem.html",imagem=imagem)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)