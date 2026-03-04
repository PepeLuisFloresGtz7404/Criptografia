ALFABETO_ES = list("abcdefghijklmnñopqrstuvwxyz")
TAM = len(ALFABETO_ES)


def _transformar(texto, desplazamiento):
    resultado = []
    for caracter in texto:
        c_lower = caracter.lower()
        if c_lower in ALFABETO_ES:
            pos_original = ALFABETO_ES.index(c_lower)
            pos_nueva = (pos_original - desplazamiento) % TAM
            letra = ALFABETO_ES[pos_nueva]
            resultado.append(letra.upper() if caracter.isupper() else letra)
        else:
            resultado.append(caracter)
    return "".join(resultado)


def fuerza_bruta_cesar():
    texto_enc = "Nc xkfc gu dgnnc"
    print("=== Fuerza Bruta ===")
    for clave in range(TAM):
        candidato = _transformar(texto_enc, clave)
        print(f"  Turno {clave:02d} -> {candidato}")


def conocimiento_previo_cesar():
    texto_enc = "Zo qgweidugot ́io sh jb hsqgsid"
    letra_cifrada = "o"
    letra_original = "d"
    shift = (ALFABETO_ES.index(letra_original) - ALFABETO_ES.index(letra_cifrada)) % TAM
    print("=== Conocimiento Previo ===")
    print("Texto original:", _transformar(texto_enc, shift))


def analisis_frecuencias_cesar():
    texto_enc = "Jx qzd kfhnp mjwnw f ptx ijqfx xnr ifwxj hzjryf xtgwj ytit hzfrit jwjx  ̃ntajr"
    conteo = {}
    for ch in texto_enc.lower():
        if ch in ALFABETO_ES:
            conteo[ch] = conteo.get(ch, 0) + 1

    letra_top = sorted(conteo, key=lambda x: conteo[x], reverse=True)[0]
    despl = (ALFABETO_ES.index(letra_top) - ALFABETO_ES.index("e")) % TAM

    print("=== Análisis de Frecuencias ===")
    print("Texto descifrado:", _transformar(texto_enc, despl))


def main():
    fuerza_bruta_cesar()
    print("=" * 80)
    conocimiento_previo_cesar()
    print("=" * 80)
    analisis_frecuencias_cesar()


if __name__ == "__main__":
    main()