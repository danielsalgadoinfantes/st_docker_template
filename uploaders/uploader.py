import paramiko
import streamlit as st
import os
from dotenv import load_dotenv




class server:
    def __init__(self):
        load_dotenv()
        self.username = os.environ.get("USER_HOST")
        self.password = os.environ.get("PASSWORD_HOST")
        self.server = "victorupm.duckdns.org"

    def upload_file(self, file):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server, username="tmp", password="d4n13l2023")#(self.server, username=self.user, password=self.password)

        sftp = ssh.open_sftp()
        remote_path = '/home/tmp/samples/sample.mp3'

        with st.spinner("Subiendo archivo..."):
            sftp.putfo(file, remote_path)

        sftp.close()
        ssh.close()

        st.write("Archivo subido correctamente")