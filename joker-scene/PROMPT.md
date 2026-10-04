# Joker Fan Film: 30s Shot-by-Shot Prompt

A 30-second fan film inspired by *Joker* (2019), starring you in the full Joker costume and makeup, speaking four of the film's best lines.

- **Format:** vertical 9:16, made as 2 × 15s generations (Part A + Part B) and edited together.
- **Model:** Higgsfield `seedance_2_0` (identity-faithful, 15s, native audio and lip-sync). It works the same way in Kling, Veo or Runway.
- **Face lock:** attach your face photo as `image_references` on **both** parts. 2–3 photos (front, 3/4 left, 3/4 right, even light, no sunglasses) hold the face much better than one.

> Fan-made tribute. Original sets, original performance, no film footage or film music. The dialogue lines are short quotes from *Joker* (2019, Warner Bros.).

## MASTER PROMPT (everything in one block)

```
30-second vertical 9:16 cinematic fan film inspired by Joker (2019). Shot on 35mm film, ARRI Alexa 35 with vintage anamorphic-look prime lenses, shallow depth of field with soft creamy bokeh. Color grade: muted green fluorescent tones, cool blue-green shadows, warm natural skin tones, soft highlight bloom and gentle halation, subtle 35mm film grain, slightly faded lifted blacks, high contrast, low saturation. Realistic motivated lighting from practical sources only. Mood: calm, melancholic, intimate, atmospheric, inspired by Wong Kar-wai and modern A24 indie cinema. Realistic skin texture with visible pores, natural subsurface scattering, real fabric movement, accurate physics, natural motion blur. Every shot belongs to the same film, with identical color grade, lighting style, wardrobe and makeup from beginning to end.

@joker: the man from the reference photo, exact same face, identity fully preserved. Adult man, 6 feet tall, lean and fit athletic build, not heavy. Makeup, identical in every shot: matte white greasepaint face base, slightly worn and cracked at the edges; sharp blue painted triangles above and below each eye; small red painted nose tip; wide red painted smile extending past the lips into the cheeks; greasy dyed-green hair slicked back with loose strands falling forward. Wardrobe, identical in every shot: rust-red two-piece suit with wide 1970s lapels, mustard-yellow vest, teal-green shirt with a wide pointed collar, no tie, worn brown leather shoes. Voice: low, soft, tired male voice, slow deliberate speech, lips perfectly synced to the dialogue.

Shot 1 (0–4s): Grimy public bathroom at night, cracked pale-green tiles, one fluorescent tube flickering softly overhead. Wide shot from behind, slow dolly push-in: @joker sits hunched on a wooden bench facing a cracked mirror, head down, shoulders rising with one slow breath. Only the hum of the light.

Shot 2 (4–9s): Over-the-shoulder into the mirror, 85mm, focus on the reflection, very slow push-in. @joker lifts his head, meets his own eyes and pushes the corners of his red-painted mouth upward with two fingers into a forced smile, then lets go. He says quietly to his reflection: "Is it just me… or is it getting crazier out there?"

Shot 3 (9–15s): Medium-wide, slow 90-degree gimbal arc around him. @joker rises and dances slowly and gracefully under the flickering green light, arms opening wide, head tilted back, eyes half closed, jacket swinging naturally. He stops and faces the lens in a tight 50mm close-up, light flickering across his face, and whispers: "All I have… are negative thoughts."

Shot 4 (15–20s): Empty late-night subway car, sickly green fluorescent light, dark tunnel rushing past the window and throwing warm light streaks across his face. Medium close-up, 50mm, handheld with subtle natural sway from the moving train. @joker sits alone by the window, head resting against the glass, then slowly turns his eyes to the lens and says flatly: "For my whole life, I didn't know if I even really existed."

Shot 5 (20–25s): Long, steep outdoor concrete staircase between old brick apartment buildings at overcast dusk, cool muted green-grey light, damp steps, a few warm windows glowing. Low-angle wide from the bottom of the stairs, slow crane-down and tilt-up. @joker dances down the stairs with total confidence, arms raised, hips swaying, sharp rhythmic steps, jacket flaring, one leg kicking out on a step. Full body, real weight on every step.

Shot 6 (25–30s): Same staircase, @joker stops on a step. Close-up, 85mm, very slow push-in, warm window bokeh behind him. Calm and still, he says: "I used to think my life was a tragedy… but now I realize, it's a comedy." A small, slow, chilling smile spreads under the painted smile. Hold on his eyes.

NEGATIVE: cartoon, illustration, 3D render, CGI, plastic skin, over-smooth skin, waxy, airbrushed, distorted face, identity change, deformed hands, extra fingers, warped proportions, oversaturated, HDR look, AI-style rendering, watermark, subtitles, text, logo.
```

> Most video models generate at most 15s per run. If yours cuts off, run Shots 1–3 and Shots 4–6 as two separate generations, keeping the full header, @joker block and negative in each. Those two halves are the PART A and PART B prompts below.

## The dialogues (in order)

| Time | Line | Delivery |
|------|------|----------|
| 4–9s | "Is it just me… or is it getting crazier out there?" | quiet, to his own reflection |
| 12–15s | "All I have… are negative thoughts." | whisper, straight into the lens |
| 15–20s | "For my whole life, I didn't know if I even really existed." | flat and tired, then a slow turn to camera |
| 25–30s | "I used to think my life was a tragedy… but now I realize, it's a comedy." | calm, then a small, chilling smile |

---

## STYLE HEADER (paste at the top of both parts)

```
Shot on 35mm film, ARRI Alexa 35 with vintage anamorphic-look prime lenses, shallow depth of field with soft creamy bokeh. Muted green fluorescent tones, cool blue-green shadows, warm natural skin tones, soft highlight bloom and gentle halation, subtle 35mm film grain, slightly faded lifted blacks, high contrast, low saturation. Realistic, motivated cinematic lighting from practical sources only. Mood: calm, melancholic, intimate, atmospheric, inspired by Wong Kar-wai and modern A24 indie cinema. Realistic skin texture with visible pores, natural subsurface scattering, real fabric movement, accurate physics, natural motion blur. Every shot belongs to the same film: identical color grade, lighting style, wardrobe and makeup from start to finish. Vertical 9:16.
```

## SUBJECT (paste right under the header in both parts)

```
@joker — the man from the reference photo, exact same face, identity preserved. Adult man, 6 feet tall, lean and fit athletic build, not heavy. Makeup (identical every shot): matte white greasepaint face base, slightly worn and cracked at the edges; sharp blue painted triangles above and below each eye; small red painted nose tip; wide red painted smile extending past the lips into the cheeks; greasy dyed-green hair slicked back with loose strands falling forward. Wardrobe (identical every shot): rust-red two-piece suit with wide 1970s lapels, mustard-yellow vest, teal-green shirt with a wide pointed collar, no tie, worn brown leather shoes. Low, soft, tired male voice; slow, deliberate speech; lips perfectly synced to the dialogue.
```

---

## PART A (0–15s): the bathroom

```
[STYLE HEADER]
[SUBJECT]

Shot 1 (0–4s): Grimy public bathroom at night, cracked pale-green tiles, a single fluorescent tube above flickering softly. Wide shot from behind, slow dolly push-in on a static track: @joker sits hunched on a wooden bench facing a cracked mirror, head down, shoulders rising with one slow breath. Only the hum of the light.

Shot 2 (4–9s): Over-the-shoulder into the mirror, 85mm lens, focus on the reflection, very slow push-in. @joker lifts his head, meets his own eyes in the glass and pushes the corners of his red-painted mouth upward with two fingers into a forced smile, then lets go. He says quietly to his reflection: "Is it just me… or is it getting crazier out there?"

Shot 3 (9–15s): Medium-wide, camera on a slow 90-degree gimbal arc around him. @joker rises and begins a slow, graceful, fluid dance under the flickering green light, arms opening wide, head tilted back, eyes half closed, the suit jacket swinging naturally. He stops and faces the lens in a tight 50mm close-up, light flickering across his face, and whispers: "All I have… are negative thoughts."

NEGATIVE: cartoon, illustration, 3D render, CGI, plastic skin, over-smooth skin, waxy, airbrushed, distorted face, identity change, deformed hands, extra fingers, warped proportions, oversaturated, HDR look, AI-style rendering, watermark, subtitles, text, logo.
```

## PART B (15–30s): the subway and the stairs

```
[STYLE HEADER]
[SUBJECT]

Shot 4 (15–20s): Empty late-night subway car, sickly green fluorescent light, dark tunnel rushing past the window and throwing warm streaks of light across his face. Medium close-up, 50mm, handheld with a subtle natural sway from the moving train. @joker sits alone by the window, head resting against the glass, then slowly turns his eyes to the lens and says flatly: "For my whole life, I didn't know if I even really existed."

Shot 5 (20–25s): A long, steep outdoor concrete staircase between old brick apartment buildings at overcast dusk, cool muted green-grey ambient light, damp steps, a few warm windows glowing. Low-angle wide shot from the bottom of the stairs, slow crane-down and tilt-up. @joker dances down the stairs with total confidence, arms raised, hips swaying, sharp rhythmic steps, suit jacket flaring, one leg kicking out on a step. Full body, natural motion, real weight on every step.

Shot 6 (25–30s): Same staircase, @joker stops on a step. Close-up, 85mm, very slow push-in, background bokeh of the warm windows. Calm and still, he says: "I used to think my life was a tragedy… but now I realize, it's a comedy." Then a small, slow, chilling smile spreads under the painted smile. Hold on his eyes.

NEGATIVE: cartoon, illustration, 3D render, CGI, plastic skin, over-smooth skin, waxy, airbrushed, distorted face, identity change, deformed hands, extra fingers, warped proportions, oversaturated, HDR look, AI-style rendering, watermark, subtitles, text, logo.
```

---

## Making it look like one film

- Generate **Part A first**. Take the cleanest close-up frame of your face in makeup from it, and attach that frame as a **second** `image_reference` for Part B. This keeps the makeup and suit identical.
- If the face drifts in a multi-shot part, generate each shot separately (4–6s each) with the same header, subject and references, then stitch them.
- If a line comes out mis-synced, regenerate only that shot. Don't regenerate the whole part.
- **Music in the edit:** a low, slow cello drone under Part A, building through the subway, then a heavy stomping drum beat when the stairs dance starts (20s). Don't use the film's actual score or its stairs song, because Instagram and YouTube will mute or claim the video.
