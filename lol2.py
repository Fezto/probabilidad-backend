from math import ceil


def partial_pass_probability(score, p=31 / 101):
    """
    Calcula la probabilidad de aprobar un parcial.

    Parámetro:
      - score: calificación conocida (0 a 100) o None si aún no se rindió.
      - p: probabilidad de obtener entre 70 y 100 en un examen (ya sea parcial o final).
    """
    if score is not None:
        if score >= 70:
            return 1.0
        else:
            # Si el parcial está reprobado, el alumno rinde el examen final
            return p
    else:
        # Parcial pendiente: se rinde directamiente;
        # si falla (prob 1-p), rinde el examen final con prob p de aprobar.
        return p + (1 - p) * p  # equivale a 2p - p^2


def subject_probability(scores, p=31 / 101):
    """
    Calcula la probabilidad de aprobar una materia.
    Se asume que para aprobar la materia se deben aprobar los 3 parciales.

    Parámetro:
      - scores: lista de 3 elementos, cada uno es la calificación de un parcial (0-100) o None.
    """
    prob = 1.0
    for score in scores:
        prob *= partial_pass_probability(score, p)
    return prob


def overall_probability(subjects, p=31 / 101):
    """
    Calcula la probabilidad de aprobar al menos la mitad de N materias.

    Parámetro:
      - subjects: lista de materias, donde cada materia es una lista de 3 parciales.
                  Por ejemplo: [[80, 20, None], [10, 20, None], [100, 80, None]]
      - p: probabilidad de aprobar un examen (ya sea parcial o final), por defecto 31/101.

    Se utiliza programación dinámica para combinar probabilidades heterogéneas.
    """
    # Calculamos la probabilidad de aprobar cada materia.
    subject_probs = [subject_probability(scores, p) for scores in subjects]
    n = len(subject_probs)
    threshold = ceil(n / 2)  # Se necesita aprobar al menos la mitad

    # dp[i] representará la probabilidad de haber aprobado i materias.
    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    for prob in subject_probs:
        new_dp = [0.0] * (n + 1)
        for i in range(n):
            new_dp[i + 1] += dp[i] * prob  # Aprobó esta materia
            new_dp[i] += dp[i] * (1 - prob)  # No la aprobó
        dp = new_dp
    overall = sum(dp[threshold:])
    return overall, subject_probs


# Ejemplo de uso:
if __name__ == '__main__':
    # Considera el siguiente escenario:
    # Física: Primer parcial 80, segundo 20, tercer parcial pendiente.
    # Matemáticas: Primer parcial 10, segundo 20, tercer parcial pendiente.
    # Español: Primer parcial 100, segundo 80, tercer parcial pendiente.
    subjects = [
        [80, 20, None],
        [10, 20, 0],
        [100, 80, 0]
    ]

    overall_prob, subj_probs = overall_probability(subjects)

    print("Probabilidad de aprobar cada materia:")
    for i, prob in enumerate(subj_probs, start=1):
        print(f"Materia {i}: {prob:.4f}")

    n = len(subjects)
    threshold = ceil(n / 2)
    print(f"\nProbabilidad de aprobar al menos {threshold} de {n} materias: {overall_prob:.4f}")
