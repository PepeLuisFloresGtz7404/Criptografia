

import base64


S_BOXES = [
    # S1
    [[14, 4,13, 1, 2,15,11, 8, 3,10, 6,12, 5, 9, 0, 7],
     [ 0,15, 7, 4,14, 2,13, 1,10, 6,12,11, 9, 5, 3, 8],
     [ 4, 1,14, 8,13, 6, 2,11,15,12, 9, 7, 3,10, 5, 0],
     [15,12, 8, 2, 4, 9, 1, 7, 5,11, 3,14,10, 0, 6,13]],
    # S2
    [[15, 1, 8,14, 6,11, 3, 4, 9, 7, 2,13,12, 0, 5,10],
     [ 3,13, 4, 7,15, 2, 8,14,12, 0, 1,10, 6, 9,11, 5],
     [ 0,14, 7,11,10, 4,13, 1, 5, 8,12, 6, 9, 3, 2,15],
     [13, 8,10, 1, 3,15, 4, 2,11, 6, 7,12, 0, 5,14, 9]],
    # S3
    [[10, 0, 9,14, 6, 3,15, 5, 1,13,12, 7,11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6,10, 2, 8, 5,14,12,11,15, 1],
     [13, 6, 4, 9, 8,15, 3, 0,11, 1, 2,12, 5,10,14, 7],
     [ 1,10,13, 0, 6, 9, 8, 7, 4,15,14, 3,11, 5, 2,12]],
    # S4
    [[ 7,13,14, 3, 0, 6, 9,10, 1, 2, 8, 5,11,12, 4,15],
     [13, 8,11, 5, 6,15, 0, 3, 4, 7, 2,12, 1,10,14, 9],
     [10, 6, 9, 0,12,11, 7,13,15, 1, 3,14, 5, 2, 8, 4],
     [ 3,15, 0, 6,10, 1,13, 8, 9, 4, 5,11,12, 7, 2,14]],
    # S5
    [[ 2,12, 4, 1, 7,10,11, 6, 8, 5, 3,15,13, 0,14, 9],
     [14,11, 2,12, 4, 7,13, 1, 5, 0,15,10, 3, 9, 8, 6],
     [ 4, 2, 1,11,10,13, 7, 8,15, 9,12, 5, 6, 3, 0,14],
     [11, 8,12, 7, 1,14, 2,13, 6,15, 0, 9,10, 4, 5, 3]],
    # S6
    [[12, 1,10,15, 9, 2, 6, 8, 0,13, 3, 4,14, 7, 5,11],
     [10,15, 4, 2, 7,12, 9, 5, 6, 1,13,14, 0,11, 3, 8],
     [ 9,14,15, 5, 2, 8,12, 3, 7, 0, 4,10, 1,13,11, 6],
     [ 4, 3, 2,12, 9, 5,15,10,11,14, 1, 7, 6, 0, 8,13]],
    # S7
    [[ 4,11, 2,14,15, 0, 8,13, 3,12, 9, 7, 5,10, 6, 1],
     [13, 0,11, 7, 4, 9, 1,10,14, 3, 5,12, 2,15, 8, 6],
     [ 1, 4,11,13,12, 3, 7,14,10,15, 6, 8, 0, 5, 9, 2],
     [ 6,11,13, 8, 1, 4,10, 7, 9, 5, 0,15,14, 2, 3,12]],
    # S8
    [[13, 2, 8, 4, 6,15,11, 1,10, 9, 3,14, 5, 0,12, 7],
     [ 1,15,13, 8,10, 3, 7, 4,12, 5, 6,11, 0,14, 9, 2],
     [ 7,11, 4, 1, 9,12,14, 2, 0, 6,10,13,15, 3, 5, 8],
     [ 2, 1,14, 7, 4,10, 8,13,15,12, 9, 0, 3, 5, 6,11]],
]

# ─────────────────────────────────────────────────────────────────────────────
#  MATRICES DE PERMUTACIÓN 
# ─────────────────────────────────────────────────────────────────────────────

# Permutación Inicial (IP): reorganiza los 64 bits del bloque de entrada
IP = [
    58,50,42,34,26,18,10, 2,
    60,52,44,36,28,20,12, 4,
    62,54,46,38,30,22,14, 6,
    64,56,48,40,32,24,16, 8,
    57,49,41,33,25,17, 9, 1,
    59,51,43,35,27,19,11, 3,
    61,53,45,37,29,21,13, 5,
    63,55,47,39,31,23,15, 7,
]

# Permutación Final (FP = IP^{-1}): inversa de IP
FP = [
    40, 8,48,16,56,24,64,32,
    39, 7,47,15,55,23,63,31,
    38, 6,46,14,54,22,62,30,
    37, 5,45,13,53,21,61,29,
    36, 4,44,12,52,20,60,28,
    35, 3,43,11,51,19,59,27,
    34, 2,42,10,50,18,58,26,
    33, 1,41, 9,49,17,57,25,
]

# Expansión E: expande 32 bits → 48 bits para XOR con la subclave
E = [
    32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32, 1,
]

# Permutación P: mezcla la salida de las S-boxes (32 bits)
P = [
    16, 7,20,21,
    29,12,28,17,
     1,15,23,26,
     5,18,31,10,
     2, 8,24,14,
    32,27, 3, 9,
    19,13,30, 6,
    22,11, 4,25,
]

# PC1: reduce la clave de 64 a 56 bits (elimina los bits de paridad)
PC1 = [
    57,49,41,33,25,17, 9,
     1,58,50,42,34,26,18,
    10, 2,59,51,43,35,27,
    19,11, 3,60,52,44,36,
    63,55,47,39,31,23,15,
     7,62,54,46,38,30,22,
    14, 6,61,53,45,37,29,
    21,13, 5,28,20,12, 4,
]

# PC2: reduce de 56 a 48 bits para generar cada subclave de ronda
PC2 = [
    14,17,11,24, 1, 5,
     3,28,15, 6,21,10,
    23,19,12, 4,26, 8,
    16, 7,27,20,13, 2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32,
]

# Desplazamientos de rotación para cada una de las 16 rondas
KEY_SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]


# ─────────────────────────────────────────────────────────────────────────────
#  FUNCIONES DEL ALGORITMO DES
# ─────────────────────────────────────────────────────────────────────────────

def permute(block: int, table: list, bits: int) -> int:
   
    result = 0
    for pos in table:
        result = (result << 1) | ((block >> (bits - pos)) & 1)
    return result


def left_rotate(val: int, shift: int, size: int) -> int:
    
    mask = (1 << size) - 1
    return ((val << shift) & mask) | (val >> (size - shift))


def sbox_substitution(block: int) -> int:
    
    result = 0
    for i in range(8):
        # Extraer bloque de 6 bits para la S-box i
        # Los bits van del más significativo al menos: posiciones 47..0
        chunk = (block >> (42 - 6 * i)) & 0x3F  # 0x3F = 0b111111
        # Fila: bit 5 (MSB) y bit 0 (LSB) del chunk
        row = ((chunk & 0x20) >> 4) | (chunk & 0x01)
        # Columna: bits 4..1
        col = (chunk >> 1) & 0x0F
        result = (result << 4) | S_BOXES[i][row][col]
    return result


def generate_subkeys(key_int: int) -> list:
    
    # Paso 1: Aplicar PC1 para pasar de 64 a 56 bits
    key56 = permute(key_int, PC1, 64)

    # Paso 2: Dividir en mitad izquierda (C) y derecha (D) de 28 bits cada una
    C = (key56 >> 28) & 0xFFFFFFF
    D =  key56        & 0xFFFFFFF

    subkeys = []
    for i in range(16):
        # Paso 3: Rotar cada mitad según KEY_SHIFT
        C = left_rotate(C, KEY_SHIFT[i], 28)
        D = left_rotate(D, KEY_SHIFT[i], 28)

        # Concatenar C y D (56 bits)
        CD = (C << 28) | D

        # Paso 4: Aplicar PC2 para obtener subclave de 48 bits
        subkeys.append(permute(CD, PC2, 56))

    return subkeys


def des_block(block: int, subkeys: list) -> int:
    
    # 1. Permutación inicial
    block = permute(block, IP, 64)

    # Dividir en mitad izquierda y derecha de 32 bits
    L = (block >> 32) & 0xFFFFFFFF
    R =  block        & 0xFFFFFFFF

    # 2. 16 rondas de Feistel
    for K in subkeys:
        L_prev = L
        R_prev = R

        # Función f de Feistel:
        #   a. Expandir R: 32 → 48 bits con E
        R_expanded = permute(R_prev, E, 32)
        #   b. XOR con la subclave de ronda
        R_xor = R_expanded ^ K
        #   c. Sustitución S-boxes: 48 → 32 bits
        R_sbox = sbox_substitution(R_xor)
        #   d. Permutación P
        R_perm = permute(R_sbox, P, 32)

        # Nueva mitad derecha: L_{i-1} XOR f(R_{i-1}, K_i)
        R = L_prev ^ R_perm
        # Nueva mitad izquierda: R_{i-1}
        L = R_prev

    # 3. Intercambio final (swap R y L antes de aplicar FP)
    pre_output = (R << 32) | L

    # 4. Permutación final
    return permute(pre_output, FP, 64)




def pad_mensaje(data: bytes, block_size: int = 8) -> bytes:
    
    diferencia = (block_size - len(data) % block_size) % block_size
    return data + b'\x00' * diferencia

def unpad_mensaje(data: bytes, longitud_original: int) -> bytes:
    
    return data[:longitud_original] if longitud_original else data.rstrip(b'\x00')


# ─────────────────────────────────────────────────────────────────────────────
#  FUNCIONES PRINCIPALES: CIFRAR Y DESCIFRAR EN MODO ECB
#  ECB (Electronic Codebook): cada bloque de 8 bytes se cifra
#  de forma independiente con la misma clave.
# ─────────────────────────────────────────────────────────────────────────────

def des_encrypt_ecb(plaintext: bytes, key_bytes: bytes) -> bytes:
    
    if len(key_bytes) != 8:
        raise ValueError(f"La clave debe tener exactamente 8 bytes, tiene {len(key_bytes)}")

    # Convertir clave a entero de 64 bits
    key_int = int.from_bytes(key_bytes, "big")

    # Generar las 16 subclaves
    subkeys = generate_subkeys(key_int)

    # Aplicar padding al mensaje (sin bloque extra si ya es múltiplo de 8)
    padded = pad_mensaje(plaintext, 8)

    ciphertext = b""
    # Procesar cada bloque de 8 bytes (64 bits) de forma independiente (ECB)
    for i in range(0, len(padded), 8):
        block_bytes = padded[i:i + 8]
        block_int   = int.from_bytes(block_bytes, "big")
        enc_int     = des_block(block_int, subkeys)
        ciphertext += enc_int.to_bytes(8, "big")

    return ciphertext


def des_decrypt_ecb(ciphertext: bytes, key_bytes: bytes) -> bytes:
    
    if len(key_bytes) != 8:
        raise ValueError(f"La clave debe tener exactamente 8 bytes, tiene {len(key_bytes)}")
    if len(ciphertext) % 8 != 0:
        raise ValueError("El ciphertext debe ser múltiplo de 8 bytes")

    # Convertir clave a entero
    key_int = int.from_bytes(key_bytes, "big")

    # Para descifrar: invertir el orden de las subclaves (K16..K1)
    subkeys = generate_subkeys(key_int)
    subkeys.reverse()

    plaintext_padded = b""
    # Descifrar cada bloque de 8 bytes de forma independiente (ECB)
    for i in range(0, len(ciphertext), 8):
        block_bytes = ciphertext[i:i + 8]
        block_int   = int.from_bytes(block_bytes, "big")
        dec_int     = des_block(block_int, subkeys)
        plaintext_padded += dec_int.to_bytes(8, "big")

    return unpad_mensaje(plaintext_padded, 0)


# ─────────────────────────────────────────────────────────────────────────────
#  FUNCIONES DE CONVENIENCIA: trabajan directamente con strings y Base64
# ─────────────────────────────────────────────────────────────────────────────

def encrypt_to_base64(message: str, key: str) -> str:
    
    cipher_bytes  = des_encrypt_ecb(message.encode("utf-8"), key.encode("utf-8"))
    return base64.b64encode(cipher_bytes).decode("ascii")


def decrypt_from_base64(cipher_b64: str, key: str) -> str:
    
    cipher_bytes  = base64.b64decode(cipher_b64)
    plain_bytes   = des_decrypt_ecb(cipher_bytes, key.encode("utf-8"))
    return plain_bytes.decode("utf-8")


# ─────────────────────────────────────────────────────────────────────────────
#  PROGRAMA PRINCIPAL – DEMOSTRACIÓN Y VERIFICACIÓN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 60)
    print("  PROBLEMA 6 – DES desde cero (modo ECB, salida Base64)")
    print("=" * 60)

    # ── Caso del enunciado ───────────────────────────────────────────────────
    mensaje  = "noche697"
    clave    = "data7Qa="
    esperado = "obuzqeTZFwc="

    cifrado = encrypt_to_base64(mensaje, clave)
    print(f"\n  Mensaje  (plaintext) : {mensaje!r}")
    print(f"  Clave    (key)       : {clave!r}")
    print(f"  Cifrado  (Base64)    : {cifrado}")
    print(f"  Esperado (enunciado) : {esperado}")
    print(f"  {' CORRECTO' if cifrado == esperado else ' DIFERENCIA – revisar implementación'}")

    # ── Verificar descifrado ─────────────────────────────────────────────────
    descifrado = decrypt_from_base64(cifrado, clave)
    print(f"\n  Descifrado           : {descifrado!r}")
    print(f"  {' Descifrado correcto' if descifrado == mensaje else ' Error en descifrado'}")

    # ── Otro ejemplo de prueba ───────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  Otro ejemplo:")
    msg2  = "Hola123!"   # exactamente 8 bytes
    key2  = "CryptoK1"
    c2    = encrypt_to_base64(msg2, key2)
    dec2  = decrypt_from_base64(c2, key2)
    print(f"  Mensaje    : {msg2!r}")
    print(f"  Clave      : {key2!r}")
    print(f"  Cifrado B64: {c2}")
    print(f"  Descifrado : {dec2!r}")
    print(f"  {' OK' if dec2 == msg2 else ' Error'}")

    # ── Mensaje más largo (>8 bytes, requiere padding) ───────────────────────
    print("\n" + "─" * 60)
    print("  Ejemplo con mensaje más largo (padding PKCS7):")
    msg3 = "Criptografia2026"   # 16 bytes (2 bloques exactos)
    key3 = "data7Qa="
    c3   = encrypt_to_base64(msg3, key3)
    dec3 = decrypt_from_base64(c3, key3)
    print(f"  Mensaje    : {msg3!r}  (len={len(msg3)})")
    print(f"  Cifrado B64: {c3}")
    print(f"  Descifrado : {dec3!r}")
    print(f"  {' OK' if dec3 == msg3 else ' Error'}")
