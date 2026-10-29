"""Harmoniques d'une note : forme d'onde, filtre (coupure, pente,
résonance), mouvement de la coupure dans le temps, battements."""

from dataclasses import dataclass

import librosa
import numpy as np
import numpy.typing as npt

from synther.audio.pitch import Floats, Note
from synther.audio.signal import Samples, dominant_period

FFT = 8192  # sustain, battements : résolution en fréquence
FFT_FAST = 2048  # attaque, mouvement du filtre : résolution en temps
HOP = 512
HOP_FAST = 128
MAX_FREQ = 16000.0
FLOOR_DB = -70.0  # sous ce niveau (relatif au pic), l'harmonique est du bruit
SLOPES = (6.0, 12.0, 18.0, 24.0, 30.0, 36.0)  # dB par octave


@dataclass(frozen=True)
class Spectrogram:
    """Module de la TFCT (fréquences × trames), axes en Hz et en s ;
    `window` = durée de la fenêtre (s)."""

    magnitude: Floats
    freqs: Floats
    times: Floats
    window: float


def spectrogram(
    samples: Samples, rate: int, fft: int = FFT, hop: int = HOP
) -> Spectrogram:
    """TFCT ; fenêtre longue (8192) pour résoudre les harmoniques d'une
    basse, courte (2048) pour suivre l'attaque et le filtre."""
    magnitude = np.abs(
        librosa.stft(samples, n_fft=fft, hop_length=hop, window="hann")
    )
    freqs = librosa.fft_frequencies(sr=rate, n_fft=fft)
    times = librosa.times_like(magnitude, sr=rate, hop_length=hop)
    return Spectrogram(
        np.asarray(magnitude, dtype=np.float64),
        np.asarray(freqs, dtype=np.float64),
        np.asarray(times, dtype=np.float64),
        fft / rate,
    )


def harmonics(column: Floats, freqs: Floats, f0: float) -> Floats:
    """Amplitude (dB) des harmoniques 1…N de `f0` dans une trame : pic
    à ± 3 % de chaque multiple, jusqu'à 16 kHz."""
    count = int(min(MAX_FREQ, freqs[-1]) // f0)
    levels = np.full(count, -120.0)
    bin_width = float(freqs[1] - freqs[0])
    for rank in range(1, count + 1):
        tolerance = min(max(0.03 * rank * f0, 1.5 * bin_width), 0.45 * f0)
        band = np.abs(freqs - rank * f0) <= tolerance
        if band.any():
            levels[rank - 1] = 20 * np.log10(column[band].max() + 1e-12)
    return levels


@dataclass(frozen=True)
class FilterFit:
    """Coupure (Hz) et pente (dB/octave) d'un passe-bas ajusté sur les
    harmoniques ; `resonance` = bosse (dB) au-dessus du modèle près de
    la coupure ; `error` = écart moyen (dB)."""

    cutoff: float
    slope: float
    resonance: float
    error: float


def _tilt(rank: Floats) -> Floats:
    """Spectre propre d'une scie ou d'un carré : −6 dB par octave."""
    result: Floats = -20 * np.log10(rank)
    return result


def fit_filter(
    levels: Floats, f0: float, odd_only: bool, slope: float | None = None
) -> FilterFit | None:
    """Ajuste « plat puis −pente au-delà de la coupure » sur l'écart des
    harmoniques au spectre propre de l'onde (scie ou carré)."""
    rank = np.arange(1, len(levels) + 1, dtype=np.float64)
    keep = levels > levels.max() + FLOOR_DB
    if odd_only:
        keep &= rank % 2 == 1
    if keep.sum() < 4:
        return None
    freq = rank[keep] * f0
    excess = levels[keep] - _tilt(rank[keep])
    excess = excess - excess[: min(3, len(excess))].max()
    cutoffs = np.geomspace(f0 * 0.7, freq[-1], 160)
    slopes = SLOPES if slope is None else (slope,)
    best: FilterFit | None = None
    for candidate_slope in slopes:
        octaves = np.log2(freq[None, :] / cutoffs[:, None])
        model = -candidate_slope * np.clip(octaves, 0, None)
        offset = (excess[None, :] - model).mean(axis=1, keepdims=True)
        errors = np.abs(excess[None, :] - model - offset).mean(axis=1)
        index = int(np.argmin(errors))
        if best is None or errors[index] < best.error - 0.3:
            near = np.abs(octaves[index]) <= 0.35
            bump = 0.0
            if near.any():
                residual = excess - model[index] - offset[index]
                bump = float(residual[near].max())
            best = FilterFit(
                float(cutoffs[index]),
                candidate_slope,
                bump,
                float(errors[index]),
            )
    return best


@dataclass(frozen=True)
class Waveform:
    """Forme d'onde estimée et indices : `even_gap` = niveau des
    harmoniques paires par rapport aux impaires voisines (dB) ;
    `third` = H3 par rapport à H1 (dB) ; `missing` = rangs absents."""

    name: str
    even_gap: float
    third: float
    missing: list[int]


def waveform(levels: Floats) -> Waveform:
    """Scie, carré, triangle ou pulse d'après les 8 premières
    harmoniques (avant que le filtre ne les écrase)."""
    low = levels[:8]
    if len(low) < 6:
        return Waveform("indéterminée (trop peu d'harmoniques)", 0, 0, [])
    gaps = [
        low[rank - 1] - (low[rank - 2] + low[rank]) / 2
        for rank in (2, 4, 6)
        if rank < len(low)
    ]
    even_gap = float(np.mean(gaps))
    third = float(low[2] - low[0])
    peak = low.max()
    missing: list[int] = []
    for width in range(3, 8):
        multiples = [rank for rank in range(width, len(low) + 1, width)]
        holes = [
            rank
            for rank in multiples
            if rank < len(low)
            and low[rank - 1] < min(low[rank - 2], low[rank]) - 15
            and low[rank - 1] < peak - 30
        ]
        if holes and holes == [r for r in multiples if r < len(low)]:
            missing = holes
            break
    if even_gap < -15:
        name = "triangle (ou sinus filtré)" if third < -15 else "carré"
    elif missing:
        name = f"pulse (rangs {missing} absents : largeur ≈ 1/{missing[0]})"
    elif third < -15:
        name = "scie très filtrée ou triangle"
    else:
        name = "scie (ou mélange scie et carré)"
    return Waveform(name, even_gap, third, missing)


@dataclass(frozen=True)
class FilterMotion:
    """Mouvement de la coupure sur une note : au pic (début), au repos,
    ampleur en octaves et constante de temps du retour (ms)."""

    peak: float
    rest: float
    octaves: float
    decay: float | None


def note_frames(spec: Spectrogram, note: Note) -> npt.NDArray[np.intp]:
    """Indices des trames dont la fenêtre tient dans la note."""
    half = spec.window / 2
    inside = (spec.times >= note.start + half) & (
        spec.times <= note.end - half
    )
    return np.flatnonzero(inside)


def motion(
    spec: Spectrogram, note: Note, odd_only: bool, slope: float
) -> FilterMotion | None:
    """Coupure trame par trame (pente fixée) : pic au début, repos à la
    fin, temps pour revenir à 37 % de l'écart en octaves."""
    frames = note_frames(spec, note)
    if len(frames) < 4:
        return None
    cutoffs = []
    for frame in frames:
        levels = harmonics(spec.magnitude[:, frame], spec.freqs, note.hz)
        fitted = fit_filter(levels, note.hz, odd_only, slope)
        cutoffs.append(np.nan if fitted is None else fitted.cutoff)
    values = np.asarray(cutoffs)
    if np.isnan(values).mean() > 0.5:
        return None
    octave = np.log2(values / note.hz)
    head = octave[: max(2, len(octave) // 5)]
    peak_oct = float(np.nanmax(head))
    rest_oct = float(np.nanmedian(octave[-max(2, len(octave) // 4) :]))
    decay = None
    amount = peak_oct - rest_oct
    if amount > 0.5:
        target = rest_oct + 0.37 * amount
        start = int(np.nanargmax(head))
        below = np.flatnonzero(octave[start:] <= target)
        if len(below):
            decay = float(spec.times[frames[start + below[0]]])
            decay = (decay - float(spec.times[frames[start]])) * 1000
    return FilterMotion(
        note.hz * 2**peak_oct, note.hz * 2**rest_oct, amount, decay
    )


def _trace(
    spec: Spectrogram, frames: npt.NDArray[np.intp], hz: float
) -> Floats:
    """Amplitude (linéaire) de la composante `hz` sur les trames."""
    bin_width = float(spec.freqs[1] - spec.freqs[0])
    band = np.abs(spec.freqs - hz) <= max(0.03 * hz, bin_width)
    level: Floats = spec.magnitude[band][:, frames].max(axis=0)
    return level


def beating(spec: Spectrogram, note: Note) -> float | None:
    """Fréquence (Hz) du battement de deux oscillateurs désaccordés,
    mesurée au cœur d'une note tenue (de 15 à 80 % de sa durée, loin de
    l'attaque et de la release) : période de l'amplitude de la
    fondamentale, confirmée par l'harmonique 2 qui bat deux fois plus
    vite. Il faut au moins 1,5 période dans la fenêtre."""
    frames = note_frames(spec, note)
    middle = (spec.times[frames] >= note.start + 0.15 * note.duration) & (
        spec.times[frames] <= note.start + 0.8 * note.duration
    )
    frames = frames[middle]
    if len(frames) < 16:
        return None
    frame_rate = 1 / float(spec.times[1] - spec.times[0])
    trace = _trace(spec, frames, note.hz)
    if trace.std() < 0.05 * (trace.mean() + 1e-12):
        return None
    rate, clarity = dominant_period(trace, frame_rate)
    if rate <= 0 or rate > 8 or clarity < 0.3:
        return None
    double, _ = dominant_period(_trace(spec, frames, 2 * note.hz), frame_rate)
    if double <= 0 or abs(double / rate - 2) > 0.3:
        return None
    return rate
