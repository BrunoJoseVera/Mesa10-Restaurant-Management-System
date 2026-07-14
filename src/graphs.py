import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, date
from collections import Counter
import database

class GraphSemanal:
    def __init__(self, root):
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=4)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(14, 6.5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.plot_graph()

    def fechas_semana(self):
        try:
            fechas = database.fechas_en_ticket()
        except:
            return [0,0,0,0,0,0,0]

        # Convertir las cadenas a objetos datetime
        fechas_dt = [datetime.strptime(f[0], "%Y-%m-%d %H:%M:%S") for f in fechas]

        # Obtener el número de semana actual y año actual
        hoy = date.today()
        semana_actual = hoy.isocalendar().week
        anio_actual = hoy.isocalendar().year

        # Filtrar las fechas que están en la misma semana y año
        fechas_semana_actual = [
            f for f in fechas_dt
            if f.isocalendar().week == semana_actual and f.isocalendar().year == anio_actual
        ]

        # Diccionario de días en español
        dias_es = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miercoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sabado",
            "Sunday": "Domingo"
        }

        # Crear una lista con los nombres de los días (en español)
        dias_semana = [dias_es[f.strftime("%A")] for f in fechas_semana_actual]

        
        conteo = Counter(dias_semana)
        dias_ordenados = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        ordenes = [conteo.get(dia, 0) for dia in dias_ordenados]

        return ordenes

    def plot_graph(self):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        ordenes = self.fechas_semana()
        #ordenes = [23,17,30,26,47,65,38]

        self.ax.clear()

        bars = self.ax.bar(dias, ordenes, color="skyblue", edgecolor="black")

        self.ax.set_title("Tickets emitidos esta semana", fontsize=14, fontweight="bold")
        self.ax.set_xlabel("Días de la semana", fontsize=12)
        self.ax.set_ylabel("Número de tickets", fontsize=12)

        offset = max(ordenes) * 0.02  # 2% del valor máximo

        for bar, valor in zip(bars, ordenes):
            self.ax.text(bar.get_x() + bar.get_width()/2, valor + offset, str(valor),
                        ha="center", fontsize=10)


        self.canvas.draw()
