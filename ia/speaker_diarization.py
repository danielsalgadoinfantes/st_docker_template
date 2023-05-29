import os

from ia.whisper import Whisper
from pyannote.audio import Pipeline
import tempfile
from config.constants import Constants
from pydub import AudioSegment
from servers.server import serv
from ia.chatgpt import Chatgpt
import uuid
import streamlit as st


C = Constants()
server = serv()


class SpeakerDiarization:

    @staticmethod
    def transcribe(audio_file, lan, model, clave:None, barra, progreso, parraf, translate):

        if clave is not None:
            if lan == "Ingles":
                lan = "en"
            else:
                lan = "es"

        path ="wavfile"+str(uuid.uuid4())

        with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:

            temp_file.write(audio_file.read())
            file_path = temp_file.name


            progreso = progreso+2

            barra.progress(progreso, text="Diarizando hablantes")

            audio = AudioSegment.from_file(file_path)

            wav_file = audio.export(path, format="wav")

            diarization = SpeakerDiarization.diarizar(wav_file)

            progreso=progreso+38

            barra.progress(progreso, text="Texto Diarizado")

            i = 0

            txt = ""
            txt_noparraf=""
            speaker_anterior = "-1"
            ini_anterior = None
            end_anterior = None
            # 5. print the result


            num_speakers=len(diarization)

            avance = int((100-progreso)/num_speakers)

            numero_actual = 1

            barra.progress(progreso, text="Transcribiendo intervencion " + str(numero_actual))

            for turn, _, speaker in diarization.itertracks(yield_label=True):

                ini = int(turn.start * 1000)
                end = int(turn.end * 1000)

                if speaker == speaker_anterior:
                    end_anterior = end
                else:
                    if (ini_anterior is not None and end_anterior is not None) and 1000<(end_anterior-ini_anterior):

                        #st.write(f"[{speaker_anterior}]: {ini_anterior}, {end_anterior}")

                        fragmento_txt = SpeakerDiarization.whisper(i, ini_anterior, end_anterior,audio, lan, model, clave, translate)

                        numero_actual += 1

                        if parraf:
                            txt_noparraf = txt_noparraf + "[" + speaker_anterior + "]: " + fragmento_txt + "\n"
                            chat = Chatgpt(clave)
                            fragmento_txt = chat.respuesta(fragmento_txt)

                        txt = txt + "\n[" + speaker_anterior + "]: " + fragmento_txt + "\n"


                        barra.progress(progreso, text="Transcribiendo intervencion " + str(numero_actual))

                    speaker_anterior = speaker
                    ini_anterior = ini
                    end_anterior = end

                progreso+=avance

            if (ini_anterior is not None and end_anterior is not None) and 1000 < (end_anterior - ini_anterior):

                fragmento_txt = SpeakerDiarization.whisper(i, ini_anterior, end_anterior, audio, lan, model, clave, translate)

                if parraf:
                    txt_noparraf = txt_noparraf + "[" + speaker_anterior + "]: " + fragmento_txt + "\n"
                    chat = Chatgpt(clave)
                    fragmento_txt = chat.respuesta(fragmento_txt)+"\n"

                txt = txt + "\n[" + speaker_anterior + "]: " + fragmento_txt + "\n"

            barra.progress(progreso, text="Finalizada trasncripcion del audio")
            os.remove(path)
            if txt_noparraf=="":
                txt_noparraf=txt

            return txt, txt_noparraf
    @staticmethod
    def diarizar(audio):
        server = serv()
        nombre_audio = server.upload_wav(audio, "diarization")
        res = server.diarizar_server(nombre_audio)

        return res

    @staticmethod
    def whisper(i, ini_anterior, end_anterior, audio, lan, model, clave: None, translate):

        fragmento_path = f"fragmento{i}_{uuid.uuid4().hex}"
        fragmento_audio = audio[ini_anterior:end_anterior]

        fragmento_audio.export(fragmento_path, format="mp3")

        if clave is None:
            with open(fragmento_path, "rb") as audio_bytes:
                nombre = server.upload(audio_bytes)
                server.whisper(nombre, lan, model)
                fragmento_txt = server.result(False, nombre)
                os.remove(fragmento_path)
        else:
            whisp = Whisper(clave)
            fragmento_txt = whisp.transcribe_long(fragmento_path, lan, translate)
        return fragmento_txt

