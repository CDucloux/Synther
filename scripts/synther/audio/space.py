"""Tempo, tonalité et image stéréo (delay gauche / droite, largeur)."""

from dataclasses import dataclass

import librosa
import numpy as np

from synther.audio.pitch import Floats
from synther.audio.signal import Audio

HOP = 256
# Profils de Krumhansl-Kessler (majeur, mineur), à partir du do.
MAJOR = np.array(
    [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
)
MINOR = np.array(
    [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
)
NAMES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")


def tempo(audio: Audio) -> float:
    """Tempo (BPM) estimé sur le mix complet."""
    value = librosa.beat.beat_track(
        y=audio.mono, sr=audio.rate, hop_length=HOP
    )[0]
    return float(np.atleast_1d(value)[0])


def key(audio: Audio) -> str:
    """Tonalité la plus probable (corrélation des chromas)."""
    chroma = librosa.feature.chroma_cqt(y=audio.mono, sr=audio.rate)
    profile = chroma.mean(axis=1)
    scores = []
    for shift in range(12):
        for mode, template in (("majeur", MAJOR), ("mineur", MINOR)):
            rolled = np.roll(template, shift)
            score = float(np.corrcoef(profile, rolled)[0, 1])
            scores.append((score, f"{NAMES[shift]} {mode}"))
    return max(scores)[1]


@dataclass(frozen=True)
class Stereo:
    """`correlation` : 1 = mono, ≈ 0 = canaux indépendants ; `delay` :
    décalage (ms) d'une copie retardée entre gauche et droite, positif
    si la droite est en retard ; `side` = part d'énergie latérale."""

    correlation: float
    delay: float | None
    side: float


def _strength(samples: Floats, rate: int) -> Floats:
    """Force des attaques, normalisée (pour comparer deux canaux)."""
    values = np.asarray(
        librosa.onset.onset_strength(y=samples, sr=rate, hop_length=HOP),
        dtype=np.float64,
    )
    values = values - values.mean()
    norm = float(np.linalg.norm(values))
    return values / norm if norm > 0 else values


def stereo(audio: Audio) -> Stereo:
    """Image stéréo : corrélation, énergie latérale et copie retardée
    (delay type I Feel Love : sec à gauche, écho à droite)."""
    left, right = audio.channels
    correlation = float(np.corrcoef(left, right)[0, 1])
    mid = (left + right) / 2
    side = (left - right) / 2
    total = float(np.sum(mid**2) + np.sum(side**2))
    side_share = float(np.sum(side**2)) / total if total > 0 else 0.0
    delay = None
    if correlation < 0.98:
        left_attacks = _strength(left, audio.rate)
        right_attacks = _strength(right, audio.rate)
        lags = np.arange(-len(left_attacks) + 1, len(left_attacks))
        cross = np.correlate(right_attacks, left_attacks, mode="full")
        frame_ms = HOP / audio.rate * 1000
        usable = (np.abs(lags) * frame_ms >= 30) & (
            np.abs(lags) * frame_ms <= 1000
        )
        if usable.any():
            index = int(np.argmax(np.where(usable, cross, -np.inf)))
            if cross[index] > 0.35 and cross[index] > 1.5 * cross[
                lags == 0
            ].max(initial=0.0):
                delay = float(lags[index] * frame_ms)
    return Stereo(correlation, delay, side_share)
