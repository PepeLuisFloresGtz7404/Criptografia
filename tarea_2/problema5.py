

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────────────────────────────────────
#  1. FUNCIONES MATEMÁTICAS AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────

def gcd(a: int, b: int) -> int:
    
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    
    return (a // gcd(a, b)) * b

def mod_pow(base: int, exp: int, mod: int) -> int:
    
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

def es_primo(n: int) -> bool:
    
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def lambda_rsa(p: int, q: int) -> int:
    
    return lcm(p - 1, q - 1)

# ─────────────────────────────────────────────────────────────────────────────
#  2. PARÁMETROS RSA (primos pequeños para demostración visual)
# ─────────────────────────────────────────────────────────────────────────────
#


CASOS = [
    {"p": 13,  "q":  7,  "e": 5,  "label": "p=13, q=7   (λ=12, muy vulnerable)"},
    {"p": 61,  "q": 53,  "e": 17, "label": "p=61, q=53  (λ=780)"},
    {"p": 89,  "q": 97,  "e": 5,  "label": "p=89, q=97  (λ=1056)"},
]


CASO = CASOS[1]          
p, q, e = CASO["p"], CASO["q"], CASO["e"]

# ─────────────────────────────────────────────────────────────────────────────
#  3. CÁLCULO DE PARÁMETROS RSA
# ─────────────────────────────────────────────────────────────────────────────

n      = p * q
phi_n  = (p - 1) * (q - 1)
lam_n  = lambda_rsa(p, q)
gcdd   = gcd(p - 1, q - 1)


assert gcd(e, phi_n) == 1, f"e={e} no es coprimo con φ(n)={phi_n}"
assert es_primo(p) and es_primo(q), "p y q deben ser primos"


N     = lam_n
dstar = 1.17741 * math.sqrt(N)
dstar_ceil = math.ceil(dstar)

print("=" * 60)
print("  PARÁMETROS RSA – Birthday Attack")
print("=" * 60)
print(f"  p          = {p}  (primo)")
print(f"  q          = {q}  (primo)")
print(f"  n = p·q    = {n}")
print(f"  e          = {e}  (exponente público)")
print(f"  φ(n)       = {phi_n}")
print(f"  gcd(p-1,q-1) = {gcdd}")
print(f"  λ(n) = lcm(p-1,q-1) = {lam_n}")
print(f"")
print(f"  Espacio efectivo N = λ(n) = {N}")
print(f"  d* (inflexión) = 1.17741·√{N} ≈ {dstar:.4f}")
print(f"  d* redondeado  = {dstar_ceil} mensajes")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────────
#  4. CURVA TEÓRICA DE PROBABILIDAD DE COLISIÓN
# ─────────────────────────────────────────────────────────────────────────────
#


max_d = math.ceil(dstar * 4)  # Graficamos hasta 4 veces el punto de inflexión
valores_d = np.arange(1, max_d + 1)

def prob_colision_teorica(d: np.ndarray, N: int) -> np.ndarray:
    
    return 1.0 - np.exp(-d * (d - 1) / (2.0 * N))

p_teorica = prob_colision_teorica(valores_d, N)

# ─────────────────────────────────────────────────────────────────────────────
#  5. SIMULACIÓN DE MONTECARLO
# ─────────────────────────────────────────────────────────────────────────────
#

NUM_ENSAYOS = 500   
print(f"\n  Ejecutando {NUM_ENSAYOS} ensayos de Montecarlo...")

colisiones_acum = np.zeros(max_d + 1, dtype=int)

for ensayo in range(NUM_ENSAYOS):
    vistos = {}          
    colision_en = max_d  

    for d in range(1, max_d + 1):
        
        m = random.randint(2, n - 1)
        
        c = mod_pow(m, e, n)

        if c in vistos and vistos[c] != m:
            
            colision_en = d
            break
        else:
            vistos[c] = m

    
    for d in range(colision_en, max_d + 1):
        colisiones_acum[d] += 1


p_montecarlo = colisiones_acum[1:max_d + 1] / NUM_ENSAYOS

print(f"  Completado.")

# ─────────────────────────────────────────────────────────────────────────────
#  6. CÁLCULO DEL PUNTO DE INFLEXIÓN Y RESULTADOS NUMÉRICOS
# ─────────────────────────────────────────────────────────────────────────────

p_en_dstar = prob_colision_teorica(np.array([dstar_ceil]), N)[0]


d_montecarlo_50 = None
for i, p_val in enumerate(p_montecarlo):
    if p_val >= 0.5:
        d_montecarlo_50 = i + 1  
        break

print(f"\n  RESULTADOS:")
print(f"  P(d*, N) teórica   = {p_en_dstar:.4f}  ({p_en_dstar*100:.2f}%)")
print(f"  d* = {dstar_ceil} → Para {dstar_ceil} mensajes interceptados, P ≈ 50%")
if d_montecarlo_50:
    print(f"  d empírico (P≥50%) = {d_montecarlo_50} mensajes (simulación)")
print(f"\n  P(2·d*) = {prob_colision_teorica(np.array([2*dstar_ceil]), N)[0]:.4f}")
print(f"  Para {2*dstar_ceil} mensajes (2·d*), P ≈ {prob_colision_teorica(np.array([2*dstar_ceil]), N)[0]*100:.1f}%")

# ─────────────────────────────────────────────────────────────────────────────
#  7. GRÁFICA
# ─────────────────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('white')

# Curva teórica
ax.plot(valores_d, p_teorica * 100,
        color='#2166ac', linewidth=2.5, label='Curva teórica $P(d, \\lambda(n))$')
ax.fill_between(valores_d, p_teorica * 100, alpha=0.08, color='#2166ac')

# Simulación Montecarlo
ax.plot(valores_d, p_montecarlo * 100,
        color='#1a7a4a', linewidth=1.5, linestyle='--',
        marker='o', markersize=2, label=f'Simulación Montecarlo ({NUM_ENSAYOS} ensayos)')

# Línea de P = 50%
ax.axhline(50, color='#888888', linewidth=1, linestyle=':', label='P = 50%')

# Línea del punto de inflexión d*
ax.axvline(dstar_ceil, color='#d62728', linewidth=1.8, linestyle='--',
           label=f'Punto de inflexión $d^*$ = {dstar_ceil}')

# Anotación del punto de inflexión
ax.annotate(
    f' $d^*$ = {dstar_ceil}\n P ≈ {p_en_dstar*100:.1f}%',
    xy=(dstar_ceil, p_en_dstar * 100),
    xytext=(dstar_ceil + max_d * 0.05, p_en_dstar * 100 - 12),
    fontsize=10,
    color='#d62728',
    arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2)
)

# Punto en la curva donde d* intersecta
ax.scatter([dstar_ceil], [p_en_dstar * 100],
           color='#d62728', s=60, zorder=5)

# Formato del eje
ax.set_xlabel('Mensajes interceptados ($d$)', fontsize=12)
ax.set_ylabel('Probabilidad de colisión (%)', fontsize=12)
ax.set_title(
    f'Birthday Attack sobre RSA  —  $p={p}$, $q={q}$, $e={e}$\n'
    f'$n={n}$,  $\\lambda(n)={lam_n}$,  $N=\\lambda(n)$',
    fontsize=13, fontweight='normal'
)
ax.set_xlim(0, max_d)
ax.set_ylim(0, 105)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax.grid(True, alpha=0.3, linewidth=0.6)
ax.legend(fontsize=10, loc='lower right')

# Caja de información
info_text = (
    f"$p={p}$,  $q={q}$\n"
    f"$\\gcd(p-1,q-1) = {gcdd}$\n"
    f"$\\lambda(n) = \\mathrm{{lcm}}({p-1},{q-1}) = {lam_n}$\n"
    f"$d^* = \\lceil 1.17741\\cdot\\sqrt{{{N}}} \\rceil = {dstar_ceil}$"
)
props = dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.8, edgecolor='#cccccc')
ax.text(0.02, 0.98, info_text,
        transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('problema5_birthday_attack.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n  Gráfica guardada como 'problema5_birthday_attack.png'")