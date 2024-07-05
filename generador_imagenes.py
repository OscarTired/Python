import requests
import streamlit as st
import os

# Asegúrate de que la carpeta 'IA_imagenes' exista
if not os.path.exists('IA_imagenes'):
    os.makedirs('IA_imagenes')

api_key = 'sk-proj-JN0ueGMQMAj5wBLnxtF1T3BlbkFJIpmxXerlUcPUgOGwjPKy'

def openai_pedir(prompt):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers=headers,
        json={
            'prompt': prompt,
            'model': 'dall-e-3',
            'size': '1024x1024',  # Cambia el tamaño a '512x512'
            'quality': 'standard',
            'n': 1
        }
    )
    if response.status_code != 200:
        st.error(f"Error: {response.status_code}, {response.json()}")
        raise Exception(f"Error: {response.status_code}, {response.json()}")
    else:
        image_url = response.json()['data'][0]['url']
    return image_url

def descargar_imagen(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        st.error(f"Error al descargar la imagen: {response.status_code}")
        raise Exception(f"Error al descargar la imagen: {response.status_code}")

# Configuración de la página
st.set_page_config(page_title="Imágenes con IA", page_icon="🩻", layout="centered")
st.image("full.jpg", use_column_width=True)
st.title("Generador de Imágenes con IA")

# Descripción del prompt
description = st.text_area("Prompt")

# Botón para generar la imagen
if st.button("Generar Imagen"):
    with st.spinner("Generando tu imagen..."):
        try:
            url = openai_pedir(description)
            filename = "IA_imagenes/imagen_generada.png"
            descargar_imagen(url, filename)
            st.image(filename, use_column_width=True)
            with open(filename, "rb") as f:
                image_data = f.read()
            st.download_button(label="Descargar Imagen", data=image_data, file_name="imagen_generada.png")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Ejecuta el archivo con: python -m streamlit run generador_imagenes.py
