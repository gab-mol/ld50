'''
**El 'controlador' (patrón MVC) correspondiente a aplicación: "Calculadora-LD50".**
'''

from tkinter import Tk
import subprocess
import os
import sys
from pathlib import Path
import subprocess
import threading

import vista
import observador


proce_serv = ''

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

class LanzServ:
    '''
    Ejecuta "servidor_logging.py" en supropio hilo.
    '''
    @staticmethod
    def lanzar_servidor():
        '''
        Lanzar Servidor de log como proceso independiente.
        '''
        if proce_serv != "":
            proce_serv.kill()
            threading.Thread(target=LanzServ.subrutina_servidor, daemon=True).start()
            print("Proceso del servidor iniciado. (if)")
        else:
            threading.Thread(target=LanzServ.subrutina_servidor, daemon=True).start()
            print("Proceso del servidor iniciado. (else)")

    @staticmethod
    def subrutina_servidor():
            global proce_serv
            ruta_server = os.path.join(Path(__file__).resolve().parent, "servidor_logging.py")
            if proce_serv != '':
                proce_serv.kill()
            proce_serv = subprocess.Popen([sys.executable, ruta_server])
            proce_serv.communicate()


if __name__=="__main__":
    LanzServ.lanzar_servidor()
    main=Tk()
    aplicacion=Controlador(main)
    main.mainloop()