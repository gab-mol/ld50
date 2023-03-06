'''
Conexión a base de datos para aplicación ld50 y Creación de tabla.
'''
from peewee import SqliteDatabase, Model, FloatField, \
    IntegerField, CharField



db = SqliteDatabase(
    "dosisld50.db"
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


# Base de datos: Conexion y creacion de tablas.
try:
    db.connect()
    db.create_tables([Ld50])
    print(
        "Conexión exitosa"
    )
except:
    raise Exception(
        "Error de Conexión"
    )
