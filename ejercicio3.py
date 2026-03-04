from math import gcd
from collections import Counter

TEXTO_CIFRADO = "ECISCRVSWVLGDDWUEFHFNGESXUVTICOKQOTAJPHWAKFBNAEUONOJFHONCPHRZNSCOKEWLSUFPFEEUWOMHPQFAEEDOLDBQROKFZLNQBSXVMFZZNMQQSACESDDVMONHBROUEBGMOCVISLZAOXDGTJDAQVZLDRTOVAKDDWOKJTFEJBBFNHBGLCRJRLSKVEVUDBXOPVDVZADBGSLCPOKUWSSJCRQWCOLFOKUC"


def buscar_repeticiones(texto, largo=3):
    registro = {}
    for inicio in range(len(texto) - largo + 1):
        fragmento = texto[inicio: inicio + largo]
        registro.setdefault(fragmento, []).append(inicio)
    return {k: v for k, v in registro.items() if len(v) > 1}


def calcular_espaciados(apariciones_dict):
    gaps = []
    for posiciones in apariciones_dict.values():
        posiciones_ord = sorted(posiciones)
        for k in range(len(posiciones_ord) - 1):
            gaps.append(posiciones_ord[k + 1] - posiciones_ord[k])
    return gaps


def divisores_de(n):
    return [d for d in range(2, n + 1) if n % d == 0]


def kasiski():
    repetidos = buscar_repeticiones(TEXTO_CIFRADO)
    distancias = calcular_espaciados(repetidos)

    print("Distancias encontradas:", distancias)

    # Contar qué divisores aparecen con más frecuencia entre todas las distancias
    # Esto es más robusto que el MCD global, ya que una sola distancia "accidental"
    # no arruina el resultado (como pasaba con la distancia 15 del trigrama OKU)
    conteo_divisores = Counter()
    for d in distancias:
        for div in divisores_de(d):
            conteo_divisores[div] += 1

    print("\nDivisores más frecuentes (posibles longitudes de clave):")
    for longitud, frecuencia in conteo_divisores.most_common(6):
        print(f"  Longitud {longitud}: aparece en {frecuencia} distancia(s)")

    mejor_candidato = conteo_divisores.most_common(1)[0][0]
    print(f"\nLongitud de clave más probable: 1")


def main():
    kasiski()


if __name__ == "__main__":
    main()