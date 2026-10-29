"""Analyse audio : mesures retrouvées sur des sons de synthèse aux
réglages connus (tests/synth_render.py)."""

from pathlib import Path

import pytest

pytest.importorskip("librosa")

import numpy as np  # noqa: E402
import soundfile  # noqa: E402

from synther.audio import pitch  # noqa: E402
from synther.audio.report import analyze, markdown  # noqa: E402
from tests.synth_render import RATE, Patch, render, sweep  # noqa: E402

A2 = 110.0
PHRASE = [(0.1, 0.6, A2), (0.9, 0.6, 130.81), (1.7, 0.6, 164.81)]


def _write(tmp_path: Path, name: str, audio: np.ndarray) -> Path:
    """Écrit `audio` (2, n) en WAV et renvoie son chemin."""
    path = tmp_path / f"{name}.wav"
    soundfile.write(path, audio.T, RATE)
    return path


def test_notes_and_envelope(tmp_path: Path) -> None:
    patch = Patch(attack=0.005, decay=0.2, sustain=0.4, release=0.1)
    path = _write(tmp_path, "phrase", render(PHRASE, patch, 3.0))
    analysis, _ = analyze(path, tmp_path / "out")
    names = [item.note.name for item in analysis.notes]
    assert names == ["A2", "C3", "E3"]
    attacks = [item.envelope.attack for item in analysis.notes]
    assert np.median(attacks) < 12
    decays = [item.envelope.decay or 0 for item in analysis.notes]
    assert 130 < np.median(decays) < 230
    releases = [item.envelope.release or 0 for item in analysis.notes]
    assert 80 < np.median(releases) < 120
    assert "Enveloppe de volume" in markdown(analysis)


@pytest.mark.parametrize(("poles", "low", "high"), [(4, 15, 24), (2, 9, 15)])
def test_filter_slope(tmp_path: Path, poles: int, low: int, high: int) -> None:
    patch = Patch(poles=poles, env_octaves=0.0)
    path = _write(tmp_path, f"p{poles}", render(PHRASE, patch, 3.0))
    analysis, _ = analyze(path, tmp_path / "out")
    slopes = [item.filter.slope for item in analysis.notes if item.filter]
    assert low <= np.median(slopes) <= high


def test_waveform(tmp_path: Path) -> None:
    patch = Patch(wave="square", cutoff=2000, env_octaves=0.0)
    path = _write(tmp_path, "square", render(PHRASE, patch, 3.0))
    analysis, _ = analyze(path, tmp_path / "out")
    shapes = [item.waveform.name for item in analysis.notes if item.waveform]
    assert all(shape.startswith("carré") for shape in shapes)


def test_detune_beating(tmp_path: Path) -> None:
    patch = Patch(detune=10, cutoff=1500, env_octaves=0.0, sustain=1.0)
    notes = [(0.1, 2.5, 220.0)]
    path = _write(tmp_path, "detune", render(notes, patch, 3.0))
    analysis, _ = analyze(path, tmp_path / "out")
    beat = 220 * (2 ** (10 / 1200) - 1)
    assert analysis.notes[0].beating == pytest.approx(beat, rel=0.1)


def test_glide_and_vibrato() -> None:
    audio = sweep([(0.6, 220.0), (0.6, 329.63), (0.6, 246.94)], 0.15)
    mono = audio.mean(axis=0)
    track = pitch.track(mono, RATE)
    found = pitch.notes(track, pitch.onsets(mono, RATE))
    assert [note.name for note in found] == ["A3", "E4", "B3"]
    glide = pitch.glide_ms(track, found[0], found[1])
    assert 100 < glide < 135
    steady = sweep([(1.5, 220.0)], 0.0, vibrato=30)
    mono = steady.mean(axis=0)
    track = pitch.track(mono, RATE)
    note = pitch.notes(track, pitch.onsets(mono, RATE))[0]
    result = pitch.vibrato(track, note)
    assert result is not None
    assert result.rate == pytest.approx(5.5, abs=0.4)


def test_stereo_delay(tmp_path: Path) -> None:
    notes = [(0.1 + 0.25 * index, 0.15, A2) for index in range(8)]
    patch = Patch(delay=0.12, attack=0.004)
    path = _write(tmp_path, "delay", render(notes, patch, 2.6))
    analysis, _ = analyze(path, tmp_path / "out")
    assert analysis.stereo.delay is not None
    assert abs(analysis.stereo.delay) == pytest.approx(120, abs=5)
    assert len(analysis.notes) == 8
