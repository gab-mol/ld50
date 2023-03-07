'''
conex_bd.py:
    Conexión a base de datos para aplicación ld50.
    :Entrega Diplomatura Python - Nivel Intermedio:
'''
from peewee import SqliteDatabase, Model, FloatField, \
    IntegerField, CharField


nombre_db = "dosisld50.db"
db = SqliteDatabase(
    nombre_db
)

class BaseModel(Model):
    
    class Meta:
        database = db


class Ld50(BaseModel):
    '''Construccion de tabla'''
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
