"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print("\n" + "=" * 50)
    print(label)
    print("=" * 50)
    try:
        recommendations = recommend_songs(user_prefs, songs, k=k)
    except KeyError as e:
        print(f"   -> KeyError: missing preference key {e}")
        return
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score:  {score:.2f}")
        print(f"   Reason: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        (
            "Demo: lofi/chill listener, lower energy, acoustic-leaning",
            {
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.35,
                "likes_acoustic": True,
            },
        ),
        (
            "Demo: pop/happy listener, wants danceable",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.7,
                "likes_acoustic": False,
                "wants_danceable": True,
            },
        ),
        (
            "Demo: rock/angry listener, high energy",
            {
                "genre": "rock",
                "mood": "angry",
                "energy": 0.8,
                "likes_acoustic": False,
                "wants_danceable": False,
            },
        ),
        (
            "Edge case: conflicting energy/mood (rock target but chill mood)",
            {
                "genre": "rock",
                "mood": "chill",
                "energy": 0.95,
                "likes_acoustic": True,
            },
        ),
        (
            "Edge case: genre with zero catalog matches (k-pop)",
            {
                "genre": "k-pop",
                "mood": "happy",
                "energy": 0.8,
                "likes_acoustic": False,
            },
        ),
        (
            "Edge case: case/whitespace mismatch (\"Lofi \" / \"Chill\")",
            {
                "genre": "Lofi ",
                "mood": "Chill",
                "energy": 0.4,
                "likes_acoustic": True,
            },
        ),
        (
            "Edge case: boundary energy = 0.0",
            {
                "genre": "metal",
                "mood": "aggressive",
                "energy": 0.0,
                "likes_acoustic": False,
            },
        ),
        (
            "Edge case: boundary energy = 1.0",
            {
                "genre": "metal",
                "mood": "aggressive",
                "energy": 1.0,
                "likes_acoustic": False,
            },
        ),
        (
            "Edge case: out-of-range energy = 1.5",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 1.5,
                "likes_acoustic": False,
            },
        ),
        (
            "Edge case: out-of-range energy = -0.3",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": -0.3,
                "likes_acoustic": False,
            },
        ),
        (
            "Edge case: everything mismatched (near-zero score profile)",
            {
                "genre": "opera",
                "mood": "furious",
                "energy": 0.5,
                "likes_acoustic": False,
                "wants_danceable": False,
            },
        ),
        (
            "Edge case: missing optional key (no likes_acoustic)",
            {
                "genre": "edm",
                "mood": "euphoric",
                "energy": 0.9,
            },
        ),
        (
            "Edge case: wants_danceable pulls down a strong-but-slow match",
            {
                "genre": "folk",
                "mood": "nostalgic",
                "energy": 0.33,
                "likes_acoustic": True,
                "wants_danceable": True,
            },
        ),
    ]

    for label, user_prefs in profiles:
        print_recommendations(label, user_prefs, songs, k=5)

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
