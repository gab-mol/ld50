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
            dosis_var,
            muert_var,
            n_var,
            uni_var
        ):
        '''
        Uso de modulo re para controlar campos.
        '''
        pat_campos = re.compile(
            "[a-zA-Z,]"
        )
        if pat_campos.search(
            dosis_var.get(), 
        ) or pat_campos.search(
            muert_var.get()
        ) or pat_campos.search(
            n_var.get()
        ):
            print(
                "caracter(es) no válido(s)"
            )
            vista.Avisos.formato_error()
        else:
            data = (
                float(dosis_var.get()),
                float(muert_var.get()),
                float(n_var.get()),
                uni_var.get(),
            )

            return data
        