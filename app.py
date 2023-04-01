# streamlit app basic template with docker 
import streamlit as st
from servers.server import serv
import io
serv = serv()
idiomas = ["Ingles", "Español"]

st.set_page_config(
     page_title="Streamlit App",
     page_icon='✌️',
     layout="wide",
     initial_sidebar_state="expanded")


def main():
    uploaded=False
    # Llamada a st.file_uploader para poder subir el archivo de audio
    uploaded_file = st.file_uploader(label="Selecciona un archivo", type="mp3")

    
    
    if uploaded_file is not None: #Si el streamlit ha reconocido el archivo hacemos lo siguiente
        
        # Mostrar el audio
        audio_bytes = io.BytesIO(uploaded_file.read())
        st.audio(audio_bytes)

        # Opciones de ejecución de whisper
        opciones_seleccionadas = st.selectbox("Selecciona idioma del audio", idiomas)
        st.write("Has seleccionado el siguiente idioma de audio:", opciones_seleccionadas)
        
        holder=st.empty()
        # Subir audio a serv remoto
        if holder.button('Cargar archivo'):
            serv.upload(uploaded_file)
            serv.whisper(uploaded_file)
            holder.empty()

    


if __name__ == '__main__':
    main()







