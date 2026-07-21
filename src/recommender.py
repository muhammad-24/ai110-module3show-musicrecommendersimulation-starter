import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Scores a single Song object against a UserProfile, returning score and reasons."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_gap = abs(song.energy - user.target_energy)
        energy_points = max(0.0, 1.0 - energy_gap)
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
            reasons.append("acoustic bonus (+0.5)")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song against the user profile and returns the top k Song objects, highest first."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)
        return [song for song, score in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song scored the way it did for this user."""
        score, reasons = self._score(user, song)
        return f"Score: {score:.2f} — " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs
def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences, returning score and reasons."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_gap = abs(song["energy"] - user_prefs["energy"])
    energy_points = max(0.0, 1.0 - energy_gap)
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    return score, reasons
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Scores every song against user preferences and returns the top k, sorted highest first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]