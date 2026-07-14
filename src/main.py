from tkinter import *
from tkinter import ttk
import database
import styles
import graphs
import initial_data
from ui import TreeViewGUI, mostrar_gui

def main():
    root = Tk()
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.title("Mesa10")
    root.config(background="lightgrey")
    root.state('zoomed')
    root.minsize(1000, 500)

    styles.style_icons_init()
    root.iconphoto(False, styles.icon_mesa)

    empleados_columnas = ("ID", "Nombre", "Apellido", "DNI", "Direccion", "Telefono", "Cargo", "Horario")
    empleados_columnas_tipo = ("text NOT NULL","text NOT NULL","integer NOT NULL","text","text","text","text")
    empleados_tabla = "Empleado"
    empleados_treeview_colores = ("white", "#ADD8E6")

    empleados_gui = TreeViewGUI(root, empleados_columnas, empleados_tabla, empleados_treeview_colores,empleados_columnas_tipo)
    empleados_gui.datos_iniciales = initial_data.EMPLEADOS_INICIALES

    inventario_columnas = ("ID", "Nombre", "Stock", "Unidad", "Categoria", "Proveedor")
    inventario_columnas_tipo = ("text NOT NULL","real NOT NULL","text","text","text")
    inventario_tabla = "Inventario"
    inventario_treeview_colores = ("white", "#FFEFD5")

    inventario_gui = TreeViewGUI(root, inventario_columnas, inventario_tabla, inventario_treeview_colores,inventario_columnas_tipo)
    inventario_gui.datos_iniciales = initial_data.INVENTARIO_INICIAL

    menu_columnas = ("ID", "Nombre", "Precio", "Categoria")
    menu_columnas_tipo = ("text NOT NULL","real NOT NULL","text")
    menu_tabla = "Menu"
    menu_treeview_colores = ("white", "#C1E1C1")

    menu_gui = TreeViewGUI(root, menu_columnas, menu_tabla, menu_treeview_colores,menu_columnas_tipo)
    menu_gui.datos_iniciales = initial_data.MENU_INICIAL

    receta_columnas = ("ID", "Menu_ID", "Inventario_ID", "Cantidad", "Unidad")
    receta_columnas_tipo = ("integer NOT NULL","integer NOT NULL", "real NOT NULL", "text NOT NULL")
    receta_columnas_extra=("UNIQUE(Menu_ID, Inventario_ID),FOREIGN KEY (Menu_ID) REFERENCES Menu(ID),FOREIGN KEY (Inventario_ID) REFERENCES Inventario(ID)")
    receta_tabla = "Receta"
    receta_treeview_colores = ("white", "#AEC6CF")

    receta_gui = TreeViewGUI(root, receta_columnas, receta_tabla, receta_treeview_colores,receta_columnas_tipo)
    receta_gui.datos_iniciales = initial_data.RECETA_INICIAL
    receta_gui.columnas_extra = receta_columnas_extra

    mesa_columnas = ("ID", "Capacidad", "Estado")
    mesa_columnas_tipo = ("integer","text DEFAULT 'libre'")
    mesa_tabla = "Mesa"
    mesa_treeview_colores = ("white", "#F4C2C2")

    mesa_gui = TreeViewGUI(root, mesa_columnas, mesa_tabla, mesa_treeview_colores,mesa_columnas_tipo)
    mesa_gui.datos_iniciales = initial_data.MESA_INICIAL

    ticket_columnas = ("ID", "Mesa_ID", "Camarero_ID", "Fecha", "Precio_Final","Estado")
    ticket_columnas_tipo = ("integer NOT NULL","integer NOT NULL", "text DEFAULT CURRENT_TIMESTAMP", "real DEFAULT 0","text DEFAULT 'pendiente'")
    ticket_columnas_extra=("FOREIGN KEY (Mesa_ID) REFERENCES Mesa(ID), FOREIGN KEY (Camarero_ID) REFERENCES Empleado(ID)")
    ticket_tabla = "Ticket"
    ticket_treeview_colores = ("white", "#E6E6FA")

    ticket_gui = TreeViewGUI(root, ticket_columnas, ticket_tabla, ticket_treeview_colores,ticket_columnas_tipo)
    #ticket_gui.datos_iniciales = Mesa10_Datos.TICKET_INICIAL
    ticket_gui.columnas_extra = ticket_columnas_extra

    ordenes_columnas = ("ID", "Ticket_ID", "Menu_ID", "Cantidad", "Precio_Total","Nota")
    ordenes_columnas_tipo = ("integer NOT NULL","integer NOT NULL", "integer NOT NULL", "real DEFAULT 0","text")
    ordenes_columnas_extra=("FOREIGN KEY (Ticket_ID) REFERENCES Ticket(ID), FOREIGN KEY (Menu_ID) REFERENCES Menu(ID)")
    ordenes_tabla = "Ordenes"
    ordenes_treeview_colores = ("white", "#FFFACD")

    ordenes_gui = TreeViewGUI(root, ordenes_columnas, ordenes_tabla, ordenes_treeview_colores,ordenes_columnas_tipo)
    #ordenes_gui.datos_iniciales = Mesa10_Datos.ORDENES_INICIAL
    ordenes_gui.columnas_extra = ordenes_columnas_extra

    graph_gui = graphs.GraphSemanal(root)

    lista_guis = (empleados_gui, inventario_gui, menu_gui, graph_gui, mesa_gui,ticket_gui,ordenes_gui,receta_gui)
    lista_db = (empleados_gui, inventario_gui, menu_gui, mesa_gui,ticket_gui,ordenes_gui,receta_gui)

    opcion_frame = Frame(root, background="lightgrey")
    opcion_frame.grid(row=0, column=0, sticky="nsew")

    for i in range(8):
        opcion_frame.grid_columnconfigure(i, weight=1)
    opcion_frame.grid_rowconfigure(0, weight=1)

    opc1_boton = ttk.Button(opcion_frame, text=" Empleados", image=styles.icon_empleado, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, empleados_gui))
    opc1_boton.grid(row=0, column=0, padx=4, pady=5, sticky=NSEW)
    opc1_boton.image = styles.icon_empleado #previene perdida de imagen

    opc2_boton = ttk.Button(opcion_frame, text="Inventario", image=styles.icon_inventario, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, inventario_gui))
    opc2_boton.grid(row=0, column=1, padx=4, pady=5, sticky=NSEW)
    opc2_boton.image = styles.icon_inventario

    opc3_boton = ttk.Button(opcion_frame, text="Menu", image=styles.icon_menu, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, menu_gui))
    opc3_boton.grid(row=0, column=2, padx=4, pady=5, sticky=NSEW)
    opc3_boton.image = styles.icon_menu

    opc4_boton = ttk.Button(opcion_frame, text="Recetas", image=styles.icon_receta, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, receta_gui))
    opc4_boton.grid(row=0, column=3, padx=4, pady=5, sticky=NSEW)
    opc4_boton.image = styles.icon_receta

    opc5_boton = ttk.Button(opcion_frame, text="Mesas", image=styles.icon_mesas_boton, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, mesa_gui))
    opc5_boton.grid(row=0, column=4, padx=4, pady=5, sticky=NSEW)
    opc5_boton.image = styles.icon_mesas_boton

    opc6_boton = ttk.Button(opcion_frame, text="Tickets", image=styles.icon_ticket, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, ticket_gui))
    opc6_boton.grid(row=0, column=5, padx=4, pady=5, sticky=NSEW)
    opc6_boton.image = styles.icon_ticket

    opc7_boton = ttk.Button(opcion_frame, text="Ordenes", image=styles.icon_orden, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, ordenes_gui))
    opc7_boton.grid(row=0, column=6, padx=4, pady=5, sticky=NSEW)
    opc7_boton.image = styles.icon_orden

    opc8_boton = ttk.Button(opcion_frame, text="Datos", image=styles.icon_grafico, compound=LEFT, style="Principal.TButton", command=lambda: mostrar_gui(lista_guis, graph_gui))
    opc8_boton.grid(row=0, column=7, padx=4, pady=5, sticky=NSEW)
    opc8_boton.image = styles.icon_grafico
    

    database.bd_inicializacion(lista_db)

    for gui in lista_guis:
        try:
            gui.actualizar_tree()
        except AttributeError:
            pass
        gui.main_frame.grid_remove()
    
    empleados_gui.main_frame.grid()
        
    root.mainloop()

if __name__ == "__main__":
    main()
