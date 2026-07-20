# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

ItzUhVibe

---

## 2. Intended Use  

ItzUhVibe helps users generate a playlist to fit their taste and mood.

---

## 3. How the Model Works  

The model systematically looks at each song and its features like gengre, moods, danceability, and acousticness. It weights these attributes and gives each song a score to be measured against a user's preferences. Scores that most align with the user's preferences are ranked highest and recommended to the user. 

---

## 4. Data  

This model uses an 18-song catalog with genres: pop, rock, lofi, indie,  folk, R&B, classical, hip-hop, EDM, country, reggae, metal, jazz, synthwave, indie pop, and ambient and 16 different moods. Data was added and there could be even more added that was not. 
---

## 5. Strengths  

The model works reasonable well for a small system. The scoring system is effective in its points system for accurately balancing genre and mood and differentiating listeners with similar energy but different tastes. It effectively rewards scores that are close but not exact and offers a wider variety of mood-matching.
---

## 6. Limitations and Bias  

Genre preference is a filter bubble with 13/15 songs having only 1 song representing that category. So when someone has a genre preference it will always return that one song - and the other genres - lofi and pop - are not doing much better with 3 and 2 songs respectively. 

Also the energy feature has a serious coverage gap. The 0.55 - 0.75 range is completely empty, with mellow and high-energy each having 8 songs. So the mid-range is ignored, and the preference being closer to eith extreme is what determines the recommendation. 
---

## 7. Evaluation  


1. Lofi/chill: low energy (0.35), likes acoustic. A "normal" listener whose stated taste matches genres that actually exist in the catalog.
2. Pop/happy, wants danceable:  moderate-high energy (0.7), wants danceable songs. Another "normal" listener, but one who cares about danceability instead of acoustic tone.
3. Rock/angry, high energy: energy 0.8. Note: "angry" isn't a mood that exists anywhere in the catalog, so this quietly tests what happens when a mood preference can never be satisfied.
4. Conflicting rock/chill: asks for genre "rock" but mood "chill" at energy 0.95 (contradictory: wants a chill song that's also nearly maximum energy).
5. Genre with zero catalog matchesfavorite genre "k-pop", which isn't in the catalog at all.
6. Case/whitespace mismatch: same taste as profile 1 in spirit ("Lofi "/"Chill") but typed with different capitalization and a trailing space.
7. Boundary energy = 0.0: metal/aggressive fan who (unrealistically) asks for zero energy.
8. Boundary energy = 1.0: same metal/aggressive fan asking for maximum energy instead.
9. Out-of-range energy = 1.5: pop/happy fan whose energy value is above the valid 0–1 scale.
10. Out-of-range energy = -0.3: pop/happy fan whose energy value is below the valid 0–1 scale.
11. Everything mismatched: genre "opera" and mood "furious", neither of which exist in the catalog, at a neutral energy of 0.5.
12. Missing required field: genre "edm"/mood "euphoric" preferences with the `likes_acoustic` key left out entirely (not even set to `False`).
13. Danceable folk fan: genre "folk", mood "nostalgic", energy 0.33, likes acoustic, and wants danceable — a listener whose favorite genre isn't a typically danceable one.

Surprises:

Genre preference isn't a strong predictor of what will be recommened as many genres only have 1 song.


Typos and whitespace tested the same as having absolutely no genre and / or mood points. The recommender has no tolerance for whitespace or capitalization.


Invalid energy values don't cause an error, they just don't have a noticable effect on the recommendations. 

Profiles with "wants danceable" doesn't exclude genres as expected as a folk genre song still makes the cut.

Profile comparisons:

P1 vs. P2:

P1 has an acoustic-leaning profile that pulls its top picks from low-energy, high-acousticness songs (*Library Rain*, *Midnight Coding*), while P2 pulls from the high-energy, high-danceability cluster (*Sunrise City*, *Rooftop Lights*). 


P3 vs. P4:

Both profiles ask for the rock genre and both put "Storm Runner" near the top, but profile 3 puts it at #1 (nothing is fighting the energy match) while profile 4 barely edges it into #2 behind a chill/acoustic song. 

P4 vs. P5
Both profiles can't get a clean recommendation because the genre and mood pull in opposite directions and because the genre doesn't exist at all — but they fail differently. Profile 4 still surfaces the one rock song near the top because a genre match is on the table; profile 5 never gets a genre bonus for anyone, so its ranking is driven entirely by mood and energy proximity.

P3 vs. P5:

These profiles look like opposite listeners (rock  vs. k-pop) but end up recommending almost the same four filler songs (*Sunrise City*, *Rooftop Lights*, *Night Drive Loop*, *Concrete Kingdom*), only reordered. This is on account of the fact that neither profile can ever get a genre match, so both rankings end up defaulting to the "closest energy to 0.8," which hurts functionality it terms of recommending something closer to what the user proabaly wanted.

P1 vs. P6:

These two profiles have the same intended taste, but P6 never gets a genre or mood point, so its whole top five is chosen by acoustic and energy closeness alone. 



---

## Intended Use and Non-Intended Use 

In its current form, ItzUhVibe is intended to make recommendations based off of a limited catalog of songs. It is not intended to pull in song catalogs from other sites or from user-generated catalogs. 

## 8. Future Work  



I would add more songs for greater variety. I would create a feature to generate more playlists based on the success of the first generated playlist (songs that are played more ofter, songs that are skipped behaviors would inform how the next playlist is generated.)
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned that user behaviours on a streaming platform (repeats, skips, etc.) are used to weight recommendations. I definitely am now more intentional with how I favorite/like a song or artist and skip songs to improve my own listening experience. 

AI was a huge help on this one by adding more functionality and scoring methods to test againsts. 

I would try to increase the song catalog to test the current functionality on a wider data set.