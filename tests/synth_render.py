"""Petit synthé soustractif de test : rend des sons aux réglages connus
pour vérifier ce que mesure l'analyse audio (scripts/synther/audio)."""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import signal

RATE = 44100
BLOCK = 64

Floats = npt.NDArray[np.float64]


@dataclass(frozen=True)
class Patch:
    """Réglages du son de test (unités physiques)."""

    wave: str = "saw"  # saw | square
    cutoff: float = 400.0  # Hz, au repos
    env_octaves: float = 2.0  # ouverture du filtre à l'attaque
    filter_decay: float = 0.15  # s, constante de temps du filtre
    poles: int = 4  # 4 → 24 dB/oct, 2 → 12 dB/oct
    attack: float = 0.004  # s
    decay: float = 0.2  # s, constante de temps
    sustain: float = 0.4  # 0 à 1
    release: float = 0.08  # s, constante de temps
    detune: float = 0.0  # cents, 2e oscillateur identique
    delay: float = 0.0  # s, copie à droite (gauche sèche)


def oscillator(hz: float, length: int, wave: str) -> Floats:
    """Onde à bande limitée (somme d'harmoniques jusqu'à 18 kHz)."""
    time = np.arange(length) / RATE
    result = np.zeros(length)
    for rank in range(1, int(18000 // hz) + 1):
        if wave == "square" and rank % 2 == 0:
            continue
        result += np.sin(2 * np.pi * rank * hz * time) / rank
    return result


def ladder(samples: Floats, cutoffs: Floats, poles: int) -> Floats:
    """Cascade de `poles` passe-bas à un pôle, coupure variable par
    blocs (approximation d'un filtre ladder sans résonance)."""
    output = samples.copy()
    for _ in range(poles):
        state = np.zeros(1)
        stage = np.zeros_like(output)
        for begin in range(0, len(output), BLOCK):
            end = min(begin + BLOCK, len(output))
            coefficient = np.exp(-2 * np.pi * cutoffs[begin] / RATE)
            stage[begin:end], state = signal.lfilter(
                [1 - coefficient],
                [1, -coefficient],
                output[begin:end],
                zi=state,
            )
        output = stage
    return output


def note_audio(hz: float, gate: float, patch: Patch) -> Floats:
    """Une note : oscillateur(s), filtre enveloppé, ADSR, release."""
    length = int((gate + 6 * patch.release) * RATE)
    time = np.arange(length) / RATE
    source = oscillator(hz, length, patch.wave)
    if patch.detune:
        detuned = hz * 2 ** (patch.detune / 1200)
        source = (source + oscillator(detuned, length, patch.wave)) / 2
    opening = patch.env_octaves * np.exp(-time / patch.filter_decay)
    cutoffs = np.minimum(patch.cutoff * 2**opening, 18000)
    filtered = ladder(source, cutoffs, patch.poles)
    rise = np.clip(time / patch.attack, 0, 1)
    held = patch.sustain + (1 - patch.sustain) * np.exp(
        -np.clip(time - patch.attack, 0, None) / patch.decay
    )
    level = np.where(time < patch.attack, rise, held)
    gate_level = level[min(int(gate * RATE), length - 1)]
    after = time >= gate
    level[after] = gate_level * np.exp(-(time[after] - gate) / patch.release)
    result: Floats = filtered * level
    return result


def render(
    notes: list[tuple[float, float, float]], patch: Patch, length: float
) -> Floats:
    """Rend des notes (début s, durée s, fréquence Hz) en stéréo (2, n)."""
    mono = np.zeros(int(length * RATE))
    for start, gate, hz in notes:
        audio = note_audio(hz, gate, patch)
        begin = int(start * RATE)
        end = min(begin + len(audio), len(mono))
        mono[begin:end] += audio[: end - begin]
    mono /= np.abs(mono).max() + 1e-9
    right = mono.copy()
    if patch.delay:
        shift = int(patch.delay * RATE)
        right = np.zeros_like(mono)
        right[shift:] = mono[:-shift]
    return np.stack([mono, right]) * 0.5


def sweep(
    pitches: list[tuple[float, float]], glide: float, vibrato: float = 0.0
) -> Floats:
    """Scie continue (legato) : notes (durée s, Hz) reliées par un glide
    linéaire en hauteur de `glide` s ; vibrato de `vibrato` cents à
    5,5 Hz. Stéréo (2, n)."""
    curve: list[Floats] = []
    previous = pitches[0][1]
    for duration, hz in pitches:
        length = int(duration * RATE)
        ramp = min(length, int(glide * RATE))
        semitones = np.full(length, 12 * np.log2(hz / 440))
        start = 12 * np.log2(previous / 440)
        semitones[:ramp] = np.linspace(start, semitones[0], ramp)
        curve.append(semitones)
        previous = hz
    track = np.concatenate(curve)
    time = np.arange(len(track)) / RATE
    track = track + vibrato / 100 * np.sin(2 * np.pi * 5.5 * time)
    freq = 440 * 2 ** (track / 12)
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    mono = np.zeros(len(track))
    for rank in range(1, int(18000 // freq.max()) + 1):
        mono += np.sin(rank * phase) / rank
    mono *= 0.3 / np.abs(mono).max()
    return np.stack([mono, mono])
