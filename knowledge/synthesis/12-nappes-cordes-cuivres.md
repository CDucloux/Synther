# Nappes, cordes, cuivres, keys : principes et blueprints (minilogue XD)

Point de départ de tout son polyphonique (minilogue XD). Sources lues en entier [1-12], recherche du 2026-10-18. Les valeurs XD sont des **départs à ajuster à l'oreille** : les recettes publiées sont faites sur d'autres synthés (Syntorial donne des « % de course », MusicRadar une échelle 0-10), on ne les reporte pas telles quelles en 0-1023. Seule exception exacte : le désaccord en UNISON (V.M. DEPTH 1023 = 50 cents, donc 1 cent ≈ 20).

## 1. Principes

**Nappes**
- Deux scies légèrement désaccordées battent à la fréquence de leur écart : un peu épaissit, trop sonne faux, « honky-tonk » [1].
- Le mouvement vient d'une petite modulation de hauteur sur **un seul** oscillateur, à une vitesse différente du battement ; un LFO aléatoire faible casse la régularité [1]. Imitation de la dérive analogique : LFO lent, peu profond, sans resynchronisation sur la note [4].
- Ampli en trapèze : montée lente, longue queue [1]. Exemples : attaque 300 ms, release 730 ms [10] ; attaque 1,5 s, release 3,6 s [7].
- Filtre plutôt fermé ; enveloppe de filtre lente et peu dosée pour le « souffle » [7][10] ; inversée pour un creux [9].
- Le chorus fait le son Juno (mode I lent, ou I+II) [9] ; exemple : chorus lent à 45 % [7].
- Contre la boue : rien d'utile sous ≈ 200 Hz, passe-haut, creux de 4 à 6 dB vers 3-4 kHz ; le désaccord brouille la hauteur ; la réverbération alourdit les changements d'accords [5].

**Cordes (string machine)**
- Scie, filtre à mi-course, suivi de clavier modéré, aucune modulation de filtre, aucune vélocité [1].
- La PWM sonne comme deux hauteurs qui vibrent l'une autour de l'autre : un chorus en soi ; mélanger scie et PWM évite le côté creux [1][2].
- Sans PWM : deux scies à 4 cents d'écart, une pointe de modulation de hauteur, réverbération [2]. Une octave grave sur le VCO 2 donne du poids ; un chorus externe donne le « lustre » [1].

**Cuivres**
- Le timbre est porté par les enveloppes [4] : le filtre s'ouvre au début puis retombe vite. Régler le CUTOFF au timbre final ou plus bas : plus il est bas, plus le mouvement est marqué [4].
- Attaque de l'ampli égale à celle du filtre ou un peu plus rapide ; un peu de release sur les deux [4]. Vélocité vers la quantité d'enveloppe, aftertouch vers la brillance [3].
- Désaccord ≈ ±6 cents ; une octave au-dessus fait une section [4]. Cor : attaque et decay plus lents, moins d'enveloppe [4]. Vibrato retardé vers 5 Hz, très faible, pour moins « électronique » [3]. Trop de résonance : réduire l'enveloppe [4].

**Keys, plucks, stabs**
- Attaque 0, decay court, sustain 0, enveloppe de filtre rapide ; oscillateurs remis en phase à chaque note pour le claquant [8].
- Stab : filtre 12 dB très fermé, enveloppe forte et brève, accord fixe joué partout (mode CHORD du XD) [11][12].
- Partie rythmique : raccourcir les notes plutôt que soutenir [5].

## 2. Traduction minilogue XD (contrôles)

- Désaccord : VCO 2 *PITCH* en cents, ou *VOICE MODE* UNISON (4 voix sur une note, *V.M. DEPTH* 0-1023 = 0-50 cents), ou POLY avec *V.M. DEPTH* > 0 (DUO : 2 voix empilées) [12].
- PWM : VCO en SQR + *LFO* TARGET SHAPE (le *SHAPE* d'un carré règle la largeur).
- Filtre 2 pôles seulement : pas de 24 dB ; *DRIVE* 0/50/100 % ; *KEY TRACK* 0/50/100 % [12].
- Une seule enveloppe de modulation (*EG*, A/D seulement) : pas de sustain de filtre. Pour un « souffle » tenu, monter le *CUTOFF* et garder l'*EG* comme une bouffée.
- *MOD FX* CHORUS ou ENSEMBLE (Stereo, Light, Mono) [12] ; REVERB et DELAY.

## 3. Blueprints minilogue XD

| Blueprint | Oscillateurs et voix | Filtre | EG (filtre) | AMP EG | Effets |
|---|---|---|---|---|---|
| **N1 Nappe analogique chaude** (Stranger Things, Survive [7]) | 2 SAW 8', POLY + *V.M. DEPTH* bas (DUO) ou VCO 2 *PITCH* ≈ +8 cents | *CUTOFF* ≈ 400-500, *RESONANCE* ≈ 150, *KEY TRACK* 50 % | A long (≈ 700), D long, *EG INT* +15-20 % | A ≈ 600-700, S ≈ 1023, R ≈ 800 | CHORUS lent ≈ 45 %, REVERB ≈ 30 % |
| **N2 Nappe Juno 80s** [9][10] | SAW 8' + VCO 2 SQR 16' (sub), *LFO* lent et faible sur PITCH | *CUTOFF* ≈ 600, *RESONANCE* ≈ 150 | *EG INT* −15 % (enveloppe inversée) ou léger + | A ≈ 350-450, D long, S ≈ 800, R ≈ 600 | CHORUS (type Juno), REVERB courte |
| **C1 Cordes Solina / Juno** [1][2] | SAW + SQR (LFO TARGET SHAPE, triangle lent), VCO 2 *PITCH* +4 cents ; option VCO 2 en 16' | *CUTOFF* ≈ 550, *RESONANCE* 0, *KEY TRACK* 50 % | *EG INT* 0 | A ≈ 300, S ≈ 950, R ≈ 500 (trapèze) | ENSEMBLE Stereo ≈ 60 %, REVERB ≈ 30 % |
| **K1 Cuivres Jump / OB** [6] | SAW, UNISON *V.M. DEPTH* ≈ 180 (≈ 9 cents) ou POLY + VCO 2 SAW +9 cents | *CUTOFF* haut (≈ 850), *RESONANCE* ≈ 250 | *EG INT* faible | A 0, D long, S 0, R court (≈ 100) | REVERB ≈ 30 % |
| **K2 Cuivres « swell » Prophet / OB** [3][4] | 2 SAW, VCO 2 *PITCH* ≈ +6 cents (option VCO 2 en 4') | *CUTOFF* au timbre final ou plus bas (≈ 400-550) | A ≈ 150-250, D ≈ 500, *EG INT* +40-60 % | A = A de l'EG ou un peu moins, S ≈ 800, R ≈ 300 | Amp Velocity et vélocité vers l'EG (PROGRAM EDIT) |
| **K3 Cuivres CS-80 Blade Runner** [8] | 2 SQR, VCO 2 4' et *PITCH* −6 cents, *LFO* BPM sur SHAPE (PWM) | *CUTOFF* ≈ 750, *RESONANCE* ≈ 150 | A ≈ 450, *EG INT* +15 % | A ≈ 250, D long, S ≈ 400, R ≈ 600 | REVERB ample ≈ 10-20 % |
| **P1 Pluck poly** (Boys and Girls [8]) | SAW (≈ 30 %) + TRI (≈ 70 %), UNISON ou DUO ≈ 6 cents | *CUTOFF* ≈ 500, *RESONANCE* ≈ 450, *KEY TRACK* 50 % | A 0, D ≈ 250, *EG INT* +25 % | A 0, D ≈ 350, S 0, R ≈ 250 | DELAY court (≈ 30 %), REVERB ≈ 20 % |
| **S1 Stab rave / house** [11] | *VOICE MODE* CHORD m7, SQR + VCO 2 SQR 4' (+10 cents) | *CUTOFF* très bas (≈ 250), *RESONANCE* faible | A 0, D court, *EG INT* +60 % | A 0, S ≈ 1023, R court | grande REVERB ou DELAY Tape |

Nappe ambient : pas de recette chiffrée trouvée ; principes N1 avec attaque et release plus longs [1][7] et réverbération mesurée aux changements d'accords [5].

## 4. Diagnostic

| Symptôme | Geste |
|---|---|
| son « orgue bon marché », buzzy | modulation de hauteur sur un seul VCO, ou PWM ; mêler scie et PWM [1] |
| mouvement trop régulier | LFO plus lent et différent du battement ; un peu d'aléatoire [1] |
| faux, honky-tonk | moins de désaccord [1] |
| PWM creuse | ajouter une scie [1] |
| nappe boueuse, nuageuse | moins de désaccord, *CUTOFF* plus bas, VCO plus haut (8'/4') ; au mix passe-haut sous 200-300 Hz [5] |
| changements d'accords pâteux | moins de REVERB et de DELAY [5] |
| cuivres sans relief | *CUTOFF* plus bas, *EG INT* plus fort [4] |
| clic à l'attaque des cuivres | *ATTACK* de l'*AMP EG* un peu plus longue [4] |
| résonance qui siffle | réduire l'*EG INT* [4] |
| cuivres trop « électroniques » | vibrato retardé et très faible [3] |

## Sources

1. Gordon Reid, « Synthesizing Strings: String Machines », Synth Secrets, Sound On Sound, février 2003, https://www.soundonsound.com/techniques/synthesizing-strings-string-machines
2. Gordon Reid, « Synthesizing Strings: PWM & String Sounds », Synth Secrets, Sound On Sound, mars 2003, https://www.soundonsound.com/techniques/synthesizing-strings-pwm-string-sounds
3. Gordon Reid, « Synthesizing Brass Instruments », Synth Secrets, Sound On Sound, mai 2001, https://www.soundonsound.com/techniques/synthesizing-brass-instruments
4. Nick Magnus, « Creating Analogue Sounds On Digital Synths, Part 3 » (cuivres), Sound On Sound, mars 1994, https://www.soundonsound.com/techniques/creating-analogue-sounds-digital-synths-part-3
5. Mike Senior, « Creating & Using Synth Pad Sounds », Sound On Sound, mai 2010, https://www.soundonsound.com/techniques/creating-using-synth-pad-sounds
6. « Van Halen, Jump | Brass », Syntorial, https://www.syntorial.com/preset-recipe/van-halen-jump-brass/
7. « Survive, Stranger Things Theme | Pad », Syntorial, https://www.syntorial.com/preset-recipe/survive-stranger-things-theme-pad/
8. « Kyle Dixon & Michael Stein, Boys and Girls | Pluck », https://www.syntorial.com/preset-recipe/kyle-dixon-michael-stein-boys-and-girls-pluck/ ; « Vangelis, Blade Runner | Brass », https://www.syntorial.com/preset-recipe/vangelis-blade-runner-brass/ ; Syntorial
9. « How to create an '80s Juno-style pad sound », MusicRadar / Computer Music, novembre 2019, https://www.musicradar.com/how-to/how-to-create-an-80s-juno-style-pad-sound
10. « How to make your own classic '80s synth pad sound », MusicRadar / Future Music, juillet 2021, https://www.musicradar.com/how-to/how-to-build-a-classic-80s-pad-sound
11. Si Truss, « How to create a classic rave chord stab », MusicRadar, février 2023, https://musicradar.com/how-to/rave-chord-stab
12. Manuel du minilogue XD, `manuals/minilogue-xd-user-manual.pdf` (VOICE MODE, UNISON 0-50 cents, CHORD, ENSEMBLE, DRIVE, KEY TRACK)

Non accessibles ou non trouvés : Reverb.com « The Synth Sounds of Van Halen's Jump » (403) ; aucune page Reverb Machine ni Attack Magazine chiffrée sur ces familles ; la figure 2 de [4] (valeurs en image).
