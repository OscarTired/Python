import pandas as pd #pip install pandas
import streamlit as st #pip install streamlit
import streamlit_shadcn_ui as ui #pip install streamlit-shadcn-ui
from local_components import card_container

# Importación de librerías:
# pandas: Librería para manipulación y análisis de datos.
# streamlit: Librería para crear aplicaciones web interactivas.
# streamlit_shadcn_ui: Extensión de Streamlit para componentes UI adicionales.
# card_container: Un componente personalizado para tarjetas dentro de la aplicación (asumimos que se encuentra en un módulo local local_components).

# Variables
dolar_symbol = "$"

# Variables:
# dolar_symbol: Define el símbolo del dólar que se usará en la visualización de los datos.

# Configuración de la página
st.set_page_config(layout="wide", page_title="Panel de facturación", page_icon=":bar_chart:")
st.title(":bar_chart: Panel de Facturación")
st.markdown("##")

# Configuración de la página:
# st.set_page_config: Configura el diseño, título y el ícono de la página.
# st.title: Establece el título de la aplicación.
# st.markdown("##"): Agrega un espaciado o separación.

# Leer datos del .csv
data_previous_year = pd.read_csv("data_2023.csv")
data = pd.read_csv("data_2024.csv")

# Lectura de datos:
# Se leen los datos de los archivos CSV para los años 2023 y 2024 y se almacenan en data_previous_year y data, respectivamente.

# Verificar existencia de columnas esperadas
expected_columns = ["Purchase Date", "Time", "City", "Gender", "Payment Method", "Invoice Amount"]
missing_columns = [col for col in expected_columns if col not in data.columns]
if missing_columns:
    st.error(f"Las columnas {', '.join(missing_columns)} no están en el archivo data_2024.csv")
    st.stop()

# Verificación de columnas:
# expected_columns: Lista de columnas que se esperan en los datos.
# Verifica si las columnas esperadas están presentes en data. Si faltan columnas, muestra un error y detiene la ejecución de la aplicación.

# Verificar formato de 'Time'
try:
    data["Time"] = pd.to_datetime(data["Time"], format="%H:%M").dt.time
except ValueError:
    st.error("El formato de 'Time' en el archivo data_2024.csv no es %H:%M")
    st.stop()

# Verificación de formato de hora:
# Convierte la columna Time a un formato de tiempo. Si el formato es incorrecto, muestra un error y detiene la ejecución.

# Obtener el mes de la fecha y la hora
data["Month"] = pd.to_datetime(data["Purchase Date"]).dt.month_name()
data["Hour"] = pd.to_datetime(data["Time"].astype(str)).dt.hour

# Procesamiento de datos:
# Extrae el nombre del mes de Purchase Date y la hora de Time, almacenándolos en nuevas columnas Month y Hour.

# Filtros
cols = st.columns(3)
with cols[0]:
    city = st.multiselect("Selecciona la ciudad", options=data["City"].unique(), default=data["City"].unique())
with cols[1]:
    gender = st.multiselect("Selecciona el género", options=data["Gender"].unique(), default=data["Gender"].unique())
with cols[2]:
    payment_method = st.multiselect("Selecciona el método de pago", options=data["Payment Method"].unique(), default=data["Payment Method"].unique())

    # Filtros:
    # Crea filtros interactivos para City, Gender y Payment Method usando st.multiselect. Permiten al usuario seleccionar múltiples valores de estas columnas para filtrar los datos.

# KPIs dependiendo de los filtros
data_filtered = data.query("City in @city and Gender in @gender and `Payment Method` in @payment_method")
data_previous_year_filtered = data_previous_year.query("City in @city and Gender in @gender and `Payment Method` in @payment_method")

# Aplicación de filtros:
# Filtra los datos del año actual y del año anterior según los valores seleccionados por el usuario en los filtros.

# KPIs año anterior
total_sales_previous_year = round(data_previous_year_filtered["Invoice Amount"].sum(), 2)
num_sales_previous_year = data_previous_year_filtered["Invoice Amount"].count()
average_sales_previous_year = round(data_previous_year_filtered["Invoice Amount"].mean() if num_sales_previous_year != 0 else 0, 2)

# KPIs año actual
total_sales = round(data_filtered["Invoice Amount"].sum(), 2)
num_sales = data_filtered["Invoice Amount"].count()
average_sales = round(data_filtered["Invoice Amount"].mean() if num_sales != 0 else 0, 2)

# Cálculo de KPIs:
# Calcula los KPIs (Key Performance Indicators) para el año anterior y el actual: total_sales, num_sales, y average_sales.

# Diferencia año anterior
diff_total_sales = total_sales - total_sales_previous_year
diff_num_sales = num_sales - num_sales_previous_year
diff_average_sales = average_sales - average_sales_previous_year

# Calcular diferencia %
diff_total_sales_percentage = round((diff_total_sales / total_sales_previous_year) * 100, 2) if total_sales_previous_year != 0 else 0
diff_num_sales_percentage = round((diff_num_sales / num_sales_previous_year) * 100, 2) if num_sales_previous_year != 0 else 0
diff_average_sales_percentage = round((diff_average_sales / average_sales_previous_year) * 100, 2) if average_sales_previous_year != 0 else 0

# Diferencias y porcentajes de cambio:
# Calcula la diferencia absoluta y el porcentaje de cambio entre los años para cada KPI.

# KPIs
st.subheader("KPIs")
cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Facturación total", content=f"{total_sales:,.2f} {dolar_symbol}", description=f"{diff_total_sales_percentage:.2f}% desde el año pasado", key="card1")
with cols[1]:
    ui.metric_card(title="Ventas totales", content=f"{num_sales:,.0f}", description=f"{diff_num_sales_percentage:.2f}% desde el año pasado", key="card2")
with cols[2]:
    ui.metric_card(title="Facturación media por transacción", content=f"{average_sales:,.2f} {dolar_symbol}", description=str(diff_average_sales_percentage) + f"% desde el año pasado", key="card3")

# Visualización de KPIs:
# Muestra los KPIs usando componentes metric_card de streamlit_shadcn_ui.

df_selection_month = data_filtered[['Month', 'Invoice Amount']].groupby('Month').sum().sort_values(by='Invoice Amount', ascending=True).reset_index()
df_selection_hour = data_filtered[['Hour', 'Invoice Amount']].groupby('Hour').sum().sort_values(by='Invoice Amount', ascending=True).reset_index()

# Preparación de datos para gráficos:
# Agrupa los datos filtrados por Month y Hour, calculando la suma de Invoice Amount para cada agrupación.

# Crear gráficos
chart1, chart2 = st.columns(2)
with chart1:
    st.subheader("Ventas por mes")
    with card_container(key="chart1"):
        st.vega_lite_chart(df_selection_month, {
            'mark': {'type': 'bar', 'tooltip': True, 'fill': 'rgb(173, 250, 29)', 'cornerRadiusEnd': 4},
            'encoding': {
                'x': {'field': 'Month', 'type': 'ordinal'},
                'y': {'field': 'Invoice Amount', 'type': 'quantitative', 'axis': {'grid': False}},
            },
        }, use_container_width=True)

with chart2:
    st.subheader("Ventas por hora")
    with card_container(key="chart2"):
        st.vega_lite_chart(df_selection_hour, {
            'mark': {'type': 'bar', 'tooltip': True, 'fill': 'rgb(173, 250, 29)', 'cornerRadiusEnd': 4},
            'encoding': {
                'x': {'field': 'Hour', 'type': 'ordinal'},
                'y': {'field': 'Invoice Amount', 'type': 'quantitative', 'axis': {'grid': False}},
            },
        }, use_container_width=True)

# Visualización de gráficos:
# Muestra gráficos de barras para las ventas por mes y por hora usando st.vega_lite_chart.

# Tabla
st.write("---")
st.subheader("Información de ventas")
y1, y2, y3 = st.columns(3)
with y1:
    choice = st.selectbox("Selecciona el año", options=["2024", "2023"])
with y2:
    st.empty()
with y3:
    st.empty()

if choice == "2023":
    data_filtered = data_previous_year_filtered

st.dataframe(data_filtered, use_container_width=True)

# Tabla de datos:
# Permite al usuario seleccionar el año de los datos a visualizar en una tabla interactiva usando st.dataframe.

#streamlit run dashboard2.py 