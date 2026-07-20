# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I manually added more attributes to recommender.py then got stuck with adding different moods to the 'mood' attribute.

**Prompts used:**

i'm adding attributes to recommender.py. I would like to expand the mood attribue to hold differenct mood tags  like "aggressive" eupohoric etc. How do I do that

**What did the agent generate or change?**

songs.csv was reformated so the exmanded mood value could be parsed.
load_songs was updated to parse the selimited string of moods into a list
_score / score_song were updated to handle the matching logic changes from equality to membership/overlap
test_recommender.py new tests were added to ensure functionality after feature expansion.

**What did you verify or fix manually?**

There was an issue with correctly parsing the new mood attributes, and a strip() function was added to aid in parsing.


---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Ranking strategy.

**How did AI help you brainstorm or implement it?**

During the brainstorm session and going through the different strategies ranking was established as one that could easily and genuinely produce different orderings.

**How does the pattern appear in your final code?**

The pattern appears in recommender. py via the RankingStrategy which defines score() that all of the strategies share including the weight attributes that the subclasses override.

BalancedStrategy, GenreFirstStrategy, MoodFirstStrategy and EnergyFocusedStrategy each override some fothe weighted class attributes.

Recommender.__init__(self, songs, strategy=None) is the context object that holds a reference to the strategy and calls the self.strategy.score() inside recommend() and the following explanation versus hardcodeing the scoring rules.  Then STATEGIES  and main.py's --strategy flag picks which strategy object to pass over to Recommender/recommend_songs at runtime. 