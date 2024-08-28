import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import holidays


# Configuración de la conexión a la base de datos
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-ODPOVVB\\SQLEXPRESS;'
    'DATABASE=chifa;'
    'Trusted_Connection=yes;'
)

# Días festivos Perú (se puede cambiar el país)
peru_holidays = holidays.Peru(years=[2024])  # se puede añadir mas años


def obtener_fecha_id(fecha):
    cursor = conn.cursor()

    # Buscar el ID de la fecha en la tabla Dim_Fecha
    cursor.execute("SELECT id FROM Dim_Fecha WHERE fecha = ?", fecha)
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        # Determinar si la fecha es festiva
        es_festivo = 1 if fecha in peru_holidays else 0
        # Si la fecha no existe, inserta la nueva fecha y devuelve el ID
        cursor.execute("""
            INSERT INTO Dim_Fecha (fecha, dia, mes, año, trimestre, dia_semana, es_festivo, nombre_mes)
            OUTPUT INSERTED.id
            VALUES (?, DAY(?), MONTH(?), YEAR(?), DATEPART(QUARTER, ?), DATENAME(WEEKDAY, ?), 0, DATENAME(MONTH, ?))
        """, fecha, fecha, fecha, fecha, fecha, fecha, fecha)
        return cursor.fetchone()[0]


# Función para obtener el ID del producto por nombre
def obtener_producto_id(nombre_producto):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Dim_Producto WHERE nombre = ?", nombre_producto)
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

# Función para insertar datos en la base de datos
def insertar_pedido(cliente, pedido, detalles):
    cursor = conn.cursor()

    # Obtener el ID de la fecha
    fecha_id = obtener_fecha_id(pedido['fecha_id'])

    # Insertar cliente y obtener el ID
    cursor.execute("""
        INSERT INTO Dim_Cliente (nombre, apellido, DNI, RUC, email, telefono, direccion)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, cliente['nombre'], cliente['apellido'], cliente['DNI'], cliente['RUC'], cliente['email'], cliente['telefono'], cliente['direccion'])
    cliente_id = cursor.fetchone()[0]

    # Verificar si el empleado existe
    cursor.execute("SELECT id FROM Dim_Empleado WHERE id = ?", pedido['empleado_id'])
    empleado = cursor.fetchone()
    if not empleado:
        st.error(f"Error: Empleado con ID {pedido['empleado_id']} no encontrado.")
        return
    empleado_id = empleado[0]

    # Insertar pedido y obtener el ID
    cursor.execute("""
        INSERT INTO Fact_Pedidos (fecha_id, cliente_id, empleado_id, sucursal_id, tipo_pedido, tipo_pago, cantidad_total, precio_total)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    fecha_id,  #ID de la fecha obtenido
    cliente_id, 
    empleado_id, 
    pedido['sucursal_id'],
    pedido['tipo_pedido'], 
    pedido['tipo_pago'], 
    pedido['cantidad_total'], 
    pedido['precio_total'])
    
    pedido_id = cursor.fetchone()[0]

    # Insertar detalles del pedido
    for detalle in detalles:
        producto_id = detalle['producto_id']
        if producto_id is not None:
            #Insertar detalle del pedido
            cursor.execute("""
                INSERT INTO Fact_DetallePedidos (pedido_id, producto_id, cantidad, precio_unitario, precio_total)
                VALUES (?, ?, ?, ?, ?)
            """, pedido_id, producto_id, detalle['cantidad'], detalle['precio_unitario'], detalle['precio_total'])           
            # Actualizar stock Dim_Producto
            cursor.execute("""
                UPDATE Dim_Producto
                SET stock_actual = stock_actual - ?
                WHERE id = ?
            """, detalle['cantidad'], producto_id)
        else:
            st.error("Error: Producto no encontrado.")

    conn.commit()
    return pedido_id


# Función para generar el comprobante de pago en PDF
def generar_comprobante(cliente, pedido, detalles, pedido_id):
    # Obtener el nombre de la sucursal
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM Dim_Sucursal WHERE id = ?", pedido['sucursal_id'])
    sucursal_nombre = cursor.fetchone()[0]
    
    c = canvas.Canvas(f"comprobante_{pedido_id}.pdf", pagesize=letter)
    c.drawString(100, 750, "Comprobante de Pago")
    c.drawString(100, 730, f"Cliente: {cliente['nombre']} {cliente['apellido']}")
    c.drawString(100, 710, f"DNI: {cliente['DNI']}")
    c.drawString(100, 690, f"RUC: {cliente['RUC']}")
    c.drawString(100, 670, f"Fecha: {pedido['fecha_id']}")
    c.drawString(100, 650, f"Tipo de Pedido: {pedido['tipo_pedido']}")
    c.drawString(100, 630, f"Sucursal: {sucursal_nombre}")
    c.drawString(100, 610, f"Tipo de Pago: {pedido['tipo_pago']}")
    c.drawString(100, 590, f"Cantidad Total: {pedido['cantidad_total']}")
    c.drawString(100, 570, f"Precio Total: {pedido['precio_total']:.2f}")

    y = 550
    for detalle in detalles:
        c.drawString(100, y, f"Producto: {detalle['producto_id']}, Cantidad: {detalle['cantidad']}, Precio Unitario: {detalle['precio_unitario']:.2f}, Precio Total: {detalle['precio_total']:.2f}")
        y -= 20

    c.save()

# Interfaz de Streamlit
st.title('Sistema de Pedidos')

# Selección de la sucursal
st.header('Seleccionar Sucursal')
sucursales = {
    'Sucursal Miraflores': 1,
    'Sucursal San Isidro': 2,
    'Sucursal Surco': 3
}
sucursal_nombre = st.selectbox('Sucursal', list(sucursales.keys()))
sucursal_id = sucursales[sucursal_nombre]

# Formulario de cliente
st.header('Datos del Cliente')
cliente = {
    'nombre': st.text_input('Nombre'),
    'apellido': st.text_input('Apellido'),
    'DNI': st.text_input('DNI'),
    'RUC': st.text_input('RUC'),
    'email': st.text_input('Email'),
    'telefono': st.text_input('Teléfono'),
    'direccion': st.text_input('Dirección')
}

# Formulario de pedido
st.header('Datos del Pedido')
pedido = {
    'fecha_id': datetime.now().strftime('%Y-%m-%d'),
    'empleado_id': None,
    'sucursal_id': sucursal_id,
    'tipo_pedido': st.selectbox('Tipo de Pedido', ['En el Local', 'Delivery']),
    'tipo_pago': st.selectbox('Tipo de Pago', ['Tarjeta de Crédito/Débito', 'Efectivo', 'Yape/Plin']),
    'cantidad_total': 0,
    'precio_total': 0.0
}

# Selección del empleado según el tipo de pedido
if pedido['tipo_pedido'] == 'En el Local':
    empleados = {
        'Juan Perez': 1,
        'Maria Lopez': 2,
        'Carlos Gomez': 3,
        'Ana Martinez': 4
    }
else:
    empleados = {
        'Luis Garcia': 5,
        'Pedro Rodriguez': 6
    }
empleado_nombre = st.selectbox('Empleado', list(empleados.keys()))
pedido['empleado_id'] = empleados[empleado_nombre]

# Formulario de detalles del pedido
st.header('Detalles del Pedido')
categorias = st.multiselect('Categorías', ['Aperitivo', 'Plato Fondo', 'Postres y Bebidas'])
productos = {
    'Aperitivo': [
        {'nombre': 'Porcion de Wantan 5 unidades', 'precio': 7.00},
        {'nombre': 'Tequeños 5 unidades', 'precio': 5.00},
        {'nombre': 'Sopa Wantan', 'precio': 5.00}
    ],
    'Plato Fondo': [
        {'nombre': 'Chaufa Tipakay', 'precio': 17.00},
        {'nombre': 'Chaufa de Pollo', 'precio': 12.00},
        {'nombre': 'Aeropuerto', 'precio': 14.00}
    ],
    'Postres y Bebidas': [
        {'nombre': 'Tajada Pastel Selva Negra', 'precio': 4.50},
        {'nombre': 'Pie de Limon', 'precio': 4.50},
        {'nombre': 'Inka Kola Personal', 'precio': 2.00},
        {'nombre': 'Coca Cola Personal', 'precio': 2.00}
    ]
}

detalles = []
for categoria in categorias:
    st.subheader(categoria)
    for producto in productos[categoria]:
        cantidad = st.number_input(f"{producto['nombre']} (S/. {producto['precio']})", min_value=0, step=1)
        if cantidad > 0:
            producto_id = obtener_producto_id(producto['nombre'])
            detalles.append({
                'producto_id': producto_id,
                'cantidad': cantidad,
                'precio_unitario': producto['precio'],
                'precio_total': cantidad * producto['precio']
            })
            pedido['cantidad_total'] += cantidad
            pedido['precio_total'] += cantidad * producto['precio']

# Mostrar el total en tiempo real
st.subheader('Total del Pedido')
st.write(f"Cantidad Total: {pedido['cantidad_total']}")
st.write(f"Precio Total: S/. {pedido['precio_total']:.2f}")

# Botón para enviar el pedido
if st.button('Enviar Pedido'):
    pedido_id = insertar_pedido(cliente, pedido, detalles)
    if pedido_id:
        st.success('Pedido enviado correctamente')

        # Generar comprobante de pago
        generar_comprobante(cliente, pedido, detalles, pedido_id)
        with open(f"comprobante_{pedido_id}.pdf", "rb") as file:
            st.download_button('Descargar Comprobante', file, file_name=f"comprobante_{pedido_id}.pdf")

# Cerrar la conexión a la base de datos
conn.close()

#Ejecutar: python -m streamlit run prueba.py
