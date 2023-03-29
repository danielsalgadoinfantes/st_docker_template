import paramiko
import streamlit as st
import os
from dotenv import load_dotenv




class server:
    def __init__(self):
        load_dotenv(dotenv_path="cred.env")
        self.username_host = os.environ.get("USER_HOST")
        self.password_host = os.environ.get("PASSWORD_HOST")
        self.server_host = os.environ.get("SERVER_HOST")

        self.username_whisper = os.environ.get("USER_WHISPER")
        self.password_whisper = os.environ.get("PASSWORD_WHISPER")
        self.server_whisper = os.environ.get("SERVER_WHISPER")

    def upload_file(self, file):
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(self.server_host, username=self.username_host, password=self.password_host)

       # Establecer un canal de reenvío a través del primer servidor remoto
        forwarding_channel = ssh1.get_transport().open_channel(
            "direct-tcpip", (self.server_whisper, 22), ('localhost', 0))

        # Conectar al segundo servidor remoto a través del canal de reenvío
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(self.server_whisper, username=self.username_whisper, password=self.password_whisper,
                    sock=forwarding_channel)

        # Abrir una conexión SFTP con el segundo servidor remoto
        sftp = ssh2.open_sftp()


        # Subir el archivo .mp3 al segundo servidor remoto
        extension = file.type.split("/")[-1]
        st.write(extension)
        remotepath = "/home/{}/samples/sample.mp3".format(self.username_whisper)
        with st.spinner("Subiendo archivo..."):
            sftp.putfo(file, remotepath)


        # Cerrar la conexión SFTP y la conexión con el segundo servidor remoto y el primer servidor remoto
        sftp.close()
        ssh2.close()
        ssh1.close()

        st.write("Archivo subido correctamente")

