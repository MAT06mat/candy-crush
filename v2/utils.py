# --- Paramètres d'Animation ---
ANIM_SPEED = 15  # Vitesse de rafraîchissement (ms)
STEPS = 10  # Nombre d'étapes pour décomposer un mouvement


def linear(t):
    return t


def ease_in_quad(t):
    return t**2


def ease_out_quad(t):
    return 1 - (1 - t) ** 2


def ease_in_cubic(t):
    return t**3


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    if t < 0.5:
        return 2 * t**2
    return 1 - 2 * (1 - t) ** 2


def ease_out_back(t):
    return 1 + 2.70158 * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2


ANIM_GRAVITY = linear
ANIM_SWAP = ease_in_out
ANIM_SCORE = ease_out_cubic


def create_animation(id, func, *args: float):
    moves = [[0] for _ in range(len(args))]
    for n in range(1, STEPS + 1):
        t = func(n / STEPS) - func((n - 1) / STEPS)
        for i in range(len(args)):
            moves[i].append(args[i] * t)
    for move in moves:
        move.pop(0)
    return [id, *moves]
