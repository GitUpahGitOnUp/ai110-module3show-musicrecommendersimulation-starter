import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 1.0
ENERGY_MAX_POINTS = 2.0
ACOUSTIC_BONUS_POINTS = 1.0
ACOUSTIC_THRESHOLD = 0.6
DANCEABILITY_MAX_POINTS = 2.0

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
    wants_danceable: bool = False

def _score(genre: str, mood: str, energy: float, acousticness: float, danceability: float,
           favorite_genre: str, favorite_mood: str, target_energy: float,
           likes_acoustic: bool, wants_danceable: bool = False) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns the score with match reasons."""
    score = 0.0
    reasons = []

    if genre == favorite_genre:
        score += GENRE_MATCH_POINTS
        reasons.append(f"Matches your favorite genre ({genre})")

    if mood == favorite_mood:
        score += MOOD_MATCH_POINTS
        reasons.append(f"Matches your favorite mood ({mood})")

    energy_gap = abs(energy - target_energy)
    energy_points = max(0.0, ENERGY_MAX_POINTS * (1 - energy_gap))
    score += energy_points
    if energy_points >= 1.5:
        reasons.append(f"Energy ({energy}) is very close to your target ({target_energy})")
    elif energy_points >= 0.5:
        reasons.append(f"Energy ({energy}) is somewhat close to your target ({target_energy})")

    if likes_acoustic and acousticness >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_BONUS_POINTS
        reasons.append("You like acoustic songs, and this one leans acoustic")

    if wants_danceable:
        danceability_points = DANCEABILITY_MAX_POINTS * danceability
        score += danceability_points
        if danceability_points >= 1.5:
            reasons.append(f"Very danceable ({danceability}) - great for getting people moving")
        elif danceability_points >= 0.8:
            reasons.append(f"Fairly danceable ({danceability})")

    return score, reasons

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by score for the given user."""
        ranked = sorted(
            self.songs,
            key=lambda song: (
                -_score(
                    song.genre, song.mood, song.energy, song.acousticness, song.danceability,
                    user.favorite_genre, user.favorite_mood, user.target_energy,
                    user.likes_acoustic, user.wants_danceable,
                )[0],
                -song.danceability,
                song.id,
            ),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended to a user."""
        _, reasons = _score(
            song.genre, song.mood, song.energy, song.acousticness, song.danceability,
            user.favorite_genre, user.favorite_mood, user.target_energy,
            user.likes_acoustic, user.wants_danceable,
        )
        if not reasons:
            return "No strong matches with your preferences, but it's still in the catalog."
        return "Recommended because: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    return _score(
        song["genre"], song["mood"], song["energy"], song["acousticness"], song["danceability"],
        user_prefs["genre"], user_prefs["mood"], user_prefs["energy"],
        user_prefs["likes_acoustic"], user_prefs.get("wants_danceable", False),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No strong matches with your preferences"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: (-item[1], -item[0]["danceability"], item[0]["id"]))
    return scored[:k]
