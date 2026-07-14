from tkinter import ttk
from PIL import Image, ImageTk

def style_icons_init():
    
    # ICONOS

    global icon_empleado, icon_inventario, icon_menu, icon_grafico, icon_mesa, icon_mesas_boton, icon_ticket, icon_orden, icon_receta

    image = Image.open('assets/icons/empleado.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_empleado = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/inventario.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_inventario = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/menu.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_menu = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/mesas_boton.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_mesas_boton = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/ticket.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_ticket = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/orden.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_orden = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/receta.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_receta = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/grafico.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_grafico = ImageTk.PhotoImage(image)

    image = Image.open('assets/icons/mesa.png')
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    icon_mesa = ImageTk.PhotoImage(image)

    # ESTILOS

    style=ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#E0E0E0", # D3D3D3 , F5F5F5
                    font=("Segoe UI",11))
    style.map("Treeview", background=[("selected","#347083")])
    style.configure("Treeview.Heading", font=("Celvetica", 11, "bold"))

    style.configure(
        "Principal.TButton",
        font=("Segoe UI", 14, "bold"),
        foreground="black",
        background="#d9eaf7",    
        padding=12,
        borderwidth=3,             
        relief="raised"            
    )
    style.map(
        "TButton",
        background=[("active", "#b0d4f1"), ("pressed", "#8ac1e3")],
        relief=[("pressed", "sunken"), ("!pressed", "raised")],
        foreground=[("active", "black"), ("pressed", "black")]
    )
    
    style.configure(
        "Secundario.TButton",
        font=("Segoe UI", 10),
        foreground="black",
        background="#f0f0f0",   
        padding=6,              
        borderwidth=2,
        relief="raised"
    )

    style.map(
        "Secundario.TButton",
        background=[("active", "#e0e0e0"), ("pressed", "#cfcfcf")],
        relief=[("pressed", "sunken"), ("!pressed", "raised")],
        foreground=[("active", "black"), ("pressed", "black")]
    )

    style.configure(
        "Imprimir.TButton",
        font=("Segoe UI", 10, "bold"),
        foreground="black",
        background="#d9eaf7",    
        padding=6,
        borderwidth=2,             
        relief="raised"            
    )
    style.map(
        "TButton",
        background=[("active", "#b0d4f1"), ("pressed", "#8ac1e3")],
        relief=[("pressed", "sunken"), ("!pressed", "raised")],
        foreground=[("active", "black"), ("pressed", "black")]
    )

    style.configure(
        "Info.TLabel",
        font=("Segoe UI", 11),
        foreground="#333333",     
        background="#f7f9fb",     
        padding=4
    )

    style.configure(
        "Secundario.TEntry",
        font=("Helvetica", 11),
        foreground="black",
        fieldbackground="#ffffff",  
        background="#d9eaf7",        
        padding=6,
        relief="solid"
    )

    style.map(
        "Secundario.TEntry",
        fieldbackground=[
            ("active", "#f2faff"),   
            ("focus", "#ffffff")   
        ],
        bordercolor=[
            ("focus", "#8ac1e3"),   
            ("!focus", "#d9eaf7")
        ]
    )

    style.configure(
        "Titulo.TLabelframe",
        background="#f7f9fb",     
        borderwidth=3,
        relief="groove"           
    )

    style.configure(
        "Titulo.TLabelframe.Label", 
        font=("Segoe UI", 11, "bold"),
        background="#f7f9fb",
        foreground="#1a1a1a"
    )