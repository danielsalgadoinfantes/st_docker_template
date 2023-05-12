import os


class Audio:

    @staticmethod
    def valid_size(file_path):

        # Obtener el tamaño del archivo en bytes
        file_size_bytes = os.path.getsize(file_path)
        # Convertir a megabytes
        file_size_mb = file_size_bytes / (1024 * 1024)
        # Comprobar si el tamaño es mayor que 25MB
        if file_size_mb > 25:
            return True
        else:
            return False



