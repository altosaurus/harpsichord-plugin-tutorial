---
title: Harpsichord plugin tutorial
parent: plugins
order: 3
permalink: /plugins/harpsichord/
---

Build a plugin for a keyboard instrument. You’ll draw a double harpsichord from a list of keyboards, ask learners to name the interval between two highlighted keys, let them choose their own range, intervals and manuals, and then add a question about the instrument’s parts, a lesson and a glossary entry. You’ll reuse the photographs and recordings from the example pack and write your own manifest.

This tutorial builds on the [viola plugin tutorial]({{ '/plugins/viola/' | relative_url }}). A keyboard needs no calibration, because Alto draws the keys itself, so you’ll spend your time on the keyboards and the settings instead.

## Working folder

Download <a href="https://github.com/altosaurus/harpsichord-plugin-tutorial/releases/latest/download/harpsichord.zip">the example harpsichord pack</a>. Find the directory that contains Alto’s database, `alto.db`, and create a `plugins` folder there if needed. See [database locations]({{ '/data/' | relative_url }}).

Inside `plugins`, create a folder named `my-keys` and extract the ZIP directly into it. Keep `CREDITS.txt` with the media. Then delete everything you won’t use yet, so the folder looks like this:

```text
my-keys/
  pack.json
  images/harpsichord-overview.webp
  sounds/C4.wav
  sounds/D4.wav
  sounds/E4.wav
  CREDITS.txt
```

## An interval exercise

Open `pack.json` in a plain-text editor and replace its contents with this manifest.

```json
{
  "format": 2,
  "id": "my-keys",
  "name": "My Keys",
  "instruments": [
    {
      "id": "studio-harpsichord",
      "name": "Studio harpsichord",
      "image": "images/harpsichord-overview.webp",
      "keyboards": [
        {"name": "Upper manual", "lowest": "E1", "highest": "F6"},
        {"name": "Lower manual", "lowest": "E1", "highest": "F6"}
      ],
      "samples": {"C4": "sounds/C4.wav", "D4": "sounds/D4.wav", "E4": "sounds/E4.wav"},
      "gain": 0.9,
      "kind": "harpsichord"
    }
  ],
  "exercises": [
    {
      "id": "intervals",
      "title": "Intervals on My Harpsichord",
      "type": "keyboard-intervals",
      "instrument": "studio-harpsichord",
      "lowest": "E1",
      "highest": "F6",
      "default_range": ["C3", "C5"],
      "intervals": ["M2", "M3", "P5"]
    }
  ]
}
```

Save and restart Alto. Open **Intervals on My Harpsichord** under **Instruments**. Alto draws both manuals, highlights two keys, and offers the three intervals as answer buttons. With the speaker on, a correct answer plays the two notes together, as a chord, on your recordings.

{% include shot.html src="plugin-harpsichord-intervals.png" alt="Harpsichord Interval Identification in Alto with two stacked manuals, highlighted keys, and interval answer buttons." caption="In Instruments → Harpsichord Interval Identification, the complete pack uses two manuals to ask the learner to identify an interval." %}

What each part does:

- **`keyboards`** lists the manuals, up to four. Each has a name, a `lowest` key and a `highest` key. Alto draws them stacked with the first one listed at the top, so list the upper manual first. The ends must be natural notes, because a keyboard can’t begin or end on a black key. Keys with the same letter and octave are the same pitch on every manual.
- **`lowest` and `highest`** on the exercise are the widest range the exercise has cards for. **`default_range`** is the range learners start with. It must fit inside the first pair.
- **`intervals`** chooses the answers from `m2`, `M2`, `m3`, `M3`, `P4`, `A4 / d5`, `P5`, `m6`, `M6`, `m7`, `M7` and `P8`. Leave it out to ask all twelve.
- **`samples`** pairs each recording with the pitch that was actually recorded. One recording is enough to start. Alto shifts it to reach the neighboring notes, so more recordings across the range keep the shift small.
- **`kind`** says what sort of instrument this is. You’ll use it later, when learners choose which instrument sounds.

Alto asks every combination of interval, lowest key and placement once. A two-manual instrument with a five-octave range has thousands of cards, which is fine, because Alto only asks the cards inside the learner’s range.

## Choose where the keys sit

An exercise can ask both keys on the same manual, one on each, or both. Add `placements` to the exercise to choose. The default is `["same", "across"]`.

```json
"placements": ["same"]
```

With `["same"]`, both highlighted keys are always on one manual. With `["across"]`, one is on each. To restrict which manuals the exercise uses, add `"keyboards": ["Lower manual"]` to the exercise. Each name must match a keyboard on the instrument.

## Choose how the keyboards look

Without `keyboard_style`, Alto draws the keys in the learner’s own keyboard style. The `keyboard_style` field on the instrument changes the look to match your instrument. Add it after `keyboards`.

```json
"keyboard_style": {
  "white": ["#4a3b30", "#241a14"],
  "black": ["#4b3b30", "#2a2019"],
  "white_edge": "#000000",
  "black_edge": "#000000",
  "case": "#120d09",
  "cap": "#eee3c8",
  "narrow": 0.95,
  "gap": 1.5,
  "round": 2,
  "length": 4.5
}
```

Colors are `#rrggbb`. `white` and `black` are each a pair of colors, for the top and the bottom of a natural or a sharp key, such as `["#4a3b30", "#241a14"]`. The numbers adjust the shape:

| Field | Effect |
| --- | --- |
| `narrow` | How wide the sharp keys are compared with a piano’s, from 0.5 to 1.5. |
| `gap` | The pixels between natural keys, from 0 to 4. |
| `round` | How much the keys’ lower corners are rounded, from 0 to 10. |
| `length` | How long a natural key is, in key widths, from 2 to 6.5. |
| `white_edge`, `black_edge`, `case`, `cap` | The outline of each kind of key, the wood around the keys, and the cap over each sharp key. |

The harpsichord example uses dark natural keys with light sharps, which is how the Ruckers instrument it pictures was built. The long, narrow keys come from a `length` of 4.5. Change the numbers, save, restart and compare. Every field is optional, and you can leave out any you don’t want to change.

## Let learners choose

Add a `settings` entry to the exercise to give learners controls. Each setting you list shows up in the exercise’s Settings panel.

```json
"settings": {
  "sound": "Harpsichord sound",
  "range": true,
  "intervals": true,
  "manuals": true
}
```

- **`range`** adds a Range page with a small draggable keyboard, and a lowest and highest key. The big keyboards redraw while it’s dragged, and a new question comes when the learner pauses.
- **`intervals`** adds a page of checkboxes. An interval too wide for the chosen range can’t be checked, and the answer buttons follow the checked intervals.
- **`manuals`** adds a page with a checkbox for each manual. If only **Upper manual** is checked, both highlighted keys are always on the upper manual. If only the lower is checked, both are on the lower. If both are checked, the keys can also be one on each.
- **`sound`** adds a row, labeled with the text you give it, that opens a list of instruments to sound. The plugin’s own instruments are first, then other instruments of the same `kind`, then everything else that’s installed. That is why you set `kind` earlier. A learner with several harpsichord plugins sees the others in the middle group. The plugin’s own sound is used until the learner picks another.

Each setting is saved for the exercise. The learner’s starting settings keep their practice history, and a changed range, interval choice or manual choice is tracked as its own set of cards.

## A picture question about the parts

A keyboard exercise draws its own keys, so it doesn’t need the photograph. You can still use the photograph in a second exercise. Add a comma after the first object in `exercises` and add this one. It marks a point on the original image and asks what part is there.

```json
{
  "id": "parts",
  "title": "Parts of My Harpsichord",
  "description": "Name the parts of the harpsichord.",
  "type": "image-choice",
  "instrument": "studio-harpsichord",
  "questions": [
    {
      "prompt": "Which part of the harpsichord is marked?",
      "point": [733, 600],
      "choices": ["Lid", "Nameboard", "Apron", "Cheek"],
      "answer": "Lid",
      "marker_size": 100,
      "focus": [250, 60, 1000, 1000]
    }
  ]
}
```

`point` is measured in pixels from the top-left corner of the original image, which is 1500 × 2250 here. `marker_size` is the diameter of the ring. `focus` is a rectangle `[x, y, width, height]` that Alto zooms to, so small parts aren’t lost in a large picture. To ask about another picture of the instrument, add it under `views` on the instrument, for example `"views": {"strings": "images/harpsichord-strings.webp"}`, and add `"view": "strings"` to the question.

{% include shot.html src="plugin-harpsichord-parts.png" alt="A blue marker sits on the upper manual in a photograph of the harpsichord, with four answer choices below." caption="In Instruments → Parts of the Harpsichord, choose the name of the part marked in blue." %}

## A lesson about intervals

A lesson walks a learner through steps, each with a picture, some text, and an optional question. A step can highlight keys on the keyboards instead of a point on a photograph. Add `lessons` after `exercises`.

```json
"lessons": [
  {
    "id": "half-and-whole",
    "title": "Half Steps and Whole Steps",
    "about": "Count the half steps between two keys on a double harpsichord.",
    "summary": "Count the steps between two keys.",
    "category": "Harpsichord",
    "exercise": "intervals",
    "steps": [
      {
        "title": "The half step",
        "picture": {
          "instrument": "studio-harpsichord",
          "keys": [["Lower manual", "C4"], ["Lower manual", "C#4"]],
          "span": ["C3", "C5"]
        },
        "text": [
          "The distance from one key to the very next key, whatever its color, is a **half step**. C4 and the sharp key just above it, C#4, are a half step apart."
        ],
        "hear": [["C4"], ["C#4"]],
        "hear_label": "Hear a half step",
        "hear_instrument": "studio-harpsichord",
        "task": {
          "prompt": "How many half steps separate C4 and D4?",
          "choices": ["1", "2", "3"],
          "answer": "2",
          "hint": "There is one key between them.",
          "explanation": "C4 to C#4 is one half step, and C#4 to D4 is another."
        }
      }
    ]
  }
]
```

- **`keys`** lists up to four `[keyboard, pitch]` pairs to highlight. **`span`** is the range of keys to draw, so the lesson shows a few octaves instead of all five.
- **`hear`** lists the notes the button plays, one after another. **`hear_instrument`** chooses the instrument. Each recorded pitch plays its own recording, and others are shifted from the nearest one.
- **`exercise`** is the exercise the last step offers for practice. An exercise can also name its lessons with `"lessons": ["half-and-whole"]`.

The example pack has two lessons: one about the parts of the instrument, and one that teaches the half step, whole step and each interval on the keys.

{% include shot.html src="plugin-harpsichord-lesson.png" alt="The half-step lesson in Alto with C4 and C-sharp highlighted on the lower manual." caption="In Lessons → Intervals on a Double Harpsichord, the half-step example places the highlighted keys next to each other on the lower manual." %}

## A glossary entry

Glossary entries explain terms in the Glossary and link them to your exercises and lessons. Add `glossary` after `lessons`.

```json
"glossary": [
  {
    "term": "double harpsichord",
    "definition": "A **double harpsichord** has two keyboards, one above the other. Each keyboard can play its own set of strings, so a player can change tone color by moving from one to the other.",
    "guide": "Look at the front of the instrument. Two rows of keys mean it is a double.",
    "picture": {"instrument": "studio-harpsichord", "marker": false},
    "caption": "The two manuals of a double harpsichord",
    "exercises": ["intervals"],
    "lessons": ["half-and-whole"]
  }
]
```

Use lowercase for the term unless it is a proper noun. Keep the definition to one concise paragraph, and use `guide` for what to look or listen for.

## Pack installation

To test the plugin you built, compress the contents of `my-keys` into `my-keys.zip`. Open the ZIP and check that `pack.json` is at its root. Move the editable folder outside Alto’s `plugins` folder so only one copy loads. Install the ZIP through **Menu → Tools → Plugins… → Install plugin from file…** and restart. Open both exercises under **Instruments**, open the lesson from **Lessons**, and look up your term in the Glossary.

If the plugin doesn’t load, **Tools → Plugins…** lists the problem. Alto names the field that’s wrong, such as a keyboard that doesn’t exist on the instrument or a range outside the keys.

## The complete harpsichord example

The original download shows the same pieces working together. Install the original `harpsichord.zip` through the Plugins dialog and restart Alto. Open **Instruments → Harpsichord Interval Identification**, open **Settings**, and try **Range**, **Intervals** and **Manuals**. Choose **Harpsichord sound** to pick another instrument.

The pack adds **Parts of the Harpsichord**, where learners name 16 marked parts across five photographs: the whole instrument, the keyboards, the strings and jacks, the bentside, and the spine. It also adds two lessons and 14 glossary entries.

The manifest fields used here are described in the [plugin API reference]({{ '/plugins/api/' | relative_url }}), including its Keyboard intervals section.

The recordings are from the Versilian Community Sample Library’s Flemish harpsichord, the 8′ register, with one take for every whole tone from F♯1 to C6. They are released under CC0, so no credit is required, though the pack gives it. For Alto, each take was trimmed to the pluck, cut to 1.6 seconds, level-matched, faded out and converted to 32 kHz mono 16-bit WAV. The recordings are of a different instrument than the pictured one. [VCSL on GitHub](https://github.com/sgossner/VCSL)

The photographs are of a double harpsichord built by Andreas Ruckers in Antwerp in 1636 and rebuilt in Paris by Pascal Taskin in 1787, from the Museum für Kunst und Gewerbe Hamburg. They were published under CC0 by Rainer Halama for Wiki Loves Music. The keyboards in the interval exercise are drawn by Alto, so they need no photograph. `CREDITS.txt` lists each file.
