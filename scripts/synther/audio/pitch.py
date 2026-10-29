"""Hauteur dans le temps (pYIN), découpage en notes, glide et vibrato."""

from dataclasses import dataclass

import librosa
import numpy as np
import numpy.typing as npt
from scipy import ndimage

from synther.audio.signal import SAMPLE_RATE, Samples, dominant_period

HOP = 256
FRAME = 4096
F_MIN = 30.0  # sous le Si 0 : basses de synthé en 32'
F_MAX = 2100.0
MIN_NOTE = 0.04  # s : plus court, c'est un clic ou un artefact
GLIDE_FLOOR = 45.0  # ms : transition plus courte = saut franc

Floats = npt.NDArray[np.float64]


@dataclass(frozen=True)
class PitchTrack:
    """f0 en Hz (NaN si non voisé), probabilité de voisement, instants."""

    f0: Floats
    voiced: npt.NDArray[np.bool_]
    times: Floats


@dataclass(frozen=True)
class Note:
    """Note détectée : début et fin en s, hauteur MIDI (médiane)."""

    start: float
    end: float
    midi: float

    @property
    def name(self) -> str:
        """Nom anglais avec octave (C4 = do central), dièses."""
        return str(librosa.midi_to_note(round(self.midi), unicode=False))

    @property
    def hz(self) -> float:
        """Fréquence fondamentale en Hz."""
        return float(librosa.midi_to_hz(self.midi))

    @property
    def duration(self) -> float:
        """Durée en s."""
        return self.end - self.start


def track(samples: Samples, rate: int) -> PitchTrack:
    """Suivi de hauteur pYIN sur un signal mono."""
    f0, voiced, _ = librosa.pyin(
        samples,
        fmin=F_MIN,
        fmax=F_MAX,
        sr=rate,
        frame_length=FRAME,
        hop_length=HOP,
    )
    times = librosa.times_like(f0, sr=rate, hop_length=HOP)
    return PitchTrack(
        np.asarray(f0, dtype=np.float64),
        np.asarray(voiced, dtype=np.bool_),
        np.asarray(times, dtype=np.float64),
    )


def onsets(samples: Samples, rate: int) -> Floats:
    """Instants d'attaque (s), recalés au début réel de la note. Une
    attaque n'est gardée que si le niveau monte d'au moins 3 dB entre
    les 30 ms d'avant et les 30 ms d'après (les fausses attaques d'un
    son tenu, ou d'un glide, sont écartées)."""
    frames = librosa.onset.onset_detect(
        y=samples, sr=rate, hop_length=HOP, backtrack=True, units="frames"
    )
    candidates = librosa.frames_to_time(frames, sr=rate, hop_length=HOP)
    window = int(0.03 * rate)
    kept = []
    for time in candidates:
        centre = int(time * rate)
        before = samples[max(0, centre - window) : centre]
        after = samples[centre : centre + window]
        level_before = float(np.sqrt(np.mean(before**2))) if len(before) else 0
        level_after = float(np.sqrt(np.mean(after**2))) if len(after) else 0
        if level_after >= 1.41 * level_before + 1e-6:
            kept.append(float(time))
    return np.asarray(kept, dtype=np.float64)


def notes(pitch: PitchTrack, attacks: Floats) -> list[Note]:
    """Découpe le suivi en notes tenues. Une trame est « stable » si la
    médiane glissante de la hauteur (± 75 ms, qui efface un vibrato)
    bouge de moins de 5 demi-tons par seconde : un glide ne l'est pas.
    Une note = trames stables consécutives à moins de 0,6 demi-ton de
    sa médiane ; une attaque, un silence ou un écart durable (3 trames)
    ouvre une nouvelle note."""
    voiced = pitch.voiced & np.isfinite(pitch.f0)
    midi = np.full_like(pitch.f0, np.nan)
    midi[voiced] = librosa.hz_to_midi(pitch.f0[voiced])
    frame = HOP / SAMPLE_RATE
    reach = max(1, int(0.075 / frame))
    filled = np.where(
        voiced,
        midi,
        np.interp(np.arange(len(midi)), np.flatnonzero(voiced), midi[voiced])
        if voiced.any()
        else 0.0,
    )
    smooth = ndimage.median_filter(filled, size=2 * reach + 1, mode="nearest")
    speed = np.abs(np.roll(smooth, -reach) - np.roll(smooth, reach))
    speed /= 2 * reach * frame
    stable = voiced & (speed < 5.0)
    attack_frames = set(np.searchsorted(pitch.times, attacks).tolist())
    found: list[Note] = []
    current: list[int] = []
    away = 0

    def close() -> None:
        if len(current) < 2:
            return
        start = float(pitch.times[current[0]])
        # La hauteur se stabilise après l'attaque : on recale le début
        # sur l'attaque qui précède de moins de 0,1 s.
        before = attacks[(attacks <= start) & (attacks >= start - 0.1)]
        if len(before):
            start = float(before[-1])
        end = float(pitch.times[current[-1]]) + HOP / SAMPLE_RATE
        if end - start >= MIN_NOTE:
            found.append(Note(start, end, float(np.median(midi[current]))))

    for index in range(len(midi)):
        if index in attack_frames and current:
            close()
            current, away = [], 0
        if not stable[index]:
            if (
                not voiced[index]
                or index - (current[-1] if current else 0) > 2
            ):
                close()
                current, away = [], 0
            continue
        if current and abs(midi[index] - np.median(midi[current])) > 0.6:
            away += 1
            if away >= 3:
                close()
                current, away = list(range(index - 2, index + 1)), 0
            continue
        away = 0
        current.append(index)
    close()
    return found


def glide_ms(pitch: PitchTrack, previous: Note, current: Note) -> float:
    """Durée (ms) de la transition de hauteur entre deux notes liées,
    de 10 % à 90 % de l'intervalle ; 0 si saut franc ou notes séparées."""
    interval = current.midi - previous.midi
    if abs(interval) < 0.5 or current.start - previous.end > 0.5:
        return 0.0
    between = (pitch.times >= previous.end) & (pitch.times <= current.start)
    if not pitch.voiced[between].all():
        return 0.0  # silence entre les deux : pas de glide (non legato)
    window = (pitch.times >= previous.end - 0.2) & (
        pitch.times <= current.start + 0.4
    )
    window &= pitch.voiced & np.isfinite(pitch.f0)
    if window.sum() < 4:
        return 0.0
    times = pitch.times[window]
    progress = (librosa.hz_to_midi(pitch.f0[window]) - previous.midi) / (
        interval
    )
    low = np.flatnonzero(progress >= 0.1)
    high = np.flatnonzero(progress >= 0.9)
    if len(low) == 0 or len(high) == 0:
        return 0.0
    duration = float(times[high[0]] - times[low[0]]) * 1000
    # En dessous, c'est le flou de la fenêtre de pYIN (≈ 93 ms) sur un
    # saut franc, pas un glide.
    return duration if duration > GLIDE_FLOOR else 0.0


@dataclass(frozen=True)
class Vibrato:
    """Vibrato : vitesse (Hz) et profondeur (cents crête)."""

    rate: float
    depth: float


def vibrato(pitch: PitchTrack, note: Note) -> Vibrato | None:
    """Vibrato d'une note tenue (≥ 0,4 s) : modulation périodique de la
    hauteur entre 3 et 12 Hz (autocorrélation), d'au moins 5 cents.
    La fenêtre de pYIN (≈ 93 ms) lisse le vibrato : la profondeur est
    sous-estimée d'environ un tiers vers 5-6 Hz."""
    if note.duration < 0.4:
        return None
    window = (pitch.times >= note.start + 0.1) & (pitch.times <= note.end)
    window &= pitch.voiced & np.isfinite(pitch.f0)
    if window.sum() < 32:
        return None
    cents = 100 * (librosa.hz_to_midi(pitch.f0[window]) - note.midi)
    rate, clarity = dominant_period(cents, SAMPLE_RATE / HOP)
    if not 3 <= rate <= 12 or clarity < 0.3:
        return None
    index = np.arange(len(cents))
    flat = cents - np.polyval(np.polyfit(index, cents, 2), index)
    depth = float(np.percentile(flat, 95) - np.percentile(flat, 5)) / 2
    if depth < 5:
        return None
    return Vibrato(rate, depth)
