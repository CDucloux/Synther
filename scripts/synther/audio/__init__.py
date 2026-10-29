"""Analyse audio d'un son de référence (partie 2 de la méthode).

Mesure, sur un enregistrement fourni par l'utilisateur, ce qui sert à
régler un synthé : notes et tempo, enveloppe de volume, forme d'onde,
pente et coupure du filtre (et son mouvement), désaccord, vibrato,
glide, delay stéréo. Chaque mesure est en unités physiques (Hz, ms,
cents) : la conversion en positions de boutons demande la calibration
de la machine (knowledge/calibration/).

Modules : `signal` (lecture, séparation Demucs), `pitch` (hauteur et
notes), `envelope` (volume), `spectrum` (harmoniques, filtre), `space`
(stéréo, tempo, tonalité), `report` (rapport en français).

Dépendances optionnelles : extra `analysis` (librosa, soundfile, scipy),
et Demucs pour la séparation (`pip install demucs`, PyTorch).
"""
