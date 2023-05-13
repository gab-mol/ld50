'''
Servidor encargado de registrar las sesiones de la aplicación.
'''
import socket
import threading
import logging
import time

HOST, PORT = "127.0.0.1", 8080
print("Entró al servidor")

class ServidorThread(threading.Thread):
    def _init__(self, conex_app, dir_spp):
        threading.Thread.__init__(self)
        self.conex = conex_app
        self.dire = dir_spp
    def correr(self):
        print("correr servidor")
        while True:
            data = self.conex.recv(1024)
            data_decod = data.decode()
            print(self.dire[0], "=>", data_decod)

class ServidorLog:
    def iniciar():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen()
        print("está intentando escuchar")
        conex_app, dir_spp = sock.accept()
        print("aceptó", dir_spp)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen()
        conex_app, dir_spp = sock.accept()
        thread_servidor = ServidorThread(conex_app, dir_spp)
        thread_servidor.start()
        mensaje = b"Conexion efectiva con servidor"
        sock.send(mensaje)
    
ServidorLog.iniciar()