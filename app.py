from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from db import get_db
import yagmail as yagmail
import utils
import os
from datos import listadatos
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/index')
def index():
    return render_template('new/index.html')

@app.route('/registro')
def registro():
    return render_template('new/registro.html')

@app.route('/registrarse', methods=['POST'])
def registrarse():
    try:
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        usuario = request.form['usuario']
        contrasena = request.form['clave']
        confirmar_contrasena = request.form['confirma-clave']
        isError = False

        if not nombre:
            error = "El nombre del usuario es requerido"            
            flash(error)

        if not apellidos:
            error = "El apellido del usuario es requerido"            
            flash(error)

        if not utils.isUsernameValid(usuario):
            error = "El usuario debe ser alfanumérico o incluir . , _ - y debe ser de al menos 8 carateres"            
            flash(error)
            isError = True
        
        if not utils.isPasswordValid(contrasena):
            error = "La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"            
            flash(error)
            isError = True

        if not utils.isEmailValid(correo):
            error = "Dirección de correo inválida"            
            flash(error)
            isError = True

        if isError:
            return render_template('new/registro.html')
        else:
            db = get_db()

            cursor = db.cursor()
            sql="SELECT MAX(id) + 1 FROM usuario"
            cursor.execute(sql)
            results = cursor.fetchone()
            maxid = results[0]

            db.execute(
                'INSERT INTO usuario (id, nombres, apellidos, correo, usuario, clave, estado) VALUES (?,?,?,?,?,?,"I")',
                (maxid, nombre, apellidos, correo, usuario, contrasena)
            )

            db.commit()

            sendmail(correo, "Activa tu cuenta", "Bienvenido a Blogs Company, utiliza este enlace para activar tu cuenta. http://localhost:5000/activar")
            flash('Se han registrado tus datos, revisa tu correo para activar tu cuenta')
            return render_template('new/registro.html')

    except:
        flash('Error interno')
        return render_template('new/registro.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        correo = request.form['correo']
        clave = request.form['clave']
        isError = False

        if not correo:
            flash('Debe ingresar el correo')
            idError = True

        if not clave:
            flash('Debe ingresar el contraseña')
            idError = True

        if isError:
            return render_template('/new/index.html')
        else:
            db = get_db()
            cursor = db.cursor()

            user = cursor.execute(
                'SELECT * FROM usuario WHERE correo = ? AND clave = ?', (correo, clave)
            ).fetchone()

            if user is None:
                flash('Correo electrónico o contraseña invalidos')
                return render_template('/new/index.html')
            else:
                name = user[1] + ' ' + user[2]
                userid = user[0]
                return render_template('/new/inicio.html', name = name, userid = userid)
        

    except:
        flash('Error interno')
        return render_template('/new/index.html')

@app.route('/inicio')
def inicio():
    return render_template('/new/inicio.html')

@app.route('/perfil')
def perfil():
    return render_template('/new/perfil.html')

@app.route('/comentarios')
def comentarios():
    return render_template('/new/comentarios.html')

@app.route('/eliminar-cuenta')
def eliminar_cuenta():
    return render_template('/new/eliminar-cuenta.html')

@app.route('/crear-blog')
@app.route('/crear-blog/<userid>')
def crear_blog(userid):
    return render_template('new/crear-blog.html', userid = userid)

@app.route('/guardar-blog', methods=['POST'])
def guardar_blog():
    titulo = request.form['titulo']
    userid = request.form['userid']
    privacidad = request.form['privacidad']
    cuerpo = request.form['cuerpo']
    isError = False

    if not titulo:
        flash('Debe ingresar un titulo para el blog')
        idError = True

    if not cuerpo:
        flash('Debe ingresar el contenido del blog')
        idError = True

    if isError:
        return render_template('/new/inicio.html')
    else:
        db = get_db()

        cursor = db.cursor()
        sql="SELECT MAX(id) + 1 FROM Blog"
        cursor.execute(sql)
        results = cursor.fetchone()
        maxid = results[0]

        flash(maxid)

        db.execute(
            'INSERT INTO Blog (id, Titulo, cuerpo, privacidad, usuario) VALUES (?,?,?,?,?);',
            (maxid,titulo,cuerpo,privacidad,userid)
        )

        db.commit()
        flash('Blog registrado')
        return render_template('/new/inicio.html')

#Funcion para enviar un correo
def sendmail(mto, msubject, mcontents):
    yag = yagmail.SMTP('misionticgrupo9@gmail.com','Holamundo1')
    yag.send(to=mto,
            subject=msubject, 
            contents=mcontents)


if __name__ == '__main__':
    app.run()