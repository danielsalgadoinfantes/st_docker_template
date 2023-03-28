import paramiko
import streamlit as st

class server:
    def __init__(self, usuario, contra, server):
        self.server=server
        self.user=usuario
        self.password=contra
    
    def upload_file(self, file):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server, username=self.user, password=self.password)

        sftp = ssh.open_sftp()
        remote_path = '/home/tmp/samples/sample.mp3'

        with st.spinner("Subiendo archivo..."):
            sftp.putfo(file, remote_path)

        sftp.close()
        ssh.close()

        st.write("Archivo subido correctamente")