import socket
import threading
import pickle
import time


# La cola compartida se declara en el hilo principal

class Cliente:
    HOST = "127.0.0.1"
    PORT = 8080    

    @classmethod
    def Cliente_log(cls, cola):
        print("ejecución: Cliente_log")
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((cls.HOST, cls.PORT))
        sesion = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sesion_ser = pickle.dumps(sesion)
        soc.send(sesion_ser)
        print("cliente a la espera")
        
        while True:
            item = cola.get()
            print("en el while cliente: ", item, type(item))
            item_serial = pickle.dumps(item)
            soc.sendall(item_serial)

    @staticmethod
    def lanzar_cliente(cola):
        try:
            threading.Thread(target=Cliente.Cliente_log, args=(cola,), daemon=True).start()
        except ConnectionError:
            print("Falló el cliente")


# Decorador logging
def enviar_log(id_item:str, cola):
    def _cliente_log(func):
        def env(*args):
            consulta = args[0].__dict__
            paquete = [id_item, consulta["dosis_var"].get(), consulta["muert_var"].get()]

            cola.put(paquete)
            print("Llega a decorador:", paquete)
            func(*args)
        return env
    return _cliente_log
    


'''try:
    Cliente_log.conectar()
except ConnectionError:
    print("Error: Servidor_log no se pudo establecer una conexión.")'''