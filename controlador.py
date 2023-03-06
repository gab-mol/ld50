'''
controlador.py:
    Controlador que lanza vista correspondiente a ld50_app
    :Entrega Diplomatura Python - Nivel Intermedio:
'''



from tkinter import Tk
import vista

class Controlador:
    '''
    Instancia la clase importada de la vista
    '''
    def __init__(self, root):
        self.root_controler=root
        self.objeto_vista=vista.Ventana(self.root_controler)


if __name__=="__main__":
    main=Tk()
    aplicacion=Controlador(main)
    main.mainloop()