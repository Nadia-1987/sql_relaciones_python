#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de clase
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3

# https://extendsclass.com/sqlite-browser.html


def create_schema():

    conn = sqlite3.connect('secundaria.db')
   
    c = conn.cursor()
    
    c.execute("""
                DROP TABLE IF EXISTS estudiante;
            """)

    c.execute("""
            DROP TABLE IF EXISTS tutor;
        """)

    c.execute("""
        CREATE TABLE tutor(
            [id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [name] TEXT NOT NULL
        );
        """)

    c.execute("""
            CREATE TABLE estudiante(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [age] INTEGER NOT NULL,
                [grade] INTEGER NOT NULL,
                [fk_tutor_id] INTEGER NOT NULL REFERENCES tutor(id)
            );
            """)

    
    conn.commit()

    conn.close()


def fill(name):
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)
    conn = sqlite3.connect('secundaria.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    values = [name]

    c.execute("""
        INSERT INTO tutor (name)
        VALUES (?);""", values)

    conn.commit()
    
    conn.close()

    
    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # fk_tutor_id --> id de su tutor

def fill_estudiantes(estudiantes):    
    conn = sqlite3.connect('secundaria.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
       
    try:
        c.executemany("""
            INSERT INTO estudiante (name, age, grade, fk_tutor_id)
            SELECT ?,?,?, t.id
            FROM tutor as t
            WHERE t.name =?;""", estudiantes)
    except sqlite3.Error as err:
        print(err)

    # Se debe utilizar la sentencia INSERT.
    # Observar que todos los campos son obligatorios
    # Cuando se insert los los estudiantes sería recomendable
    # que utilice el INSERT + SELECT para que sea más legible
    # el INSERT del estudiante con el nombre del tutor

    # No olvidarse que antes de poder insertar un estudiante debe haberse
    # primero insertado el tutor.
    # No olvidar activar las foreign_keys!

    conn.commit()
    
    conn.close()

def fetch():
    print('Comprovemos su contenido, ¿qué hsay en la tabla?')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas de la tabla estudiante.
    # No debe imprimir el id del tutor, debe reemplazar el id por el nombre
    # del tutor en la query, utilizando el concepto de INNER JOIN,
    # se puede usar el WHERE en vez del INNER JOIN.
    # Utilizar fetchone para imprimir de una fila a la vez

    # columnas que deben aparecer en el print:
    # id / name / age / grade / tutor_nombre

    conn = sqlite3.connect('secundaria.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    c.execute("""SELECT e.id, e.name, e.age, e.grade, t.name
                 FROM estudiante as e INNER JOIN tutor as t
                 on e.fk_tutor_id = t.id """)


    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)

    
    conn.close()




def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age / tutor_nombre
    conn = sqlite3.connect('secundaria.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    
    c.execute("""SELECT e.id, e.name, e.age, t.name
                 FROM estudiante as e, tutor as t
                 WHERE e.fk_tutor_id = ?;""", (tutor,))
    
    #Inove:
    # Este caso puntual es el ms dificil de resolver, porque se solicita encontrar
    # todos los estudiantes que tengan un determinado tutor, pero el tutor se pasa como "nombre" (name)
    # y no su ID, mientras que la tabla de estudiante tienen IDs de tutores
    # El problema en la implementacin anteriores es que se estaba comparando el ID del tutor con su nombre:
    # WHERE e.fk_tutor_id = ? --> WHERE e.fk_tutor_id = tutor, tutor es el nombre (string) y no el ID que es nuerico
    # Por lo tanto el ID del tutor del estudiante se debe comparar con el "ID" del tutor, es como realizar un INNER JOINT:
    #  --> WHERE e.fk_tutor_id = t.id
    # Pero no queremos obtener los tutores, solo nos interesa el tutor que tenga el name almaenado en "tutor"
    # Es por eso queagregamos:
    # WHERE e.fk_tutor_id = t.id AND t.name = ?. --> WHERE e.fk_tutor_id = t.id AND t.name = tutor
    c.execute("""SELECT e.id, e.name, e.age, t.name
                 FROM estudiante as e, tutor as t
                 WHERE e.fk_tutor_id = t.id AND t.name = ?;""", (tutor,))

    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)

    #while True:
     #   row = c.fetchone()
      #  if row[4] == tutor:
       ##else:
         #   break

                    

    # Cerrar la conexión con la base de datos
    conn.close()

def modify(id, name):
    print('Modificando la tabla')
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar el tutor asignado (fk_tutor_id --> id) por aquel que coincida
    # con el nombre del tutor pasado como parámetro
    conn = sqlite3.connect('secundaria.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    rowcount = c.execute("""UPDATE estudiante
                        SET fk_tutor_id = 
                        (SELECT t.id FROM tutor as t 
                        WHERE t.id =?)
                        WHERE id =?""", (id, name)).rowcount
    
    # Inove:
    # La implementación anterior estaba muuuuy cerca, solo faltaba un pequeño
    # cambio en el orden de las variables pasadas a la query
    # Orden --> EN la implemnentación anterior estaba (id, name)
    # Pero en la query primero se utiliza el nombre del tutor y luego se utiliza el ID del alaumno
    # Por lo que:
    # orden correcto --> (name, id)
    # Por otro lado, la condicin de búsqueda del tutor es por su nombre, es decir, por "t.name":
    # --> WHERE t.name =?
    rowcount = c.execute("""UPDATE estudiante
                    SET fk_tutor_id = 
                    (SELECT t.id FROM tutor as t 
                    WHERE t.name =?)
                    WHERE id =?""", (name, id)).rowcount
    
    
    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()



def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    conn = sqlite3.connect('secundaria.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute("""SELECT COUNT(e.id) AS estudiante_count
                 FROM estudiante as e, tutor as t
                 WHERE e.grade =?;""", (grade,))

    result = c.fetchone()
    count = result[0]
    print('Los estudiantes en el grade 2 son:', count)


    # Cerrar la conexión con la base de datos
    conn.close()

if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill('Angel')
    fill('Silvia')

    estudiantes = [('Anabela', 34, 2, 'Angel'),
               ('Marcos', 27, 1, 'Silvia'),
               ('Alma', 11, 4, 'Angel'),
               ('Cristobal', 2, 3, 'Silvia'),
               ('Juan', 34, 5, 'Angel'),
               ]
    fill_estudiantes(estudiantes)

    
    

    fetch()

    tutor = 'Angel'
    search_by_tutor(tutor)

    # Inove: Ojo! Javier no existe en la tabla de tutores, debemos agregarlo:
    fill('Javier')
    nuevo_tutor = 'Javier'
    id = 2
    
    modify(id, nuevo_tutor)

    grade = 2
    count_grade(grade)
