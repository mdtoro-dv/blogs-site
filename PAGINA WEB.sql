--
-- File generated with SQLiteStudio v3.2.1 on sáb. dic. 12 15:53:59 2020
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Blog
CREATE TABLE Blog (id INTEGER PRIMARY KEY, Titulo VARCHAR (100) NOT NULL, cuerpo TEXT NOT NULL, privacidad BOOLEAN NOT NULL, usuario INTEGER NOT NULL REFERENCES usuario (id) ON DELETE NO ACTION ON UPDATE NO ACTION);

-- Table: comentario
CREATE TABLE comentario (id INTEGER NOT NULL, usuario INTEGER NOT NULL REFERENCES usuario (id) ON DELETE NO ACTION ON UPDATE NO ACTION, blog INTEGER NOT NULL REFERENCES Blog (id) ON DELETE NO ACTION ON UPDATE NO ACTION, comentario TEXT NOT NULL);

-- Table: Preguntas
CREATE TABLE Preguntas(

    id INTEGER primary key,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL
     
);

-- Table: usuario
CREATE TABLE usuario (id INTEGER PRIMARY KEY, nombres VARCHAR (30) NOT NULL, apellidos VARCHAR (30) NOT NULL, correo VARCHAR (50) NOT NULL, usuario VARCHAR (320) NOT NULL, clave VARCHAR (50) NOT NULL, estado BOOLEAN);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
