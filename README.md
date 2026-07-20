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
   Reason: Energy (0.37) is very close to your target (0.35); You like 
   acoustic songs, and this one leans acoustic

genre (lofi); Matches your favorite mood (chill); Energy (0.42) is very close to your target (0.35); You like acoustic songs, and this one leans acoustic


==================================================
Demo: pop/happy listener, wants danceable
==================================================

1. Sunrise City by Neon Echo
   Score:  6.34
   Reason: Matches your favorite genre (pop); Matches your favorite mood (happy); Energy (0.82) is very close to your target (0.7); Very danceable (0.79) - great for getting people moving

2. Gym Hero by Max Pulse
   Score:  5.30
   Reason: Matches your favorite genre (pop); Energy (0.93) is very close to your target (0.7); Very danceable (0.88) - great for getting people moving

3. Rooftop Lights by Indigo Parade
   Score:  4.52
   Reason: Matches your favorite mood (happy); Energy (0.76) is very close to your target (0.7); Very danceable (0.82) - great for getting people moving

4. Night Drive Loop by Neon Echo
   Score:  3.36
   Reason: Energy (0.75) is very close to your target (0.7); Fairly danceable (0.73)

5. Concrete Kingdom by Trap Cartel
   Score:  3.34
   Reason: Energy (0.88) is very close to your target (0.7); Very danceable (0.85) - great for getting people moving

   ==================================================
Demo: rock/angry listener, high energy
==================================================

1. Storm Runner by Voltline
   Score:  3.78
   Reason: Matches your favorite genre (rock); Energy (0.91) is very close to your target (0.8)

2. Sunrise City by Neon Echo
   Score:  1.96
   Reason: Energy (0.82) is very close to your target (0.8)

3. Rooftop Lights by Indigo Parade
   Score:  1.92
   Reason: Energy (0.76) is very close to your target (0.8)

4. Night Drive Loop by Neon Echo
   Score:  1.90
   Reason: Energy (0.75) is very close to your target (0.8)

5. Concrete Kingdom by Trap Cartel
   Score:  1.84
   Reason: Energy (0.88) is very close to your target (0.8)

==================================================
==================================================
Edge case: conflicting energy/mood (rock target but chill mood)
==================================================

1. Storm Runner by Voltline
   Score:  3.92
   Reason: Matches your favorite genre (rock); Energy (0.91) is very close to your target (0.95)

2. Midnight Coding by LoRoom
   Score:  2.94
   Reason: Matches your favorite mood (chill); Energy (0.42) is somewhat close to your target (0.95); You like acoustic songs, and this one leans acoustic

3. Library Rain by Paper Lanterns
   Score:  2.80
   Reason: Matches your favorite mood (chill); Energy (0.35) is somewhat close to your target (0.95); You like acoustic songs, and this one leans acoustic

4. Spacewalk Thoughts by Orbit Bloom
   Score:  2.66
   Reason: Matches your favorite mood (chill); Energy (0.28) is somewhat close to your target (0.95); You like acoustic songs, and this one leans acoustic

5. Neon Pulse Rave by Circuit Bloom
   Score:  2.00
   Reason: Energy (0.95) is very close to your target (0.95)

==================================================
Edge case: genre with zero catalog matches (k-pop)
==================================================

1. Sunrise City by Neon Echo
   Score:  2.96
   Reason: Matches your favorite mood (happy); Energy (0.82) is very close to your target (0.8)

2. Rooftop Lights by Indigo Parade
   Score:  2.92
   Reason: Matches your favorite mood (happy); Energy (0.76) is very close to your target (0.8)

3. Night Drive Loop by Neon Echo
   Score:  1.90
   Reason: Energy (0.75) is very close to your target (0.8)

4. Concrete Kingdom by Trap Cartel
   Score:  1.84
   Reason: Energy (0.88) is very close to your target (0.8)

5. Storm Runner by Voltline
   Score:  1.78
   Reason: Energy (0.91) is very close to your target (0.8)

==================================================
==================================================
Edge case: case/whitespace mismatch ("Lofi " / "Chill")
==================================================

1. Focus Flow by LoRoom
   Score:  3.00
   Reason: Energy (0.4) is very close to your target (0.4); You like acoustic songs, and this one leans acoustic

2. Midnight Coding by LoRoom
   Score:  2.96
   Reason: Energy (0.42) is very close to your target (0.4); You like acoustic songs, and this one leans acoustic

3. Coffee Shop Stories by Slow Stereo
   Score:  2.94
   Reason: Energy (0.37) is very close to your target (0.4); You like acoustic songs, and this one leans acoustic

4. Library Rain by Paper Lanterns
   Score:  2.90
   Reason: Energy (0.35) is very close to your target (0.4); You like acoustic songs, and this one leans acoustic

5. Harvest Moon Porch by Cedar Hollow
   Score:  2.86
   Reason: Energy (0.33) is very close to your target (0.4); You like acoustic songs, and this one leans acoustic

==================================================
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



