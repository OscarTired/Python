import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from datetime import datetime
from dueno import Dueño
from mascota_factory import MascotaFactory

class RegistroMascotasGUI:
    def __init__(self, root):
        self._root = root
        self._root.title("Registro de Atención de Mascotas")
        self._registros = []  # Lista para guardar los registros
        self._dueños = {}  # Diccionario para guardar información de dueños

        self._tipo_animal_ventana = {
            "Gato": self.abrir_ventana_gato,
            "Perro": self.abrir_ventana_perro,
            "Conejo": self.abrir_ventana_conejo,
            "Loro": self.abrir_ventana_loro,
            "Otro": self.abrir_ventana_otro
        }

        self.init_gui()

    def init_gui(self):
        self._tab_control = ttk.Notebook(self._root)

        self._tab1 = tk.Frame(self._tab_control)
        self._tab2 = tk.Frame(self._tab_control)

        self._tab_control.add(self._tab1, text="Registro")
        self._tab_control.add(self._tab2, text="Historial")
        self._tab_control.pack(expand=1, fill="both")

        self.crear_tab1()
        self.crear_tab2()

    def crear_tab1(self):
        # Crear labels y entries para nombres, edad, peso, dieta
        self._label_nombres = tk.Label(self._tab1, text="Nombres:")
        self._entry_nombres = tk.Entry(self._tab1)

        self._label_apellidos = tk.Label(self._tab1, text="Apellidos:")
        self._entry_apellidos = tk.Entry(self._tab1)

        self._label_dni = tk.Label(self._tab1, text="DNI:")
        self._entry_dni = tk.Entry(self._tab1)

        # Combobox para seleccionar tipo de animal
        self._label_tipo = tk.Label(self._tab1, text="Tipo de Animal:")
        self._cbox_tipo = ttk.Combobox(self._tab1, values=list(self._tipo_animal_ventana.keys()))

        # Botón para abrir ventana de registro
        btn_registrar = tk.Button(self._tab1, text="Registrar", command=lambda: self.abrir_ventana_registro(self._cbox_tipo.get()))

        # Posicionamiento de los widgets
        self._label_nombres.grid(row=0, column=0)
        self._entry_nombres.grid(row=0, column=1)
        self._label_apellidos.grid(row=1, column=0)
        self._entry_apellidos.grid(row=1, column=1)
        self._label_dni.grid(row=2, column=0)
        self._entry_dni.grid(row=2, column=1)
        self._label_tipo.grid(row=3, column=0)
        self._cbox_tipo.grid(row=3, column=1)
        btn_registrar.grid(row=4, columnspan=2)

    def crear_tab2(self):
        self._label_buscar = tk.Label(self._tab2, text="Buscar:")
        self._entry_buscar = tk.Entry(self._tab2)
        btn_buscar = tk.Button(self._tab2, text="Buscar", command=self.buscar_en_registros)
        self._listbox = tk.Listbox(self._tab2, width=150)  # Aumenta el ancho de la lista
        self._label_buscar.grid(row=0, column=0)
        self._entry_buscar.grid(row=0, column=1)
        btn_buscar.grid(row=1, columnspan=2)
        self._listbox.grid(row=2, columnspan=2)
        self._listbox.bind("<Double-Button-1>", self.on_double_click)

        # Botón para exportar los datos a un archivo de texto
        btn_exportar = tk.Button(self._tab2, text="Exportar txt", command=self.exportar_txt)
        btn_exportar.grid(row=3, column=1)

    def abrir_ventana_registro(self, tipo):
        if tipo in self._tipo_animal_ventana:
            self._tipo_animal_ventana[tipo]()

    def abrir_ventana_gato(self):
        self.abrir_ventana_mascota("Gato")

    def abrir_ventana_perro(self):
        self.abrir_ventana_mascota("Perro")

    def abrir_ventana_conejo(self):
        self.abrir_ventana_mascota("Conejo")

    def abrir_ventana_loro(self):
        self.abrir_ventana_mascota("Loro")

    def abrir_ventana_otro(self):
        self.abrir_ventana_mascota("Otro")

    def abrir_ventana_mascota(self, tipo):
        top = tk.Toplevel(self._root)
        top.title(f"Registro de {tipo}")
        self.crear_formulario_registro(top, tipo)

    def crear_formulario_registro(self, top, tipo):
        label_nombre = tk.Label(top, text="Nombre:")
        entry_nombre = tk.Entry(top)
        label_edad = tk.Label(top, text="Edad:")
        entry_edad = tk.Entry(top)
        label_peso = tk.Label(top, text="Peso:")
        entry_peso = tk.Entry(top)
        label_dieta = tk.Label(top, text="Dieta:")
        entry_dieta = tk.Entry(top)
        label_tipo_atencion = tk.Label(top, text="Tipo de Atención:")
        entry_tipo_atencion = tk.Entry(top)

        label_nombre.grid(row=0, column=0)
        entry_nombre.grid(row=0, column=1)
        label_edad.grid(row=1, column=0)
        entry_edad.grid(row=1, column=1)
        label_peso.grid(row=2, column=0)
        entry_peso.grid(row=2, column=1)
        label_dieta.grid(row=3, column=0)
        entry_dieta.grid(row=3, column=1)
        label_tipo_atencion.grid(row=4, column=0)
        entry_tipo_atencion.grid(row=4, column=1)

        extra_label = None
        extra_entry = None

        if tipo == "Gato":
            extra_label = tk.Label(top, text="Cantidad de Maullidos:")
            extra_entry = tk.Entry(top)
        elif tipo == "Perro":
            extra_label = tk.Label(top, text="Cantidad de Ladridos:")
            extra_entry = tk.Entry(top)
        elif tipo == "Conejo":
            extra_label = tk.Label(top, text="Altura de Salto (cm):")
            extra_entry = tk.Entry(top)
        elif tipo == "Loro":
            extra_label = tk.Label(top, text="Diámetro de Alas (cm):")
            extra_entry = tk.Entry(top)
        elif tipo == "Otro":
            extra_label = tk.Label(top, text="Tipo de animal:")
            extra_entry = tk.Entry(top)

        if extra_label and extra_entry:
            extra_label.grid(row=5, column=0)
            extra_entry.grid(row=5, column=1)

        btn_registrar = tk.Button(top, text="Registrar", command=lambda: self.registrar_mascota(
            entry_nombre.get(), entry_edad.get(), entry_peso.get(), entry_dieta.get(), entry_tipo_atencion.get(), extra_entry.get() if extra_entry else None, tipo))

        btn_registrar.grid(row=6, columnspan=2)
        
        if tipo.lower() == "gato":
            self._entry_maullidos = extra_entry
        elif tipo.lower() == "perro":
            self._entry_ladridos = extra_entry
        elif tipo.lower() == "loro":
            self._entry_alas = extra_entry
        elif tipo.lower() == "conejo":
            self._entry_salto = extra_entry
        else:
            self._entry_nombre = entry_nombre
            self._entry_edad = entry_edad
            self._entry_peso = entry_peso
            self._entry_dieta = entry_dieta
            self._entry_tipo_atencion = entry_tipo_atencion


    def registrar_mascota(self, nombre, edad, peso, dieta, tipo_atencion, extra_attr, tipo):
        if not all([nombre, edad, peso, dieta, tipo_atencion]):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        
        self.guardar_datos()
        
        # Crear un dueño con los datos del formulario
        dueño = Dueño(self._entry_nombres.get(), self._entry_apellidos.get(), self._entry_dni.get())
        

        # Generar un ID único
        registro_id = f"ID: {str(len(self._registros) + 1).zfill(3)}"
        

        # Crear una mascota con los datos del formulario y el dueño        
    
        
        if extra_attr:  # Solo pasa el atributo extra si no es None
            mascota = MascotaFactory.create_mascota(tipo, nombre, edad, peso, dieta, tipo_atencion, extra_attr)
        else:
            mascota = MascotaFactory.create_mascota(tipo, nombre, edad, peso, dieta, tipo_atencion)
            dueño.asignar_mascota(mascota)

        # Agregar el registro a la lista de registros
        fecha_registro = str(datetime.now())
        self._registros.append({"id": registro_id, "mascota": mascota, "dueño": dueño, "fecha_registro": fecha_registro})

        # Limpiar los campos de entrada en el formulario
        self.clear_fields(tipo.lower())

        self.guardar_datos()

    def clear_fields(self, tipo):
        if tipo == "gato":
            self._entry_maullidos.delete(0, tk.END)
        elif tipo == "perro":
            self._entry_ladridos.delete(0, tk.END)
        elif tipo == "loro":
            self._entry_alas.delete(0, tk.END)
        elif tipo == "conejo":
            self._entry_salto.delete(0, tk.END)
        else:
            self._entry_nombre.delete(0, tk.END)
            self._entry_edad.delete(0, tk.END)
            self._entry_peso.delete(0, tk.END)
            self._entry_dieta.delete(0, tk.END)
            self._entry_tipo_atencion.delete(0, tk.END)

    def guardar_datos(self):
        data = []
        for registro in self._registros:
            mascota = registro["mascota"]
            dueño = registro["dueño"]
            fecha_registro = registro["fecha_registro"]
            data.append({
                "id": registro["id"],
                "fecha_registro": fecha_registro,
                "mascota": {
                    "nombre": mascota.nombre,
                    "edad": mascota.edad,
                    "peso": mascota.peso,
                    "dieta": mascota.dieta,
                    "tipo_atencion": mascota._tipo_atencion,
                    "extra_attr": mascota._extra_attr if hasattr(mascota, "_extra_attr") else None,
                    "altura_salto": mascota._altura_salto if hasattr(mascota, "_altura_salto") else None,
                    "cantidad_maullidos": mascota._cantidad_maullidos if hasattr(mascota, "cantidad_maullidos") else None,
                    "cantidad_ladridos": mascota._cantidad_ladridos if hasattr(mascota, "_cantidad_ladridos") else None,
                    "diametro_alas": mascota._diametro_alas if hasattr(mascota, "_diametro_alas") else None,
                    "tipo": type(mascota).__name__
                },
                "dueño": {
                    "nombres": dueño._nombres,
                    "apellidos": dueño._apellidos,
                    "dni": dueño._dni
                }
            })
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def exportar_txt(self):
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
        with open('data.txt', 'w') as txt_file:
            for registro in data:
                txt_file.write("Registro: {}\n".format(registro["id"]))
                txt_file.write("Dueño: {} {}\n".format(registro["dueño"]["nombres"], registro["dueño"]["apellidos"]))
                txt_file.write("DNI: {}\n".format(registro["dueño"]["dni"]))
                txt_file.write("Mascota: {} ({})\n".format(registro["mascota"]["nombre"], registro["mascota"]["tipo"]))
                txt_file.write("Edad: {}\n".format(registro["mascota"]["edad"]))
                txt_file.write("Peso: {}\n".format(registro["mascota"]["peso"]))
                txt_file.write("Dieta: {}\n".format(registro["mascota"]["dieta"]))
                txt_file.write("Tipo de Atención: {}\n".format(registro["mascota"]["tipo_atencion"]))
                if registro["mascota"]["extra_attr"]:
                    txt_file.write("Atributo Extra: {}\n".format(registro["mascota"]["extra_attr"]))
                txt_file.write("Fecha registro: {}\n".format(registro["fecha_registro"]))
                txt_file.write("\n")

    def buscar_en_registros(self):
        if os.path.exists('data.json'):
            with open('data.json', 'r') as json_file:      
                data = json.load(json_file)
            self._registros = []
            for registro in data:
                dueño_data = registro["dueño"]
                dueño = Dueño(dueño_data["nombres"], dueño_data["apellidos"], dueño_data["dni"])
                mascota_data = registro["mascota"]
                mascota = MascotaFactory.create_mascota(mascota_data["tipo"], mascota_data["nombre"], mascota_data["edad"], mascota_data["peso"], mascota_data["dieta"], mascota_data["tipo_atencion"], mascota_data["extra_attr"])
                dueño.asignar_mascota(mascota)
                self._registros.append({"id": registro["id"], "mascota": mascota, "dueño": dueño, "fecha_registro": registro["fecha_registro"]})
            busqueda = self._entry_buscar.get().lower()
            resultados = []

        for registro in self._registros:     
            if busqueda in registro["mascota"].nombre.lower() or busqueda in registro["dueño"]._dni:
                resultados.append(registro["id"] + " - " + registro["mascota"].nombre)

        self._listbox.delete(0, tk.END)
        for resultado in resultados:
            self._listbox.insert(tk.END, resultado)

    def on_double_click(self, event):
        item = self._listbox.get(self._listbox.curselection()[0])
        for registro in self._registros:
            if item == registro["id"] + " - " + registro["mascota"].nombre:
                top = tk.Toplevel(self._root)
                top.geometry("400x200")
                top.title(f"Información de {registro['mascota'].nombre}")
                tk.Label(top, text=f"Nombre de la Mascota: {registro['mascota'].nombre}").pack()
                tk.Label(top, text=f"Edad: {registro['mascota'].edad}").pack()
                tk.Label(top, text=f"Peso: {registro['mascota'].peso}").pack()
                tk.Label(top, text=f"Dieta: {registro['mascota'].dieta}").pack()
                tk.Label(top, text=f"Tipo de Atención: {registro['mascota']._tipo_atencion}").pack()

                if hasattr(registro['mascota'], "_cantidad_maullidos"):
                    tk.Label(top, text=f"Maullidos: {registro['mascota']._cantidad_maullidos}").pack()

                if hasattr(registro['mascota'], "_extra_attr"):
                    tk.Label(top, text=f"Atributo Extra: {registro['mascota']._extra_attr}").pack()
                    
                if hasattr(registro['mascota'], "_cantidad_ladridos"):
                    tk.Label(top, text=f"Cantidad de Ladridos: {registro['mascota']._cantidad_ladridos}").pack()

                if hasattr(registro['mascota'], "_altura_salto"):
                    tk.Label(top, text=f"Altura Salto: {registro['mascota']._altura_salto}").pack()
                    
                    
                if hasattr(registro['mascota'], "_diametro_alas"):
                    tk.Label(top, text=f"Diámetro de Alas (cm): {registro['mascota']._diametro_alas}").pack()
                    
                    
                tk.Label(top, text=f"Nombre del Dueño: {registro['dueño']._nombres} {registro['dueño']._apellidos}").pack()
                tk.Label(top, text=f"DNI del Dueño: {registro['dueño']._dni}").pack()
                tk.Label(top, text=f"Fecha de Registro: {str(registro['fecha_registro'])}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroMascotasGUI(root)
    root.mainloop()
