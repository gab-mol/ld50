'''
    **La 'vista' (patrón MVC) correspondiente a aplicación: "Calculadora-LD50"**
'''

from tkinter import Label, Entry, StringVar, Button, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

import modelo


class Ventana():
    '''
    **Declaración de ventana y componentes de salida \
de datos de la interfaz visual.**
    Modulo empleado: *tkinter*

    :param principal: Recibe el objeto Tk (tkinter mainloop).
    '''
    def __init__(
            self,
            principal
        ):
        self.vista_ensayos = Vista_arbol(principal)

        self.cargador_arbol = modelo.Arbol(
            self.vista_ensayos.vista_ensayos
        )

        self.entradas = Entr(principal)

        self.datos = modelo.Crud(
            self.vista_ensayos.vista_ensayos, 
            self.entradas.dosis_var, 
            self.entradas.muert_var, 
            self.entradas.n_var, 
            self.entradas.uni_var
        )

        #Formateo y maquetación de ventana
        col_fond = "#BFBFBF"
        principal.geometry(
            "1210x620"
        )

        principal.configure(
            bg=col_fond
        )

        principal.title(
            "Calculadora de DL50 - Método PROBIT"
        )

        principal.after(
            1,
            lambda: self.cargador_arbol.cargador_bd()
        )

        # Instruccion superior
        font_instrucc = (
            "Lucida Console", 12, "underline"
        )

        instrucc = Label(
            principal,
            text="Ingrese dosis ensayada \
y respuesta (muertos): ", 
            bd=8, font=font_instrucc
        )

        instrucc.grid(
            row=0,
            column=0,
            sticky="w",
            columnspan=2
        )

        # Botones
        font_botones1 = (
            "Arial", 11, "bold"
        )

        font_botones2 = (
            "Arial", 11
        )

        calcular = Button(
            principal, 
            text="Calcular>>", 
            font=font_botones1,
            command=lambda:modelo.ver_100_0(
                ax,
                self.vista_ensayos.vista_ensayos,
                sal_ld50,
                sal_inter_ld50,
                equ_reg,
                canvas
            ),
            padx=30,
            pady=10,
            width=10
        )

        calcular.grid(
            row=1,
            column=2,
            rowspan=2,
            pady=8,
            sticky="n"
        )

        guard_ensy = Button(
            principal,
            text=">>Guardar ensayo",
            font=font_botones2,
            command=lambda:self.datos.alta_ensay(),
            padx=30,
            pady=10,
            width=10
        )

        guard_ensy.grid(
            row=3,
            column=2,
            rowspan=2
        )

        borr = Button(
            principal,
            text="Borrar",
            font=font_botones2,
            command=lambda:self.datos.borr_ensay(), 
            padx=30,
            pady=10,
            width=10
        )

        borr.grid(
            row=6,
            column=2,
            rowspan=2,
            sticky="s",
            pady=7
        )

        modif = Button(
            principal,
            text="Modificar",
            font=font_botones2,
            command=lambda:self.datos.modif_ensay(), 
            padx=30,
            pady=10,
            width=10
        )

        modif.grid(
            row=7,
            column=2,
            rowspan=2,
            sticky="s"
        )

        # Salida de valores ######
        ## GRAFICO Logdosis x probit.
        fig = Figure(
            figsize=(
                4.2, 4.5
            ), 
            dpi=100
        )

        ax = fig.add_subplot(
            1, 
            1, 
            1
        )

        canvas = FigureCanvasTkAgg(
            fig, 
            master=principal
        ) 

        canvas.draw()

        canvas.get_tk_widget().grid(
            row=6, 
            column=4,
            pady=5,
            columnspan=2,
            rowspan=7,
            padx=10,
            sticky="n"
        )

        # LD50 salida
        font_et_ld50 = (
            "Lucida Console", 9, "bold"
        )

        font_et_ld502 = (
            "Lucida Console", 11, "underline"
        )

        et_ld50 = Label(
            principal,
            text="Resultado LD50:",
            justify="center",
            bg="#857b7b",
            font=font_et_ld502,
            pady=5,
            padx=50,
            width=35,
            height=1
        )

        et_ld50.grid(
            row=1,
            column=4,
            columnspan=2,
            rowspan=1,
            padx=10,
            sticky="n"
        )

        # salida LD50
        sal_ld50 = Label(
            principal,
            text="Dosis Letal 50%: <...>",
            padx=36,
            bg="#DECDCD",
            justify="center",
            font=font_et_ld50,
            pady=15,
            width=43,
            height=1
        )

        sal_ld50.grid(
            row=2,
            column=4,
            columnspan=3,
            rowspan = 2,
            padx=5,
            sticky="n"
        )

        # Salida intervalo
        et_int =Label(
            principal,
            text="Intervalo de confianza 95%:",
            pady=5, 
            padx=4,
            bg="#DECDCD",
            justify="center",
            font=font_et_ld50,
            width=51,
            height=1
        )

        et_int.grid(
            row=3,
            column=4,
            columnspan=3,
            rowspan = 3,
            padx=5,
            sticky="n"
        )

        sal_inter_ld50 = Label(
            principal, 
            text="<...>", 
            pady=6, 
            padx=4,
            bg="#DECDCD",
            justify="center",
            font=font_et_ld50,
            width=51,
            height=1
        )

        sal_inter_ld50.grid(
            row=4,
            column=4,
            columnspan=3,
            rowspan = 2,
            padx=9,
            sticky="s"
        )

        # Ecuación regresión
        font_ecu1 = (
            "Arial", 9, "bold"
        )

        font_ecu2 = (
            "Arial", 9
        )

        et_equ_reg =Label(
            principal,
            text="Línea de regresión:",
            pady=5,
            padx=4,
            bg="#DECDCD",
            justify="center",
            font=font_ecu1,
            width=15,
            height=1
        )

        et_equ_reg.grid(
            row=9,
            column=2,
            rowspan=2
        )

        equ_reg =Label(
            principal, 
            text="Pendiente= ... | Ordenada= ...",
            bg="#DECDCD",
            justify="center",
            font=font_ecu2,
            width=25,
            height=1
        )

        equ_reg.grid(
            row=10,
            column=2,
            rowspan=1,
            sticky="e"
        )


class Entr():
    '''
    **Declaracion de entradas de datos para los \
ensayos, sus variables y sus etiquetas.**

    :param principal: Recibe objeto Tk (ventana tkinter).
    '''
    def __init__(self, principal):
        font_etiqs = (
            "Arial", 10
        )

        font_entr = (
            "Arial", 11
        )

        # Etiqueta: "dosis"
        instrucc_dosis = Label(
            principal,
            text="Dosis:",
            pady=2,
            padx=4,
            justify="left",
            font=font_etiqs
        )
        
        instrucc_dosis.grid(
            row=1,
            column=0,
            pady=5,
            columnspan=1,
            rowspan = 2,
            padx=10,
            sticky="w"
        )

        # Campo de entrada: "dosis"
        self.dosis_var = StringVar()

        dosis_ent = Entry(
            principal,
            textvariable=self.dosis_var,
            width=25,
            justify="left",
            font=font_entr
        )

        dosis_ent.grid(
            row=2,
            column=0,
            pady=5,
            columnspan=1,
            rowspan = 2,
            padx=10,
            sticky="w"
        )

        # Etiqueta: unidad
        unid = Label(
            principal,
            text="Unidades usadas: ",
            pady=2,
            padx=4,
            justify="left",
            font=font_etiqs
        )

        unid.grid(
            row=4,
            column=0,
            pady=5,
            columnspan=1,
            rowspan = 2,
            padx=10,
            sticky="sw"
        )

        # Campo de entrada: "unidad"
        self.uni_var = StringVar()

        uni_var_ent = Entry(
            principal,
            textvariable=self.uni_var,
            width=25,
            justify="left",
            font=font_entr
        )

        uni_var_ent.grid(
            row=6,
            column=0,
            pady=5,
            columnspan=1,
            rowspan = 1,
            padx=10,
            sticky="w"
        )

        # Etiqueta: "muertos"
        instrucc_muer = Label(
            principal,
            text="Muertos:",
            pady=2,
            padx=4,
            justify="left",
            font=font_etiqs
        )

        instrucc_muer.grid(
            row=1,
            column=1,
            pady=5,
            columnspan=1,
            rowspan = 2,
            padx=10,
            sticky="w"
        )

        # Campo de entrada: "muertos"
        self.muert_var = StringVar()

        muert_ent = Entry(
            principal,
            textvariable=self.muert_var,
            width=25,
            justify="left",
            font=font_entr
        )

        muert_ent.grid(
            row=2,
            column=1,
            pady=5,
            columnspan=1,
            rowspan = 2,
            padx=10,
            sticky="w"
        )

        # Etiqueta: "n"
        instrucc_n = Label(
            principal,
            text="n del ensayo (Dosis):",
            justify="left",
            font=font_etiqs
        )

        instrucc_n.grid(
            row=4,
            column=1,
            pady=5,
            columnspan=1,
            rowspan = 2,
            padx=10,
            sticky="sw"
        )

        # Campo de entrada: "n"
        self.n_var = StringVar()

        n_ent = Entry(
            principal,
            textvariable=self.n_var,
            width=25,
            justify="left",
            font=font_entr
        )

        n_ent.grid(
            row=6,
            column=1,
            pady=5,
            columnspan=1,
            rowspan = 1,
            padx=10,
            sticky="w"
        )


class Vista_arbol(ttk.Treeview):
    '''
    **Árbol donde se listan los ensayos cargados \
(treeview de tkinter).**

    :param principal: Recibe objeto Tk (ventana tkinter).
    '''
    def __init__(self, principal) -> None:
        anch = 110
        self.vista_ensayos = ttk.Treeview(
            principal, 
            height=18
        )
        self.vista_ensayos["columns"] = (
            "Dosis", 
            "Muertos",
            "n",
            "Unid"
        )
        self.vista_ensayos.column(
            "#0",
            width=0,
            minwidth=0,
            anchor="n"
        )
        self.vista_ensayos.heading(
            "Dosis",
            text="Dosis"
        )
        self.vista_ensayos.column(
            "Dosis",
            width=anch,
            anchor="n"
        )
        self.vista_ensayos.heading(
            "Muertos",
            text="Muertos"
        )
        self.vista_ensayos.column(
            "Muertos",
            width=anch,
            anchor="n"
        )
        self.vista_ensayos.heading(
            "n",
            text="n"
        )
        self.vista_ensayos.column(
            "n",
            width=anch,
            anchor="n"
        )
        self.vista_ensayos.heading(
            "Unid",
            text="Unid"
        )
        self.vista_ensayos.column(
            "Unid",
            width=anch,
            anchor="n"
        )
        self.vista_ensayos.grid(
            row=7,
            column=0,
            pady=5,
            columnspan=2,
            rowspan=7,
            padx=10,
            sticky="nw"
        )        


class Avisos():
    '''
    **Mensajes emergentes de error y aviso de eventos**
    '''
    @staticmethod
    def formato_error():
        '''
        Notifica campo con tipo de dato inválido.
        '''
        messagebox.showwarning(
            "Formato incorrecto",
            "Solo números (Dosis, muertos, n). Decimales con punto (.)"
        )

    @staticmethod
    def aviso_modif(
        item_1,
        item_2,
        item_3,
        item_4,
        verf
    ):
        '''
        Notifica modificación a un ensayo.

        :param item_1: Dosis a eliminar
        :param item_2: Muertos a eliminar
        :param item_3: n a eliminar
        :param item_4: Unidad a eliminar
        :param verf: Lista con valores nuevos
        '''
        messagebox.showinfo(
            "Aviso. Se Modificó ensayo:",
            f" Dos.: {item_1},\
Muer.: {item_2}, n: {item_3}, Uni.: {item_4}, > A > Dos.: {verf[0]}, \
Muer.: {verf[1]}, n: {verf[2]}, Uni.: {verf[3]}"
        )

    @staticmethod
    def aviso_borr(item_bd, item_bu):
        '''
        Notifica eliminación a un ensayo.

        :param item_bd: Dosis a eliminar
        :param item_bu: Unidad a eliminar
        '''
        messagebox.showinfo(
            "Aviso:", f"Se borró Dosis: {item_bd} {item_bu}"
        )

    @staticmethod
    def error_estadistico():
        '''
        Notifica error por ensayos con 0% y/o 100% \
de mortalidad (inadmisible).
        '''
        messagebox.showerror(
            "Error estadístico:",
            "Imposible modelar \
con mortalidad del 100% y/o 0% (elimine dichos ensayos)"
        )
        raise Exception(
        "Ensayo con mortalidad 0 y/o 100 % (Error estadisico)"
        )
        
    @staticmethod  
    def error_sin_datos():
        '''
        Notifica error por ausencia de ensayos cargados.
        '''
        messagebox.showerror(
            "Error:",
            "No se ingresaron datos"
        )

