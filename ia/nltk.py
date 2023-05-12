import nltk
nltk.download('punkt')

class Nltk:

    @staticmethod
    def dividir_texto(texto, max_longitud=4096):

        if not isinstance(texto, str):
            raise TypeError("El parámetro 'texto' debe ser una cadena de texto. " + str(type(texto)))


        # Divide el texto en oraciones
        oraciones = nltk.sent_tokenize(texto)

        # Une las oraciones en fragmentos de longitud aproximada
        fragmentos = []
        fragmento_actual = ""
        for oracion in oraciones:
            if len(fragmento_actual) + len(oracion) < max_longitud:
                fragmento_actual += oracion + " "
            else:
                fragmentos.append(fragmento_actual.strip())
                fragmento_actual = oracion + " "

        # Agrega el último fragmento
        fragmentos.append(fragmento_actual.strip())

        return fragmentos