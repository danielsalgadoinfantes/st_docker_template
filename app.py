# streamlit app basic template with docker 
import streamlit as st
from servers.server import serv
import io
from config.constants import Constants
from streamlit_option_menu import option_menu
from ia.chatgpt import Chatgpt
from ia.whisper import Whisper
import streamlit_toggle as tog
import os
os.environ['PATH'] += ':/usr/bin/ffprobe'


serv = serv()

C = Constants()

st.set_page_config(
     page_title="Streamlit App",
     page_icon='✌️',
     layout="wide",
     initial_sidebar_state="expanded")


def main():
    # Llamada a st.file_uploader para poder subir el archivo de audio
    uploaded_file = st.file_uploader(label="Selecciona un archivo", type = C.AUDIO_TYPE)

    
    
    if uploaded_file is not None: #Si el streamlit ha reconocido el archivo hacemos lo siguiente
        
        # Mostrar el audio
        audio_bytes = io.BytesIO(uploaded_file.read())
        st.audio(audio_bytes)

        option = option_menu(
            menu_title=None,
            options=C.OPCIONES_EJECUCION,
            icons = ["hdd-fill", "key-fill"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

        with col5:
            parrafear = tog.st_toggle_switch(label="Dividir en párrafos",
                                 key="Key1",
                                 default_value=False,
                                 label_after=False,
                                 inactive_color='#FAFAFA',
                                 active_color="#FAFAFA",
                                 track_color="#0CFD00"
                                 )

        # Opciones de ejecución de whisper
        col1, col2, col3, col4 = st.columns(4)

        with col2:

            idioma = st.selectbox("Selecciona el idioma del audio", C.IDIOMAS)
            st.write("Has seleccionado el siguiente idioma de audio:", idioma)

        with col3:

            model = st.selectbox("Selecciona un modelo de whisper", C.MODELS)
            st.write("Has seleccionado el siguiente modelo:", model)

        col1, col2, col3= st.columns(3)

        with col2:

            if option == "API de whisper":
                clave = st.text_input("OpenAI API Key")
                error_placeholder = st.empty()

            holder = st.empty()


            # Agrega un estilo CSS al botón para que ocupe todo el ancho de la columna
            st.write("<style>div.row-widget.stButton > button:first-child { width: 100%; }</style>",
                     unsafe_allow_html=True)

            boton = holder.button('Cargar archivo')

        # Subir audio a serv remoto
        if boton:

            if option == "Servidor remoto":
                serv.upload(uploaded_file)
                holder.empty()
                with st.spinner("Cargando..."):
                    serv.whisper(uploaded_file, idioma, model)
                    respuesta = serv.result(parrafear)
                    with st.container():
                        st.write("Transcripción: ")
                        st.write(respuesta)

            elif option == "API de whisper":
                with col2:
                    with st.spinner("Validando clave..."):
                        valida = Chatgpt.checkKey(clave)

                if valida:
                    whisper = Whisper(clave)
                    with col2:
                        with st.spinner("Transcribiendo..."):
                            holder.empty()
                            txt = whisper.transcribe(audio_bytes, idioma)
                            if parrafear:
                                txt=whisper.result(txt)
                            #st.write(type(uploaded_file))
                    st.write(txt)
                else:
                    with col2:
                        texto_rojo = '<div style="display: flex; justify-content: center;"><font color="red">Clave ' \
                                     'no válida</font></div>'
                        error_placeholder.write(texto_rojo, unsafe_allow_html=True)



if __name__ == '__main__':
    main()







