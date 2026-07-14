import sqlite3
from tkinter import messagebox

def bd_inicializacion(guis):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    for gui in guis:
        # TABLAS
        columnas = gui.columnas[1:] # ignora id
        columnas_tipo = gui.columnas_tipo
        tabla = gui.tabla
        
        column_definitions = [f"{col} {tipo}" for col, tipo in zip(columnas, columnas_tipo)]
        columns_string = ", ".join(column_definitions)

        try:
            crear_tabla_sql = f"""CREATE TABLE if not exists {tabla} (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                {columns_string},
                {gui.columnas_extra}
                ) STRICT"""
        except AttributeError:
            crear_tabla_sql = f"""CREATE TABLE if not exists {tabla} (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                {columns_string}
                ) STRICT"""

        cursor.execute(crear_tabla_sql)
        
        # INSERTAR 
        columns_string = ", ".join(columnas)
        
        placeholders = ", ".join([f":{col}" for col in columnas])
        
        insertar_inicial = f"INSERT INTO {tabla} ({columns_string}) VALUES ({placeholders})"
        
        empleados_dict_list = []

        try:
            for empleado_tuple in gui.datos_iniciales:
                empleado_dict = {col: val for col, val in zip(columnas, empleado_tuple)}
                empleados_dict_list.append(empleado_dict)

            cursor.execute(f"SELECT * FROM {tabla}")
            if not cursor.fetchall(): # checks si ya esta insertado
                for empleado_data in empleados_dict_list:
                    cursor.execute(insertar_inicial, empleado_data)
        except AttributeError:
            pass
    
    conn.commit()
    conn.close()

def extraer_tabla(tabla):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + tabla)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos

def actualizar_registros_db(tabla, columnas, valores_entradas):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    oid = valores_entradas[0]
    valores = list(valores_entradas[1:])
    columnas = list(columnas[1:])

    #filtra los ""
    indices = [i for i, item in enumerate(valores) if item == '']
    for indice in sorted(indices, reverse=True):
        valores[indice] = None

    set_clause = ", ".join([f"{col} = :{col}" for col in columnas])

    sql = f"UPDATE {tabla} SET {set_clause} WHERE oid = :oid"

    params = {"oid": oid}
    params.update({col: val for col, val in zip(columnas, valores)})

    try:
        cursor.execute(sql, params)
        conn.commit()
    except sqlite3.IntegrityError as error:
        msg = str(error)
        if "NOT NULL constraint failed" in msg:
            messagebox.showerror("Error", "No lleno todos los campos obligatorios")
        elif "FOREIGN KEY constraint failed" in msg:
            messagebox.showerror("Error", "La ID ingresada no existe")
        else:
            messagebox.showerror("Error", msg)
    finally:
        conn.close()

def insertar_registro_db(tabla, columnas, valores_entradas):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    columnas = list(columnas[1:])

    #filtra los ""
    indices = [i for i, item in enumerate(valores_entradas) if item == ""]
    for indice in sorted(indices, reverse=True):
        columnas.pop(indice)
        valores_entradas.pop(indice)

    cols_clause = ", ".join(columnas)

    placeholders = ", ".join([f":{col}" for col in columnas])

    sql = f"INSERT INTO {tabla} ({cols_clause}) VALUES ({placeholders})"

    params = {col: val for col, val in zip(columnas, valores_entradas)}

    try:
        cursor.execute(sql, params)
        conn.commit()
    except sqlite3.IntegrityError as error:
        msg = str(error)
        if "NOT NULL constraint failed" in msg:
            messagebox.showerror("Error", "No lleno todos los campos obligatorios")
        elif "FOREIGN KEY constraint failed" in msg:
            messagebox.showerror("Error", "La ID ingresada no existe")
        else:
            messagebox.showerror("Error", msg)
    finally:
        conn.close()

def borrar_registros_db(tabla, registros_a_borrar):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    cursor.executemany("DELETE FROM " + tabla + " WHERE oid=?", [(id,) for id in registros_a_borrar]) #weird list thing

    conn.commit()
    conn.close()

def buscar_registros_db(tabla, columnas, valores_entradas):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    columnas = columnas[1:]
    
    condiciones = []
    params = []
    
    for campo, entrada in zip(columnas, valores_entradas):
        if entrada:  # si entrada no esta vacia
            condiciones.append(f"{campo} LIKE ?")
            params.append(entrada)
    
    sql = "SELECT * FROM " + tabla
    
    if condiciones:  # si hay al menos una entrada rellenada
        sql += " WHERE " + " AND ".join(condiciones)

    cursor.execute(sql, params)
    registros_encontrados = cursor.fetchall()

    conn.commit()
    conn.close()
    return registros_encontrados

def fechas_en_ticket():
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Fecha FROM Ticket")
    fechas = cursor.fetchall()

    conn.commit()
    conn.close()
    return fechas

def descontar_stock(menu_id, orden_cantidad):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Inventario_ID, Cantidad FROM Receta WHERE Menu_ID = ?", (menu_id,))
    receta_resultados = cursor.fetchall()
    
    for inventario_id, cantidad in receta_resultados:
        cursor.execute("SELECT Stock FROM Inventario WHERE ID = ?", (inventario_id,))
        resultado = cursor.fetchone()
        if resultado is None:
            continue 
        stock_actual = resultado[0]
        
        stock_descontar = (cantidad * orden_cantidad) / 1000 #pasa g a kg
        
        nuevo_stock = round(max(stock_actual - stock_descontar, 0), 2) #redondea decimales y pone 0 como minimo

        cursor.execute("UPDATE Inventario SET Stock = ? WHERE ID = ?", (nuevo_stock, inventario_id))
    
    conn.commit()
    conn.close()

def agregar_precio_ticket(menu_id, orden_cantidad, ticket_id):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Precio FROM Menu WHERE ID = ?", (menu_id,))
    menu_resultado = cursor.fetchone()
    if menu_resultado is None:
        conn.close()
        return 

    precio_a_sumar = round(menu_resultado[0] * orden_cantidad, 2)

    cursor.execute("SELECT Precio_Final FROM Ticket WHERE ID = ?", (ticket_id,))
    ticket_resultado = cursor.fetchone()
    precio_actual = ticket_resultado[0] if ticket_resultado and ticket_resultado[0] is not None else 0

    nuevo_precio = round(precio_actual + precio_a_sumar, 2)

    cursor.execute("UPDATE Ticket SET Precio_Final = ? WHERE ID = ?", (nuevo_precio, ticket_id))

    conn.commit()
    conn.close()

def ocupar_mesa(mesa_id):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT Estado FROM Mesa WHERE ID = ?", (mesa_id,))
    mesa_resultado = cursor.fetchone()

    if mesa_resultado[0] != "ocupado":
        cursor.execute("UPDATE Mesa SET Estado = ? WHERE ID = ?", ("ocupado", mesa_id))
    else:
        messagebox.showerror("Error", "Mesa Ocupada")
        conn.close()
        return True

    conn.commit()
    conn.close()
    return False

def finalizar_ticket(mesa_id, ticket_id):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE Mesa SET Estado = ? WHERE ID = ?", ("libre", mesa_id))

    cursor.execute("UPDATE Ticket SET Estado = ? WHERE ID = ?", ("finalizado", ticket_id))
    
    conn.commit()
    conn.close()

def agregar_precio_orden(menu_id, orden_cantidad):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Precio FROM Menu WHERE ID = ?", (menu_id,))
    menu_resultado = cursor.fetchone()
    if menu_resultado is None:
        conn.close()
        return 

    precio_orden = round(menu_resultado[0] * orden_cantidad, 2)

    cursor.execute("SELECT ID FROM Ordenes ORDER BY ID DESC LIMIT 1")
    ultimo_id = cursor.fetchone()

    cursor.execute("UPDATE Ordenes SET Precio_Total = ? WHERE ID = ?", (precio_orden, ultimo_id[0]))

    conn.commit()
    conn.close()

def estado_ticket(ticket_id):
    conn = sqlite3.connect("database/mesa10.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT Estado FROM Ticket WHERE ID = ?", (ticket_id,))
    ticket_resultado = cursor.fetchone()

    if ticket_resultado[0] == "finalizado":
        messagebox.showerror("Error", "Ticket esta finalizado")
        conn.close()
        return True

    conn.commit()
    conn.close()
    return False