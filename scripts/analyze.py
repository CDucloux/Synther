#!/usr/bin/env python3
"""Synther : analyse un enregistrement de référence (partie 2).

    scripts/analyze.py <audio> [--debut S] [--duree S] [--piste bass]

Isole la piste demandée avec Demucs (bass, other, piano, guitar, vocals,
drums ; sans --piste : mix complet), puis mesure notes, tempo,
enveloppe, forme d'onde, filtre, désaccord, vibrato, glide et stéréo.
Écrit rapport.md, mesures.json et spectrogramme.png dans --sortie
(défaut : original-sources/analyses/<nom>/, exclu de git).
Dépendances : extra `analysis` (librosa, soundfile, scipy) ; Demucs
pour --piste (pip install demucs).
"""

import argparse
import dataclasses
import json
import sys
from pathlib import Path

from synther import ROOT
from synther.audio.report import analyze, markdown, spectrogram_image


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--debut", type=float, default=0.0)
    parser.add_argument("--duree", type=float, default=None)
    parser.add_argument("--piste", default=None)
    parser.add_argument("--sortie", type=Path, default=None)
    args = parser.parse_args()
    audio = args.audio.resolve()
    if not audio.exists():
        print(f"✗ fichier introuvable : {audio}", file=sys.stderr)
        return 1
    out_dir = args.sortie or (
        ROOT / "original-sources" / "analyses" / audio.stem
    )
    analysis, part = analyze(
        audio, out_dir, args.debut, args.duree, args.piste
    )
    report = markdown(analysis)
    (out_dir / "rapport.md").write_text(report, encoding="utf-8")
    (out_dir / "mesures.json").write_text(
        json.dumps(dataclasses.asdict(analysis), indent=2, default=str),
        encoding="utf-8",
    )
    spectrogram_image(part, out_dir)
    print(report)
    print(f"→ {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
