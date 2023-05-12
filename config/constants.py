class Constants:
    def __init__(self):
        self.AUDIO_TYPE = ["mp3", "wav", "aac", "wma", "ogg", "flac", 
                           "alac", "aiff", "au", "m4a"]
        self.IDIOMAS = ["Ingles", "Español"]

        self.MODELS = ["tiny", "base", "small", "medium", "large"]

        self.OPCIONES_EJECUCION = ["Servidor remoto", "API de whisper"]

        self.MAX_TOKENS = 4096