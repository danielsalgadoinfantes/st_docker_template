import openai

import os
from dotenv import load_dotenv
import streamlit as st
from ia.nltk import Nltk
import re


class Chatgpt:

    def __init__(self, apis_key=None):

        if apis_key:
            openai.api_key = apis_key
        else:
            load_dotenv(dotenv_path="config/cred.env")
            openai.api_key = os.environ.get("API_KEY")



    def pregunta(self, pregunta, contenido):

        pregunta_completa = pregunta+" "+contenido
        #st.write(pregunta_completa)
        completion = openai.Completion.create(engine = "text-davinci-003",
                                            prompt = pregunta_completa,
                                            max_tokens=1024,
                                            n=1,
                                            stop=None,
                                            temperature=0.5,
        )

        respuesta = completion.choices[0].text.strip()
        return respuesta
    

    def respuesta(self, contenido):

        fragmentos = Nltk.dividir_texto(contenido)
        pregunta = "Tengo un texto sin dividir en párrafos, es decir, en una sola linea. Quiero que lo dividas en párrafos sin cambiar ni una sola palabra. Un requisito importante es que tenga un formato muy estricto, el cual es el siguiente: [parrafo 1]: " \
                   "contenido párrafo 1\n[parrafo 2]: contenido párrafo 2\n...[parrafo n]: contenido párrafo n. Una última petición es que no escribas nada de introducción como por ejemplo: Aquí tienes tu texto o algo similar. Aquí te muestro el texto que" \
                   " quiero que dividas en párrafos tal y como te he descrito: "

        txt = ""
        j=0
        for i in fragmentos:
            # st.write("Fragmento "+str(j)+": "+i)

            try :
            
                res = self.pregunta(pregunta, i)
            except openai.InvalidRequestError as e:
                res = i

            # st.write(res)
            txt = txt + "\n\n" + res

            j = j+1

        txt = re.sub(r"\[parrafo \d+\]:\s*", "\n", txt)
        txt = re.sub(r"\[párrafo \d+\]:\s*", "\n", txt)
        txt = re.sub(r"\[Parrafo \d+\]:\s*", "\n", txt)
        txt = re.sub(r"\[Párrafo \d+\]:\s*", "\n", txt)

        return txt

    @staticmethod
    def checkKey(key):

        openai.api_key = key
        try:
            response = openai.Completion.create(engine="text-davinci-003", prompt="Hello, World!")
            return True
        except:
            return False
