'''
Para registrar log a la aplicación
'''
import socket
import logging
import pickle

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
        logging.basicConfig(filename='app_ld50.log', level="INFO")

        with conn:
            print(f"Conectado a observador.py: {addr}")
            while True: # recibe los datos. loop infinito
                data = conn.recv(1024)
                data_deser= pickle.loads(data)
                print("Inicio sesión: ", str(data_deser))
                logging.info(str(data_deser))


# archivo de log



# Ejecución
try:
    Servidor_log.conectar()
except ConnectionError:
    print("Servidor_log no pudo establecer conexión. O se cerró la aplicación")
