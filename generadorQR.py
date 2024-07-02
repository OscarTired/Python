import qrcode
import streamlit as st

import os

if not os.path.exists('qr_code'):
    os.makedirs('qr_code')
#importamos recursos de Sistema para que si no existe la carpeta, la cree


filename = "qr_code/qr_cod.png" #aca se almacenara

def generar_qr(url, filename):
    qr = qrcode.QRCode(
        version =1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white") #genera la imagen
    img.save(filename) #guardar imagen en carpeta

#creacion pagina
st.set_page_config(page_title="Generador QR", page_icon="🗿", layout="centered")
st.image("qr.png", use_column_width=True)
st.title("Generador QR")
url = st.text_input("Ingresa la URL")

if st.button("Generar QR"):
    generar_qr(url, filename)
    st.image(filename, use_column_width=True)
    with open(filename, "rb") as f:
                    image_data = f.read() #abrimos la imagen
    download = st.download_button(label="Descargar QR", data=image_data, file_name="qr_generado.png") #le damos al usuario la posibilidad de descargar la imagen

#python -m streamlit run generadorQR.py
#pip install qrcode[pil]