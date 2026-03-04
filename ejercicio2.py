CUADRADO = [
    ['a', 'b', 'c', 'd', 'e'],
    ['f', 'g', 'h', 'i', 'j'],
    ['k', 'l', 'm', 'n', 'o'],
    ['p', 'q', 'r', 's', 't'],
    ['u', 'v', 'w', 'x', 'y'],
]

_LOOKUP = {CUADRADO[r][c]: (r, c) for r in range(5) for c in range(5)}


def pares_a_texto(secuencia):
    letras = []
    it = iter(secuencia)
    for fila in it:
        col = next(it)
        letras.append(CUADRADO[fila - 1][col - 1])
    return "".join(letras)


def texto_a_pares(cadena):
    tokens = []
    for ch in cadena:
        if ch in _LOOKUP:
            r, c = _LOOKUP[ch]
            tokens.append(f"{r+1}{c+1}")
    return " ".join(tokens)


def descifrar_polibio():
    codigo = [
        1,5, 3,2, 4,5, 2,4, 1,5, 3,3, 4,1, 3,5,
        3,4, 3,5, 1,5, 4,4, 4,1, 1,5, 4,3, 1,1,
        1,1, 3,4, 1,1, 1,4, 2,4, 1,5
    ]
    print("Mensaje descifrado:", pares_a_texto(codigo))


def cifrar_polibio():
    frase = (
        "si la felicidad tuviera una forma tendria forma de cristal porque puede estar "
        "a tu alrededor sin que la notes pero si cambias de perspectiva puede reflejar "
        "una luz capaz de iluminarlo todo"
    )
    print("Mensaje cifrado:", texto_a_pares(frase))


def main():
    descifrar_polibio()
    cifrar_polibio()


if __name__ == "__main__":
    main()