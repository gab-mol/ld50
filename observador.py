'''
**Módulo encargado de seguir el CRUD de la aplicación y conectarse con \
el servidor de logging. | "Calculadora-LD50".**
'''

import socket
import threading
import subprocess
import sys
import os
from pathlib import Path


class Sujeto:
    registro_observadores = []
    registro_referencias = []

    def agregar_obs(self, objeto_seguido, referencia):
        self.registro_observadores.append(objeto_seguido)
        self.registro_referencias.append(referencia)


    def informar_registro_obs(self, ref_met:str):
        '''
        Metodo que decide que notificación debe activase según el método.\n
        Para notificar (argumento):
                        CRUD Alta: "alta"\n
                        CRUD Baja: "baja"\n
                        CRUD Modificacion: "modif"
        '''
        if ref_met == self.registro_referencias[0]:
            self.registro_observadores[0].actualizacion()
        if ref_met == self.registro_referencias[1]:
            self.registro_observadores[1].actualizacion()
        if ref_met == self.registro_referencias[2]:
            self.registro_observadores[2].actualizacion()


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ObservadorCrudAlta(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.referencia_metodo = "alta"
        self.obj_observado.agregar_obs(self, self.referencia_metodo)

    def actualizacion(self):
        print("<<<Alta de ensayo>>>")
        print(f"Dosis= {self.obj_observado.dosis_var.get()} \
Muertos= {self.obj_observado.muert_var.get()} \
n= {self.obj_observado.n_var.get()} \
Unidad= {self.obj_observado.uni_var.get()}")


class ObservadorCrudBaja(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.referencia_metodo = "baja"
        self.obj_observado.agregar_obs(self, self.referencia_metodo)

    def actualizacion(self):
        print("<<<Baja de ensayo>>>")
        print(f"Eliminado => Dosis: {self.obj_observado.dosis_var.get()} \
(muertos: {self.obj_observado.muert_var.get()})")


class ObservadorCrudModificacion(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.referencia_metodo = "modif"
        self.obj_observado.agregar_obs(self, self.referencia_metodo)

    def actualizacion(self):
        print("<<<Modificación de ensayo>>>")
        print(f"Nuevos datos: Dosis= {self.obj_observado.dosis_var.get()} \
Muertos= {self.obj_observado.muert_var.get()} \
n= {self.obj_observado.n_var.get()} \
Unidad= {self.obj_observado.uni_var.get()}")


"""# Decorador logging
class Cliente_log:
    '''
    **Conexión con servidor de logging.**
    '''
    HOST = "127.0.0.1"
    PORT = 8080

    @classmethod
    def conectar(cls):
        print("ejecución: Cliente_log.conectar()")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((cls.HOST, cls.PORT))
            for i in range(10):
                s.sendall(b"Hola mundo")

                data = s.recv(1024) # espera la devolución
                print("Recibido", repr(data)) # repr muestra data literalmente como llega


def cliente_log(func):
    '''
    **Vincula el método con el servidor de log.**
    '''
    def env(*args):
        func(*args)
        threading.Thread(target=Cliente_log.conectar, daemon=True).start()
    return env"""
