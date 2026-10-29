# Calibration : position de bouton → valeur réelle

But : passer de « cutoff assez fermé » à « CUTOFF ≈ 10:00 » avec des chiffres mesurés sur **ces** machines.
Statut : **aucune mesure pour l'instant** (l'analyse audio est mise de côté).

## Ce que Moog documente (et ce qui manque)

Vérifié le 2026-10-29 dans le manuel du Messenger (texte intégral, CONFIG, MIDI, SPECIFICATIONS), le test de Sound On Sound (septembre 2025) et les fiches produit des revendeurs.

| Paramètre | Documenté | Source |
|---|---|---|
| LFO 1 et LFO 2 RATE | ≈ 0,05 Hz à ≈ 12 Hz ; CONFIG 1.4 : PGM 2 = 0,5-120 Hz, PGM 3 = 5 Hz-1,2 kHz (LFO 1) | manuel p. 8, 20, 28 |
| Pitch bend | ±7 demi-tons par défaut, jusqu'à ±24 (CONFIG 1.1 et 1.2) | manuel p. 8, 28 |
| Hauteur de référence | OSC en 8', KB OCTAVE neutre : le Do le plus grave = C4 (≈ 261,63 Hz) ; séquence transposée par rapport au C5 | manuel p. 8, 22 |
| Glide | modes legato / gated, courbes exponentielle, linéaire vitesse constante, linéaire temps constant ; **pas de durée** | manuel p. 28 |
| Tempo | 30 à 300 BPM | manuel (MIDI) |
| Filtre | pentes : LP 24 et 12 dB/oct, BP, HP ; auto-oscillation vers 2:00 de RESONANCE (selon SOS) ; **pas de plage de CUTOFF en Hz** | manuel p. 17-18 ; SOS |
| Enveloppes A / D / S / R | **aucune durée publiée** | - |
| EG AMOUNT, KB TRACKING | bipolaire ; suivi 1 V/oct (0, 2/3, 1:1 en MIDI) ; **pas d'ampleur en Hz** | manuel p. 17 ; MIDI |
| MIDI | toutes les commandes en 14 bits (0-16383), sans unité physique | manuel (MIDI) |

Conclusion : la correspondance position → Hz du CUTOFF et position → ms des enveloppes **n'existe nulle part chez Moog** ; même publiée, elle ne donnerait pas la courbe du potard ni l'écart d'un exemplaire à l'autre (analogique). D'où la mesure ci-dessous.

## Protocole (Messenger)

1. Laisser chauffer 15 min. Patch init (PANEL 1 s), note **C3 tenue** (KB OCTAVE 0, OCTAVE 8'), enregistrement WAV direct, sans effet.
2. Ne faire varier **qu'un seul paramètre**, aux positions 7, 8.5, 10, 11, 12, 13, 14, 15.5, 17.
3. Nommer les fichiers `messenger_<param>_<position>.wav` (ex. `messenger_cutoff_10.5.wav`).

| Paramètre | Ce qu'on mesure | Réglage du reste |
|---|---|---|
| CUTOFF | fréquence de coupure (Hz) | scie, résonance 0, EG AMOUNT midi, KB TRACK off |
| RESONANCE | hauteur du pic, seuil d'auto-oscillation | cutoff 12 |
| LFO 1 / LFO 2 RATE | Hz | LFO → pitch, depth fort |
| A / D / R (ampli) | secondes | sustain 0 pour D, note courte pour R |
| GLIDE | secondes pour une octave | deux notes à l'octave en legato |
| OSC 2 FREQ près de midi | cents / battements | 2 scies, mixer égal |
| WAVESHAPE | forme réelle (où est le carré exact ?) | balayage lent |

## Format des résultats

Un CSV par machine et paramètre : `messenger_cutoff.csv` → `position,valeur,unite,note`.
Une fois rempli, les fiches peuvent citer les valeurs réelles (et la confiance des réglages monte).
