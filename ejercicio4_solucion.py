import hashlib
import math
import unicodedata
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ─────────────────────────────────────────────
# PASO 1 — Cargar y filtrar el texto
# ─────────────────────────────────────────────
with open("file.txt", encoding="utf-8") as f:
    texto_raw = f.read()

def solo_letras(texto):
    """Normaliza unicode (quita tildes) y deja solo letras a-z."""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if c.isalpha() and ord(c) < 128).lower()

letras = solo_letras(texto_raw)
print(f"[1] Letras filtradas: {len(letras)} caracteres")
print(f"    Muestra: {letras[:40]}...\n")

# ─────────────────────────────────────────────
# PASO 2 — Generar índices primos
# ─────────────────────────────────────────────
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

primos = [i for i in range(5000) if es_primo(i)]
print(f"[2] Primeros 10 primos: {primos[:10]}\n")

# ─────────────────────────────────────────────
# PASO 3 — Extraer caracteres del texto (cíclico)
#   Desplazamiento: índice = (primo - 2) % len(letras)
# ─────────────────────────────────────────────
extraidos = [letras[(p - 2) % len(letras)] for p in primos[:100]]
print(f"[3] Primeros 25 chars extraídos: {''.join(extraidos[:25])}\n")

# ─────────────────────────────────────────────
# PASO 4 — Construir la clave de 50 caracteres
#   Inserción cíclica de "kevinmitnick":
#   posición par  → char extraído del texto
#   posición impar → char de kevinmitnick (cíclico)
# ─────────────────────────────────────────────
PALABRA_BASE = "kevinmitnick"
clave_chars = []
ki = 0  # índice en kevinmitnick
ei = 0  # índice en extraidos

for pos in range(50):
    if pos % 2 == 0:          # par → del texto
        clave_chars.append(extraidos[ei])
        ei += 1
    else:                      # impar → de kevinmitnick
        clave_chars.append(PALABRA_BASE[ki % len(PALABRA_BASE)])
        ki += 1

CLAVE = "".join(clave_chars)
print(f"[4] Clave construida (50 chars):\n    {CLAVE}\n")

# ─────────────────────────────────────────────
# PASO 5 — Calcular SHA-256 y verificar contra hashes.txt
# ─────────────────────────────────────────────
clave_hash = hashlib.sha256(CLAVE.encode()).hexdigest()
print(f"[5] SHA-256 de la clave:\n    {clave_hash}\n")

with open("hashes.txt") as f:
    lista_hashes = set(f.read().strip().split("\n"))

if clave_hash in lista_hashes:
    print("     El hash está en hashes.txt — ¡clave válida!\n")
else:
    print("     El hash NO está en la lista. Revisa la construcción de la clave.\n")

# ─────────────────────────────────────────────
# PASO 6 — Descifrado AES-GCM
# ─────────────────────────────────────────────
def derive_key(key: str) -> bytes:
    """Deriva la clave AES de 32 bytes usando SHA-256."""
    return hashlib.sha256(key.encode()).digest()

def decrypt_gcm(cipher_data: bytes, key: str) -> str:
    """
    Descifra AES-GCM.
    Formato esperado: nonce (12 bytes) || ciphertext+tag
    """
    key_bytes = derive_key(key)
    aesgcm = AESGCM(key_bytes)
    nonce = cipher_data[:12]
    ciphertext = cipher_data[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")

# Cargar cipher.txt — línea 0 (78 bytes = 12 nonce + 50 texto + 16 tag)
with open("cipher.txt") as f:
    lineas = f.read().strip().split("\n")

print("[6] Intentando descifrar cada línea del cipher.txt...")
for i, linea in enumerate(lineas):
    linea = linea.strip()
    # Las líneas con número impar de caracteres llevan un 0 inicial perdido
    if len(linea) % 2 == 1:
        linea = "0" + linea
    try:
        cipher_bytes = bytes.fromhex(linea)
    except ValueError:
        continue
    if len(cipher_bytes) < 28:   # mínimo: 12 nonce + 0 bytes + 16 tag
        continue
    try:
        mensaje = decrypt_gcm(cipher_bytes, CLAVE)
        print(f"\n     Línea {i} descifrada:")
        print(f"    {mensaje}")
    except Exception:
        print(f"    Línea {i}: sin resultado (tag incorrecto o formato diferente)")

print("\n─── Resumen ──────────────────────────────────────────")
print(f"Clave (50 chars) : {CLAVE}")
print(f"SHA-256 de clave : {clave_hash}")
print(f"Hash en lista    : {'Sí' if clave_hash in lista_hashes else 'No'}")
