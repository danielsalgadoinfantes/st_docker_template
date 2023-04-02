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
        idioma = st.selectbox("Selecciona idioma del audio", idiomas)
        st.write("Has seleccionado el siguiente idioma de audio:", idioma)
        
        holder=st.empty()
        # Subir audio a serv remoto
        if holder.button('Cargar archivo'):
            serv.upload(uploaded_file)
            holder.empty()
            with st.spinner("Cargando..."):
                serv.whisper(uploaded_file, idioma)
            serv.result()

    


if __name__ == '__main__':
    main()







