from pyannote.audio import Pipeline
import tempfile
import argparse
import pickle
import uuid
import os
import paramiko

def send(output, server, username, password):
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(server, username=username, password=password)

    sftp = ssh1.open_sftp()

    nombre_archivo = os.path.basename(output)

    print(nombre_archivo)

    remotepath = "/home/{}/st_docker_template/{}".format(username, nombre_archivo)

    with open(output, "rb") as picklefile:
        sftp.putfo(picklefile, remotepath)

    # Cerrar la conexión SFTP y la conexión con el servidor remoto
    sftp.close()
    ssh1.close()


def main(path, output, server, user, passw):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                                use_auth_token="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")

    with open(path, "rb") as audio_bytes:

        with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
            temp_file.write(audio_bytes.read())
            file_path = temp_file.name
            # 4. apply pretrained pipeline
            pipeline.to("cuda")
            diarization = pipeline(file_path)
            #try:
            with open(output, "wb") as pickle_file:
                pickle.dump(diarization, pickle_file)
            send(output, server, user, passw)
            os.remove(output)
            #except Exception as e:
            #    print("Error al guardar el archivo pickle:", str(e))
    os.remove(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The path to the input audio file")
    parser.add_argument("output", help="The path dir to the output file")
    parser.add_argument("server", help="the server where to copy the output file")
    parser.add_argument("user", help="The user to acces the server where to copy the output file")
    parser.add_argument("passw", help="The password to acces the server where to copy the output file")

    args = parser.parse_args()
    main(args.path, args.output, args.server, args.user, args.passw)


file_path=""



from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                           use_auth_token="token_usuario")
diarization = pipeline(file_path)

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"[{speaker}] --> ({turn.start}, {turn.end})")