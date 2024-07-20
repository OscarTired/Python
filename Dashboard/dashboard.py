import pandas as pd #pip install pandas
import streamlit as st #pip install streamlit
import streamlit_shadcn_ui as ui #pip install streamlit-shadcn-ui
from local_components import card_container

#Variables
dolar_symbol = "$"

st.set_page_config(layout="wide", page_title="Panel de facturación", page_icon=":bar_chart:")
st.title(":bar_chart: Panel de Facturación")
st.markdown("##")

#leer data del .csv
data_previous_year = pd.read_csv("data_2023.csv")
data = pd.read_csv("data_2024.csv")

#obtener el mes de la fecha
data["Month"] = pd.to_datetime(data["Purchase Date"]).dt.month_name()
data["Hour"] = pd.to_datetime(data["Time"], format= "%H:%M").dt.hour

#Filtros
cols = st.columns(3)
with cols[0]:
    city = st.multiselect("Selecciona la ciudad", options= data["City"].unique().tolist(), default= data["City"].unique().tolist())
with cols[1]:
    gender = st.multiselect("Selecciona el genero", options= data["Gender"].unique().tolist(), default= data["Gender"].unique().tolist())
with cols[2]:
    payment_method = st.multiselect("Selecciona el metodo de pago", options= data["Payment Method"].unique().tolist(), default= data["Payment Method"].unique().tolist())

#KPIs dependendiendo de los filtros
data_filtered = data.query(
    "`City` == @city & `Gender` == @gender & `Payment Method` == @payment_method")

data_previous_year_filtered = data_previous_year.query(
    "`City` == @city & `Gender` == @gender & `Payment Method` == @payment_method")

#KPIs año anterior
total_sales_previous_year = round(data_previous_year_filtered["Invoice Amount"].sum(),2)
num_sales_previous_year = data_previous_year_filtered["Invoice Amount"].count()
average_sales_previous_year = round(data_previous_year_filtered["Invoice Amount"].mean() if data_previous_year_filtered["Invoice Amount"].count() != 0 else 0,2)

#KPIs año actual
total_sales = round(data_filtered["Invoice Amount"].sum(),2)
num_sales = data_filtered["Invoice Amount"].count()
average_sales = round(data_filtered["Invoice Amount"].mean() if data_filtered["Invoice Amount"].count() != 0 else 0,2)

#Diferencia año anterior
diff_total_sales = total_sales - total_sales_previous_year
diff_num_sales = num_sales - num_sales_previous_year
diff_average_sales = average_sales - average_sales_previous_year

#Calcular diferencia %
diff_total_sales_porcentage = round((diff_total_sales / total_sales_previous_year) * 100, 2) if total_sales_previous_year != 0 else 0
diff_num_sales_porcentage = round((diff_num_sales / num_sales_previous_year) * 100, 2) if num_sales_previous_year != 0 else 0
diff_average_sales_porcentage = round((diff_average_sales / average_sales_previous_year) * 100, 2) if average_sales_previous_year != 0 else 0

#KPIs
st.subheader("KPIs")
cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Facturación total", content=f"{total_sales:,.2f} {dolar_symbol}", description=f"{diff_total_sales_porcentage:.2f}% desde el año pasado", key="card1")
with cols[1]:
    ui.metric_card(title="Ventas totales", content=f"{num_sales:,.0f}", description=f"{diff_num_sales_porcentage:.2f}% desde el año pasado", key="card2")
with cols[2]:
    ui.metric_card(title="Facturación media por transacción", content=f"{average_sales:,.2f} {dolar_symbol}", description=str(diff_average_sales_porcentage)+ f"% desde el año pasado", key="card3")

df_selection_month = data_filtered[['Month', 'Invoice Amount']].groupby('Month').sum().sort_values(by='Invoice Amount', ascending=True).reset_index()
df_selection_hour = data_filtered[['Hour', 'Invoice Amount']].groupby('Hour').sum().sort_values(by='Invoice Amount', ascending=True).reset_index()

#Crear graficos
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

#tabla
st.write("---")
st.subheader("Información de ventas")
y1,y2,y3 = st.columns(3)
with y1:
    choice = ui.select(options=["2024", "2023"])
with y2:
    st.empty()
with y3:
    st.empty()

if choice == "2023":
    data_filtered = data_previous_year_filtered

st.dataframe(data_filtered, use_container_width=True)
#streamlit run dashboard.py 