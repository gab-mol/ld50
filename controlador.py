'''
**El 'controlador' (patrón MVC) correspondiente a aplicación: "Calculadora-LD50".**
'''

from tkinter import Tk

import vista
import observador


class Controlador:
    '''
    **Instancia la clase importada de la vista**

    :param root: Recibe el objeto Tk.
    '''
    def __init__(self, root):
        self.root_controler=root
        self.objeto_vista=vista.Ventana(self.root_controler)
        self.observador_alta = observador.ObservadorCrudAlta(self.objeto_vista.datos)
        self.observador_baja = observador.ObservadorCrudBaja(self.objeto_vista.datos)
        self.observador_modif = observador.ObservadorCrudModificacion(self.objeto_vista.datos)


if __name__=="__main__":
    main=Tk()
    aplicacion=Controlador(main)
    main.mainloop()