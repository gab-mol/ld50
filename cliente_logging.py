'''
**Recoje actividad de la clase CRUD y la envía a servidor_logging**
'''
import socket
import threading
import time


# La cola compartida se declara en el hilo principal

def hora() -> str:
    '''
    **Imprime hora y fecha para logs**
    '''
    h = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return h

class Cliente:
    '''
    **Clase encargada de declarar el cliente y lanzarlo**

    :param cola: Recibe el objeto de clase queue (módulo Queue) \
que permite comunicación con decorador de logging.
    '''
    HOST = "127.0.0.1"
    PORT = 8080    

    @classmethod
    def Cliente_log(cls, cola):
        '''
        Conecta con el socket local (puerto 8080). Arma el mensaje \
de log según el caso (indicado por "id_item")

        :param cola: Recibe el objeto de clase queue (módulo Queue) \
que permite comunicación con decorador de logging.
        '''
        print("ejecución: Cliente_log")
        soc = socket.socket(socket.AF_INET, 
                            socket.SOCK_STREAM
        )
        soc.connect((cls.HOST, cls.PORT))
        sesion = f"---- INICIO SESION: {hora()} ----"
        sesion_ser = bytes(sesion, "utf-8")
        soc.send(sesion_ser)
        print("cliente a la espera")
        
        while True:
            item = cola.get()
            print("en el while cliente: ", item, type(item))
            if item[0] == "alta":
                mensaje = f"<Alta> Dosis: {item[1]}, \
Muertos: {item[2]} | {hora()}"
            elif item[0] == "baja":
                mensaje = f"<Baja> Dosis: {item[1]}, \
Muertos: {item[2]} | {hora()}"
            elif item[0] == "modif":
                mensaje = f"<Modificacion>  (Dosis: {item[3]}, \
Muertos: {item[4]}) => (Dosis: {item[1]}, Muertos: {item[2]}) | {hora()}"
            item_serial = bytes(mensaje, "utf-8")
            soc.sendall(item_serial)

    @staticmethod
    def lanzar_cliente(cola):
        '''
        Lanza el cliente en un hilo en segundo plano.

        :param cola: Recibe el objeto de clase queue (módulo Queue) \
que permite comunicación con decorador de logging.
        '''
        try:
            threading.Thread(target=Cliente.Cliente_log,
                            args=(cola,), 
                            daemon=True).start()
        except ConnectionError:
            print("Falló el cliente")


# Decorador logging
def enviar_log(
        id_item:str, 
        cola
    ):
    '''
    Función decoradora destinada a registrar actividad de los \
métodos de la clase CRUD.

    :param id_item: str que indica el método CRUD que se registrará.
    :param cola: Recibe el objeto de clase queue (módulo Queue) \
que permite comunicación con decorador de logging.
    '''
    def _cliente_log(func):
        def env(*args):
            consulta = args[0].__dict__
            if id_item == "alta":
                paquete = [id_item, 
                           consulta["dosis_var"].get(), 
                           consulta["muert_var"].get()
                ]
            elif id_item == "baja":
                selec = consulta["vista_ensayos"].focus()
                item = consulta["vista_ensayos"].item(selec)
                paquete = [id_item, 
                           item["values"][0], 
                           item["values"][1]
                ]
                print("\nDecorador:")
                print(paquete)
                print("\n")
            elif id_item == "modif":
                selec = consulta["vista_ensayos"].focus()
                item = consulta["vista_ensayos"].item(selec)
                paquete = [id_item, 
                           consulta["dosis_var"].get(),
                           consulta["muert_var"].get(),
                           item["values"][0], 
                           item["values"][1]
                ]
            cola.put(paquete)
            func(*args)
        return env
    return _cliente_log