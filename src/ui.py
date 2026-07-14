from tkinter import *
from tkinter import ttk
from . import database


class TreeViewGUI:
    def __init__(self, root, columnas, tabla, treeview_colores, columnas_tipo):
        self.root = root
        self.columnas = columnas
        self.tabla = tabla
        self.treeview_colores = treeview_colores
        self.columnas_tipo = columnas_tipo

        self.main_frame = Frame(root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=4)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.tree_scroll = ttk.Scrollbar(self.main_frame)
        self.tree_scroll.grid(row=0, column=1, sticky="nsew")

        self.treeview = ttk.Treeview(
            self.main_frame,
            yscrollcommand=self.tree_scroll.set,
            selectmode="extended"
        )
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.treeview.tag_configure("oddrow", background=treeview_colores[0])
        self.treeview.tag_configure("evenrow", background=treeview_colores[1])
        self.tree_scroll.config(command=self.treeview.yview)
        self.treeview.bind("<ButtonRelease-1>", self.seleccion_registro)

        self.treeview["columns"] = self.columnas
        self.treeview.column("#0", width=0, stretch=NO)
        self.treeview.heading("#0", text="", anchor=W)

        for col in self.columnas:
            if col == "ID":
                self.treeview.column(col, anchor=CENTER, width=70)
                self.treeview.heading(col, text=col, anchor=CENTER)
            else:
                self.treeview.column(col, anchor=CENTER, width=140)
                self.treeview.heading(col, text=col.replace("_", " "), anchor=CENTER)

        self.entradas_frame = ttk.LabelFrame(self.main_frame, text="Entradas",style="Titulo.TLabelframe")
        self.entradas_frame.grid(row=1, column=0, sticky="nsew", padx=(4, 0))

        numero_columnas = min(((len(self.columnas)-1)*2), 8)

        for i in range(numero_columnas):
            self.entradas_frame.grid_columnconfigure(i, weight= 0 if i % 2 == 0 else 1)

        self.entries = {}
        row = 0
        col = 0
        for col_name in self.columnas:
            if col_name != "ID":
                label = ttk.Label(self.entradas_frame, text=col_name.replace("_", " "), style="Info.TLabel")
                label.grid(row=row, column=col, padx=5, pady=10, sticky=NSEW)
                entry = ttk.Entry(self.entradas_frame,style="Secundario.TEntry")
                entry.grid(row=row, column=col+1, padx=5, pady=10, sticky=NSEW)
                self.entries[col_name] = entry

                col += 2
                if col >= 8:  
                    row += 1
                    col = 0

        self.botones_frame = ttk.LabelFrame(self.main_frame, text="Opciones",style="Titulo.TLabelframe")
        self.botones_frame.grid(row=2, column=0, sticky="nsew", padx=(4, 0), pady=(0, 4))
        for i in range(5):
            self.botones_frame.columnconfigure(i, weight=1)

        btn = ttk.Button(self.botones_frame, text="Actualizar Registro", command=self.actualizar_registro, style="Secundario.TButton")
        btn.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        btn = ttk.Button(self.botones_frame, text="Agregar Registro", command=self.agregar_registro, style="Secundario.TButton")
        btn.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

        btn = ttk.Button(self.botones_frame, text="Borrar Registros", command=self.borrar_registros, style="Secundario.TButton")
        btn.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

        btn = ttk.Button(self.botones_frame, text="Vaciar Entradas", command=self.vaciar_entradas, style="Secundario.TButton")
        btn.grid(row=0, column=3, padx=10, pady=10, sticky=NSEW)

        btn = ttk.Button(self.botones_frame, text="Buscar Registros", command=self.buscar_registros, style="Secundario.TButton")
        btn.grid(row=0, column=4, padx=10, pady=10, sticky=NSEW)

        if self.tabla == "Ticket":
            btn = ttk.Button(self.botones_frame, text="Imprimir Ticket", command=self.imprimir_ticket, style="Imprimir.TButton")
            btn.grid(row=0, column=5, padx=10, pady=10, sticky=NSEW)

    def actualizar_tree(self):
        for registro in self.treeview.get_children():
            self.treeview.delete(registro)

        lista_db = database.extraer_tabla(self.tabla)

        for i, registro_db in enumerate(lista_db):
            registro = ["" if item is None else item for item in registro_db] #reemplaza null values
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert(
                parent="",
                index="end",
                iid=i,
                text="",
                values=registro[:len(self.columnas)],  # recorre los valores
                tags=(tag,)
            )

    def vaciar_entradas(self):
        for entry in self.entries.values():
            entry.delete(0, END)

    def seleccion_registro(self,e):
        self.vaciar_entradas()

        selecccion = self.treeview.focus()
        if selecccion: # previene seleccion null
            values = self.treeview.item(selecccion, "values")

            for i,entry in enumerate(self.entries.values()):
                entry.insert(0, values[i+1])
    
    def borrar_registros(self):
        registros_a_borrar = []
        registros = self.treeview.selection()
        for registro in registros:
            registros_a_borrar.append(self.treeview.item(registro, "values")[0])

        database.borrar_registros_db(self.tabla, registros_a_borrar)
    
        for registro in registros:
            self.treeview.delete(registro)
        
        self.actualizar_tree()
        self.vaciar_entradas()

    def actualizar_registro(self):
        seleccion_row = self.treeview.focus()
        if not seleccion_row: 
            return
        
        seleccion_id = self.treeview.item(seleccion_row, "values")[0]
        valores_entradas = [seleccion_id] + [entry.get() for entry in self.entries.values()]
        
        database.actualizar_registros_db(self.tabla, self.columnas, valores_entradas)

        self.actualizar_tree()
        self.vaciar_entradas()
    
    def agregar_registro(self):
        valores_entradas = [entry.get() for entry in self.entries.values()]

        if self.tabla == "Ordenes":
            ticket_id = valores_entradas[0]

            ticket_finalizado = database.estado_ticket(ticket_id)

            if ticket_finalizado == True: #no agrega ticket si la mesa esta ocupada
                self.vaciar_entradas()
                self.actualizar_tree()
                return

        if self.tabla == "Ticket":
            mesa_id = valores_entradas[0]
            mesa_ocupada = database.ocupar_mesa(mesa_id)

            if mesa_ocupada == True: #no agrega ticket si la mesa esta ocupada
                self.vaciar_entradas()
                self.actualizar_tree()
                return

        database.insertar_registro_db(self.tabla, self.columnas, valores_entradas)

        if self.tabla == "Ordenes":
            ticket_id = valores_entradas[0]
            menu_id = valores_entradas[1]
            orden_cantidad = float(valores_entradas[2])

            database.descontar_stock(menu_id, orden_cantidad)
            database.agregar_precio_ticket(menu_id, orden_cantidad,ticket_id)
            database.agregar_precio_orden(menu_id, orden_cantidad)

        self.vaciar_entradas()
        self.actualizar_tree()

    def buscar_registros(self):
        valores_entradas = [entry.get() for entry in self.entries.values()]
        registros_encontrados_db = database.buscar_registros_db(self.tabla, self.columnas, valores_entradas)

        for registro in self.treeview.get_children():
            self.treeview.delete(registro)

        for i, registro_db in enumerate(registros_encontrados_db):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.treeview.insert(
                parent="",
                index="end",
                iid=i,
                text="",
                values=registro_db[:len(self.columnas)],  # recorre los valores
                tags=(tag,)
            )

        self.vaciar_entradas()
    
    def imprimir_ticket(self):
        seleccion_row = self.treeview.focus()
        if not seleccion_row: 
            return
        
        ticket_id = self.treeview.item(seleccion_row, "values")[0]
        valores_entradas = [entry.get() for entry in self.entries.values()]

        mesa_id = valores_entradas[0]
        database.finalizar_ticket(mesa_id, ticket_id)

        self.vaciar_entradas()
        self.actualizar_tree()

def mostrar_gui(lista_guis, gui_seleccionado):
    for gui in lista_guis:
        try:
            gui.plot_graph() #actualizar grafico
        except:
            pass
        if gui is gui_seleccionado:
            try:
                gui.actualizar_tree()
            except AttributeError:
                pass
            gui.main_frame.grid()
        else:
            gui.main_frame.grid_remove()