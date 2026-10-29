"""Analyse complète d'un extrait et rapport en français (Markdown)."""

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import soundfile

from synther.audio import envelope, pitch, space, spectrum
from synther.audio.signal import Audio, load, separate


@dataclass
class NoteReport:
    """Mesures d'une note ; None = non mesurable sur cette note."""

    note: pitch.Note
    envelope: envelope.Envelope
    waveform: spectrum.Waveform | None = None
    filter: spectrum.FilterFit | None = None
    motion: spectrum.FilterMotion | None = None
    beating: float | None = None
    vibrato: pitch.Vibrato | None = None
    glide: float = 0.0


@dataclass
class Analysis:
    """Résultat de l'analyse d'un extrait."""

    source: str
    stem: str | None
    duration: float
    tempo: float
    key: str
    stereo: space.Stereo
    notes: list[NoteReport] = field(default_factory=list)


def analyze(
    path: Path,
    work_dir: Path,
    start: float = 0.0,
    duration: float | None = None,
    stem: str | None = None,
) -> tuple[Analysis, Audio]:
    """Analyse l'extrait de `path` ; `stem` = piste Demucs à isoler
    (bass, other, piano, guitar…) ou None pour analyser le mix."""
    work_dir.mkdir(parents=True, exist_ok=True)
    full = load(path, start, duration)
    part = full
    if stem is not None:
        excerpt = work_dir / "extrait.wav"
        soundfile.write(excerpt, full.channels.T, full.rate)
        part = load(separate(excerpt, stem, work_dir))
    result = Analysis(
        str(path),
        stem,
        full.duration,
        space.tempo(full),
        space.key(full),
        space.stereo(part),
    )
    # Delay sec d'un côté, écho de l'autre : analyser le côté sec, sinon
    # chaque note est comptée deux fois.
    mono = part.mono
    if result.stereo.delay is not None:
        mono = part.channels[0 if result.stereo.delay > 0 else 1]
    track = pitch.track(mono, part.rate)
    found = pitch.notes(track, pitch.onsets(mono, part.rate))
    spec = spectrum.spectrogram(mono, part.rate)
    fast = spectrum.spectrogram(
        mono, part.rate, spectrum.FFT_FAST, spectrum.HOP_FAST
    )
    for index, note in enumerate(found):
        following = found[index + 1].start if index + 1 < len(found) else None
        report = NoteReport(
            note, envelope.measure(mono, part.rate, note, following)
        )
        early = spectrum.note_frames(fast, note)
        frames = spectrum.note_frames(spec, note)
        if len(early) >= 2:
            first = spectrum.harmonics(
                fast.magnitude[:, early[0]], fast.freqs, note.hz
            )
            report.waveform = spectrum.waveform(first)
            odd_only = report.waveform.even_gap < -15
            source = spec if len(frames) >= 2 else fast
            frames = frames if len(frames) >= 2 else early
            rest = np.median(
                [
                    spectrum.harmonics(
                        source.magnitude[:, frame], source.freqs, note.hz
                    )
                    for frame in frames[len(frames) // 2 :]
                ],
                axis=0,
            )
            report.filter = spectrum.fit_filter(rest, note.hz, odd_only)
            if report.filter is not None:
                report.motion = spectrum.motion(
                    fast, note, odd_only, report.filter.slope
                )
        report.beating = spectrum.beating(spec, note)
        report.vibrato = pitch.vibrato(track, note)
        if index > 0:
            report.glide = pitch.glide_ms(track, found[index - 1], note)
        result.notes.append(report)
    return result, part


def _median(values: list[float]) -> float | None:
    """Médiane des valeurs présentes, None s'il n'y en a pas."""
    return float(np.median(values)) if values else None


def _number(value: float | None, unit: str, digits: int = 0) -> str:
    """Nombre formaté à la française, ou « non mesurable »."""
    if value is None:
        return "non mesurable"
    text = f"{value:.{digits}f}".replace(".", ",")
    return f"{text} {unit}".strip()


def sequence(analysis: Analysis, steps: int = 64) -> str:
    """Notes calées sur une grille de doubles croches au tempo mesuré,
    au format `steps` des fiches (« . » silence, « _ » liaison)."""
    if not analysis.notes or analysis.tempo <= 0:
        return ""
    step = 60 / analysis.tempo / 4
    origin = analysis.notes[0].note.start
    grid = ["."] * steps
    for item in analysis.notes:
        first = round((item.note.start - origin) / step)
        length = max(1, round(item.note.duration / step))
        if first >= steps:
            break
        grid[first] = item.note.name
        for index in range(first + 1, min(first + length, steps)):
            if grid[index] == ".":
                grid[index] = "_"
    while grid and grid[-1] in (".", "_"):
        grid.pop()
    rows = [grid[index : index + 16] for index in range(0, len(grid), 16)]
    return " |\n".join(" ".join(row) for row in rows)


def tracking(notes: list[NoteReport]) -> float | None:
    """Suivi de clavier apparent : pente de log2(coupure au repos) en
    fonction de log2(fondamentale) ; 1 = suit la note, 0 = fixe."""
    points = [
        (np.log2(item.note.hz), np.log2(item.filter.cutoff))
        for item in notes
        if item.filter is not None
    ]
    pitches = {round(x, 2) for x, _ in points}
    if len(pitches) < 3:
        return None
    xs, ys = zip(*points, strict=True)
    return float(np.polyfit(xs, ys, 1)[0])


def markdown(analysis: Analysis) -> str:
    """Rapport lisible, en unités physiques ; la conversion en positions
    de boutons attend la calibration de la machine."""
    notes = analysis.notes
    attacks = [item.envelope.attack for item in notes]
    decays = [item.envelope.decay for item in notes if item.envelope.decay]
    sustains = [
        item.envelope.sustain
        for item in notes
        if item.envelope.sustain is not None
    ]
    releases = [
        item.envelope.release
        for item in notes
        if item.envelope.release is not None
    ]
    fits = [item.filter for item in notes if item.filter is not None]
    shapes = [item.waveform.name for item in notes if item.waveform]
    motions = [item.motion for item in notes if item.motion is not None]
    beats = [item.beating for item in notes if item.beating]
    # Battement de la fondamentale → écart entre oscillateurs en cents.
    cents = [
        1200 * float(np.log2(1 + item.beating / item.note.hz))
        for item in notes
        if item.beating
    ]
    vibratos = [item.vibrato for item in notes if item.vibrato]
    glides = [item.glide for item in notes if item.glide > 0]
    lines = [
        f"# Analyse : {Path(analysis.source).name}",
        "",
        f"- Extrait : {_number(analysis.duration, 's', 1)}"
        f" ; piste analysée : {analysis.stem or 'mix complet'}",
        f"- Tempo : {_number(analysis.tempo, 'BPM', 1)}"
        f" ; tonalité probable : {analysis.key}",
        f"- Notes détectées : {len(notes)}",
        "",
        "## Notes (grille de doubles croches)",
        "",
        "```",
        sequence(analysis) or "(aucune note)",
        "```",
        "",
        "## Forme d'onde",
        "",
    ]
    if shapes:
        common = max(set(shapes), key=shapes.count)
        lines.append(
            f"- Estimation la plus fréquente : {common}"
            f" ({shapes.count(common)} notes sur {len(shapes)})"
        )
    lines += ["", "## Filtre", ""]
    if fits:
        slope = _median([fit.slope for fit in fits])
        octaves = [
            float(np.log2(item.filter.cutoff / item.note.hz))
            for item in notes
            if item.filter is not None
        ]
        lines += [
            f"- Pente : {_number(slope, 'dB/octave')}"
            " (≈ 24 : 4 pôles, ≈ 12 : 2 pôles)",
            "- Coupure au repos : "
            f"{_number(_median([fit.cutoff for fit in fits]), 'Hz')}"
            f", soit {_number(_median(octaves), 'octaves', 1)}"
            " au-dessus de la fondamentale",
            "- Bosse de résonance près de la coupure : "
            f"{_number(_median([fit.resonance for fit in fits]), 'dB', 1)}",
            "- Suivi de clavier apparent : "
            f"{_number(tracking(notes), '', 2)} (1 = suit la note)",
        ]
    if motions:
        lines += [
            "- Ouverture à l'attaque (enveloppe de filtre) : "
            f"{_number(_median([m.octaves for m in motions]), 'oct.', 1)}",
            "- Retour au repos (constante de temps) : "
            f"{_number(_median([m.decay for m in motions if m.decay]), 'ms')}",
        ]
    lines += [
        "",
        "## Enveloppe de volume",
        "",
        f"- Attaque : {_number(_median(attacks), 'ms')}",
        f"- Decay : {_number(_median(decays), 'ms')}",
        f"- Sustain : {_number(_median(sustains), '(0 à 1)', 2)}",
        f"- Release : {_number(_median(releases), 'ms')}",
        "",
        "## Mouvement et jeu",
        "",
        f"- Battement (désaccord) : {_number(_median(beats), 'Hz', 1)}"
        + (
            f", soit {_number(_median(cents), 'cents', 1)} entre oscillateurs"
            if cents
            else ""
        ),
        "- Vibrato : "
        + (
            _number(_median([v.rate for v in vibratos]), "Hz", 1)
            + ", "
            + _number(_median([v.depth for v in vibratos]), "cents")
            if vibratos
            else "aucun"
        ),
        "- Glide (10 à 90 % de l'intervalle) : "
        + (
            f"{_number(_median(glides), 'ms')}, soit environ"
            f" {_number(float(np.median(glides)) / 0.8, 'ms')} en tout"
            if glides
            else "aucun"
        ),
        "",
        "## Espace",
        "",
        "- Corrélation gauche / droite : "
        f"{_number(analysis.stereo.correlation, '', 2)} (1 = mono)",
        f"- Part latérale : {_number(100 * analysis.stereo.side, '%')}",
        "- Copie retardée gauche / droite : "
        + _number(analysis.stereo.delay, "ms"),
        "",
        "## Limites",
        "",
        "- Notes courtes (< 120 ms) : decay et sustain non mesurés.",
        "- Release : seulement quand la note est suivie d'un silence.",
        "- Profondeur de vibrato sous-estimée d'environ un quart.",
        "- Coupure : genou estimé environ 0,4 octave trop bas, biais"
        " constant ; ne comparer qu'à une calibration faite avec cet"
        " outil.",
        "- Piste isolée par Demucs : des restes d'autres instruments"
        " peuvent fausser filtre et enveloppe.",
        "",
        "Valeurs en unités physiques. Positions de boutons : à convertir"
        " avec la calibration de la machine (knowledge/calibration/).",
        "",
    ]
    return "\n".join(lines)


def spectrogram_image(audio: Audio, work_dir: Path) -> Path:
    """Spectrogramme PNG (échelle log) de la piste analysée (ffmpeg)."""
    wav = work_dir / "piste.wav"
    soundfile.write(wav, audio.channels.T, audio.rate)
    image = work_dir / "spectrogramme.png"
    subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(wav),
            "-lavfi",
            "showspectrumpic=s=1600x700:legend=1:fscale=log:scale=log",
            "-frames:v",
            "1",
            str(image),
        ],
        check=True,
    )
    return image
