import math
from itertools import product
from scipy.stats import binom  # Necesitarás instalar scipy: pip install scipy

# Probabilidad de obtener entre 70 y 100 (ya sea en parcial o final)
p_exam = 31 / 101
q_exam = 1 - p_exam  # 70/101

def asignature_probability(materia, p=p_exam, q=q_exam):
    """
    Calcula la probabilidad de aprobar una materia.
    Cada materia es una lista de 3 elementos (correspondientes a los 3 parciales),
    donde un valor numérico indica el resultado ya obtenido y None indica que aún no se rindió.
    """
    # Contabilizamos los parciales ya rendidos:
    fixed_pass = 0  # parciales ya aprobados (>=70)
    fixed_fail = 0  # parciales ya reprobados (<70)
    none_count = 0  # parciales pendientes
    for nota in materia:
        if nota is None:
            none_count += 1
        else:
            if nota >= 70:
                fixed_pass += 1
            else:
                fixed_fail += 1

    # Si no hay parciales pendientes, la probabilidad es fija
    if none_count == 0:
        if fixed_pass == 0:
            return 0  # No se pasa ni un parcial
        else:
            return p ** fixed_fail  # Probabilidad de aprobar con los parciales aprobados

    total_prob = 0
    # Para cada parcial pendiente se tienen dos posibles resultados: aprobar (1) o reprobar (0)
    # Enumeramos todas las combinaciones para los exámenes pendientes.
    for outcomes in product([1, 0], repeat=none_count):
        branch_prob = 1  # Probabilidad de obtener esta combinación en la fase de parciales pendientes.
        branch_passes = 0
        branch_fails = 0
        for resultado in outcomes:
            if resultado == 1:  # Aprobó el parcial pendiente
                branch_prob *= p
                branch_passes += 1
            else:  # Reprobó el parcial pendiente
                branch_prob *= q
                branch_fails += 1

        # Totales al concluir la fase de parciales:
        total_pass = fixed_pass + branch_passes
        total_fail = fixed_fail + branch_fails

        # Si el alumno reprueba los 3 parciales (total_pass == 0), no tiene derecho a finales.
        if total_pass == 0:
            conversion = 0
        else:
            # Por cada parcial reprobado se rinde final, que se aprueba con probabilidad p.
            conversion = p ** total_fail

        total_prob += branch_prob * conversion

    return total_prob

def period_probability(materias, p=p_exam, q=q_exam):
    """
    Dada una lista de materias, calcula la probabilidad de aprobar el cuatrimestre
    aprobando al menos la mitad de las materias.
    """
    # Calculamos la probabilidad de aprobar cada materia:
    probs = [asignature_probability(materia, p, q) for materia in materias]
    n = len(probs)
    
    if n == 0:  # Si no hay materias, no se puede calcular la probabilidad
        return 0, []

    # Para pasar el cuatrimestre se debe aprobar al menos la mitad (redondeando hacia arriba)
    req = math.ceil(n / 2)

    # Contamos cuántas materias ya están aprobadas
    passed = sum(1 for prob in probs if prob == 1)  # Probabilidad 1 significa que la materia está aprobada

    # Si ya se aprobaron al menos 'req' materias, la probabilidad es 100%
    if passed >= req:
        return 1, probs

    # Si no se aprobaron ninguna, la probabilidad es 0%
    if passed == 0:
        return 0, probs

    # Usamos la distribución binomial para calcular la probabilidad de aprobar al menos 'req' materias.
    total = 0
    for k in range(req, n + 1):
        # Calculamos la probabilidad de aprobar exactamente 'k' materias.
        prob_k = binom.pmf(k, n, sum(probs) / n)  # Normalizamos las probabilidades

        total += prob_k

    return total, probs

