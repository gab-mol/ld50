'''
**El 'controlador' (patrón MVC) correspondiente a aplicación: "Calculadora-LD50".**
'''

from tkinter import Tk
import sys
import os
from pathlib import Path
import subprocess
import asyncio

import vista
import observador
import cliente


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

        
#class ServerLog:   
async def lanzamiento():
    main=Tk()
    aplicacion=Controlador(main)
    main.mainloop()

def serv_init():    
    global proc_log
    proc_log=""
    raiz=Path(__file__).resolve().parent
    ruta=os.path.join(raiz, "servidor.py")
    try:
        proc_log=subprocess.Popen([sys.executable, ruta])
        proc_log.communicate()
    except:
        print("error en iniciacion de proceso servidor")


async def main():
    '''
    tareas asincronas
    '''
    stop_event = asyncio.Event()
    asyncio.create_task(serv_init())
    asyncio.create_task(lanzamiento())
    await stop_event.wait()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
