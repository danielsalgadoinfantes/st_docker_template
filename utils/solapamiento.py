

class Solapamiento:

    @staticmethod
    def encontrar_texto(texto1, texto2):
        txt1 = texto1.lower().replace(".", "")  # .replace(",", "")
        txt2 = texto2.lower().replace(".", "")  # .replace(",", "")

        if texto1[len(texto1) - 1] == ".":
            punto = 1
        else:
            punto = 0

        indice = txt1.find(txt2)
        if indice != -1:
            res = texto1[:indice + len(texto2)]
            puntos = res.count(".")
            # comas = res.count(",")
            return True, texto1[:indice + puntos - punto]  # +len(texto2)]#+ comas]
        else:
            return False, "No se encontró el texto 2 en el texto 1."

    @staticmethod
    def recortar_texto(texto1, texto2):
        # print(texto2)

        # Divide el texto en una lista de palabras
        palabras = texto2.split()
        i = 0
        encontrado = False
        while not encontrado and i < len(palabras):
            iteracion = palabras[:len(palabras) - i]
            result = " ".join(iteracion)
            bol, txt = Solapamiento.encontrar_texto(texto1, result)
            encontrado = bol
            # print(str(i) + " :" + str(encontrado) + " --> " + txt)
            i += 1

        if encontrado:
            return txt, encontrado
        else:
            return texto1, encontrado
