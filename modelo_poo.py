'''
modelo_poo.py:
    Este es el modelo correspondiente a ld50_app
    :Entrega Diplomatura Python - Nivel Intermedio:
'''
__author__ = "Gabriel Molina"
__maintainer__ = "Gabriel Molina"
__email__ = "gabrielmolina149@gmail.com"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"

from peewee import *
from math import log10, sqrt
from numpy import polyfit, array
from statistics import NormalDist, mean
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import vista_poo

db = SqliteDatabase("dosisld50.db")

class BaseModel(Model):
    class Meta:
        database = db

class Ld50(BaseModel):
    '''Construccion de tabla'''
    dosis = FloatField()
    muertos = FloatField()
    n = IntegerField()
    unid = CharField()

# Base de datos: Conexion y creacion de tablas
try:
    db.connect()
    db.create_tables([Ld50])
except:
    raise Exception("error de Conexión")
#

class Arbol():
    '''Carga el arbol con info almacenada en base de datos. Depende de Clase Conex()'''
    def __init__(self, treeview):
        self.treeview = treeview

    def cargador_bd(self):
        global lista_dosis, lista_logdosis, lista_muertos, lista_n,\
            lista_prop_muer, lista_probit_un, lista_un
        # limpieza del arbol
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        lista_dosis = []
        lista_logdosis =[]
        lista_muertos = []
        lista_n = []
        lista_un = []
        lista_prop_muer = []
        lista_probit_un = []

        for fila in Ld50.select():
            print(fila)
            self.treeview.insert("", 0, text=fila.id, values=(fila.dosis, fila.muertos, fila.n, fila.unid))
            lista_dosis.append(fila.dosis)
            lista_muertos.append(fila.muertos)
            lista_n.append(fila.n)
            lista_un.append(fila.unid)


class Grafico(FigureCanvasTkAgg):
    '''
    Para crear el grafico de regresion.
    '''
    @staticmethod         
    def graf(ax, lista_logdosis, lista_probit_un, b, a, canvas):
        x = lista_logdosis
        y = lista_probit_un
        ax.clear()
        ax.scatter(x, y, color='g')
        ax.set_title("Regresión PROBIT:")
        ax.set_ylabel("PROBIT")
        ax.set_xlabel("Log Dosis")
        canvas.draw()
        ax.plot(array(x), b*array(x)+a)
        canvas.draw()

class Utilidades():
    '''
    Herramientas varias para CRUD y parte matematica
    '''    
    def __init__(self, vista_ensayos) -> None: # 
        self.vista_ensayos = vista_ensayos
        #self.canvas = canvas
        self.arbol = Arbol(vista_ensayos)     
        self.grafico = Grafico()  

    @staticmethod
    def verif_campos(dosis_var, muert_var, n_var, uni_var):
        '''uso de Re para controlar campos'''
        pat_campos = re.compile("[a-zA-Z,]")
        if pat_campos.search(dosis_var.get(), 
        ) or pat_campos.search(muert_var.get()
        ) or pat_campos.search(n_var.get()):
            print("no match caracter válido")
            vista_poo.Avisos.formato_error()
        else:
            data = (float(dosis_var.get()), float(muert_var.get()), 
            float(n_var.get()), uni_var.get(),)
            return data

    def operaciones(self, ax, canvas):
        self.arbol.cargador_bd()
        global ld50, lim_sup, lim_inf, a ,b,lista_dosis, lista_logdosis, lista_muertos, lista_n, lista_prop_muer, lista_probit_un, lista_un
        for i in range(0, len(lista_dosis)):
            prop_muet = float(lista_muertos[i])/float(lista_n[i])
            lista_prop_muer.append(prop_muet)
            logdosis = log10(lista_dosis[i])
            lista_logdosis.append(logdosis)
        for i in lista_prop_muer:
            probit_un = 5 + NormalDist(mu=0, sigma=1).inv_cdf(i)
            lista_probit_un.append(probit_un)
        try:
            b, a = polyfit(lista_logdosis, lista_probit_un, 1)
        except:
            vista_poo.Avisos.error_sin_datos()
            raise Exception("Error: sin datos para modelar")
        ld50 = round(10**((5-a)/b), ndigits=2)
        menos_sd = 10**((4-a)/b)
        mas_sd = 10**((6-a)/b)
        sd_ld50 = (mas_sd-menos_sd)/sqrt(mean(lista_n))
        lim_sup = round(ld50+sd_ld50, ndigits=2)
        lim_inf = round(ld50-sd_ld50, ndigits=2)
        self.grafico.graf(ax, lista_logdosis, lista_probit_un, b, a, canvas)
        
class Crud_ORM(): 
    '''Alta baja y modificacion. Ingresar variables de tkinter'''
    def __init__(self, vista_ensayos, dosis_var, muert_var, 
                 n_var, uni_var):
        self.vista_ensayos = vista_ensayos
        self.dosis_var = dosis_var
        self.muert_var = muert_var
        self.n_var = n_var
        self.uni_var = uni_var
        #self.con = Conex()
        self.arbol = Arbol(vista_ensayos)
    def alta_ensay(self):
        '''Guarda en bd y suma al arbol'''
        data = Utilidades(self.vista_ensayos).verif_campos(self.dosis_var, 
                                                           self.muert_var, 
                                                           self.n_var, 
                                                           self.uni_var)
        nuevo_ensayo = Ld50()
        nuevo_ensayo.dosis = data[0]
        nuevo_ensayo.muertos = data[1]
        nuevo_ensayo.n = data[2]
        nuevo_ensayo.unid = data[3]
        nuevo_ensayo.save()
        IDtree = str(self.con.cursor.lastrowid)
        self.vista_ensayos.insert("", "end", text=str(IDtree), 
        values=(self.dosis_var.get(), self.muert_var.get(), 
        self.n_var.get(), self.uni_var.get(),))
        print("GUARDADO", self.dosis_var.get(), self.uni_var.get())

    def modif_ensay(self):
            '''Modifica el item seleccionado en arbol y bd'''
            selec = self.vista_ensayos.focus()
            item = self.vista_ensayos.item(selec)
            verf = Utilidades(self.vista_ensayos).verif_campos(self.dosis_var, 
                                                               self.muert_var, 
                                                               self.n_var, 
                                                               self.uni_var)
            actualizar=Ld50.update(dosis=verf[0], 
                                     muertos=verf[1], 
                                     n = verf[2], 
                                     unid = verf[3]).where(Ld50.id==item["text"])
            actualizar.execute()
            for item in self.vista_ensayos.get_children():
                self.vista_ensayos.delete(item)
            self.arbol.cargador_bd()
            vista_poo.Avisos.aviso_modif(verf[0], verf[1], verf[2], verf[3], verf)

    def borr_ensay(self):
        '''Baja del árbol y de la base'''
        selec = self.vista_ensayos.focus()
        item = self.vista_ensayos.item(selec)
        borrar=Ld50.get(Ld50.id==item["text"])
        borrar.delete_instance()
        item_bd = item["values"][0]
        item_bu = item["values"][3]
        self.arbol.cargador_bd()
        vista_poo.Avisos.aviso_borr(item_bd, item_bu)

 
class ver_100_0():
    '''Eventos para el boton "Calcular"'''
    def __init__(self, ax, vista_ensayos, sal_ld50, sal_inter_ld50, equ_reg, canvas):
        global ld50, lista_dosis
        self.arbol = Arbol(vista_ensayos)
        self.op = Utilidades(vista_ensayos)
        self.arbol.cargador_bd()
        for i in range(0, len(lista_dosis)):
            if float(lista_muertos[i]) == float(lista_n[i]
            ) or float(lista_muertos[i]) == 0.0:
                vista_poo.Avisos.error_estadistico()
        self.op.operaciones(ax, canvas)
        sal_ld50["text"] = "".join(("Dosis Letal \
50%: "+str(ld50)+" " +str(lista_un[0])))
        sal_inter_ld50["text"] = " ".join(("SUP: "+ str(lim_sup), "| \
INF: "+ str(lim_inf)))
        equ_reg["text"] = f"Pendiente= {round(b,1)} | Ordenada= {round(a,1)}"