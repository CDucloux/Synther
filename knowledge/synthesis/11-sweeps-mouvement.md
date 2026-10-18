# Sweeps, mouvement et effets sonores : principes et blueprints

Balayages de filtre, risers, chutes, sirènes, wobble, filtre auto-oscillant, enveloppes en boucle. Sources lues en entier [1-10], recherche du 2026-10-18. Positions Messenger en heures (7 = MIN, 17 = MAX). Les vitesses de LFO en Hz ne sont pas gravées sur le panneau : la conversion en heures ci-dessous suppose une échelle logarithmique de 0,05 à 12 Hz (plage PGM 1 du manuel [10]) et reste **à vérifier à l'oreille**.

## 1. Principes

**À la main, au LFO ou à l'enveloppe.** Un petit déplacement du cutoff s'entend à peine : il faut balayer une grande partie de la course [1]. Le LFO répète le mouvement ; l'enveloppe redonne la même courbe à chaque note, même jouée vite [1]. Les grands joueurs de synthé jouent autant des potards que du clavier (Eno, Larry Fast) [1].

**Vitesse du LFO sur le filtre** [2] :
- ≈ 0,1 Hz : balayage lent, ambient (Messenger *LFO 1 RATE* vers 8:00-8:30) ;
- ≈ 1 à 2 Hz : wah-wah (vers 12:30-1:30) ;
- 10 à 20 Hz : growl, grain de cuivre (vers 4:30-MAX ; au-delà, CONFIG 1.4 PGM 2 ou 3 élargit la plage [10]).

**La résonance fait entendre le balayage.** Elle accentue la fréquence de coupure qui bouge et fait sortir les harmoniques une à une ; le balayage lent d'une seule note grave est le plus parlant [1][3]. Elle aide un son à passer dans un mix chargé [1]. En passe-bas, beaucoup de résonance retire du grave [3] : sur le Messenger, sauf avec RES BASS [10] (critère : `machines/messenger.md`).

**Auto-oscillation.** Au maximum, le filtre sort une sinusoïde à la fréquence de coupure [3][10] ; sur du bruit blanc, le cutoff devient une « hauteur approximative » [1]. Juste avant ce point : des sons qu'aucun instrument acoustique ne fait [3].

**Bruit pour les risers.** Bruit blanc dans un passe-bas ou passe-bande dont la coupure monte [5][7] ; plus de résonance ajoute un sifflement à hauteur définie et amincit le bas [7].

**Balayage de hauteur.** Enveloppe à attaque longue sur la hauteur [5][6], de 2 demi-tons à plusieurs octaves [7]. Messenger : *MOD DESTINATION* F ENV → OSC 2 FREQ avec *MOD AMOUNT* (un seul oscillateur), ou LFO 1 vers OSC 2 FREQ.

**Faire monter la tension.** Accélérer le LFO pendant la montée et augmenter sa profondeur [7]. Une ligne droite sonne rarement le mieux : enregistrer le geste à la main [7].

**Modulation à fréquence audio.** Ce n'est pas un trémolo très rapide : elle crée de nouvelles fréquences (somme et différence), en général inharmoniques, « agressives », qui changent avec la note [4]. Messenger : *OSC 2 → CUTOFF* (du vibrato de filtre léger au FM de filtre accordé), FM 1→2, LFO en plage audio [10].

**Enveloppes en boucle (Messenger).** Avec *F ENV LOOP* ou *A ENV LOOP*, l'attaque repart à la fin du release : l'enveloppe agit comme un LFO à quatre étapes, de forme réglable [10].

**Effets et mix.** Reverb et delay contre l'effet sec ; sidechain de la grosse caisse pour caler un riser sur le groove ; phaser à vitesse modulée, distorsion au sommet [5]. Grande hall ≈ 3 s, retirer le bas, petit shelf aigu vers 5 kHz [7].

**Durée en mesures.** La note dure toute la montée ; une chute de 4 mesures sur un break ; reverb lancée ≈ 3 mesures avant la fin, delay 1 mesure plus tôt [7].

## 2. Blueprints

| Blueprint | Messenger | minilogue XD | Source |
|---|---|---|---|
| **W1 Balayage lent de filtre** | scie 16', 4P, *RESONANCE* 1:00-2:30 (+ RES BASS si c'est une basse), *LFO 1* TRI → CUTOFF, *RATE* ≈ 8:00, *DEPTH* fort ; une note grave tenue | SAW, *LFO* NORMAL TRI → CUTOFF, *RATE* bas, *INT* fort, *RESONANCE* ≈ 600 | [1][2][10] |
| **W2 Balayage à la main** | même son, *LFO* coupé, *CUTOFF* tourné sur plusieurs mesures (ex. Veridis Quo arpège) | *CUTOFF* à la main, ou motion sequence du *CUTOFF* | [1][7] |
| **W3 Riser de bruit** | *MIXER* NOISE seul, *MODE* BAND PASS, *CUTOFF* et *RESONANCE* au plus bas au départ, *CUTOFF* monté sur toute la montée, puis *RESONANCE* pour le sifflement | MULTI ENGINE NOISE, *CUTOFF* et motion sequence ; REVERB Hall longue | [5][7] |
| **W4 Wind-up** | NOISE, 4P, *CUTOFF* et *RESONANCE* ≈ 10:00, *LFO 1* → CUTOFF *DEPTH* MAX, *RATE* ≈ 11:00 qu'on accélère à la main (adaptation) | *LFO* → CUTOFF, *RATE* accéléré en motion sequence | [7] |
| **W5 Riser de hauteur** | 2 scies (OSC 2 à +7 demi-tons), filtre ouvert, *MOD DESTINATION* F ENV → OSC 2 FREQ, F ENV *ATTACK* long et *SUSTAIN* MAX ; ou *LFO 1* → OSC 2 FREQ accéléré | *EG* TARGET PITCH, *ATTACK* long, *EG INT* fort ; *LFO* BPM → PITCH | [6][7] |
| **W6 Chute / downlifter** | note tenue 4 mesures, 4P, *CUTOFF* ≈ 2:30, *RESONANCE* ≈ midi, *EG AMOUNT* négatif et F ENV lent (le filtre se referme), *MOD AMOUNT* négatif vers OSC 2 FREQ | *EG INT* négatif sur PITCH et CUTOFF (SHIFT + INT pour inverser) | [7][9] |
| **W7 Sirène dub / alarme** | scie ou carré, *LFO 1* SAW ou RAMP → OSC 2 FREQ (le manuel ne dit pas laquelle descend : écouter), *SYNC* ON (1/1) ; LFO SQUARE pour une alarme | *LFO* SAW BPM → PITCH ; DELAY Tape avec beaucoup de feedback | [7][10] |
| **W8 Wobble** | scie + SUB, 4P, *CUTOFF* ≈ 12:30, *RESONANCE* ≈ 11:00 + RES BASS, *LFO 1* TRI → CUTOFF *SYNC* ON (croche de triolet), *DEPTH* moyen, F ENV léger | *LFO* BPM TRI → CUTOFF, *INT* moyen | [8][9][10] |
| **W9 Filtre auto-oscillant / laser** | *RESONANCE* MAX, oscillateurs à MIN (ou NOISE seul), *KB TRACKING* ON, *CUTOFF* joué comme une hauteur ; « zap » : F ENV court sur le cutoff (déduction, pas de recette publiée) | *RESONANCE* MAX, *EG* court sur CUTOFF | [1][3][10] |
| **W10 Enveloppe en boucle** | *F ENV LOOP* ON, A/D/S/R choisis pour la forme du cycle ; *A ENV LOOP* pour un trémolo à formes libres | non (pas de boucle d'EG ; *LFO* à la place) | [10] |

## 3. Diagnostic

| Symptôme | Geste |
|---|---|
| le balayage ne s'entend pas | balayer plus large ; monter la *RESONANCE* [1] |
| le filtre résonant ne fait rien sur un son statique | bouger le *CUTOFF* : il faut des harmoniques près de la coupure [1] |
| la basse perd son poids pendant la wobble | RES BASS ON [10] ; LFO qui démarre après l'attaque ou qui en coupe un autre [8][9] |
| riser sec et plat | reverb, delay, phaser [5][7] |
| riser pas en place dans le groove | sidechain de la grosse caisse (au mix) [5] |
| la montée manque d'énergie | accélérer le LFO et augmenter sa profondeur, geste enregistré à la main [7] |
| riser perdu dans le mix | shelf aigu vers 5 kHz, distorsion au sommet [5][7] |
| la sirène part dans le mauvais sens | passer de SAW à RAMP (ou SQUARE) [7] ; XD : inverser le LFO (SHIFT + INT) [10] |

## Sources

1. Paul Wiffen, « Synth School: Part 2, Resonance, Envelopes & Routing », Sound On Sound, août 1997, https://www.soundonsound.com/techniques/synth-school-part-2
2. Gordon Reid, « Modulation », Synth Secrets, Sound On Sound, février 2000, https://www.soundonsound.com/techniques/modulation
3. Gordon Reid, « Of Responses & Resonance », Synth Secrets, Sound On Sound, octobre 1999, https://www.soundonsound.com/techniques/responses-resonance
4. Gordon Reid, « Amplitude Modulation », Synth Secrets, Sound On Sound, mars 2000, https://www.soundonsound.com/techniques/amplitude-modulation
5. Jon Musgrave, « How to make synth sweep FX for EDM drops », MusicRadar, février 2023, https://www.musicradar.com/how-to/synth-sweep-fx
6. « How to produce a basic synth riser », MusicRadar / Computer Music, novembre 2012, https://musicradar.com/tuition/tech/how-to-produce-a-basic-synth-riser-566881
7. « Essential Transition FX: Technique Masterclass », Attack Magazine, août 2015, https://www.attackmagazine.com/technique/tutorials/essential-transition-fx-technique-masterclass/
8. Roland Schmidt, « How to build an LFO wobble bass », MusicRadar, juin 2024, https://musicradar.com/how-to/lfo-wobble-bass
9. Adam Douglas, « A Look At Synth Modulations For Beginners », Attack Magazine, mars 2023, https://www.attackmagazine.com/technique/tutorials/a-look-at-synth-modulations-for-beginners/
10. Manuels : `manuals/moog-messenger-user-manual.pdf` (LOOP des enveloppes, plages de LFO en CONFIG 1.4, OSC 2 → CUTOFF, auto-oscillation, RES BASS) et `manuals/minilogue-xd-user-manual.pdf` (LFO 1-SHOT / NORMAL / BPM, EG en AD avec TARGET)

Non accessibles ou non trouvés : test du Messenger par Perfect Circuit (403) ; aucun article Moog officiel sur les enveloppes en boucle ; aucune recette de laser ou de zap dans une source de qualité (seulement des forums, non retenus).
