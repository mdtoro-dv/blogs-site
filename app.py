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
    blogs = obtenerblogs(limit = 3, publico = 1)
    return render_template('new/index.html', blogs = blogs)

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
                'SELECT id FROM usuario WHERE correo = ? AND clave = ?', (correo, clave)
            ).fetchone()

            if user is None:
                flash('Correo electrónico o contraseña invalidos')
                return render_template('/new/index.html')
            else:
                userid = user[0]
                
                return redirect(url_for('inicio', userid = userid))
    except:
        flash('Error interno')
        return render_template('/new/index.html')

@app.route('/inicio', methods=['GET'])
def inicio():
    try:
        userid = request.args.get('userid', default = 0, type = int)
        db = get_db()
        cursor = db.cursor()

        user = cursor.execute(
                'SELECT * FROM usuario WHERE id = ?', (str(userid))
            ).fetchone()

        name = user[1] + " " + user[2]

        blogs = obtenerblogs(publico = 1)

        return render_template('/new/inicio.html', userid = userid, name = name, blogs = blogs)
    except:
        flash("Error interno")
        return render_template('/new/index.html')

@app.route('/perfil')
@app.route('/perfil/<userid>')
def perfil(userid):
    return render_template('/new/perfil.html', userid = userid)

@app.route('/comentarios')
@app.route('/comentarios/<userid>')
def comentarios(userid):
    return render_template('/new/comentarios.html', userid = userid)

@app.route('/eliminar-cuenta')
@app.route('/eliminar-cuenta/<userid>')
def eliminar_cuenta(userid):
    return render_template('/new/eliminar-cuenta.html', userid = userid)

@app.route('/crear-blog')
@app.route('/crear-blog/<userid>')
def crear_blog(userid):
    return render_template('new/crear-blog.html', userid = userid)

@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        userid = request.form['userid']
        titulo = request.form['titulo']
        cuerpo = request.form['cuerpo']
        publico = request.form.get("privacidad") != None
        isError = False

        if not titulo or titulo == None:
            flash('Debe ingresar un titulo para el blog')
            isError = True
        
        if not cuerpo or cuerpo == None:
            flash('Debe ingresar un contenido para el blog')
            isError = True
        
        if isError:
            return render_template('new/crear-blog.html', userid = userid)
        else:
            db = get_db()

            cursor = db.cursor()
            sql="SELECT MAX(id) + 1 FROM Blog"
            cursor.execute(sql)
            results = cursor.fetchone()
            maxid = results[0]

            db.execute(
                'INSERT INTO Blog (id,Titulo, cuerpo, privacidad, usuario) VALUES (?,?,?,?,?)',
                (maxid,titulo,cuerpo,publico,userid)
            )

            db.commit()

            if publico:
                flash('Se ha publicado tu blog')
            else:
                flash('Tu blog ha sido guardado')
            
            return render_template('new/crear-blog.html', userid = userid)

    except:
        flash('Error interno')
        return render_template('new/index.html')

@app.route('/biblioteca/<userid>', methods=['POST', 'GET'])
def biblioteca(userid):

    if request.method == 'POST':
        try:
            searchtext = request.form['searchtext']
            blogs = obtenerblogs(userid = userid, searchtext = searchtext)
            return render_template('new/biblioteca.html', userid = userid, blogs = blogs)
        except:
            flash("Error interno")
            blogs = obtenerblogs(userid = userid)
            return render_template('new/biblioteca.html', userid = userid, blogs = blogs)
    else:
        blogs = obtenerblogs(userid = userid)
        return render_template('new/biblioteca.html', userid = userid, blogs = blogs)

@app.route('/explorar/<userid>', methods=['POST', 'GET'])
def explorar(userid):

    if request.method == 'POST':
        try:
            searchtext = request.form['searchtext']
            blogs = obtenerblogs(searchtext = searchtext, publico = 1)
            return render_template('new/explorar.html', userid = userid, blogs = blogs)
        except:
            flash("Error interno")
            blogs = obtenerblogs(publico = 1)
            return render_template('new/explorar.html', userid = userid, blogs = blogs)
    else:
        blogs = obtenerblogs(publico = 1)
        return render_template('new/explorar.html', userid = userid, blogs = blogs)


#Funcion para enviar un correo
def sendmail(mto, msubject, mcontents):
    yag = yagmail.SMTP('misionticgrupo9@gmail.com','Holamundo1')
    yag.send(to=mto,
            subject=msubject, 
            contents=mcontents)

#Funcion para obtener blogs
def obtenerblogs(limit=None, userid=None, publico=None, searchtext=None):
    db = get_db()

    cursor = db.cursor()
    limitclause = (" LIMIT " + str(limit)) if limit != None else ""
    userclause = (" AND Blog.usuario = " + str(userid)) if userid != None else ""
    publicclause = (" AND Blog.privacidad = " + str(publico)) if publico != None else ""
    searchclause = (" AND (Blog.titulo LIKE '%" + searchtext + "%' OR Blog.cuerpo LIKE '%" + searchtext + "%')") if searchtext != None else ""

    sql="SELECT Blog.*, usuario.nombres, usuario.apellidos FROM Blog INNER JOIN usuario on Blog.usuario = usuario.id WHERE 1=1" + userclause + publicclause + searchclause + limitclause
    cursor.execute(sql)
    blogs = cursor.fetchall()
    return blogs

if __name__ == '__main__':
    app.run()