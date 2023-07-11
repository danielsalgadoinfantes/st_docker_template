# Start from a base CUDA-enabled Python 3.8 image
FROM nvidia/cuda:11.6.2-base-ubuntu20.04

# Update and install some dependencies
RUN apt-get update && apt-get install -y python3.8 python3-pip libsndfile1

# Set a working directory

WORKDIR /app


# Install pyannote.audio

RUN pip install -qq https://github.com/pyannote/pyannote-audio/archive/refs/heads/develop.zip

RUN python3 -m pip install --force-reinstall soundfile

RUN python3 -m pip install pydub

RUN python3 -m pip install paramiko


# Copy your Python script into the container

COPY pruebas.py .

# Define the entrypoint script that will receive the arguments

ENTRYPOINT ["python3", "pruebas.py"]




