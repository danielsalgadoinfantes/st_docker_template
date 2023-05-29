from servers.server import serv
import streamlit as st

from config.constants import Constants

C= Constants()
uploaded_file = st.file_uploader(label="Selecciona un archivo", type=C.AUDIO_TYPE)

holdet =st.empty()

if holdet.button("Subir archivo"):
    server = serv()
    audio = server.upload_wav(uploaded_file, "diarization")
    diarization=server.diarizar_server(audio)

    for turn, _, speaker in diarization.itertracks(yield_label=True):

        st.write(f"[{speaker}]: {str(turn.start)}, {str(turn.end)}")
