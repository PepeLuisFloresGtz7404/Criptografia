

import base64
import string
import time


from problema6 import des_decrypt_ecb


CIPHERTEXT_B64 = "h+F7XMoHpF0="

# ─────────────────────────────────────────────────────────────────────────────
#  FUNCIÓN: verificar si el resultado del descifrado parece texto válido
# ─────────────────────────────────────────────────────────────────────────────

CARACTERES_VALIDOS = set(string.printable)

def es_texto_legible(data: bytes) -> bool:
    
    try:
        texto = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    # Verificar que todos los caracteres sean imprimibles o espacios/tabulaciones
    for c in texto:
        if c not in CARACTERES_VALIDOS:
            return False
    # Filtro adicional: la mayoría deben ser letras/dígitos/símbolos comunes
    conteo_legible = sum(1 for c in texto if c in string.ascii_letters + string.digits + "_-@#$%^&*!?+=")
    return conteo_legible >= len(texto) // 2


def preparar_clave(word: str) -> bytes:
    
    key_bytes = word.encode("utf-8")
    if len(key_bytes) < 8:
        key_bytes = key_bytes.ljust(8, b'\x00')
    elif len(key_bytes) > 8:
        key_bytes = key_bytes[:8]
    return key_bytes


# ─────────────────────────────────────────────────────────────────────────────
#  FUNCIÓN PRINCIPAL: ATAQUE DE FUERZA BRUTA CON DICCIONARIO
# ─────────────────────────────────────────────────────────────────────────────

def ataque_fuerza_bruta(archivo_claves: str, ciphertext_b64: str):
    
    print("=" * 65)
    print("  PROBLEMA 7 – Ataque de fuerza bruta con diccionario (DES-ECB)")
    print("=" * 65)
    print(f"  Ciphertext (Base64) : {ciphertext_b64}")

    # Decodificar el ciphertext de Base64 a bytes
    try:
        cipher_bytes = base64.b64decode(ciphertext_b64)
    except Exception as e:
        print(f"  [ERROR] No se pudo decodificar Base64: {e}")
        return

    print(f"  Ciphertext (bytes)  : {cipher_bytes.hex().upper()}")
    print(f"  Longitud cifrado    : {len(cipher_bytes)} bytes")
    print()

    # Leer el archivo de palabras
    try:
        with open(archivo_claves, "r", encoding="utf-8") as f:
            claves = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"  [ERROR] No se encontró el archivo: {archivo_claves}")
        return

    print(f"  Cargadas {len(claves)} claves del archivo '{archivo_claves}'")
    print(f"  Iniciando ataque...")
    print("─" * 65)

    candidatos = []       # (clave, texto_descifrado)
    inicio = time.time()

    for i, word in enumerate(claves):
        key_bytes = preparar_clave(word)

        try:
            # Intentar descifrar con esta clave
            plain_bytes = des_decrypt_ecb(cipher_bytes, key_bytes)

            # Verificar si el resultado es texto legible
            if es_texto_legible(plain_bytes):
                texto = plain_bytes.decode("utf-8")
                print(f"  [✓] Clave encontrada: {word!r:15} → Descifrado: {texto!r}")
                candidatos.append((word, texto))

        except Exception:
            # El descifrado produjo padding inválido u otro error → clave incorrecta
            pass

    fin = time.time()
    elapsed = fin - inicio

    print("─" * 65)
    print(f"\n  Tiempo de búsqueda : {elapsed:.4f} segundos")
    print(f"  Claves probadas    : {len(claves)}")
    print(f"  Candidatos válidos : {len(candidatos)}")

    if candidatos:
        print("\n" + "═" * 65)
        print("  RESULTADO DEL ATAQUE:")
        print("═" * 65)
        for clave, texto in candidatos:
            print(f"  Clave DES : {clave!r}")
            print(f"  Plaintext : {texto!r}")
            print(f"  Esta es la clave k para el cifrado PlayFair del Problema 7.")
        print("═" * 65)
    else:
        print("\n  [!] No se encontraron claves válidas en el diccionario.")
        print("      Verificar: ¿El ciphertext fue cifrado con una de estas claves?")

    return candidatos


# ─────────────────────────────────────────────────────────────────────────────
#  ANÁLISIS ADICIONAL: ¿QUÉ PASARÍA SIN EL DICCIONARIO?
# ─────────────────────────────────────────────────────────────────────────────

def analisis_tiempo_bruto():
    
    print("\n" + "=" * 65)
    print("  PREGUNTA OBLIGATORIA:")
    print("  ¿Qué pasaría sin el diccionario? ¿Cuánto tiempo tomaría?")
    print("=" * 65)

    # ── Caso 1: Fuerza bruta sobre todos los ASCII imprimibles ──────────────
    print("\n  Caso 1: Clave = 8 caracteres ASCII imprimibles")
    print("  (95 caracteres: letras, dígitos, símbolos)")
    espacio_ascii = 95 ** 8
    print(f"    Espacio total de claves : 95^8 = {espacio_ascii:,}")

    from problema6 import des_encrypt_ecb
    N_mediciones = 1000
    t0 = time.time()
    for _ in range(N_mediciones):
        des_encrypt_ecb(b"testmsgg", b"testkey1")
    t1 = time.time()
    velocidad = N_mediciones / (t1 - t0)   # cifrados por segundo

    print(f"    Velocidad de Python puro : ~{velocidad:,.0f} cifrados/segundo")

    # Con un hilo
    tiempo_segundos = espacio_ascii / velocidad
    tiempo_anios    = tiempo_segundos / (365.25 * 24 * 3600)
    print(f"    Tiempo estimado (1 hilo) : {tiempo_segundos:.2e} segundos")
    print(f"                              = {tiempo_anios:.2e} años")
    print(f"     Completamente inviable en Python puro.")

    # ── Caso 2: Sabemos que la clave son caracteres alfanuméricos + símbolos ─
    print("\n  Caso 2: Clave = 8 caracteres del set words.txt")
    print("  (solo los 100 candidatos del archivo)")
    espacio_dict = 100
    tiempo_dict  = espacio_dict / velocidad
    print(f"    Espacio total de claves : {espacio_dict}")
    print(f"    Tiempo estimado          : {tiempo_dict:.6f} segundos")
    print(f"     Instantáneo. El diccionario hace factible el ataque.")

    # ── Caso 3: Si se usara GPU ────────────────
    print("\n  Caso 3: GPU ")
    gpu_speed = 1e10   
    tiempo_gpu = espacio_ascii / gpu_speed
    print(f"    GPU ~10^10 claves/seg:")
    print(f"    Tiempo para 95^8 claves : {tiempo_gpu:.2e} segundos")
    print(f"                             = {tiempo_gpu/3600:.2f} horas")

# ─────────────────────────────────────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Ataque con diccionario
    candidatos = ataque_fuerza_bruta("words.txt", CIPHERTEXT_B64)

    # Análisis del tiempo sin diccionario
    analisis_tiempo_bruto()