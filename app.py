# streamlit app basic template with docker 
import streamlit as st
from uploaders.uploader import server


idiomas = ["Ingles", "Español"]

st.set_page_config(
     page_title="Streamlit App",
     page_icon='✌️',
     layout="wide",
     initial_sidebar_state="expanded")


def main():

    uploaded_file = st.file_uploader(label="Selecciona un archivo", type="mp3")

    if uploaded_file is not None:
        # Aquí puedes realizar cualquier acción que desees con el archivo subido
        serv = server()
        serv.upload_file(uploaded_file)
        #st.write("Archivo subido correctamente")

    st.write('Hola mundo')

    opciones_seleccionadas = st.selectbox("Selecciona idioma del audio", idiomas)

    st.write("Has seleccionado el siguiente idioma de audio:", opciones_seleccionadas)


if __name__ == '__main__':
    main()







