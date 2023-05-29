import paramiko
import streamlit as st
import os
from dotenv import load_dotenv
from ia.chatgpt import Chatgpt
from pydub import AudioSegment
import numpy as np
import uuid
import pickle


class serv:
    def __init__(self):
        load_dotenv(dotenv_path="config/cred.env")
        self.username_host = os.environ.get("USER_HOST")
        self.password_host = os.environ.get("PASSWORD_HOST")
        self.server_host = os.environ.get("SERVER_HOST")

        self.username_whisper = os.environ.get("USER_WHISPER")
        self.password_whisper = os.environ.get("PASSWORD_WHISPER")
        self.server_whisper = os.environ.get("SERVER_WHISPER")


    def open_conexion(self):
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(self.server_whisper, username=self.username_whisper, password=self.password_whisper)
        return ssh1
        


    def upload(self, file):
        ssh1 = self.open_conexion()
        sftp = ssh1.open_sftp()

        nombre = "sample" + str(uuid.uuid4().hex)

        remotepath = "/home/{}/samples/{}".format(self.username_whisper, nombre)
        with st.spinner("Subiendo archivo..."):
            file.seek(0)
            sftp.putfo(file, remotepath)

        # Cerrar la conexión SFTP y la conexión con el servidor remoto
        sftp.close()
        ssh1.close()

        return nombre
        #st.write("Archivo subido correctamente")

    def upload_wav(self, file, carpeta):
        ssh1 = self.open_conexion()
        sftp = ssh1.open_sftp()

        nombre = carpeta + str(uuid.uuid4().hex) + ".wav"

        remotepath = "/home/{}/{}/{}".format(self.username_whisper, carpeta, nombre)
        with st.spinner("Subiendo archivo..."):
            file.seek(0)
            sftp.putfo(file, remotepath)

        # Cerrar la conexión SFTP y la conexión con el servidor remoto
        sftp.close()
        ssh1.close()

        return nombre
        # st.write("Archivo subido correctamente")

    def whisper(self, nombre, len, model):
        ssh = self.open_conexion()

        if len == "Ingles":
            lan = "English"
        else:
            lan = "Spanish"

        gpu = self.idle()

        comand='CUDA_VISIBLE_DEVICES={} whisper samples/{} --model {} --output_format txt --language {} --output_dir samples'.format(gpu, nombre, model, lan)
        stdin, stdout, stderr = ssh.exec_command(comand)

        # Imprimir el error en caso de que algo falle
        if stderr.channel.recv_exit_status() != 0:
            st.write(stderr.read().decode())

        ssh.close()

        self.borrar(nombre)



    def result(self, parrafear, nombre):
        # Leer el archivo .txt en el servidor remoto
        ssh = self.open_conexion()
        stdin, stdout, stderr = ssh.exec_command('cat samples/{}.txt'.format(nombre))

        respuesta = stdout.read().decode()

        if parrafear:
            #st.write(contenido)
            chat = Chatgpt()
            respuesta = chat.respuesta(respuesta)

        ssh.close()

        self.borrar(nombre + ".txt")

        return respuesta

    def sin_p(self, nombre):

        ssh = self.open_conexion()
        stdin, stdout, stderr = ssh.exec_command('cat samples/{}.txt'.format(nombre))

        respuesta = stdout.read().decode()

        ssh.close()

        return respuesta


    def idle(self):
        server = serv()
        # Establecer la conexión SSH con el servidor remoto
        ssh = server.open_conexion()

        # Ejecutar el comando nvidia-smi para obtener información de las GPUs
        stdin, stdout, stderr = ssh.exec_command('nvidia-smi --query-gpu=memory.free --format=csv,noheader')

        # Leer la salida del comando y convertir los valores a un arreglo numpy
        gpu_memory = np.array([int(x.strip().split()[0]) for x in stdout.readlines()])

        # Cerrar la conexión SSH
        ssh.close()

        # Obtener el índice de la GPU con más espacio libre
        gpu_index = np.argmax(gpu_memory)

        return gpu_index

    def borrar(self, nombre):

        ssh1 = self.open_conexion()
        sftp = ssh1.open_sftp()

        remotepath = "/home/{}/samples/{}".format(self.username_whisper, nombre)

        sftp.remove(remotepath)

        sftp.close()
        ssh1.close()
    def diarizar_server(self, nombre_audio):

        ssh1 = self.open_conexion()
        sftp = ssh1.open_sftp()

        nombre_pickle = "output{}.pickle".format(uuid.uuid4())

        comand = "docker run --gpus all -v /home/tmp/diarization:/data my-pyannote-audio /data/{} /data/{} {} {} {}".format(nombre_audio, nombre_pickle, self.server_host, self.username_host, self.password_host)

        stdin, stdout, stderr = ssh1.exec_command(comand)

        if stderr.channel.recv_exit_status() != 0:
            st.write(stderr.read().decode())
        else:
            with open(nombre_pickle, 'rb') as archivo:
                diarization = pickle.load(archivo)
            os.remove(nombre_pickle)
            return diarization

        sftp.close()
        ssh1.close()



