# streamlit app basic template with docker 
import streamlit as st
from servers.server import serv
from config.constants import Constants
from streamlit_option_menu import option_menu
from ia.chatgpt import Chatgpt
from ia.whisper import Whisper
import streamlit_toggle as tog
import os
from ia.speaker_diarization import SpeakerDiarization
from utils.correo import Gmail

#import pywebview

os.environ['PATH'] += ':/usr/bin/ffprobe'


serv = serv()

C = Constants()

st.set_page_config(
     page_title="Streamlit App",
     page_icon='✌️',
     layout="wide",
     initial_sidebar_state="expanded")


def set_stage(stage):
    st.session_state.stage = stage

def set_originalystage(stage):
    set_stage(stage)
    st.session_state.original = not st.session_state.original


def main():

    mail = Gmail()

    # Llamada a st.file_uploader para poder subir el archivo de audio
    uploaded_file = st.file_uploader(label="Selecciona un archivo", type=C.AUDIO_TYPE)

    if uploaded_file is not None: #Si el streamlit ha reconocido el archivo hacemos lo siguiente

        # Mostrar el audio
        #audio_bytes = io.BytesIO(uploaded_file.read())
        #st.audio(audio_bytes)

        if "reciever" not in st.session_state:
            st.session_state.reciever = ""

        if "parraf" not in st.session_state:
            st.session_state.parraf = ""

        if 'stage' not in st.session_state:
            st.session_state.stage = 0

        if "option" not in st.session_state:
            st.session_state.option = ""

        if "diar" not in st.session_state:
            st.session_state.diar = ""

        if "translate" not in st.session_state:
            st.session_state.translate = ""

        if "resp" not in st.session_state:
            st.session_state.resp = ""

        if "resp_sinparraf" not in st.session_state:
            st.session_state.resp_sinparraf = ""

        if "sended" not in st.session_state:
            st.session_state.sended = False
        if "mail_valido" not in st.session_state:
            st.session_state.mail_valido = ""

        anterior = st.session_state.option

        option = option_menu(
            menu_title=None,
            options=C.OPCIONES_EJECUCION,
            icons = ["hdd-fill", "key-fill"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        st.session_state.option = option

        if st.session_state.option != anterior:
            set_stage(0)
            st.session_state.sended = False

        col1, col2, col3, col4, col5 = st.columns([15, 6, 6, 6, 15])

        with col2:
            parrafear = tog.st_toggle_switch(label="Dividir en párrafos",
                                 key="parrafear",
                                 default_value=False,
                                 label_after=False,
                                 inactive_color='#FAFAFA',
                                 active_color="#FAFAFA",
                                 track_color="#0CFD00"
                                 )
            if st.session_state.stage == 0:
                st.session_state.parraf = parrafear

        with col3:

            diarization = tog.st_toggle_switch(label="Speaker Diarization",
                                 key="diarizar",
                                 default_value=False,
                                 label_after=False,
                                 inactive_color='#FAFAFA',
                                 active_color="#FAFAFA",
                                 track_color="#0CFD00"
                                 )
            if st.session_state.stage == 0:
                st.session_state.diar = diarization

        with col4:

            translate = tog.st_toggle_switch(label="Traducir Audio a Inglés",
                                               key="transalte",
                                               default_value=False,
                                               label_after=False,
                                               inactive_color='#FAFAFA',
                                               active_color="#FAFAFA",
                                               track_color="#0CFD00"
                                               )
            if st.session_state.stage == 0:
                st.session_state.translate = translate

        # Opciones de ejecución de whisper
        col1, col2, col3, col4 = st.columns(4)

        with col2:

            idioma = st.selectbox("Selecciona el idioma del audio", C.IDIOMAS)
            st.write("Has seleccionado el siguiente idioma de audio:", idioma)

        with col3:

            model = st.selectbox("Selecciona un modelo de whisper", C.MODELS)
            st.write("Has seleccionado el siguiente modelo:", model)

        if st.session_state.option == "API de whisper":
            col1, col2, col3, col4 = st.columns(4)

            with col2:
                clave = st.text_input("OpenAI API Key")
                error_placeholder = st.empty()
            with col3:
                st.session_state.reciever = st.text_input("Email Adress")
                error_placeholder_email = st.empty()
        else:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.session_state.reciever = st.text_input("Email Adress")
                error_placeholder_email = st.empty()


        col1, col2, col3 = st.columns(3)

        with col2:
            holder = st.empty()

            # Agrega un estilo CSS al botón para que ocupe todo el ancho de la columna
            st.write("<style>div.row-widget.stButton > button:first-child { width: 100%; }</style>",
                     unsafe_allow_html=True)

            holder.button('Cargar archivo', on_click=set_stage, args=(1,))
            st.session_state.mail_valido = mail.check(st.session_state.reciever)
            if not st.session_state.mail_valido:
                txt_rojo = '<div style="display: flex; justify-content: center;"><font color="red">' \
                           'Correo electrónico no válido</font></div>'
                error_placeholder_email.write(txt_rojo, unsafe_allow_html=True)
            else:
                error_placeholder_email.empty()

        # Subir audio a serv remoto
        if st.session_state.stage > 0 and st.session_state.mail_valido:

            holder.empty()

            barra_placeholder = st.empty()

            progreso = 0

            barra = barra_placeholder.progress(0,text="Iniciando")

            if st.session_state.option == "Servidor remoto":

                if st.session_state.stage<2:

                    if st.session_state.diar:
                        respuesta, resp_sinparraf = SpeakerDiarization.transcribe(uploaded_file, idioma, model, None, barra, progreso, st.session_state.parraf, st.session_state.translate)

                        st.session_state.resp = respuesta
                        st.session_state.resp_sinparraf = resp_sinparraf
                    else:
                        progreso =2

                        barra.progress(progreso, text="Subiendo archivo a servidor remoto")
                        nombre = serv.upload(uploaded_file)
                        progreso += 28

                        barra.progress(progreso, text="Transcribiendo audio")
                        serv.whisper(nombre, idioma, model)
                        progreso += 45

                        res_sinparraf=""
                        if st.session_state.parraf:
                            barra.progress(progreso, text="Dividiendo en parrafos")
                        else:
                            barra.progress(progreso, text="Obteniendo texto")

                        st.session_state.resp_sinparraf=serv.sin_p(nombre)

                        respuesta = serv.result(st.session_state.parraf, nombre)

                        st.session_state.resp = respuesta
                        progreso += 15
                        barra.progress(progreso, text="Enviando correo")

                col0, col1, espacio, col2, col3, col4 = st.columns([0.5, 0.5, 0.25, 1.5, 23.5, 2])

                if mail.check(st.session_state.reciever):
                    if st.session_state.parraf:
                        if not st.session_state.sended:
                            mail.send(uploaded_file.name, st.session_state.resp, st.session_state.reciever)
                            st.session_state.sended = True
                    else:
                        if not st.session_state.sended:
                            mail.send(uploaded_file.name, st.session_state.resp_sinparraf, st.session_state.reciever)
                            st.session_state.sended = True

                barra_placeholder.empty()
                set_stage(2)

                with col0:
                    if st.button("⇐", on_click=set_stage, args=(0,)):
                        st.session_state.sended = False

                if st.session_state.parraf:

                    if "original" not in st.session_state:
                        st.session_state.original = False

                    if st.session_state.original:
                        txt_btn = "Parrafos"
                    else:
                        txt_btn = "Original"
                    with col2:
                        st.button(txt_btn, on_click=set_originalystage, args=(2,))
                    if st.session_state.original:
                        with col1:
                            st.download_button("⬇️", st.session_state.resp_sinparraf)
                    else:
                        with col1:
                            st.download_button("⬇️", st.session_state.resp)
                    with col3:
                        st.write("Trasncripción: ")
                        if not st.session_state.original:
                            st.write(st.session_state.resp)
                        else:
                            st.write(st.session_state.resp_sinparraf)

                else:
                    with col3:
                        st.write("Trasncripción: ")
                        st.write(st.session_state.resp_sinparraf)  # , language="textile")
                    with col1:
                        st.download_button("⬇️", st.session_state.resp_sinparraf)


            elif st.session_state.option == "API de whisper":

                progreso+=5

                if st.session_state.stage<2:
                    barra.progress(progreso, text="Validando clave")
                    if "valida" not in st.session_state:
                        st.session_state.valida = False
                    valida = Chatgpt.checkKey(clave)
                    if not valida:
                        set_stage(0)
                        st.session_state.sended=False
                        barra_placeholder.empty()
                    st.session_state.valida = valida

                if st.session_state.valida:

                    if st.session_state.stage<2:

                        if st.session_state.diar:
                            respuesta, sin_parr = SpeakerDiarization.transcribe(uploaded_file, idioma, model, clave,  barra, progreso, st.session_state.parraf, st.session_state.translate)

                            st.session_state.resp = respuesta
                            st.session_state.resp_sinparraf = sin_parr

                        else:
                            whisper = Whisper(clave)

                            progreso += 15
                            barra.progress(progreso, text="Haciendo llamada a la API de Whisper")

                            respuesta = whisper.transcribe(uploaded_file, idioma, st.session_state.translate)#audio_bytes, idioma)

                            st.session_state.resp_sinparraf = respuesta

                            progreso += 60
                            if st.session_state.parraf:
                                barra.progress(progreso, text="Dividiendo en parrafos")
                                respuesta = whisper.result(respuesta)
                                st.session_state.resp = respuesta

                            progreso+=15
                            barra.progress(progreso, text="Enviando correo")

                    col0, col1, espacio, col2, col3, col4 = st.columns([0.5, 0.5, 0.25, 1.5, 23.5, 2])

                    if mail.check(st.session_state.reciever):
                        if st.session_state.parraf:
                            if not st.session_state.sended:
                                mail.send(uploaded_file.name, st.session_state.resp, st.session_state.reciever)
                                st.session_state.sended = True
                        else:
                            if not st.session_state.sended:
                                mail.send(uploaded_file.name, st.session_state.resp_sinparraf,
                                              st.session_state.reciever)
                                st.session_state.sended = True

                    barra_placeholder.empty()
                    set_stage(2)

                    with col0:
                        if st.button("⇐", on_click=set_stage, args=(0,)):
                            st.session_state.sended = False

                    if st.session_state.parraf:

                        if "original" not in st.session_state:
                            st.session_state.original = False

                        if st.session_state.original:
                            txt_btn = "Parrafos"
                        else:
                            txt_btn = "Original"
                        with col2:
                            st.button(txt_btn, on_click=set_originalystage, args=(2,))
                        if st.session_state.original:
                            with col1:
                                st.download_button("⬇️", st.session_state.resp_sinparraf)
                        else:
                            with col1:
                                st.download_button("⬇️", st.session_state.resp)
                        with col3:
                            st.write("Trasncripción: ")
                            if not st.session_state.original:
                                st.write(st.session_state.resp)
                            else:
                                st.write(st.session_state.resp_sinparraf)
                    else:
                        with col3:
                            st.write("Trasncripción: ")
                            st.write(st.session_state.resp_sinparraf)  # , language="textile")
                        with col1:
                            st.download_button("⬇️", st.session_state.resp_sinparraf)

                else:
                    with col2:
                        texto_rojo = '<div style="display: flex; justify-content: center;"><font color="red">Clave ' \
                                     'no válida. Introduzca una nueva clave válida y pulse intro</font></div>'
                        error_placeholder.write(texto_rojo, unsafe_allow_html=True)






if __name__ == '__main__':
    main()







