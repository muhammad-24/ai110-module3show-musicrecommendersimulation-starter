# 🎵 Music Recommender Simulation

## Project Summary

This version simulates a content-based music recommender. Given a
user's favorite genre, favorite mood, and target energy level, it
scores every song in a 16-song catalog and returns the top 5 matches
with plain-language reasons for each score.

---

## How The System Works

Real platforms like Spotify use two main approaches. Collaborative
filtering predicts what you'll like based on what similar users liked
(e.g. "people who liked X also liked Y"), using no info about the song
itself. Content-based filtering predicts what you'll like based on the
song's own attributes (genre, tempo, energy, mood) compared to your
taste profile. Most real systems combine both; collaborative filtering
handles discovery and cold start, content-based handles fine-grained
"vibe" matching.

This simulation is a content-based recommender only. It has no
knowledge of other users — it only compares song attributes to a
single taste profile.

**Song features used:** genre, mood, energy, tempo_bpm, valence,
danceability, acousticness

**UserProfile features used:** favorite genre, favorite mood, target
energy

**Scoring:** each song gets +2.0 for a genre match, +1.0 for a mood
match, and up to +1.0 more based on how close its energy is to the
user's target energy (full points at 0 gap, scaling down as the gap
grows).

**Ranking:** every song in the catalog is scored this way, then sorted
highest score to lowest, and the top k are returned as recommendations.

**Expected bias:** this system relies on exact genre-string matching,
so it may under-rank songs that are a good vibe fit but labeled with
a different (though related) genre — e.g. "pop" and "indie pop" score
as a complete mismatch even though they're musically close.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
```

2. Install dependencies

```bash
   pip install -r requirements.txt
```

3. Run the app:

```bash
   python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Top recommendations:
Sunrise City - Score: 3.98
Because: ['genre match (+2.0)', 'mood match (+1.0)', 'energy closeness (+0.98)']
Gym Hero - Score: 2.87
Because: ['genre match (+2.0)', 'energy closeness (+0.87)']
Rooftop Lights - Score: 1.96
Because: ['mood match (+1.0)', 'energy closeness (+0.96)']
Electric Bloom - Score: 1.90
Because: ['mood match (+1.0)', 'energy closeness (+0.90)']
Night Drive Loop - Score: 0.95
Because: ['energy closeness (+0.95)']

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Doubled the weight on energy closeness (1.0 → 2.0) and halved the
genre match weight (2.0 → 1.0) for the Happy Pop profile. Sunrise
City stayed #1 either way, but songs with no genre match and good
mood/energy fit (Rooftop Lights, Electric Bloom) jumped above Gym
Hero, which had a genre match but the wrong mood. This showed the
ranking is sensitive to weight choices, not just the underlying data.

---

## Limitations and Risks

- Works on a tiny catalog (16 songs), so most genres have only 1-2
  entries, limiting real variety in results.
- Genre matching is exact-string only — no partial credit for related
  genres like "pop" vs "indie pop."
- Has no concept of low confidence — it always returns a top 5 even
  when no song is really a good match (see the EDM+Sad test in
  model_card.md).
- Does not use lyrics, audio, or listening history — only hand-labeled
  attributes.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project showed how a recommender turns raw data into a
prediction: it's really just arithmetic (point additions and sorting)
dressed up as "taste understanding." The scoring weights are design
choices, not objective truths — changing them changed the ranking
without changing the underlying data at all. Bias shows up in what the
system can't express: it has no way to say "I don't have a good match
for you," and its exact-string genre matching means musically similar
but differently-labeled songs get treated as complete mismatches.


