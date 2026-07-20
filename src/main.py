"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
import textwrap

from src.recommender import load_songs, recommend_songs, STRATEGIES

REASONS_COLUMN_WIDTH = 60


def _render_table(headers: list, rows: list, wrap_widths: dict) -> str:
    """
    Renders rows as a simple ASCII table (no external dependency). Columns
    listed in wrap_widths get word-wrapped onto extra lines within their row
    instead of stretching the whole table.
    """
    wrapped_rows = [
        [textwrap.wrap(str(cell), wrap_widths[header]) or [""] if header in wrap_widths else [str(cell)]
         for header, cell in zip(headers, row)]
        for row in rows
    ]

    col_widths = [
        max([len(header)] + [len(line) for wrapped_row in wrapped_rows for line in wrapped_row[col_idx]])
        for col_idx, header in enumerate(headers)
    ]

    def border(char: str = "-") -> str:
        return "+" + "+".join(char * (width + 2) for width in col_widths) + "+"

    def format_row(cells: list) -> str:
        return "| " + " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(cells)) + " |"

    lines = [border(), format_row(headers), border("=")]
    for wrapped_row in wrapped_rows:
        for line_idx in range(max(len(col) for col in wrapped_row)):
            lines.append(format_row([col[line_idx] if line_idx < len(col) else "" for col in wrapped_row]))
        lines.append(border())

    return "\n".join(lines)


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5, strategy=None) -> None:
    print("\n" + "=" * 50)
    print(label)
    print("=" * 50)
    try:
        recommendations = recommend_songs(user_prefs, songs, k=k, strategy=strategy)
    except KeyError as e:
        print(f"   -> KeyError: missing preference key {e}")
        return

    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    rows = [
        [rank, song["title"], song["artist"], f"{score:.2f}", explanation]
        for rank, (song, score, explanation) in enumerate(recommendations, start=1)
    ]
    print(_render_table(headers, rows, wrap_widths={"Reasons": REASONS_COLUMN_WIDTH}))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the music recommender simulation.")
    parser.add_argument(
        "--profile",
        type=int,
        default=None,
        help="Index (0-based) of a single profile to run. Omit to run all profiles.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available profile indices and labels, then exit.",
    )
    parser.add_argument(
        "--strategy",
        choices=sorted(STRATEGIES.keys()),
        default="balanced",
        help="Ranking strategy to use (default: balanced).",
    )
    args = parser.parse_args()

    strategy = STRATEGIES[args.strategy]
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

    if args.list:
        for i, (label, _) in enumerate(profiles):
            print(f"{i}: {label}")
        return

    print(f"Ranking strategy: {strategy.name}")

    if args.profile is not None:
        label, user_prefs = profiles[args.profile]
        print_recommendations(label, user_prefs, songs, k=5, strategy=strategy)
    else:
        for label, user_prefs in profiles:
            print_recommendations(label, user_prefs, songs, k=5, strategy=strategy)

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
