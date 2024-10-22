def random_vectors_in_circle(amount, radius):
    import random, numpy as np
    angles = [random.random() * 6.28 for _ in range(amount)]
    mag = [radius * (random.random() ** 0.5) for _ in range(amount)]
    positions = [np.array([mag[i] * np.cos(angles[i]), mag[i] * np.sin(angles[i])]) for i in range(amount)]
    return positions