
'''
Requirements:
pip install -r requirements.txt

Variables a declarar:
$env:FLASK_APP="app.py"
$env:FLASK_DEBUG=1
$env:FLASK_ENV="development"

https://bootstrap-flask.readthedocs.io/en/stable/basic/
https://getbootstrap.com/docs/5.2/components/buttons/
https://pandas.pydata.org/docs/user_guide/indexing.html
'''

import pandas as pd
import os
from distutils.log import debug
from flask import Flask, request, make_response, redirect, render_template, send_from_directory
from flask_bootstrap import Bootstrap5


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.update(
    DEBUG=True,
    ENV='development'
)
bootsrap = Bootstrap5(app)

tabla = pd.read_excel('data/data.xlsx', header=0)
ruts = tabla["Run propietario"].unique().tolist()

todos = ['Tema libre (ideal en el marco de su proyecto)',
        'Instale Flask en un ambiente virtual',
        'Acceda a algún conjunto de datos en formato .json (ejemplo en link adjunto referente a constitución), o cree sus datos usando diccionarios/listas de python (ejemplo adjunto en run.py app de programas presidenciales).',
        'Construya su aplicación con al menos dos ruteos además del ruteo a la página inicial "/". Total 3 ruteos.',
        'Rutee los tres patrones de URL, dos de los cuales deben incluir SLUGs a vistas que rendericen la información.',
        'Cree plantillas HTML, utilizando una base y tres adicionales, para mostrar la información de forma con una buena presentación gráfica.',
        'Utilice CSS en archivos estáticos para mejorar la visualización de su página. También puede usar una plantilla predefinida que incluya imágenes.',
        'Opcionalmente puede utilizar librerías .JScript para visualizar datos.',
        'Suba el código de su APP en su GitHub personal. Incluya un archivo ReadMe con su nombre y una breve descripción de su aplicación.']


@app.route('/')
def index():
    user_ip = request.remote_addr

    response =  make_response(redirect('/index'))
    response.set_cookie('user_ip', user_ip)

    return response

@app.route('/index')
def hello():
    user_ip = request.cookies.get('user_ip')
    
    context = {
        'user_ip':user_ip, 
        'todos':todos
    }

    return render_template('index.html', **context)

@app.route('/propietarios/')
def propietarios():
    return render_template('propietarios.html', tabla=tabla, ruts=ruts)

@app.route('/propietario/<string:rut>')
def propietario(rut):
    if rut in ruts:
        return render_template('propietario.html', tabla=tabla, rut=rut)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
    