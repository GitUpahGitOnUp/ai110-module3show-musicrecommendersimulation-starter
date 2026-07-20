import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_MATCH_POINTS = 1.0
MOOD_MATCH_POINTS = 1.0
ENERGY_MAX_POINTS = 2.0
ACOUSTIC_BONUS_POINTS = 1.0
ACOUSTIC_THRESHOLD = 0.6
DANCEABILITY_MAX_POINTS = 2.0
ARTIST_REPEAT_PENALTY = 1.5
GENRE_REPEAT_PENALTY = 0.5

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
    mood: List[str]
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

def _score(genre: str, mood: List[str], energy: Optional[float], acousticness: float, danceability: float,
           favorite_genre: str, favorite_mood: str, target_energy: Optional[float],
           likes_acoustic: bool, wants_danceable: bool = False,
           genre_weight: float = GENRE_MATCH_POINTS, mood_weight: float = MOOD_MATCH_POINTS,
           energy_weight: float = ENERGY_MAX_POINTS, acoustic_weight: float = ACOUSTIC_BONUS_POINTS,
           danceability_weight: float = DANCEABILITY_MAX_POINTS) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns the score with match reasons.

    The weight_* args let a RankingStrategy emphasize different factors without
    duplicating the matching logic.
    """
    score = 0.0
    reasons = []

    if genre == favorite_genre:
        score += genre_weight
        reasons.append(f"Matches your favorite genre ({genre})")

    if favorite_mood in mood:
        score += mood_weight
        reasons.append(f"Matches your favorite mood ({favorite_mood})")

    if energy is not None and target_energy is not None:
        energy_gap = abs(energy - target_energy)
        energy_points = max(0.0, energy_weight * (1 - energy_gap))
        score += energy_points
        if energy_points >= energy_weight * 0.75:
            reasons.append(f"Energy ({energy}) is very close to your target ({target_energy})")
        elif energy_points >= energy_weight * 0.25:
            reasons.append(f"Energy ({energy}) is somewhat close to your target ({target_energy})")

    if likes_acoustic and acousticness >= ACOUSTIC_THRESHOLD:
        score += acoustic_weight
        reasons.append("You like acoustic songs, and this one leans acoustic")

    if wants_danceable:
        danceability_points = danceability_weight * danceability
        score += danceability_points
        if danceability_points >= danceability_weight * 0.75:
            reasons.append(f"Very danceable ({danceability}) - great for getting people moving")
        elif danceability_points >= danceability_weight * 0.4:
            reasons.append(f"Fairly danceable ({danceability})")

    return score, reasons

class RankingStrategy:
    """
    Base class for a pluggable ranking algorithm (Strategy pattern).
    Subclasses tune the relative weights of genre, mood, and energy matches;
    `score()` defers the actual matching rules to `_score()` so they stay in one place.
    """
    name = "balanced"
    genre_weight = GENRE_MATCH_POINTS
    mood_weight = MOOD_MATCH_POINTS
    energy_weight = ENERGY_MAX_POINTS
    acoustic_weight = ACOUSTIC_BONUS_POINTS
    danceability_weight = DANCEABILITY_MAX_POINTS

    def score(self, genre: str, mood: List[str], energy: Optional[float], acousticness: float,
              danceability: float, favorite_genre: str, favorite_mood: str,
              target_energy: Optional[float], likes_acoustic: bool,
              wants_danceable: bool = False) -> Tuple[float, List[str]]:
        return _score(
            genre, mood, energy, acousticness, danceability,
            favorite_genre, favorite_mood, target_energy,
            likes_acoustic, wants_danceable,
            genre_weight=self.genre_weight,
            mood_weight=self.mood_weight,
            energy_weight=self.energy_weight,
            acoustic_weight=self.acoustic_weight,
            danceability_weight=self.danceability_weight,
        )

class BalancedStrategy(RankingStrategy):
    """The original, unweighted scoring rule."""
    name = "balanced"

class GenreFirstStrategy(RankingStrategy):
    """Prioritizes matching the user's favorite genre above all else."""
    name = "genre-first"
    genre_weight = GENRE_MATCH_POINTS * 3
    mood_weight = MOOD_MATCH_POINTS * 0.5

class MoodFirstStrategy(RankingStrategy):
    """Prioritizes matching the user's favorite mood tag above all else."""
    name = "mood-first"
    mood_weight = MOOD_MATCH_POINTS * 3
    genre_weight = GENRE_MATCH_POINTS * 0.5

class EnergyFocusedStrategy(RankingStrategy):
    """Prioritizes how closely a song's energy matches the user's target energy."""
    name = "energy-focused"
    energy_weight = ENERGY_MAX_POINTS * 2
    genre_weight = GENRE_MATCH_POINTS * 0.5
    mood_weight = MOOD_MATCH_POINTS * 0.5

STRATEGIES: Dict[str, RankingStrategy] = {
    strategy.name: strategy
    for strategy in (BalancedStrategy(), GenreFirstStrategy(), MoodFirstStrategy(), EnergyFocusedStrategy())
}

@dataclass
class _ScoredCandidate:
    """A song already scored against a user, pending diversity re-ranking."""
    item: object
    score: float
    reasons: List[str]
    artist: str
    genre: str
    danceability: float
    id: int

def _rank_with_diversity(candidates: List[_ScoredCandidate], k: int) -> List[_ScoredCandidate]:
    """
    Greedily builds a top-k list, penalizing candidates whose artist or genre
    is already present among the picks made so far. This keeps one artist (or
    genre) from dominating the results even if they score highest overall.
    Each repeated occurrence deepens the penalty, so a third song by the same
    artist is pushed down further than the second.
    """
    remaining = list(candidates)
    selected: List[_ScoredCandidate] = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    while remaining and len(selected) < k:
        def rank_key(candidate: _ScoredCandidate):
            penalty = (
                artist_counts.get(candidate.artist, 0) * ARTIST_REPEAT_PENALTY
                + genre_counts.get(candidate.genre, 0) * GENRE_REPEAT_PENALTY
            )
            return (-(candidate.score - penalty), -candidate.danceability, candidate.id)

        remaining.sort(key=rank_key)
        chosen = remaining.pop(0)

        penalty = (
            artist_counts.get(chosen.artist, 0) * ARTIST_REPEAT_PENALTY
            + genre_counts.get(chosen.genre, 0) * GENRE_REPEAT_PENALTY
        )
        if penalty > 0:
            chosen.reasons = chosen.reasons + [
                f"Diversity penalty applied (-{penalty:.2f}) for repeating an artist/genre already recommended"
            ]

        selected.append(chosen)
        artist_counts[chosen.artist] = artist_counts.get(chosen.artist, 0) + 1
        genre_counts[chosen.genre] = genre_counts.get(chosen.genre, 0) + 1

    return selected

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], strategy: Optional[RankingStrategy] = None):
        self.songs = songs
        self.strategy = strategy or BalancedStrategy()

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Returns the top k songs ranked by score for the given user, with a
        diversity penalty so one artist or genre can't dominate the list.
        """
        candidates = [
            _ScoredCandidate(
                item=song,
                score=self.strategy.score(
                    song.genre, song.mood, song.energy, song.acousticness, song.danceability,
                    user.favorite_genre, user.favorite_mood, user.target_energy,
                    user.likes_acoustic, user.wants_danceable,
                )[0],
                reasons=[],
                artist=song.artist,
                genre=song.genre,
                danceability=song.danceability,
                id=song.id,
            )
            for song in self.songs
        ]
        selected = _rank_with_diversity(candidates, k)
        return [candidate.item for candidate in selected]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended to a user."""
        _, reasons = self.strategy.score(
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
                "mood": [tag.strip() for tag in row["mood"].split(";") if tag.strip()],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "song_popularity": float(row["song_popularity"]),
                "release_year": int(row["release_year"]),
                
            })
    return songs

def score_song(user_prefs: Dict, song: Dict, strategy: Optional[RankingStrategy] = None) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    strategy = strategy or STRATEGIES["balanced"]
    return strategy.score(
        song["genre"], song["mood"], song.get("energy"), song["acousticness"], song["danceability"],
        user_prefs["genre"], user_prefs["mood"], user_prefs.get("energy"),
        user_prefs["likes_acoustic"], user_prefs.get("wants_danceable", False),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                     strategy: Optional[RankingStrategy] = None) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic. Applies a
    diversity penalty so one artist or genre can't dominate the top k.
    Required by src/main.py
    """
    strategy = strategy or STRATEGIES["balanced"]
    candidates = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        candidates.append(_ScoredCandidate(
            item=song,
            score=score,
            reasons=reasons,
            artist=song["artist"],
            genre=song["genre"],
            danceability=song["danceability"],
            id=song["id"],
        ))

    selected = _rank_with_diversity(candidates, k)
    return [
        (
            candidate.item,
            candidate.score,
            "; ".join(candidate.reasons) if candidate.reasons else "No strong matches with your preferences",
        )
        for candidate in selected
    ]
