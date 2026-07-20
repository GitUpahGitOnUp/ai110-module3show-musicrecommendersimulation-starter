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

The features used for each 'Song' are: genre, mood, tempo_bpm, valence, danceability,, acousticness.

The UserProfile stores: target_enery, likes_acousitc, target_energy, favorite_mood, favorite_genre

The Recommender uses a score to determine how well a song matches the user's preference overall.

Once songs are scored based on the user's preferences, the songs are ranked from highest - lowest, and then the top k songs are recommended to the user.

The Algorithm Recipe

The input layer consists of a user's preference stored in a dict and the list of songs and their categorical values.

Each song is scored with genre, energy, and danceability(an optional setting) weighted the most, and mood and acousticness have the potential to weigh about half as much.

Each song that matches the user's criteria is added as a recommendation, along with a justification as to why it is a match and the overal score.

The recommended scores are given with the highest scoring songs first. 

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

==================================================
Top Recommendations
==================================================

1. Library Rain by Paper Lanterns
   Score:  6.00
   Reason: Matches your favorite genre (lofi); Matches your favorite mood (chill); Energy (0.35) is very close to your target (0.35); You like acoustic songs, and this one leans acoustic

2. Midnight Coding by LoRoom
   Score:  5.86
   Reason: Matches your favorite genre (lofi); Matches your favorite mood (chill); Energy (0.42) is very close to your target (0.35); You like acoustic songs, and this one leans acoustic

3. Focus Flow by LoRoom
   Score:  4.90
   Reason: Matches your favorite genre (lofi); Energy (0.4) is very close to your target (0.35); You like acoustic songs, and this one leans acoustic

4. Spacewalk Thoughts by Orbit Bloom
   Score:  3.86
   Reason: Matches your favorite mood (chill); Energy (0.28) is very close to your target (0.35); You like acoustic songs, and this one leans acoustic

5. Coffee Shop Stories by Slow Stereo
   Score:  2.96
   Reason: Energy (0.37) is very close to your target (0.35); You like acoustic songs, and this one leans acoustic

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



