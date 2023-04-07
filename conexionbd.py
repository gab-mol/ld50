'''
**Módulo de conexión a base de datos correspondiente \
a aplicación: "Calculadora-LD50".**
'''
from peewee import SqliteDatabase, Model, FloatField, \
    IntegerField, CharField


nombre_db = "ld50.db"
db = SqliteDatabase(
    nombre_db
)

class Conexion(Model):
    '''
    **Conexión con base de datos.**
    Depende del módulo peewee (ORM).
    '''
    class Meta():
        '''
        Clase necesaria para el ORM (peewee).
        '''
        database = db


class Ld50(Conexion):
    '''
    **Construccion de tabla.**
    '''
    dosis = FloatField()
    muertos = FloatField()
    n = IntegerField()
    unid = CharField()


# Base de datos: Conexion y/o creacion de tablas.
try:
    db.connect()
    db.create_tables([Ld50])
    print(
        f"Conexión con base de datos '{nombre_db}' exitosa"
    )
except:
    raise Exception(
        "Error de Conexión con base de datos"
    )