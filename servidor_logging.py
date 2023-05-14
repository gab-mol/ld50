'''
Para registrar log a la aplicación
'''
import socket
import logging


class Servidor_log:
    '''
    ...
    '''
    HOST = "127.0.0.1"
    PORT = 8080

    @classmethod
    def conectar(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((cls.HOST, cls.PORT)) #
        sock.listen()
        print("escuchando...")
        conn, addr = sock.accept()

        with conn:
            print(f"Conectado a observador.py: {addr}")
            while True: # recibe los datos. loop infinito
                data = conn.recv(1024)
                print("Inicio sesión: ", str(data))


# Ejecución
try:
    Servidor_log.conectar()
except ConnectionError:
    print("Error: Servidor_log no se pudo establecer una conexión.")