import paramiko
import streamlit as st
import os
from dotenv import load_dotenv




class serv:
    def __init__(self):
        load_dotenv(dotenv_path="cred.env")
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

        remotepath = "/home/{}/samples/sample".format(self.username_whisper)
        with st.spinner("Subiendo archivo..."):
            file.seek(0)
            sftp.putfo(file, remotepath)

        # Cerrar la conexión SFTP y la conexión con el segundo servidor remoto y el primer servidor remoto
        sftp.close()
        ssh1.close()

        st.write("Archivo subido correctamente")

    def whisper(self, file):
        ssh = self.open_conexion()

        comand='CUDA_VISIBLE_DEVICES=1 whisper samples/sample --model small'
        stdin, stdout, stderr = ssh.exec_command(comand)

        # Guardar la salida en una variable
        output = stdout.read().decode()

        # Imprimir la salida en la interfaz de usuario
        st.write(output)

        # Imprimir el error en caso de que algo falle
        if stderr.channel.recv_exit_status() != 0:
            print(stderr.read().decode())

        ssh.close()

