'''
**Módulo encargado de seguir el CRUD de la aplicación y conectarse con \
el servidor de logging. | "Calculadora-LD50".**
'''

class Sujeto:
    registro_observadores = []
    registro_referencias = []

    def agregar_obs(self, objeto_seguido, referencia):
        self.registro_observadores.append(objeto_seguido)
        self.registro_referencias.append(referencia)


    def informar_registro_obs(self, ref_met:str, *args):
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
            self.registro_observadores[1].actualizacion(*args)
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
        print(self.obj_observado)
        print(f"Dosis= {self.obj_observado.dosis_var.get()} \
Muertos= {self.obj_observado.muert_var.get()} \
n= {self.obj_observado.n_var.get()} \
Unidad= {self.obj_observado.uni_var.get()}")


class ObservadorCrudBaja(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.referencia_metodo = "baja"
        self.obj_observado.agregar_obs(self, self.referencia_metodo)

    def actualizacion(self, borrado):
        print("<<<Baja de ensayo>>>")
        item = borrado['values']
        print(f"Eliminado => Dosis: {item[0]} \
(muertos: {item[1]})")


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