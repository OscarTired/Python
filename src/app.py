import streamlit as st
from dotenv import load_dotenv
import os
import openai

load_dotenv()
#python -m venv imgIA
#.\imgIA\Scripts\Activate
#si no tenemos habilitada la ejecucion de scripts: Powershell en admin y "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
#pip install streamlit openai python-dotenv 
#streamlit run src/app.py
openai.api_key = os.getenv("OPENAI_API_key")


st.title("Generador de imagenes con IA")

with st.form("images_form"):
    text = st.text_input("Prompt para generar imagen")
    num_image = st.number_input("Numero de imagenes a generar", min_value=1, max_value=10, value=1)
    image_size = st.selectbox("Tamaño de la imagen", ["256x256", "512x512", "1024x1024"], index=0)
    submit_button = st.form_submit_button(label="Generar imagenes")

if submit_button:
    st.write("Generando imagenes...")
    response = openai.images.generate(
        prompt=text,
        n=num_image,
        size=image_size
    )

    print(response)