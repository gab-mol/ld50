'''
    **Módulo con funcionalidad de verificacion de campos correspondiente a aplicación: "Calculadora-LD50".**
'''

import re

import vista


class Verificador():
    '''
    Contiene el metodo estatico de verificacion de campos.
    :verif_campos:
    '''
    def __init__(            
            self,
            campo,
            funcion,
            convertir_float
        ):
        '''
        Uso de modulo re para controlar campos.

        :param campo: Campo a verificar (StringVar).
        :param convertir_float: "True" si se desea \
convertir a flotante luego de verificar.
        '''
        pat_campo = re.compile(
            "[a-zA-Z,]"
        )
        if pat_campo.search(
            campo.get()
            ):
            print(
                "caracter(es) no válido(s)"
            )
            vista.Avisos.formato_error()
        else:
            if convertir_float == True:
                data_verif = float(campo.get())
                funcion
            else:
                data_verif = campo.get()
                return data_verif
        