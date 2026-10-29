# Analyse audio d'un enregistrement (partie 2)

Outil : `scripts/analyze.py`, code dans `scripts/synther/audio/`. Il mesure
le son **d'origine** en unités physiques (Hz, ms, dB/octave, cents). La
conversion en positions de boutons attend la calibration de la machine
(`calibration/`, partie 1) : en attendant, les mesures servent à trancher
entre des hypothèses (2 ou 4 pôles, scie ou carré, désaccord ou pas,
attaque franche ou lente) et à justifier la fiche dans `traceability`
(« Mesuré sur l'enregistrement : … »).

## Utilisation

```bash
pip install -e '.[analysis]'          # librosa, soundfile, scipy
pip install demucs                    # seulement pour --piste (lourd)
scripts/analyze.py morceau.wav --debut 42 --duree 8 --piste bass
```

- L'audio vient de l'utilisateur (fichier déposé dans la conversation ou dans
  `original-sources/`, exclu de git) : YouTube n'est pas joignable d'ici.
- Choisir un extrait de 4 à 10 s où la partie est **la plus exposée**
  (intro, break) : c'est le premier facteur de précision.
- `--piste` : bass, other (synthés), piano, guitar, vocals, drums (Demucs
  `htdemucs_6s`). Sans `--piste` : mix complet, à réserver à un son seul.
- Sorties dans `original-sources/analyses/<nom>/` : `rapport.md` (lisible),
  `mesures.json` (note par note), `spectrogramme.png` (à regarder aussi).

## Ce qui est mesuré, et comment

| Mesure | Méthode |
|---|---|
| Notes | pYIN (fenêtre 4096), notes = zones de hauteur stable, début calé sur l'attaque |
| Tempo, tonalité | suivi de pulsation et profils de Krumhansl, sur le mix complet |
| Forme d'onde | harmoniques pairs absents → carré ; trous réguliers → impulsion ; sinon scie |
| Filtre | pente et genou ajustés sur la pente naturelle d'une scie (« plat puis −pente ») |
| Enveloppe de filtre | ouverture en octaves à l'attaque et temps de retour (STFT courte) |
| Ampli | sur la fondamentale isolée (le filtre ne la touche pas) : attaque, decay, sustain, release |
| Désaccord | battement de la fondamentale (autocorrélation), confirmé par H2 au double |
| Vibrato, glide | sur la courbe de hauteur (glide = 10 à 90 % de l'intervalle) |
| Espace | corrélation et part latérale ; copie retardée gauche / droite (delay) |

## Précision vérifiée (sons de synthèse aux réglages connus)

Tests : `tests/test_audio.py`, synthé de test `tests/synth_render.py`.

| Réglage réel | Mesuré |
|---|---|
| Notes, tempo, tonalité | justes |
| Scie / carré | justes |
| Filtre 4 pôles / 2 pôles | pente ≈ 18 / ≈ 12 dB/oct (l'ordre est bien distingué) |
| Attaque 5 / 20 ms | 7 / 19 ms |
| Decay 200 ms | 175 à 185 ms |
| Sustain 0,4 | 0,3 à 0,4 |
| Release 100 / 200 ms | 99 / 199 ms |
| Ouverture du filtre 2 oct., retour 150 ms | 1,8 oct., 140 à 150 ms |
| Désaccord 6, 10, 20 cents | battement exact au centième de Hz |
| Glide 150 / 300 ms | 116 / 238 ms (10 à 90 %), soit ≈ 145 / 300 ms en tout |
| Vibrato 5,5 Hz, 30 cents | 5,5 à 5,7 Hz, 21 à 24 cents |
| Delay stéréo 120 ms | 122 ms |

Après séparation Demucs (mix synthétique basse + lead + batterie) : les
**notes restent justes** (le mix seul donne des notes fausses), mais les
mesures de timbre se dégradent (decay 86 ms au lieu de ≈ 180, pente 12 au
lieu de 18, attaque 15 au lieu de 7 ms). Sur une piste séparée, ne retenir
avec confiance que les notes, le tempo, la forme d'onde et les ordres de
grandeur.

## Limites (à dire dans la fiche)

- Notes de moins de 120 ms : ni decay ni sustain.
- Release mesurée seulement si la note est suivie d'un silence.
- Profondeur de vibrato sous-estimée d'environ un quart (fenêtre pYIN).
- Coupure : genou estimé environ 0,4 octave trop bas (biais constant) ;
  la calibration du Messenger devra se faire **avec le même outil**.
- Résonance : seulement une bosse en dB près de la coupure, indicative.
- Effets (reverb, chorus) et compression du mixage faussent decay et
  release : les lire comme des bornes hautes.
- Une mesure ne remplace pas une source : elle confirme ou infirme. Une fiche
  reconstituée surtout par mesure reste à la confiance 2.

## Suite prévue

1. Calibration du Messenger (positions → Hz, ms) avec ce même outil, quand
   l'utilisateur a la machine.
2. Comparaison mesurée : enregistrement de l'essai de l'utilisateur contre
   l'original, écart paramètre par paramètre.
