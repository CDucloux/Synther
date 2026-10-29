"""Lecture d'un fichier audio et séparation des instruments (Demucs)."""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import librosa
import numpy as np
import numpy.typing as npt

SAMPLE_RATE = 44100

# Pistes du modèle Demucs à 6 sources.
STEMS = ("bass", "drums", "other", "vocals", "guitar", "piano")
DEMUCS_MODEL = "htdemucs_6s"

Samples = npt.NDArray[np.float64]


@dataclass(frozen=True)
class Audio:
    """Signal stéréo (2, n) en flottants, à la fréquence `rate`."""

    channels: Samples
    rate: int

    @property
    def mono(self) -> Samples:
        """Somme des deux canaux divisée par deux."""
        result: Samples = self.channels.mean(axis=0)
        return result

    @property
    def duration(self) -> float:
        """Durée en secondes."""
        return float(self.channels.shape[1]) / self.rate


def load(
    path: Path, start: float = 0.0, duration: float | None = None
) -> Audio:
    """Lit `path` (tout format lu par ffmpeg), extrait de `start`
    secondes pendant `duration` secondes ; mono dupliqué en stéréo."""
    data, rate = librosa.load(
        path,
        sr=SAMPLE_RATE,
        mono=False,
        offset=start,
        duration=duration,
    )
    samples = np.asarray(data, dtype=np.float64)
    if samples.ndim == 1:
        samples = np.stack([samples, samples])
    return Audio(samples[:2], int(rate))


def separate(path: Path, stem: str, out_dir: Path) -> Path:
    """Isole la piste `stem` (basse, autres…) avec Demucs et renvoie
    le chemin du fichier WAV obtenu."""
    if stem not in STEMS:
        raise ValueError(f"piste inconnue : {stem} (choix : {STEMS})")
    command = [
        sys.executable,
        "-m",
        "demucs",
        "-n",
        DEMUCS_MODEL,
        "-o",
        str(out_dir),
        str(path),
    ]
    subprocess.run(command, check=True, capture_output=True)
    result = out_dir / DEMUCS_MODEL / path.stem / f"{stem}.wav"
    if not result.exists():
        raise FileNotFoundError(result)
    return result


def dominant_period(values: Samples, frame_rate: float) -> tuple[float, float]:
    """Période dominante d'une courbe (tendance retirée par un polynôme
    de degré 2), par autocorrélation : (fréquence en Hz, netteté du pic
    0 à 1) ; (0, 0) sans pic net. Il faut 1,5 période dans la courbe ;
    on ignore les périodes de moins de 1/15 s."""
    index = np.arange(len(values))
    flat = values - np.polyval(np.polyfit(index, values, 2), index)
    if flat.std() < 1e-9:
        return 0.0, 0.0
    corr = np.correlate(flat, flat, mode="full")[len(flat) - 1 :]
    corr = corr / (corr[0] + 1e-12)
    shortest = max(2, int(frame_rate / 15))
    longest = int(len(flat) / 1.5)
    if longest <= shortest + 2:
        return 0.0, 0.0
    peaks = [
        lag
        for lag in range(shortest + 1, longest - 1)
        if corr[lag] > corr[lag - 1] and corr[lag] >= corr[lag + 1]
    ]
    if not peaks:
        return 0.0, 0.0
    lag = max(peaks, key=lambda candidate: float(corr[candidate]))
    left, centre, right = corr[lag - 1], corr[lag], corr[lag + 1]
    shift = 0.5 * (left - right) / (left - 2 * centre + right + 1e-12)
    return frame_rate / (lag + shift), float(centre)
