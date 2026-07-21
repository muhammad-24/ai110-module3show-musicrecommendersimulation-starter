# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

​
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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



