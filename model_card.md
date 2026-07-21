# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeMatch 1.0

---

## 2. Intended Use

This is a classroom simulation, not a production system. It's designed
to show how a simple content-based recommender turns song attributes
and a taste profile into a ranked list. It assumes the user can state
their preferences directly (favorite genre, favorite mood, target
energy) rather than inferring taste from listening history.

---

## 3. How the Model Works

Every song has attributes like genre, mood, and energy. A user profile
states what genre, mood, and energy level they prefer. The system goes
through every song in the catalog one at a time and gives it points:
2 points if the genre matches exactly, 1 point if the mood matches
exactly, and up to 1 more point based on how close the song's energy
is to the user's target energy (closer energy means more points, exact
match means the full point). After every song has a score, the list is
sorted from highest to lowest, and the top 5 are shown to the user
along with the reasons for their score.

---

## 4. Data

The catalog has 16 songs across 12 genres (pop, lofi, rock, ambient,
jazz, synthwave, indie pop, folk, punk, rnb, electropop, edm). Each
song has: genre, mood, energy, tempo_bpm, valence, danceability, and
acousticness, all on a 0.0-1.0 scale except tempo_bpm. Most genres
only have 1-2 songs, so there isn't much variety within any single
genre. There's no listening history, lyrics, or audio data — just
these hand-labeled attributes.

---

## 5. Strengths

The scorer gives sensible, explainable results for "normal" taste
profiles that match real combinations in the dataset — Happy Pop
correctly surfaced Sunrise City, and Chill Lofi correctly surfaced
Library Rain. The reasons list makes it clear why each song ranked
where it did, which is more transparent than a black-box score.

---

## 6. Limitations and Bias

The system does not know when it has no good match. In the adversarial
test (genre=edm, mood=sad, energy=0.9), it still confidently returned
a top pick even though no song in the catalog is both high-energy and
"sad" — mood contributed 0 points to every single result, but the
score still looked "normal."

Genre matching is exact-string only, so close genres don't get partial
credit. "Pop" and "indie pop" are conceptually similar but score
identically to "pop" vs "rock" (zero points) unless the string matches
exactly. This likely under-ranks songs that are a good vibe match but
technically a different genre label.

The weight-shift experiment showed the ranking is sensitive to
arbitrary design choices. Doubling energy's weight and halving genre's
weight changed the top 5 order (Rooftop Lights and Electric Bloom beat
Gym Hero under the new weights, despite no genre match). This means
"the recommendation" isn't objective — it reflects whichever weights
the engineer picked.

The dataset is only 16 songs across 12 genres, so most genres have
just 1-2 songs. A user whose favorite genre only has one song will
almost always get that one song recommended regardless of mood/energy
fit, simply because there's nothing else to compete with it — this is
a small-scale version of a filter bubble.

tempo_bpm and energy are highly correlated in this dataset, so even
though tempo isn't used directly in scoring, energy alone is already
capturing most of that signal — adding tempo to future scoring could
double-count it.

---

## 7. Evaluation

Tested three user profiles:

1. **Happy Pop** (genre=pop, mood=happy, energy=0.8) → top pick was
   Sunrise City, a direct genre+mood+energy match. Matched intuition.

2. **Chill Lofi** (genre=lofi, mood=chill, energy=0.35) → top pick was
   Library Rain, again a clean match. Confirms the scorer works well
   across very different taste profiles, not just pop.

3. **Adversarial** (genre=edm, mood=sad, energy=0.9) → top pick was
   Bass Drop Riot, but only on genre + energy. No song in the catalog
   is both high-energy and "sad," so mood contributed 0 points to
   every result. The system still confidently returned a "best" pick
   even though nothing actually matched the mood.

What surprised me: the recommender doesn't know when it doesn't have
a good answer. A real match (Happy Pop) and a nonsense match
(EDM+Sad) both get displayed the same confident way — there's no
signal in the output that tells the user "this fit poorly."

Comparison: Happy Pop and Chill Lofi landed on intuitive top picks
because their profiles describe real combinations in the dataset.
The adversarial profile broke that pattern — mood silently dropped
out and genre + energy carried the whole ranking.

I also ran a weight-shift experiment: doubling energy's weight and
halving genre's weight on the Happy Pop profile. Sunrise City stayed
#1 either way, but Rooftop Lights and Electric Bloom (no genre match,
good mood/energy fit) jumped above Gym Hero (genre match, wrong mood)
under the new weights. This confirmed the ranking is sensitive to
weight choices, not just the underlying data.

---

## 8. Future Work

- Give partial credit for related genres instead of requiring an exact
  string match (e.g. "pop" and "indie pop" should share some points).
- Add a "confidence" indicator so the system can tell the user when no
  song is really a good match, instead of always returning a top 5.
- Add more songs per genre so recommendations aren't dominated by
  whichever genre only has one entry in the catalog.

---

## 9. Personal Reflection

The biggest learning moment was realizing how much the "correct"
answer depends on arbitrary weight choices — when I doubled the energy
weight and halved the genre weight, the ranking order actually
changed. That made it clear these systems aren't discovering some
objective truth about taste, they're just executing whatever weights
an engineer picked. Using AI help was fastest for writing the
boilerplate CSV loading and sorting logic, but I had to double check
the actual scoring math myself, since it's easy for weights to look
reasonable but produce results that don't match real intuition (like
the EDM+Sad test, where the system still confidently returned a "best"
song even though nothing in the catalog was a good fit). What
surprised me is how convincing a simple weighted-sum can feel even
though it's just addition — the "reasons" list makes it feel like
real reasoning even though it's just arithmetic.