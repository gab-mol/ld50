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
    @staticmethod
    def verif_campos(
            campo,
            convertir_float
        ):
        '''
        Uso de modulo re para controlar campos.

        :param campo: Campo a verificar (StringVar).
        :param convertir_float: "True" si se desea \
convertir a flotante luego de verificar.
        '''
        pat_campos = re.compile(
            "[a-zA-Z,]"
        )
        if pat_campos.search(
            campo.get()
            ):
            print(
                "caracter(es) no válido(s)"
            )
            vista.Avisos.formato_error()
        else:
            if convertir_float == True:
                data_verif = float( campo.get())
                return data_verif
            else:
                data_verif = campo.get()
                return data_verif
        