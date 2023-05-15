'''
**Para registrar log a la aplicación**
'''
import socket
import logging

from cliente_logging import hora

class Servidor_log:
    '''
    **Clase servidor. Encargada de recibir los ensajes de log del CRUD**
        Emplea paquete logging.
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
                mensaje = data.decode()
                logging.info(mensaje)


# Ejecución
try:
    Servidor_log.conectar()
except ConnectionError:
    logging.info(f"---- FIN DE SESION {hora()} ----")
    print("Se cerró la aplicación, o Servidor_log perdió la conexión.")
