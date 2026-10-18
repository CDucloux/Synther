# Basses mono : principes et blueprints

Point de départ de toute basse sur un monophonique (Moog Messenger d'abord). Croise ce que disent des sources de qualité [1-8] avec les essais de l'utilisateur (`retours.md`, 2026-10-16 et 2026-10-17). Les positions sont en heures Messenger (7 = MIN, 12 = midi, 17 = MAX) ; elles sont **calées sur l'oreille de l'utilisateur**, pas sur une mesure en Hz (le manuel ne donne ni Hz ni durées).

## 1. Ce que disent les sources

Chaque principe porte ses sources ; « Essai » = confirmé par un retour de l'utilisateur.

**Partir d'un son riche, puis filtrer.** Une scie ou un carré passés dans un passe-bas plutôt qu'une sinusoïde : le filtre a de la matière à sculpter et à moduler [1][3]. Commencer avec un seul oscillateur, n'en ajouter que si besoin [3].

**Formes d'onde.** Scie : paires et impaires, mordante, la plus « basse » une fois filtrée [3][5]. Carré : impaires seulement, rond et « rebondissant », le son de basse synthé générique [2][3]. Triangle : du poids sans médiums [3]. Pulse : nasale, pour les basses fines [3]. Triangle + pulse = grave et présence, si la pulse ne domine pas [3].

**Octaves.** Classique Moog : OSC 1 en 32', OSC 2 (et 3) en 16', un cran plus haut pour que la basse s'entende aussi sur petites enceintes [3][6][7]. Trop d'écart entre oscillateurs et le son ne « colle » plus [3].

**Désaccord : quelques cents, pas plus.** Quelques cents épaississent ; au-delà la basse paraît fausse [3][4]. Deux ondes identiques désaccordées s'annulent par moments : le volume « pompe » (annulation de phase), ou le son « dérive » dans le mix avec des VCO [3][8]. À ne garder que pour une Reese voulue.

**Le filtre fait le caractère.** Le passe-bas de type Moog (ladder) donne le grave rond et profond [3]. La résonance du Minimoog, comme celle du Messenger sans RES BASS, **retire du grave** quand elle monte : sur les basses Model D, on la laisse à zéro [7] (Essai : « dull, sans profondeur »). Peu de résonance accentue légèrement la coupure ; beaucoup + modulation = acid [3].

**L'enveloppe de filtre articule, elle ne fait pas le son.** Une ouverture brève à chaque note (attaque et decay courts, pas de sustain) fait entendre où commence chaque note [1][2] et donne du « punch » dans les médiums en gardant le corps grave [3]. Doses publiées : « Amount of Contour » 2 à 3 sur 10 sur un Model D [7], 40 % sur une basse Thriller façon Moog [6] ; 60 % seulement quand la coupure est très basse [6]. Decay du filtre 0,2 à 0,6 s [6][7]. (Essai : coupure basse + EG fort = son éteint ; coupure haute + EG modéré = bon.)

**Le suivi de clavier garde la même couleur sur toute la ligne.** Sans lui, les notes aiguës s'étouffent ; 50 % est un bon départ [2], les deux interrupteurs ON sur un Model D [7]. Avec un peu de résonance, il donne du grave aux notes basses et du « pointu » aux notes hautes [5].

**Enveloppe d'ampli.** Attaque toujours rapide : une basse ne doit jamais paraître en retard [1][4]. Deux familles :
- basse « tenue » : sustain à fond, petite release pour ne pas couper sec (le petit tail grossit la note) [5][6][7] ;
- basse « électrique / pincée » : attaque rapide, decay long, pas de sustain, release assez courte [1].
Peu de sensibilité à la vélocité sur l'ampli : moins de compression nécessaire [4].

**Saturation : la vraie source du « gras ».** Pousser le filtre ou le mixer ajoute des harmoniques qui font passer la basse dans le mix [3][5]. Sur le Model D, la sortie réinjectée dans l'entrée externe donne une bosse vers 100 Hz puis du grain ; sweet spot vers 6-7 sur 10 [7]. Sur le Messenger : *FB / EXT IN*. Une pointe de bruit blanc ajoute aussi du grain [1].

**Mix.** Basse mono, au centre [1][4] ; pas de reverb ni de delay (ou filtrés) [1]. Une basse un peu sombre peut être plus forte sans gêner voix et guitares [4]. Une sub pure se place vers 40-60 Hz, et la basse médium se coupe sous ≈ 130 Hz quand on superpose [8].

## 2. Ce que ça change à nos règles (rectifications)

1. **CUTOFF pour le corps, EG pour l'attaque** : confirmé [1][2][3][6][7]. Positions Messenger calées à l'essai : corps à **1:00-2:00**.
2. **EG AMOUNT +10 à +30 %** : confirmé (Model D 20-30 % [7], Thriller 40 % [6]).
3. **Résonance par défaut à MIN-9:30 sur une basse** ; RES BASS selon le critère de `machines/messenger.md` dès qu'on en met plus. Confirmé [7].
4. **Nouveau : KB TRACKING ON par défaut** dès que la ligne couvre plus d'une octave ou monte en notes de passage [2][5][7]. OFF seulement pour une ligne sur 2-3 notes graves ou un son volontairement plus sombre en haut. Le Messenger ne suit qu'à 1:1 au bouton ; [KB ASSIGN] permet une dose plus faible (2/3 en MIDI, manuel p. 17).
5. **Nouveau : deux familles d'enveloppe d'ampli** (tenue ou pincée), au lieu d'une enveloppe sans sustain partout [1][5][7]. Beaucoup de nos fiches avaient un ampli à SUSTAIN MIN : bon pour une basse pincée, mais il amincit une basse ronde.
6. **Nouveau : *FB / EXT IN* ≈ 9:30-11:00 pour le gras** [3][7] ; laisser à MIN pour une basse propre.
7. **Nouveau : octaves 32' + 16'** comme point de départ « Moog » [3][6][7] ; 16' + 16' pour une basse plus serrée.
8. **Désaccord limité** (OSC 2 FREQ à quelques cents de midi, ≤ 12:10) sauf Reese [3][4].

## 3. Blueprints Messenger

Départs, à ajuster à l'oreille ; une fiche part du blueprint le plus proche puis applique ce que disent les sources du morceau. Enveloppes : A = attaque, D = decay, S = sustain, R = release.

| Blueprint | Oscillateurs | Mixer | Filtre | Env. filtre | Env. ampli | Divers |
|---|---|---|---|---|---|---|
| **B1 Basse ronde Moog** (Model D [7], Alchemy [6]) | OSC 1 scie 32', OSC 2 carré 16' (OSC 2 FREQ ≈ 12:05) | OSC 1 MAX, OSC 2 ≈ 1:00, SUB carré ≈ 11:00 | 4P, CUTOFF 1:00, RESO MIN, EG +20 %, KB TRACKING ON | A ≈ 7:30, D ≈ 11:00, S MIN | A MIN, S MAX, R ≈ 9:30-10:30 | FB / EXT IN ≈ 10:00 |
| **B2 Basse pincée électrique** (MusicRadar [1]) | carré ou scie 16', SUB ≈ 10:30 | OSC 1 MAX, SUB ≈ midi | 4P, CUTOFF 1:00-1:30, RESO ≤ 9:30, EG +20-30 %, KB ON | A MIN, D ≈ 10:30, S MIN | A MIN, D ≈ 12:00-1:00, S MIN, R ≈ 9:30 | MULTI-TRIG ON |
| **B3 Basse « plop » / marteau** (I Feel Love, Supernature) | 2 scies 16' / 32' | OSC 1 MAX, OSC 2 ≈ 2:00 | 4P, CUTOFF ≈ midi-12:30, RESO 10:00-11:00 + RES BASS, EG +30-50 %, KB ON | A MIN, D ≈ 10:00, S MIN | A MIN, D ≈ 11:00, S MIN | MULTI-TRIG ON, séquence |
| **B4 Sub / fondation** (Attack [8], MusicRadar [3]) | triangle 32' + SUB triangle | OSC 1 MAX, SUB ≈ 2:00 | 4P, CUTOFF 2:00-3:00, RESO MIN, EG à midi, KB OFF | - | A ≈ 7:30 (pas de clic), S MAX, R ≈ 9:30 | à superposer à une basse médium |
| **B5 Acid** ([3], archétype 303) | scie (ou carré) 16' seule | OSC 1 MAX | 4P, CUTOFF ≈ midi, RESO 1:30-2:30, RES BASS OFF, EG +40-70 % | A MIN, D 10:00-11:00, S MIN | A MIN, D ≈ 1:00, S ≈ 3:00, R ≈ 8:30 | F ENV VEL, glide legato |
| **B6 Basse épaisse / Taurus** (Nick Magnus [4] : ±7 cents + sinus) | 2 scies 16' (OSC 2 FREQ ≈ 12:05-12:10) | OSC 1 MAX, OSC 2 ≈ 3:00, SUB triangle ≈ 1:00 | 4P, CUTOFF 1:30-2:30, RESO MIN, EG +10 %, KB ON | A ≈ 9:00, D ≈ 2:00, S ≈ 2:00 | A MIN, S MAX, R ≈ 11:00 | si le volume « pompe » : rapprocher OSC 2 FREQ de midi |
| **B7 Basse séquencée** (octaves, doubles croches) | scie 16' + carré 16' | OSC 1 MAX, OSC 2 ≈ 2:00 | 4P, CUTOFF 1:00, RESO 9:30-10:00 (+ RES BASS), EG +20-30 %, KB ON | A MIN, D ≈ 10:00, S MIN | A MIN, D ≈ 11:00, S MIN-9:00 | MULTI-TRIG ON, GATE 50-70 % |

## 4. Diagnostic à l'oreille (basses)

| Symptôme | Geste, dans l'ordre |
|---|---|
| terne, éteint, « dull » | CUTOFF +1 h ; KB TRACKING ON ; puis EG |
| creux, sans grave | RES BASS ON (si RESONANCE ≥ 9:30) ; SUB ; OCTAVE 1 en 32' |
| boueux, « boomy » | SUB ou OSC 2 plus bas ; CUTOFF −½ h ; moins de FB / EXT IN |
| pas de punch, notes molles | DECAY du filtre plus court ; EG +10 % ; ampli A à MIN |
| trop « plop », synthétique | EG −10 % ; CUTOFF +½ h ; DECAY filtre plus long |
| fin, ne passe pas dans le mix | FB / EXT IN ≈ 10:00 ; OSC 2 en 16' ; un peu de NOISE |
| volume qui pompe ou dérive | OSC 2 FREQ plus près de midi (annulation de phase) |
| notes aiguës sourdes | KB TRACKING ON |
| la note coupe sec | RELEASE ampli ≈ 9:30-10:00 |

## Sources

1. « Better synth bass in 9 easy steps », MusicRadar, https://www.musicradar.com/tuition/tech/better-synth-bass-in-9-easy-steps-148695
2. « Create your own simple synth bass sound in 6 easy steps », Computer Music / MusicRadar, https://www.musicradar.com/how-to/create-your-own-simple-synth-bass-sound-in-6-easy-steps
3. « How to craft the perfect synth bassline », Si Truss, MusicRadar, juin 2024, https://www.musicradar.com/news/how-to-craft-the-perfect-synth-bassline
4. Nick Magnus, « Creating Analogue Sounds On Digital Synths, Part 4 : Recreating Analogue Bass », Sound On Sound, avril 1994, https://www.soundonsound.com/techniques/creating-analogue-sounds-digital-synths-part-4 ; Tom Flint, « Q. How can I get more effective synth bass in my mixes? », Sound On Sound, janvier 2007, https://www.soundonsound.com/sound-advice/q-how-can-get-more-effective-synth-bass-my-mixes
5. « Fat juicy analog style bass tutorial », Syntorial, https://www.syntorial.com/tutorials/fat-juicy-analog-style-bass-tutorial/
6. « How to make a Minimoog-style bass patch », MusicRadar, https://www.musicradar.com/how-to/minimoog-analogue-bass (coupure ≈ 120 Hz, résonance 25 %, enveloppe 60 %, decay 0,2 s ; ampli A 0, S max, R 1 s) ; basse Thriller façon Moog, Computer Music, juillet 2021 (Amount ≈ 40 %, decay filtre ≈ 10:00 ; lu dans un résumé de moteur de recherche seulement)
7. « Master the Minimoog Model D and create a classic Minimoog bass sound », Future Music / MusicRadar, février 2022, https://www.musicradar.com/news/master-the-minimoog-model-d-create-classic-bass (OSC 1 32', OSC 2 et 3 en 16' désaccordés ; mixer 10 / 5-8 ; entrée externe 6-7 ; cutoff −3, emphasis 0, contour 2-3, keyboard control ON ; filtre A 5-10 ms, D 400-600 ms, S 0 ; ampli A 0, D 0,8-1 s, S 10)
8. « Layering synths », Attack Magazine, https://www.attackmagazine.com/technique/synth-secrets/layering-synths/ (sub sinus vers 40-60 Hz, basse médium coupée sous ≈ 130 Hz)

Non accessibles cette fois : les « Sound Charts » de Moog (Minimoog Patch Book, synthzone.com : 403 ; manuel du Model D 2016 introuvable) et le manuel Minimoog de 1974 (zzounds : 403). Ce seraient des réglages publiés par le fabricant : à récupérer si l'utilisateur les dépose dans `original-sources/`.

Attention aux équivalences : les positions d'un Model D (cutoff −3 sur −5…+5) ne se transposent pas telles quelles sur le Messenger (plage, suivi de clavier, sensibilité différents). Seul l'essai de l'utilisateur a calé le Messenger (corps vers 1:00-2:00).
