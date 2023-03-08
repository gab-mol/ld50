'''
**El 'modelo' (patrón MVC) correspondiente a aplicación: "Calculadora-LD50".**
'''
__author__ = "Gabriel Molina"
__maintainer__ = "Gabriel Molina"
__email__ = "gabrielmolina149@gmail.com"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"


from math import log10, sqrt
from numpy import polyfit, array
from statistics import NormalDist, mean
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import vista
from verificacion_campos import Verificador
from base_conexion import Ld50


class Arbol():
    '''
    **Gestiona vista de ensayos (objeto treeview de tkinter)**

    :param root: Recibe el objeto Tk.
    '''
    def __init__(self, treeview):
        self.treeview = treeview

    def cargador_bd(self):
        '''
        Carga el arbol con info almacenada en base de datos.
        '''
        global lista_dosis, lista_logdosis, lista_muertos, lista_n,\
            lista_prop_muer, lista_probit_un, lista_un
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
            self.treeview.insert(
                "",
                0,
                text=fila.id,
                values=(fila.dosis,
                        fila.muertos,
                        fila.n,
                        fila.unid
                ))
            
            lista_dosis.append(
                fila.dosis
            )

            lista_muertos.append(
                fila.muertos
            )

            lista_n.append(
                fila.n
            )

            lista_un.append(
                fila.unid
            )


class Grafico(FigureCanvasTkAgg):
    '''
    **Crea el grafico de regresión.**

    :param root: Recibe el objeto Tk (mainloop tkinter).
    '''
    @staticmethod         
    def graf(
            ax,
            lista_logdosis,
            lista_probit_un,
            b,
            a,
            canvas
        ):
        '''
        **Gráfico PROBIT vs Log(dosis)**

        :param ax: Recibe objeto de ejes (canvas)
        :param lista_logdosis: Recibe lista de Dosis cargadas (eje x)
        :param lista_probit_un: Recibe lista de unidades PROBIT calculadas (eje y)
        :param b: Recibe pendiente de la regresión
        :param a: Recibe ordenada de la regresión
        :param canvas: Recibe objeto canvas
        '''
        x = lista_logdosis
        y = lista_probit_un
        ax.clear()
        ax.scatter(
            x,
            y,
            color='g'
        )
        ax.set_title(
            "Regresión PROBIT:"
        )
        ax.set_ylabel(
            "PROBIT"
        )
        ax.set_xlabel(
            "Log Dosis"
        )
        canvas.draw()
        ax.plot(
            array(x),
            b*array(x)
            +a
        )
        canvas.draw()


class Mat():
    '''
    **Realiza los cálculos para obtener la LD50.**

    :param vista_ensayos: Recibe objeto ttk (treeview tkinter)
    '''    
    def __init__(
            self, 
            vista_ensayos
        ) -> None:
        self.vista_ensayos = vista_ensayos
        self.arbol = Arbol(vista_ensayos)     
        self.grafico = Grafico()  

    def operaciones(
            self,
            ax,
            canvas
        ):
        '''
        Modela a partir de los ensayos guardados. 
        Calcula la LD50 y su intervalo de confianza.

        :param ax: Recibe objeto de ejes (canvas)
        :param canvas: Recibe objeto canvas
        '''
        self.arbol.cargador_bd()
        global ld50, lim_sup, lim_inf, a ,b,lista_dosis, lista_logdosis, \
        lista_muertos, lista_n, lista_prop_muer, lista_probit_un, lista_un

        for i in range(0, len(lista_dosis)):
            prop_muet = float(lista_muertos[i])/float(lista_n[i])
            lista_prop_muer.append(prop_muet)
            logdosis = log10(lista_dosis[i])
            lista_logdosis.append(logdosis)

        for i in lista_prop_muer:
            probit_un = 5 + NormalDist(mu=0, sigma=1).inv_cdf(i)
            lista_probit_un.append(probit_un)

        try:
            b, a = polyfit(
                lista_logdosis,
                lista_probit_un,
                1
            )
        except:
            vista.Avisos.error_sin_datos()
            raise Exception(
                "Error: sin datos para modelar"
                )
        
        ld50 = round(
            10**((5-a)/b),
            ndigits = 2
        )
        menos_sd = 10**((4-a)/b)
        mas_sd = 10**((6-a)/b)
        sd_ld50 = (mas_sd-menos_sd)/sqrt(mean(lista_n))
        lim_sup = round(
            ld50
            + sd_ld50,
            ndigits = 2
        )
        lim_inf = round(ld50-sd_ld50, ndigits=2)
        self.grafico.graf(
            ax,
            lista_logdosis,
            lista_probit_un,
            b,
            a,
            canvas
        )
        

class Crud(): 
    '''
    **Alta baja y modificacion.**

    :param vista_ensayos: Recibe objeto ttk (treeview tkinter) 
    :param dosis_var: Recibe objeto StringVar (tkinter) correspondiente a dosis
    :param muert_var: Recibe objeto StringVar (tkinter) correspondiente a muertos
    :param n_var: Recibe objeto StringVar (tkinter) correspondiente a n
    :param uni_var: Recibe objeto StringVar (tkinter) correspondiente a las unidades
    '''
    def __init__(
            self,
            vista_ensayos,
            dosis_var,
            muert_var, 
            n_var,
            uni_var
        ):
        self.vista_ensayos = vista_ensayos
        self.dosis_var = dosis_var
        self.muert_var = muert_var
        self.n_var = n_var
        self.uni_var = uni_var
        self.arbol = Arbol(vista_ensayos)

    def alta_ensay(self):
        '''
        Guarda en bd y suma al arbol.
        '''
        nuevo_ensayo = Ld50()
        nuevo_ensayo.dosis = self.dosis_var
        nuevo_ensayo.muertos = self.muert_var
        nuevo_ensayo.n = self.n_var
        nuevo_ensayo.unid = self.uni_var
        nuevo_ensayo.save()
        self.vista_ensayos.insert(
            "",
            "end",
            text=str(0),
            values=(
                self.dosis_var.get(),
                self.muert_var.get(),
                self.n_var.get(),
                self.uni_var.get(),
        ))
        print(
            "GUARDADO",
            self.dosis_var.get(),
            self.uni_var.get()
        )

    def modif_ensay(self):
            '''
            Modifica el item seleccionado en arbol y bd.
            '''
            selec = self.vista_ensayos.focus()

            item = self.vista_ensayos.item(selec)

            verf = Verificador().verif_campos(
                self.dosis_var, 
                self.muert_var, 
                self.n_var, 
                self.uni_var
            )

            actualizar=Ld50.update(
                dosis=verf[0], 
                muertos=verf[1], 
                n = verf[2], 
                unid = verf[3]).where(Ld50.id==item["text"])
            actualizar.execute()
            for item in self.vista_ensayos.get_children():
                self.vista_ensayos.delete(item)
            self.arbol.cargador_bd()
            vista.Avisos.aviso_modif(
                verf[0],
                verf[1],
                verf[2],
                verf[3],
                verf
            )

    def borr_ensay(self):
        '''
        Baja del árbol y de la base.
        '''
        selec = self.vista_ensayos.focus()
        item = self.vista_ensayos.item(selec)
        borrar=Ld50.get(Ld50.id==item["text"])
        borrar.delete_instance()
        item_bd = item["values"][0]
        item_bu = item["values"][3]
        self.arbol.cargador_bd()
        vista.Avisos.aviso_borr(
            item_bd,
            item_bu
        )

 
class ver_100_0():
    '''
    Eventos para el boton "Calcular"

    :param ax: Recibe objeto de ejes (canvas)
    :param vista_ensayos: Recibe objeto ttk (treeview tkinter) 
    :param sal_ld50: Recibe variable StringVar (tkinter) para LD50 
    :param sal_inter_ld50: Recibe variable StringVar (tkinter) para intervalo  conf. de LD50
    :param equ_reg: Recibe ordenada de la regresión
    :param canvas: Recibe objeto canvas
    '''
    def __init__(
            self, 
            ax, 
            vista_ensayos, 
            sal_ld50, 
            sal_inter_ld50, 
            equ_reg, 
            canvas
        ):
        global ld50, lista_dosis
        self.arbol = Arbol(
            vista_ensayos
        )
        self.op = Mat(
            vista_ensayos
        )
        self.arbol.cargador_bd()
        for i in range(0, len(lista_dosis)):
            if float(lista_muertos[i]) == float(lista_n[i]
            ) or float(lista_muertos[i]) == 0.0:
                vista.Avisos.error_estadistico()

        self.op.operaciones(
            ax, 
            canvas
        )

        sal_ld50["text"] = "".join(
            "Dosis Letal 50%: "
            + str(ld50) 
            + " "
            + str(lista_un[0])
        )

        sal_inter_ld50["text"] = "".join(
            "SUP: "
            + str(lim_sup)
            + "| INF: "
            + str(lim_inf)
        )

        equ_reg["text"] = f"Pendiente= {round(b,1)} | \
Ordenada= {round(a,1)}"