#Antes de iniciar instalar:
#pip install pyshorteners streamlit

#python -m streamlit run acortarUrl.py

import pyshorteners #realiza el proceso de acortar la URL
import streamlit as st #para creacion de la web

def acortar_url(url):
    s = pyshorteners.Shortener()
    acortado_url = s.tinyurl.short(url)
    return acortado_url
#esta funcion recibe nuestra URL, creamos un ojeto de la primera libreria; llamamos al metodo que acorta la URL y devuelve la URL acortada

#creacion web
st.set_page_config(page_title="Acortador URL", page_icon="🪚", layout="centered") #loyout = como se mostrara el contenido (ver cambios con= wide)
st.image("acortar.png", use_column_width=True)
st.title("Acortador URL")
#colocamos en una condicional el boton para que al pulsarse llame a la funcion
url = st.text_input("Ingresa la URL")
if st.button("Genera una nueva URL"):
    st.write("Url acortada: ", acortar_url(url))