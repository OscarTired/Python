import pandas as pd
import streamlit as st
import pyodbc

# Configuración de la conexión a SQL Server
server = 'DESKTOP-ODPOVVB\SQLEXPRESS'  # Reemplaza con el nombre de tu servidor
database = 'mod_chifa'
# username = 'your_username'  # Reemplaza con tu nombre de usuario
# password = 'your_password'  # Reemplaza con tu contraseña
driver = '{ODBC Driver 17 for SQL Server}'  # Asegúrate de tener el driver ODBC correcto

# Función para crear la conexión
def create_connection():
    try:
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

# Función para obtener las columnas de una tabla
def get_table_columns(table_name):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return columns
    return []

# Interfaz de Streamlit
st.title("Carga de datos a SQL Server")

# Selección de tabla
table_name = st.selectbox("Selecciona la tabla", [
    "tb_cliente",
    "tb_comprobante",
    "tb_empleados",
    "tb_gerentes",
    "tb_ingredientes",
    "tb_menu",
    "tb_mesa",
    "tb_pedido",
    "tb_proveedor",
    "tb_stock",
    "tb_sucursales"
])

# Mostrar columnas de la tabla seleccionada
if table_name:
    columns = get_table_columns(table_name)
    st.write(f"Columnas en la tabla {table_name}: {', '.join(columns)}")

    # Cargar el archivo CSV
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

    # Procesar el archivo CSV si se carga
    if uploaded_file is not None:
        try:
            # Leer el archivo CSV
            data = pd.read_csv(uploaded_file)
            st.write("Vista previa de los datos:")
            st.dataframe(data.head())

            # Verificar que las columnas del CSV coincidan con las de la tabla
            csv_columns = set(data.columns)
            table_columns = set(columns)
            if csv_columns != table_columns:
                st.warning("Las columnas del CSV no coinciden exactamente con las de la tabla. Por favor, asegúrate de que los nombres de las columnas sean correctos.")
            else:
                # Convertir los datos del DataFrame a lista de tuplas para la inserción en SQL Server
                data_tuples = [tuple(x) for x in data.to_numpy()]

                # Definir la consulta de inserción
                columns_str = ', '.join(columns)
                placeholders = ', '.join(['?'] * len(columns))
                insert_query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})'

                if st.button("Insertar datos en SQL Server"):
                    conn = create_connection()
                    if conn:
                        cursor = conn.cursor()
                        try:
                            cursor.executemany(insert_query, data_tuples)
                            conn.commit()
                            st.success("Datos insertados exitosamente")
                        except Exception as e:
                            st.error(f"Error al insertar datos: {e}")
                        finally:
                            cursor.close()
                            conn.close()
        except Exception as e:
            st.error(f"Error al procesar el archivo CSV: {e}")

#python -m streamlit run inserccion_datos.py