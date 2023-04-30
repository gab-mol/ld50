class Sujeto:
    registro_observadores =[]

    def agregar_obs(self, objeto_seguido):
        self.registro_observadores.append(objeto_seguido)

    def informar_registro_obs(self, ref_met:str):
        if ref_met == "alta":
            self.registro_observadores[0].actualizacion()
        if ref_met == "baja":
            self.registro_observadores[1].actualizacion()
        if ref_met == "modif":
            self.registro_observadores[2].actualizacion()


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ObservadorCrudAlta(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.obj_observado.agregar_obs(self)

    def actualizacion(self):
        print("<<<Alta de ensayo>>>")
        print(f"Dosis= {self.obj_observado.dosis_var.get()} \
Muertos= {self.obj_observado.muert_var.get()} \
n= {self.obj_observado.n_var.get()} \
Unidad= {self.obj_observado.uni_var.get()}")


class ObservadorCrudBaja(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.obj_observado.agregar_obs(self)

    def actualizacion(self):
        print("<<<Baja de ensayo>>>")
        print(f"Eliminado => Dosis: {self.obj_observado.dosis_var.get()} \
(muertos: {self.obj_observado.muert_var.get()})")


class ObservadorCrudModificacion(Observador):
    def __init__(self, objeto):
        self.obj_observado = objeto
        self.obj_observado.agregar_obs(self)

    def actualizacion(self):
        print("<<<Modificación de ensayo>>>")
        print(f"Nuevos datos: Dosis= {self.obj_observado.dosis_var.get()} \
Muertos= {self.obj_observado.muert_var.get()} \
n= {self.obj_observado.n_var.get()} \
Unidad= {self.obj_observado.uni_var.get()}")