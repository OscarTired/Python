import streamlit as st
import pandas as pd
import pyodbc
from fpdf import FPDF

# Configuración de la conexión a SQL Server
server = 'DESKTOP-ODPOVVB\SQLEXPRESS'  # Cambia esto si es necesario
database = 'mod_chifa'
username = ''  # Vacío para autenticación de Windows
password = ''  # Vacío para autenticación de Windows
driver = '{ODBC Driver 17 for SQL Server}'

# Establecer la conexión
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)

# Función para obtener datos de la base de datos
def fetch_data(query):
    return pd.read_sql(query, conn)

# Función para generar el PDF del comprobante
def generate_pdf(comprobante_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Comprobante de Pedido", ln=True, align='C')
    
    for key, value in comprobante_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')
    
    pdf.output("comprobante.pdf")

# Cargar datos para los menús desplegables
sucursales = ['Los Olivos', 'San Miguel', 'Callao', 'San Martin de Porres']
empleados = ['A', 'B', 'C', 'D']
mesas = ['1', '2', '3', '4']
menus = ['Ejecutivo', 'A la carta']
estados_pedido = ['Pendiente', 'Entregado']
tipos_pago = ['Credit Card', 'Efectivo', 'Yape/Plin']

# Interfaz de Streamlit
st.title('Sistema de Pedido')

# Campos de entrada
cliente = st.text_input('Nombre del Cliente')
sucursal = st.selectbox('Sucursal', sucursales)
empleado = st.selectbox('Empleado', empleados)
mesa = st.selectbox('Mesa', mesas)
menu = st.selectbox('Menú', menus)
estado_pedido = st.selectbox('Estado del Pedido', estados_pedido)
tipo_pago = st.selectbox('Tipo de Pago', tipos_pago)

# Calcular el pago total (esto es solo un ejemplo, necesitas implementar la lógica de cálculo adecuada)
pago_total = st.number_input('Pago Total', min_value=0.0, format="%.2f")

if st.button('Generar Comprobante'):
    if cliente and pago_total >= 0:
        # Insertar datos en la tabla tb_comprobante
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_comprobante (idComprobante, idCliente, idLocal, idPedido, idMenu, tipo_comp, pago_total, fecha_pago, tipo_pago, ruc_rest)
        VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), ?, ?)
        """
        # Datos ficticios para el ejemplo, ajusta según sea necesario
        cursor.execute(query, (None, cliente, sucursal, None, menu, estado_pedido, pago_total, tipo_pago, '147258369'))
        conn.commit()
        
        # Obtener el ID del último comprobante insertado
        cursor.execute("SELECT @@IDENTITY AS idComprobante")
        id_comprobante = cursor.fetchone()[0]
        
        # Datos para el comprobante
        comprobante_data = {
            'ID Comprobante': id_comprobante,
            'Nombre del Cliente': cliente,
            'Sucursal': sucursal,
            'Menú Seleccionado': menu,
            'Pago Total': pago_total,
            'Tipo de Pago': tipo_pago,
            'RUC de la Empresa': '147258369'
        }
        
        # Generar PDF
        generate_pdf(comprobante_data)
        
        st.success('Comprobante generado exitosamente! Descárgalo desde el archivo generado en el directorio de trabajo.')
    else:
        st.error('Por favor, completa todos los campos correctamente.')

# Cierre de la conexión
conn.close()
#pip install pandas pyodbc fpdf