# Leads mono : principes et blueprints

Leads de monophonique (Moog Messenger d'abord) : leads Moog chantants, glide, sync, sifflets, leads piqués. Sources lues en entier [1-11], recherche du 2026-10-18. Positions Messenger en heures (7 = MIN, 17 = MAX). Les recettes publiées sont faites sur d'autres synthés (Minimoog, Prophet, plug-ins ; Syntorial les dit « approximatives, à l'oreille ») : les valeurs ci-dessous sont des départs. Calage du filtre du Messenger : voir `08-basses.md` (le corps d'une basse est vers 1:00-2:00 ; un lead se règle plus haut).

## 1. Principes

**Mono et legato.** Un lead se joue en mono pour profiter du glide et d'enveloppes non redéclenchées [6][7]. Le Minimoog : priorité à la note grave, déclenchement simple [2] (c'est le comportement par défaut du Messenger, `machines/messenger.md`). Un glide legato ne part que si les notes se chevauchent [8].

**Oscillateurs.** Formes « tranchantes » : scie, carré, PWM, sync ; sinus et triangle pour les leads doux, sifflés, thérémine [6]. Une scie seule suffit souvent [1][9]. OSC 2 une octave au-dessus et plus bas au mixer (0,4 contre 0,17) [7]. Désaccord léger, quelques cents (±1 à +5) [7][10].

**Pas de sub, ou très peu.** Il alourdit et entre en conflit avec la basse et la grosse caisse ; couper sous ≈ 150 Hz [6] ; sub très bas, ou supprimé si l'arrangement est chargé [7].

**Saturation d'entrée.** Sur le Minimoog, au-delà de 5/10 au mixer, les oscillateurs saturent le filtre : 5 pour un son propre, plus pour du grain [1]. Le mixer du Messenger ne sature pas (`machines/messenger.md`) : le grain vient de *FB / EXT IN*. Un peu de drive donne du mordant et compresse [6] ; Jan Hammer passait par un ampli guitare saturé pour percer [4].

**Filtre.** Moins de pôles = plus doux ; un peu de résonance « siffle » bien, trop agresse [6] (vers 2/10 [1], 32 % [9], 60 % pour un lead 70s [7]). **Suivi de clavier à 100 %** pour garder le timbre sur toute la tessiture [1] : sur le Messenger, *KB TRACKING* ON (1:1).

**Enveloppe de filtre.** Elle ouvre le filtre à chaque note : attaque rapide pour du piqué, plus lente pour un son « rêveur » [9]. Exemple Reid (cuivre au Minimoog) : cutoff fermé, AMOUNT 6,5/10, A 600 ms, D 800 ms, S 5/10 [1].

**Enveloppe d'ampli.** « Orgue » dans la plupart des recettes : A 0, S 100 %, R court (≈ 20 ms) [10]. Une attaque vers 100 ms donne un son « soufflé » [1].

**Glide.** Le GLIDE du Minimoog est un portamento [11]. En linéaire à temps constant, la durée ne dépend pas de l'intervalle [9][11]. Valeurs relevées : ≈ 80 ms (Nutbush) [8], 70 ms (Lucky Man), 30 ms, 10 ms [10]. Plus l'intervalle est grand, plus il s'entend [9]. Messenger : *GLIDE* (main gauche) + CONFIG 1.3 (PGM 1 legato, PGM 2 gated ; PGM 14 exponentiel, 15 linéaire vitesse constante, 16 linéaire temps constant).

**Vibrato et pitch bend.** Vibrato dosé à la mod wheel, pas fixe [3][7] ; LFO lent qui balaie le filtre (0,1-0,15 Hz) [3][7]. Pitch bend « comme un violoniste », sur plus de 2 demi-tons (Hammer : une quarte) [4][5] ; le Messenger est à ±7 demi-tons par défaut. Messenger : *LFO 2* (triangle) vers PITCH, dosé par la *MOD WHEEL*.

**Sync.** On n'entend que l'oscillateur synchronisé ; une enveloppe balaie sa hauteur (19 demi-tons, decay 3,9 s pour The Cars) [10]. Messenger : *SYNC 1→2*, OSC 2 seul au mixer, *MOD DESTINATION* F ENV → OSC 2 FREQ.

**FM.** FM rapide pour un « sifflet buzzy » [10] ; cross-modulation à 65 % pour l'agressivité [7]. Messenger : 1+2 FM, *MOD AMOUNT*.

**Effets.** Delay et réverb avec modération (ils éloignent le lead), graves de l'effet coupés [6] ; delay à la croche, feedback 15 %, mix 7 % [7] ; plate en wet bas [9]. Penser mono sur scène [6].

## 2. Blueprints Messenger

| Blueprint | Oscillateurs | Mixer | Filtre | Env. filtre | Env. ampli | Jeu, glide, modulations | Source |
|---|---|---|---|---|---|---|---|
| **L1 Lead Moog chantant 70s** | 2 scies, OSC 2 en 4' (une octave au-dessus) et OSC 2 FREQ ≈ 12:03 | OSC 1 MAX, OSC 2 ≈ 11:00 | 4P, *CUTOFF* ≈ 2:00, *RESONANCE* ≈ 1:00, *KB TRACKING* ON, *EG AMOUNT* +20 % | A ≈ 7:30, D long (≈ 1:00), S ≈ midi | A ≈ 7:15, S ≈ 3:30, R ≈ 11:00 | *GLIDE* court en legato (CONFIG 1.3 PGM 1), vibrato *LFO 2* → PITCH à la molette, *LFO 1* très lent → CUTOFF faible | [7] |
| **L2 Glide legato « Nutbush »** | scie 8' | OSC 1 MAX | 4P, *CUTOFF* ≈ 2:30, *KB TRACKING* ON | à l'oreille | orgue (A MIN, S MAX, R court) | *GLIDE* ≈ 80 ms, legato, notes chevauchées | [8] |
| **L3 Lucky Man** (ELP) | 2 carrés (*WAVESHAPE* ≈ 1:15), OSC 2 FREQ ≈ 12:10 (≈ 17 cents) | OSC 1 et 2 ≈ MAX | 4P, *CUTOFF* ≈ 3:30, *KB TRACKING* ON | *EG AMOUNT* à midi | orgue, R très court | *GLIDE* ≈ 70 ms en legato ; petite réverb externe | [10] |
| **L4 Sifflet G-funk** (Dr Dre) | 2 scies (OSC 2 FREQ ≈ 12:01) ou triangle | OSC 1 MAX, OSC 2 ≈ 2:00 | 4P ou 2P, *CUTOFF* ≈ 3:00 | A très lent, S MAX, *EG AMOUNT* +10 % | orgue | *GLIDE* très court (≈ 10 ms) en legato, vibrato à la molette | [10] |
| **L5 Lead sync new wave** (The Cars) | OSC 1 maître, OSC 2 pulse (*WAVESHAPE* ≈ 3:00) à +9 demi-tons, *SYNC 1→2* ON | OSC 2 seul | 4P, *CUTOFF* ≈ 3:30 | *MOD DESTINATION* F ENV → OSC 2 FREQ, *MOD AMOUNT* fort, F ENV A MIN, D très long, S MIN | orgue | vibrato à la molette | [10] |
| **L6 Lead rock façon Hammer** | scie (+ carré 4') | OSC 1 MAX | 4P, *CUTOFF* ≈ 3:00, *RESONANCE* ≈ 11:00 | *EG AMOUNT* +20 % | orgue | *FB / EXT IN* ≈ 2:00 (saturation), pitch bend joué, vibrato à la main | [4][5] |
| **L7 Lead feedback / saturé** | scie + carré 4' (OSC 2 FREQ ≈ 12:04), FM 1+2 ≈ 1:00, SUB carré bas | OSC 1 MAX, OSC 2 ≈ 1:00, SUB ≈ 8:00 | 4P, *CUTOFF* ≈ 1:00, *RESONANCE* ≈ 1:00, *EG AMOUNT* +40 % | A ≈ 7:15, D long, S ≈ midi | à l'oreille | *FB / EXT IN* ≈ 2:30, *LFO 1* lent → CUTOFF | [7] |
| **L8 Lead piqué pop** (Popcorn) | pulse en registre aigu (OCTAVE 4') | OSC 1 MAX | 4P, *CUTOFF* ≈ 2:30, *KB TRACKING* ON | *EG AMOUNT* faible | A MIN, D très court, S MIN | pas de réverb, pas de glide | [10] |

Autres recettes relevées : Gary Numan (scie, cutoff 80 %, keytrack 50 %, chorus et grande réverb) et Rockit (scie 70 % + pulse 30 %, keytrack 100 %, attaque 10 ms) [10].

## 3. Diagnostic

| Symptôme | Geste |
|---|---|
| lead boueux, masque la basse | SUB à MIN, OCTAVE plus haut ; au mix, couper sous ≈ 150 Hz [6][7] |
| lointain, noyé | moins de réverb et de delay, graves de l'effet coupés [6] |
| strident | *RESONANCE* plus bas, passer en 2P [6] |
| terne, sans mordant | *FB / EXT IN* (saturation) [4][6] ; plus d'*EG AMOUNT* [1][7] ; *CUTOFF* plus haut |
| le timbre change selon le registre | *KB TRACKING* ON [1] |
| le glide ne se déclenche pas | jouer legato en chevauchant les notes [8] ; vérifier CONFIG 1.3 [11] |
| notes en retard en jeu rapide | priorité au grave : relâcher la note précédente plus tôt [2] |
| son statique | vibrato à la molette, *LFO 1* lent sur le *CUTOFF* [3][7] |

## Sources

1. Gordon Reid, « Brass Synthesis On A Minimoog », Synth Secrets, Sound On Sound, juin 2001, https://www.soundonsound.com/techniques/brass-synthesis-minimoog
2. Gordon Reid, « Priorities & Triggers », Synth Secrets, Sound On Sound, octobre 2000, https://www.soundonsound.com/techniques/priorities-triggers
3. Gordon Reid, « Modulation », Synth Secrets, Sound On Sound, février 2000, https://www.soundonsound.com/techniques/modulation
4. « Jan Hammer » (interview), Sound On Sound, https://www.soundonsound.com/people/jan-hammer
5. « Jan Hammer Interview: Mahavishnu, Miami Vice and More », Synthtopia, octobre 2004, https://synthtopia.com/?p=291
6. Adam McLellan, « Anatomy Of A Synth Lead Patch », Sonicstate, septembre 2013, https://sonicstate.com/news/2013/09/06/blog-anatomy-of-a-lead-patch/
7. Lasse Eilers, Michael Geisel, « Synthesizer und Sounddesign #8 : Leadsounds », Bonedo, juillet 2021, https://www.bonedo.de/artikel/synthesizer-und-sounddesign-8-leadsounds
8. Dave Clews, « Legato Synths: Glide, Slide & Portamento », Attack Magazine, novembre 2015, https://www.attackmagazine.com/technique/passing-notes/legato-synths-glide-slide-portamento/
9. « Analogue Portamento Lead with U-he Diva », Attack Magazine, octobre 2015, https://www.attackmagazine.com/technique/synth-secrets/analogue-portamento-lead-with-u-he-diva/
10. Recettes Syntorial (valeurs approximatives selon leurs auteurs) : Lucky Man https://www.syntorial.com/preset-recipe/emerson-lake-and-palmer-lucky-man-lead/ ; From the Beginning https://www.syntorial.com/preset-recipe/emerson-lake-and-palmer-from-the-beginning-lead ; Nuthin' but a G Thang https://www.syntorial.com/preset-recipe/dr-dre-nuthin-but-a-g-thang-lead ; Let's Go https://www.syntorial.com/preset-recipe/the-cars-lets-go-lead ; Are Friends Electric https://www.syntorial.com/preset-recipe/gary-numan-are-friends-electric-lead/ ; Rockit https://www.syntorial.com/preset-recipe/herbie-hancock-rockit-lead/ ; Popcorn https://www.syntorial.com/preset-recipe/hot-butter-popcorn-lead
11. Dave Crombie, « Guide to Electronic Music Techniques (Part 5): From One Note to the Next », Electronics & Music Maker, juillet 1983 (archive mu:zines), https://www.muzines.co.uk/articles/guide-to-electronic-music-techniques/6082

Non accessibles : Reverb.com « The synth sounds of 5 classic Minimoog tracks » (403) ; Computer Music « Step by step » Minimonsta (PressReader, 403) ; aucune interview Keyboard de Hammer, Emerson, Wakeman, Corea, Worrell ou Hancock trouvée sur mu:zines. Non vérifiés (forums) : balayage de sync de Hammer à la pédale pour Miami Vice.
