# Séquences et arpèges : principes et blueprints

Séquences pas à pas, ostinatos et arpèges (Moroder, New Order, Tangerine Dream, synthwave, Stranger Things). Sources lues en entier [1-16], recherche du 2026-10-18. Positions Messenger en heures (7 = MIN, 17 = MAX), calées comme les basses (`08-basses.md`) : un CUTOFF « à 9 h » ou « 171 Hz » sur un autre synthé ne se recopie pas tel quel sur le Messenger (essai de l'utilisateur, 2026-10-17). Les règles de relevé des notes (piste qui joue vraiment la partie, accords réduits sur le Messenger) sont dans la skill sound-sheet.

## 1. Principes

**Le son de la note : un pluck.** Court, sans sustain, ouvert par une enveloppe de filtre marquée : coupure 600 Hz, enveloppe 65 %, decay 192 ms (I Feel Love) [2] ; coupure 171 Hz, decay 490 ms (A Real Hero) [11]. Un decay plus court donne un timbre métallique, « robotique » [10]. Un second oscillateur à l'octave épaissit [2][9].

**Gate et legato.** Notes répétées très rapides avec une gate à 99 % pour qu'elles ne se coupent pas [10]. Une seule note tenue dans l'arpégiateur donne une pulsation hachée ou une basse en sauts d'octave [12][14]. Un long decay ou release fait déborder les notes : séquence plus douce [10].

**Accents.** Franke (Tangerine Dream) avait 8 niveaux d'accent envoyés au VCA, et quatre types de pas : note, silence, legato, accent [6]. Accents sur les contretemps = énergie [11]. Une rampe de vélocité vers la coupure crée une montée [14].

**Le filtre bouge.** Après la hauteur, la coupure est le premier paramètre à faire varier d'un pas à l'autre [6][7] : à la main, automatisée [15], mod wheel légère [9], LFO très lent [2], ou LFO de la durée d'une mesure (triangle d'une mesure vers le filtre) [12].

**Le delay fait partie du rythme.** I Feel Love : note sèche à gauche, répétition retardée à droite [3][4] ; recette : delay 120 ms, 100 % wet, un seul canal, à 125 BPM, soit une double croche [2]. Ping-pong à la noire, aigus amortis vers 1000 Hz [9] ; ping-pong à réinjection filtrée [14]. Delay et release « rendent de la polyphonie » à un arpège mono [14]. Le Messenger n'a pas de delay : écrire l'écho en notes dans la grille, ou ajouter une pédale.

**Octaves et transposition.** Varier l'octave et la disposition des notes [14] ; enchaîner des séquences (4 fois la première, 8 fois la seconde) [6][7] ; I Feel Love est transposée à intervalles réguliers [2][4]. Messenger : touche tenue pendant PLAY (référence C5) ; minilogue XD : pas de transposition au clavier pendant la lecture.

**Swing et métrique.** Longueur de note et swing [13] ; Franke superpose deux pulsations et aime les mesures impaires (7/4) [6].

**Garder la séquence vivante.** Ne pas jouer la même séquence plus de 50 fois ; changer la couleur d'une note à l'autre : on entend une mélodie de timbres en plus des hauteurs ; prévoir la structure pour éviter le « disque rayé » [6]. Séquence aléatoire animée par plusieurs LFO à vitesses différentes [12] ; notes de passage avant les changements d'accord [14].

**Mix.** Peu de couches, des registres séparés [10] ; filtre bas, résonance modeste, aigus calmés [9] ; reverb et delay sombres, envois forts sauf sur la basse [10] ; compression après les effets [11].

## 2. Outils des deux machines

- **Messenger** : 64 pas ; *GATE LENGTH* 6,25-100 % (*SETTINGS* 3) ; *SWING* (50 % = droit) ; *CLOCK DIV* de 1/32 à la ronde (*SETTINGS* 9 ; 1/8 pour des croches au vrai tempo) ; NOTE PROB et GATE PROB ; *MULTI-TRIG* pour relancer les enveloppes sur des notes liées ; HOLD (liaison), ADV (silence) ; transposition au clavier.
- **minilogue XD** : 16 pas polyphoniques, gate par pas, Swing, Step Resolution, 4 motion sequences (pour animer *CUTOFF*, *SHAPE*…), DELAY et REVERB.

## 3. Blueprints

| Blueprint | Messenger | minilogue XD | Source |
|---|---|---|---|
| **Q1 Séquence disco Moroder** (I Feel Love) | 2 scies 16' / 32' (OSC 2 FREQ ≈ 12:05), 4P, *CUTOFF* ≈ 12:30, *RESONANCE* ≈ 11:00 + RES BASS, *EG AMOUNT* +30-50 %, F ENV D ≈ 10:00 S MIN, A ENV D ≈ 11:00 S MIN ; écho écrit en notes à la double croche | 2 SAW (VCO 2 16'), *EG* D court sur CUTOFF, DELAY Stereo BPM à la double croche, 100 % sur un canal si possible | [2][3][4][16] |
| **Q2 Basse séquencée New Order** (Blue Monday) | 2 oscillateurs, 4P, *CUTOFF* ≈ 1:00, *RESONANCE* ≈ 10:00 + RES BASS, *EG AMOUNT* fort (+50 %), F ENV S ≈ 9:30, A ENV S MAX | 2 VCO, *EG INT* fort, AMP EG S max | [5] |
| **Q3 Arpège Berlin school** (Tangerine Dream) | scie ou carré 8', *CUTOFF* tourné à la main pendant la séquence, accents (F ENV VEL + vélocité), enchaînement de séquences, peu de transposition | séquence 16 pas + motion sequence du *CUTOFF* | [6][7][8] |
| **Q4 Ostinato Stranger Things** (thème) | 2 scies à l'octave, *GLIDE* très court, filtre bas et résonance faible, *FB / EXT IN* léger ; 16 doubles croches | même chose en UNISON léger, CHORUS, DELAY ping-pong à la noire, aigus amortis | [9] |
| **Q5 Arpège percussif lumineux** (Eight Fifteen) | 2 oscillateurs à l'octave, *CUTOFF* bas et *EG AMOUNT* très fort, *GATE* ≈ 99 %, triples croches ; variante douce : decay et release longs (notes qui débordent) | CHORUS, REVERB sombre | [10] |
| **Q6 Arpège synthwave à contretemps** (A Real Hero) | non (repose sur les effets) | SAW en UNISON, *CUTOFF* bas sans *KEY TRACK*, A ≈ 70 ms, D ≈ 1,2 s, S haut ; CHORUS, DELAY 25 %, REVERB 50 % ; notes sur les contretemps | [11] |
| **Q7 Séquence modulaire animée** (In Motion) | une note en sauts d'octave, *LFO 1* TRI → CUTOFF *SYNC* ON (1 mesure), *OSC 2 SYNC* modulé par un 2e mouvement (LFO 2 ou F ENV LOOP) | *LFO* BPM → CUTOFF, motion sequence | [12] |
| **Q8 Arpège « produit »** | mode Up/Down de l'arpégiateur, notes hautes plus sourdes (*KB TRACKING* OFF), *CUTOFF* automatisé à la main | *VOICE MODE* ARP, motion sequence du *CUTOFF*, DELAY et REVERB | [15] |

## 4. Diagnostic

| Symptôme | Geste |
|---|---|
| séquence plate, « disque rayé » | faire bouger le *CUTOFF* et les accents, enchaîner des variantes, changer le timbre d'une note à l'autre [6][12][15] |
| notes molles, empâtées | SUSTAIN à 0, decay de filtre plus court, plus d'*EG AMOUNT* [2][11] |
| notes coupées, trop sèches | *GATE* plus longue (jusqu'à 99 %) ou RELEASE plus long [10][14] |
| arpège maigre | delay ping-pong et release pour faire chevaucher les notes [14] |
| criard, trop « growl » | *CUTOFF* plus bas, résonance modeste [9] |
| groove raide | accents sur les contretemps, *SWING* [11][13] |
| l'écho brouille le rythme | caler le delay sur une valeur de note (double croche pour I Feel Love) [2] |

## Sources

1. Richard Buskin, « Classic Tracks: Donna Summer, I Feel Love », Sound On Sound, octobre 2009, https://www.soundonsound.com/techniques/classic-tracks-donna-summer-feel-love (selon Pete Bellotte, seuls compression et réverbe ajoutées : contredit [3][4] sur le delay)
2. « The 40 greatest synth sounds of all time, No 3: Donna Summer, I Feel Love », MusicRadar, mai 2021, https://www.musicradar.com/news/donna-summer-i-fee-love-best-synth-sound
3. « How to create Donna Summer I feel love bassline and pad sounds in DRC », Imaginando, juin 2018, https://www.imaginando.pt/news/how-to-create-donna-summer-i-feel-love-bassline-and-pad-sounds-in-drc
4. « I Feel Love », Wikipédia (anglais), https://en.wikipedia.org/wiki/I_Feel_Love
5. « Greatest synth sounds: New Order, Blue Monday », MusicRadar, janvier 2022, https://www.musicradar.com/news/blue-monday-synth-sound
6. « Chris Franke on Sequencers », Electronics & Music Maker, mars 1983 (archive mu:zines), https://www.muzines.co.uk/articles/chris-franke-on-sequencers/5932
7. « Chris Franke: The Sequencer King », Sound On Sound, mai 1994, https://www.soundonsound.com/node/4926398
8. « Tangerine Dream: Changing Use Of Technology, Part 2: 1977-1994 », Sound On Sound, janvier 1995, https://www.soundonsound.com/node/4925748
9. John Walden, « Stranger Things Synths With Retrologue 2 », Sound On Sound, décembre 2022, https://www.soundonsound.com/techniques/cubase-stranger-things-synths-retrologue-2
10. « Stranger Things Synths: Eight Fifteen », Reverb Machine, https://reverbmachine.com/blog/stranger-things-synths-eight-fifteen/
11. « Drive Synth Sounds », Reverb Machine, janvier 2025, https://reverbmachine.com/blog/drive-synth-sounds/
12. « How Trent Reznor & Atticus Ross Made In Motion », Reverb Machine, https://reverbmachine.com/blog/trent-reznor-atticus-ross-in-motion/
13. Bruce Aisher, « An Introduction To Arpeggiators », Attack Magazine, février 2013, https://www.attackmagazine.com/technique/tutorials/an-introduction-to-arpeggiators/
14. Bruce Aisher, « Complex Arps », Attack Magazine, juin 2014, https://www.attackmagazine.com/technique/tutorials/complex-arps-arpeggiator/2/
15. « How to produce perfect synth arpeggiator parts », MusicRadar, mai 2022, https://www.musicradar.com/how-to/synth-arpeggiators
16. « Donna Summer, I Feel Love | Bass », Syntorial, https://syntorial.com/preset-recipe/donna-summer-i-feel-love-bass (attribue le son à un Minimoog, contredit par [1] : Moog modulaire)

Non accessibles : PressReader (tutoriel Computer Music « Berlin school »), inkl (MusicRadar sur I Feel Love), DJ Mag, Reverb.com (I Feel Love), vintagedigital.com.au (Blue Monday) ; aucun article de fond sur le delay à la croche pointée pour une séquence.
