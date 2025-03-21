import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import customtkinter as ctk

class AtrasosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Atrasos")
        self.root.geometry("1000x700")
        
        # Configurar tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configurar estilo para la tabla
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                      background="#2a2d2e",
                      foreground="white",
                      rowheight=25,
                      fieldbackground="#2a2d2e")
        style.configure("Treeview.Heading",
                       background="#1f6aa5",
                       foreground="white",
                       relief="flat")
        style.map("Treeview",
                 background=[('selected', '#1f6aa5')])

        # Lista de profesores y atrasos
        self.profesores = set()
        self.atrasos = []

        # Crear interfaz
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Sistema de Gestión de Atrasos",
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)

        # Botones
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=10)

        registrar_btn = ctk.CTkButton(btn_frame, text="Registrar Atraso",
                                    command=self.registrar_atraso,
                                    font=ctk.CTkFont(size=14))
        registrar_btn.pack(side=tk.LEFT, padx=10)

        reporte_btn = ctk.CTkButton(btn_frame, text="Reporte General",
                                  command=self.mostrar_reporte,
                                  font=ctk.CTkFont(size=14))
        reporte_btn.pack(side=tk.LEFT, padx=10)

        reporte_profesor_btn = ctk.CTkButton(btn_frame, text="Reporte por Profesor",
                                          command=self.mostrar_reporte_profesor,
                                          font=ctk.CTkFont(size=14))
        reporte_profesor_btn.pack(side=tk.LEFT, padx=10)

        # Botón de reinicio
        self.btn_reiniciar = ctk.CTkButton(
            main_frame,
            text="Reiniciar Registros",
            fg_color="#FF4444",
            hover_color="#CC0000",
            command=self.confirmar_reinicio
        )
        self.btn_reiniciar.pack(pady=10, padx=20, side="top", anchor="e")

        # Tabla de atrasos
        self.tree = ttk.Treeview(main_frame, columns=("Nombre", "Fecha", "Horario Programado", "Horario Real", "Atraso"),
                                show="headings", style="Treeview")
        
        # Configurar columnas
        for col in ("Nombre", "Fecha", "Horario Programado", "Horario Real", "Atraso"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def registrar_atraso(self):
        # Ventana para registrar atraso
        registrar_window = ctk.CTkToplevel(self.root)
        registrar_window.title("Registrar Atraso")
        registrar_window.geometry("500x400")

        # Frame para el formulario
        form_frame = ctk.CTkFrame(registrar_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Campos de entrada
        ctk.CTkLabel(form_frame, text="Nombre del Profesor:",
                    font=ctk.CTkFont(size=14)).pack(pady=5)
        
        # Combobox para profesores
        self.nombre_var = tk.StringVar()
        self.nombre_combo = ttk.Combobox(form_frame, textvariable=self.nombre_var,
                                  values=list(self.profesores) + ["Nuevo Profesor"])
        self.nombre_combo.pack(pady=5)

        # Campo para nuevo profesor
        self.nuevo_profesor_entry = ctk.CTkEntry(form_frame,
                                          font=ctk.CTkFont(size=14))
        self.nuevo_profesor_entry.pack(pady=5)
        self.nuevo_profesor_entry.pack_forget()

        def on_combo_select(event):
            if self.nombre_combo.get() == "Nuevo Profesor":
                self.nuevo_profesor_entry.pack(pady=5)
            else:
                self.nuevo_profesor_entry.pack_forget()

        self.nombre_combo.bind('<<ComboboxSelected>>', on_combo_select)

        # Selector de fecha
        ctk.CTkLabel(form_frame, text="Fecha:",
                    font=ctk.CTkFont(size=14)).pack(pady=5)
        self.fecha_entry = DateEntry(form_frame, width=20, background='darkblue',
                              foreground='white', borderwidth=2)
        self.fecha_entry.pack(pady=5)

        # Selectores de hora
        hora_frame = ctk.CTkFrame(form_frame)
        hora_frame.pack(pady=10)

        # Horario programado
        ctk.CTkLabel(hora_frame, text="Horario Programado:",
                    font=ctk.CTkFont(size=14)).pack(side=tk.LEFT, padx=5)
        self.horario_programado_entry = ttk.Spinbox(hora_frame, from_=0, to=23, width=3)
        self.horario_programado_entry.pack(side=tk.LEFT)
        ctk.CTkLabel(hora_frame, text=":",
                    font=ctk.CTkFont(size=14)).pack(side=tk.LEFT)
        self.min_programado_entry = ttk.Spinbox(hora_frame, from_=0, to=59, width=3)
        self.min_programado_entry.pack(side=tk.LEFT)

        # Horario real
        hora_real_frame = ctk.CTkFrame(form_frame)
        hora_real_frame.pack(pady=10)
        
        ctk.CTkLabel(hora_real_frame, text="Horario Real:",
                    font=ctk.CTkFont(size=14)).pack(side=tk.LEFT, padx=5)
        self.horario_real_entry = ttk.Spinbox(hora_real_frame, from_=0, to=23, width=3)
        self.horario_real_entry.pack(side=tk.LEFT)
        ctk.CTkLabel(hora_real_frame, text=":",
                    font=ctk.CTkFont(size=14)).pack(side=tk.LEFT)
        self.min_real_entry = ttk.Spinbox(hora_real_frame, from_=0, to=59, width=3)
        self.min_real_entry.pack(side=tk.LEFT)

        # Botón para guardar
        guardar_btn = ctk.CTkButton(
            form_frame,
            text="Guardar",
            command=self.guardar_atraso,
            font=ctk.CTkFont(size=14)
        )
        guardar_btn.pack(pady=20)

    def guardar_atraso(self):
        try:
            # Obtener valores del formulario
            nombre = self.nombre_var.get()
            if nombre == "Nuevo Profesor":
                nombre = self.nuevo_profesor_entry.get().strip()
                if not nombre:
                    messagebox.showerror("Error", "Debe ingresar el nombre del nuevo profesor.")
                    return
            
            fecha = self.fecha_entry.get_date().strftime("%Y-%m-%d")
            horario_programado = f"{self.horario_programado_entry.get()}:{self.min_programado_entry.get()}"
            horario_real = f"{self.horario_real_entry.get()}:{self.min_real_entry.get()}"

            # Validar que los campos no estén vacíos
            if not all([nombre, fecha, horario_programado, horario_real]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Calcular atraso
            h_prog = datetime.strptime(horario_programado, "%H:%M")
            h_real = datetime.strptime(horario_real, "%H:%M")
            diferencia = h_real - h_prog

            # Convertir a horas y minutos
            horas, segundos = divmod(diferencia.seconds, 3600)
            minutos, _ = divmod(segundos, 60)
            atraso = f"{horas}h {minutos}m"

            # Crear registro
            registro = {
                "nombre": nombre,
                "fecha": fecha,
                "horario_programado": horario_programado,
                "horario_real": horario_real,
                "atraso": atraso
            }
            self.atrasos.append(registro)

            # Agregar profesor si no existe
            if nombre not in self.profesores:
                self.profesores.add(nombre)
                # Actualizar combobox
                self.nombre_var.set("")  # Limpiar selección actual
                self.nombre_combo['values'] = list(self.profesores) + ["Nuevo Profesor"]

            # Actualizar tabla
            self.tree.insert("", tk.END, values=(nombre, fecha, horario_programado, horario_real, atraso))

            # Limpiar campos
            self.nombre_var.set("")
            self.nuevo_profesor_entry.delete(0, tk.END)
            self.nuevo_profesor_entry.pack_forget()  # Ocultar campo de nuevo profesor
            self.horario_programado_entry.set(0)
            self.min_programado_entry.set(0)
            self.horario_real_entry.set(0)
            self.min_real_entry.set(0)

            messagebox.showinfo("Éxito", "Atraso registrado correctamente.")

        except ValueError as e:
            messagebox.showerror("Error", "Formato de fecha u hora incorrecto.")

    def confirmar_reinicio(self):
        respuesta = messagebox.askyesno(
            "Confirmar Reinicio",
            "¿Está seguro que desea reiniciar todos los registros?\nEsta acción no se puede deshacer.",
            icon='warning'
        )
        if respuesta:
            self.reiniciar_registros()

    def reiniciar_registros(self):
        self.atrasos = []
        self.profesores = set()
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        messagebox.showinfo("Éxito", "Todos los registros han sido eliminados.")

    def mostrar_reporte(self):
        # Ventana para mostrar el reporte general
        reporte_window = ctk.CTkToplevel(self.root)
        reporte_window.title("Reporte General")
        reporte_window.geometry("1000x700")

        # Título
        ctk.CTkLabel(reporte_window, text="Reporte General de Atrasos",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

        # Tabla de reporte
        tree = ttk.Treeview(reporte_window,
                           columns=("Nombre", "Fecha", "Horario Programado", "Horario Real", "Atraso"),
                           show="headings",
                           style="Treeview")
        
        # Configurar columnas
        for col in ("Nombre", "Fecha", "Horario Programado", "Horario Real", "Atraso"):
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Llenar tabla
        for atraso in self.atrasos:
            tree.insert("", tk.END, values=(atraso["nombre"], atraso["fecha"], atraso["horario_programado"], atraso["horario_real"], atraso["atraso"]))

        # Calcular total de atraso
        total_horas = 0
        total_minutos = 0
        for atraso in self.atrasos:
            horas = int(atraso["atraso"].split('h')[0])
            minutos = int(atraso["atraso"].split('h')[1].split('m')[0])
            total_horas += horas
            total_minutos += minutos

        total_horas += total_minutos // 60
        total_minutos = total_minutos % 60

        # Mostrar total
        ctk.CTkLabel(reporte_window, text=f"Total de Atraso: {total_horas}h {total_minutos}m",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

    def mostrar_reporte_profesor(self):
        if not self.profesores:
            messagebox.showwarning("Aviso", "No hay profesores registrados")
            return

        # Ventana para seleccionar profesor
        selector_window = ctk.CTkToplevel(self.root)
        selector_window.title("Seleccionar Profesor")
        selector_window.geometry("400x200")

        # Frame para el selector
        select_frame = ctk.CTkFrame(selector_window)
        select_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(select_frame, text="Seleccione un Profesor:",
                    font=ctk.CTkFont(size=14)).pack(pady=10)

        # Combobox para profesores
        profesor_var = tk.StringVar()
        profesor_combo = ttk.Combobox(select_frame, textvariable=profesor_var,
                                    values=list(self.profesores))
        profesor_combo.pack(pady=10)

        def generar_reporte():
            profesor = profesor_var.get()
            if not profesor:
                messagebox.showwarning("Aviso", "Por favor seleccione un profesor")
                return
            
            selector_window.destroy()
            self.generar_reporte_profesor(profesor)

        # Botón para generar reporte
        ctk.CTkButton(select_frame, text="Generar Reporte",
                     command=generar_reporte,
                     font=ctk.CTkFont(size=14)).pack(pady=10)

    def generar_reporte_profesor(self, profesor):
        # Ventana para mostrar el reporte del profesor
        reporte_window = ctk.CTkToplevel(self.root)
        reporte_window.title(f"Reporte de Atrasos - {profesor}")
        reporte_window.geometry("1000x700")

        # Frame principal
        main_frame = ctk.CTkFrame(reporte_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(main_frame, text=f"Reporte de Atrasos - {profesor}",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

        # Tabla de reporte
        tree = ttk.Treeview(main_frame,
                           columns=("Fecha", "Horario Programado", "Horario Real", "Atraso"),
                           show="headings",
                           style="Treeview")
        
        # Configurar columnas
        tree.heading("Fecha", text="Fecha")
        tree.heading("Horario Programado", text="Horario Programado")
        tree.heading("Horario Real", text="Horario Real")
        tree.heading("Atraso", text="Atraso")

        for col in ("Fecha", "Horario Programado", "Horario Real", "Atraso"):
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Filtrar atrasos del profesor
        atrasos_profesor = [atraso for atraso in self.atrasos if atraso["nombre"] == profesor]

        # Ordenar por fecha
        atrasos_profesor.sort(key=lambda x: x["fecha"])

        # Llenar tabla
        for atraso in atrasos_profesor:
            tree.insert("", tk.END, values=(
                atraso["fecha"].strftime("%Y-%m-%d"),
                atraso["horario_programado"].strftime("%H:%M"),
                atraso["horario_real"].strftime("%H:%M"),
                atraso["atraso"]
            ))

        # Calcular total de atraso
        total_horas = 0
        total_minutos = 0
        for atraso in atrasos_profesor:
            horas = int(atraso["atraso"].split('h')[0])
            minutos = int(atraso["atraso"].split('h')[1].split('m')[0])
            total_horas += horas
            total_minutos += minutos

        total_horas += total_minutos // 60
        total_minutos = total_minutos % 60

        # Frame para el resumen
        resumen_frame = ctk.CTkFrame(main_frame)
        resumen_frame.pack(fill=tk.X, pady=10)

        # Mostrar resumen
        ctk.CTkLabel(resumen_frame, text="Resumen:",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        ctk.CTkLabel(resumen_frame, 
                    text=f"Total de registros: {len(atrasos_profesor)}",
                    font=ctk.CTkFont(size=14)).pack(pady=2)
        
        ctk.CTkLabel(resumen_frame,
                    text=f"Total de atrasos acumulados: {total_horas}h {total_minutos}m",
                    font=ctk.CTkFont(size=14)).pack(pady=2)

if __name__ == "__main__":
    root = ctk.CTk()
    app = AtrasosApp(root)
    root.mainloop()
