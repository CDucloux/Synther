"""Enveloppe de volume d'une note : attaque, decay, sustain, release.

Le volume global mélange l'enveloppe d'ampli et la fermeture du filtre
(les harmoniques qui disparaissent font aussi baisser le niveau). On
mesure donc l'ampli sur la fondamentale seule, isolée par un passe-bande
étroit : un passe-bas réglé au-dessus d'elle ne la touche pas.
"""

from dataclasses import dataclass

import numpy as np
from scipy import signal

from synther.audio.pitch import Floats, Note
from synther.audio.signal import Samples

SMOOTH = 0.002  # s, lissage de l'enveloppe
ATTACK_FRAME = 128  # échantillons (≈ 3 ms) pour l'attaque, large bande


@dataclass(frozen=True)
class Envelope:
    """Mesures en ms ; `sustain` = niveau tenu / niveau crête (0 à 1) ;
    `decay` et `release` = constantes de temps (retour à 37 %)."""

    attack: float
    decay: float | None
    sustain: float | None
    release: float | None


def fundamental_level(
    samples: Samples, rate: int, hz: float, start: float, stop: float
) -> tuple[Floats, Floats]:
    """Amplitude de la fondamentale `hz` entre `start` et `stop` (s) :
    passe-bande ± 1/3 d'octave, enveloppe de Hilbert lissée."""
    begin = max(0, int((start - 0.05) * rate))
    end = min(len(samples), int(stop * rate))
    low, high = hz * 2 ** (-1 / 3), min(hz * 2 ** (1 / 3), rate / 2.2)
    sos = signal.butter(
        2, [low, high], btype="bandpass", fs=rate, output="sos"
    )
    band = signal.sosfiltfilt(sos, samples[begin:end])
    amplitude = np.abs(signal.hilbert(band))
    width = max(1, int(SMOOTH * rate))
    amplitude = np.convolve(amplitude, np.ones(width) / width, mode="same")
    times = (np.arange(len(amplitude)) + begin) / rate
    return (
        np.asarray(amplitude, dtype=np.float64),
        np.asarray(times, dtype=np.float64),
    )


def _time_constant(
    level: Floats, times: Floats, start: int, target: float
) -> float | None:
    """Temps (ms) entre l'indice `start` et le premier passage sous
    `target` ; None si jamais atteint."""
    below = np.flatnonzero(level[start:] <= target)
    if len(below) == 0:
        return None
    return float(times[start + below[0]] - times[start]) * 1000


def _release(
    level: Floats,
    times: Floats,
    peak_index: int,
    sustain_level: float,
    next_start: float | None,
) -> float | None:
    """Release (ms) : depuis le dernier instant tenu au niveau du sustain
    (fin du gate, la hauteur seule ne la donne pas : pYIN suit la note
    jusque dans sa queue) jusqu'à 37 % de ce niveau, avant la note
    suivante ; None si la note suivante coupe la queue."""
    if sustain_level <= 0:
        return None
    held = np.flatnonzero(level[peak_index:] >= 0.8 * sustain_level)
    gate = peak_index + int(held[-1])
    result = _time_constant(level, times, gate, 0.37 * float(level[gate]))
    if result is None:
        return None
    if next_start is not None and times[gate] + result / 1000 > next_start:
        return None
    return result


def _attack(samples: Samples, rate: int, note: Note) -> float:
    """Attaque (ms) de 10 % à 90 % du pic, sur l'enveloppe large bande
    à fenêtre courte : l'attaque d'un synthé dure souvent < 10 ms, trop
    vite pour le passe-bande de la fondamentale."""
    begin = max(0, int((note.start - 0.03) * rate))
    end = min(len(samples), int((note.start + 0.25) * rate))
    chunk = np.abs(samples[begin:end])
    if len(chunk) < 2 * ATTACK_FRAME:
        return 0.0
    kernel = np.ones(ATTACK_FRAME) / ATTACK_FRAME
    level = np.sqrt(np.convolve(chunk**2, kernel, mode="same"))
    peak_index = int(np.argmax(level))
    # La queue de la note précédente peut encore sonner : on mesure la
    # montée depuis le creux qui précède le pic.
    valley = int(np.argmin(level[: peak_index + 1]))
    floor = float(level[valley])
    rising = level[valley : peak_index + 1] - floor
    span = float(level[peak_index]) - floor
    if span <= 0:
        return 0.0
    low = np.flatnonzero(rising >= 0.1 * span)
    high = np.flatnonzero(rising >= 0.9 * span)
    return float(high[0] - low[0]) / rate * 1000


def measure(
    samples: Samples, rate: int, note: Note, next_start: float | None
) -> Envelope:
    """Mesure l'enveloppe d'ampli de `note` sur sa fondamentale.

    - attaque : de 10 % à 90 % du pic ;
    - decay : pic → sustain + 37 % de l'écart ;
    - sustain : médiane entre 60 et 90 % de la note, rapportée au pic ;
    - release : fin du gate → 37 % du niveau tenu, si la queue finit
      avant la note suivante.
    """
    stop = next_start if next_start is not None else note.end + 1.0
    level, times = fundamental_level(samples, rate, note.hz, note.start, stop)
    in_note = (times >= note.start - 0.02) & (times <= note.end)
    if in_note.sum() < 8:
        return Envelope(0.0, None, None, None)
    first = int(np.flatnonzero(in_note)[0])
    peak_index = first + int(np.argmax(level[in_note]))
    peak = float(level[peak_index])
    attack = _attack(samples, rate, note)
    held = (times >= note.start + 0.4 * note.duration) & (
        times <= note.start + 0.7 * note.duration
    )
    sustain = decay = release = None
    if note.duration >= 0.12 and held.any():
        sustain_level = float(np.median(level[held]))
        sustain = min(1.0, sustain_level / peak)
        if sustain < 0.9:
            target = sustain_level + 0.37 * (peak - sustain_level)
            decay = _time_constant(level, times, peak_index, target)
        release = _release(level, times, peak_index, sustain_level, next_start)
    return Envelope(attack, decay, sustain, release)
