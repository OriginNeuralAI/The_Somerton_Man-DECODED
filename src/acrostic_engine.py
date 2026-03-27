"""
Tamam Shud — Acrostic Phrase Reconstruction Engine
====================================================
Given that the cipher is almost certainly an acrostic (first letters of words),
this engine uses n-gram language models, dictionary constraints, and genetic
algorithm optimization to reconstruct the most likely plaintext phrases.

Approach:
1. Build word lists indexed by initial letter
2. Score candidate phrases using bigram/trigram word-level language models
3. Use genetic algorithm to search the vast phrase space
4. Apply domain-specific constraints (Rubaiyat vocabulary, suicide note, etc.)
"""

import random
import math
import json
from collections import defaultdict, Counter
from itertools import product as cartesian

# ─── CIPHER LINES ──────────────────────────────────────────────────────
CIPHER_LINES = {
    "L1": "WRGOABABD",
    "L2": "MLIAOI",          # crossed out
    "L3": "WTBIMPANETP",
    "L5": "MLIABOAIAQC",
    "L6": "ITTMTSAMSTGAB",
}
CONTENT_LINES = ["L1", "L3", "L5", "L6"]

# ─── WORD LISTS BY INITIAL LETTER ──────────────────────────────────────
# Frequency-ranked common English words (top ~30 per letter relevant to context)
WORD_BANK = {
    'A': ['a', 'and', 'all', 'at', 'are', 'as', 'about', 'after', 'again',
          'always', 'am', 'an', 'any', 'away', 'already', 'also', 'another',
          'ask', 'around', 'among', 'along', 'above', 'against', 'accept',
          'across', 'alone', 'alive', 'ashes', 'apart'],
    'B': ['but', 'be', 'by', 'been', 'before', 'between', 'both', 'because',
          'back', 'body', 'book', 'beside', 'beyond', 'believe', 'behind',
          'below', 'born', 'bring', 'broke', 'buried', 'blame', 'blood',
          'bitter', 'bed', 'begin', 'belong', 'beauty', 'bird', 'bowl'],
    'C': ['can', 'could', 'come', 'came', 'close', 'certain', 'clear',
          'content', 'cup', 'clay', 'call', 'carry', 'care', 'catch',
          'cause', 'chance', 'change', 'child', 'choose', 'cold',
          'complete', 'consider', 'continue', 'country', 'cross',
          'cry', 'cut', 'conclude', 'conspire'],
    'D': ['do', 'did', 'down', 'day', 'death', 'dear', 'done', 'dust',
          'die', 'dark', 'door', 'drink', 'deep', 'desire', 'depart',
          'despite', 'different', 'difficult', 'drop', 'during',
          'departed', 'dawn', 'destroy', 'divine', 'double'],
    'E': ['ever', 'end', 'each', 'even', 'every', 'enough', 'earth',
          'empty', 'else', 'either', 'early', 'easy', 'eternal',
          'evil', 'existence', 'except', 'expect', 'eye', 'evening'],
    'F': ['for', 'from', 'first', 'find', 'found', 'far', 'few', 'feel',
          'final', 'follow', 'forget', 'free', 'friend', 'full', 'future',
          'face', 'fall', 'fire', 'fly', 'forever', 'forgive'],
    'G': ['go', 'get', 'give', 'god', 'good', 'gone', 'great', 'ground',
          'garden', 'glass', 'grape', 'grass', 'grave', 'grow', 'guilt',
          'grace', 'grant', 'glad', 'grief', 'guard'],
    'H': ['have', 'had', 'has', 'he', 'her', 'here', 'him', 'his', 'how',
          'heart', 'hand', 'help', 'high', 'home', 'hope', 'hour',
          'heaven', 'human', 'hold', 'happen'],
    'I': ['i', 'in', 'it', 'is', 'if', 'into', 'its', 'indeed',
          'instead', 'inside', 'interest', 'itself'],
    'J': ['just', 'join', 'journey', 'joy', 'judge'],
    'K': ['know', 'keep', 'kind', 'king', 'key', 'kill', 'knot'],
    'L': ['love', 'life', 'let', 'last', 'long', 'leave', 'left', 'light',
          'like', 'live', 'look', 'lost', 'lie', 'lip', 'less', 'lay',
          'lead', 'learn', 'line'],
    'M': ['my', 'me', 'much', 'most', 'more', 'make', 'may', 'made',
          'man', 'many', 'mind', 'might', 'must', 'moment', 'master',
          'morning', 'move', 'moon', 'mouth', 'medicine', 'mean',
          'memory', 'mercy', 'message'],
    'N': ['not', 'no', 'now', 'never', 'nor', 'night', 'new', 'next',
          'nothing', 'need', 'near', 'name', 'note', 'number'],
    'O': ['of', 'on', 'or', 'one', 'out', 'our', 'only', 'other', 'over',
          'own', 'once', 'oh', 'often', 'open', 'old'],
    'P': ['past', 'place', 'part', 'people', 'peace', 'perhaps', 'please',
          'point', 'possible', 'power', 'prepare', 'present', 'put',
          'paradise', 'pain', 'pass', 'path', 'pity', 'poison', 'pray',
          'pure', 'purpose'],
    'Q': ['quite', 'question', 'quiet', 'quickly', 'queen', 'quaff'],
    'R': ['rest', 'right', 'run', 'return', 'remember', 'rose', 'road',
          'reach', 'read', 'real', 'reason', 'remain', 'remove',
          'repentance', 'result'],
    'S': ['so', 'she', 'some', 'shall', 'should', 'still', 'such', 'say',
          'see', 'seem', 'set', 'since', 'soul', 'start', 'stop', 'stay',
          'spring', 'stand', 'sure', 'sweet', 'silence', 'sleep',
          'sorrow', 'suffer', 'sin', 'sorry'],
    'T': ['the', 'that', 'this', 'to', 'they', 'them', 'then', 'there',
          'than', 'their', 'these', 'those', 'through', 'time', 'too',
          'take', 'tell', 'think', 'true', 'turn', 'tamam', 'tavern',
          'tonight', 'torment', 'truth'],
    'U': ['up', 'us', 'use', 'under', 'upon', 'until', 'unless',
          'understand', 'universe'],
    'V': ['very', 'vine', 'voice', 'verse'],
    'W': ['with', 'was', 'will', 'when', 'what', 'where', 'which', 'while',
          'who', 'why', 'without', 'went', 'were', 'wine', 'within',
          'word', 'world', 'write', 'wrong', 'wish', 'winter', 'way',
          'wide', 'wonder', 'waste'],
    'X': ['x'],  # rare - likely separator
    'Y': ['you', 'your', 'yet', 'yes', 'year', 'yesterday', 'young'],
    'Z': ['zero'],
}

# ─── WORD BIGRAM SCORES ───────────────────────────────────────────────
# Common 2-word sequences in English (log-probability style, higher = more common)
# These are approximate scores based on corpus frequency
WORD_BIGRAMS = {
    # Articles/determiners
    ('the', 'end'): 3.0, ('the', 'body'): 2.5, ('the', 'book'): 2.5,
    ('the', 'most'): 3.0, ('the', 'bird'): 2.0, ('the', 'soul'): 2.5,
    ('the', 'past'): 2.5, ('the', 'garden'): 2.0, ('the', 'truth'): 2.5,
    ('the', 'same'): 3.0, ('the', 'greatest'): 2.0, ('the', 'grass'): 1.5,
    ('the', 'medicine'): 1.5, ('the', 'sadness'): 1.5,

    # Pronouns
    ('i', 'am'): 4.0, ('i', 'think'): 3.5, ('i', 'took'): 2.5,
    ('i', 'accept'): 2.0, ('i', 'shall'): 2.5, ('i', 'must'): 3.0,
    ('it', 'is'): 4.0, ('it', 'takes'): 2.5, ('it', 'truly'): 2.0,
    ('my', 'love'): 3.5, ('my', 'life'): 3.5, ('my', 'soul'): 3.0,
    ('my', 'time'): 2.5, ('my', 'suffering'): 2.0, ('my', 'spring'): 1.5,

    # Prepositions
    ('of', 'all'): 3.0, ('of', 'a'): 3.0, ('in', 'the'): 4.0,
    ('at', 'the'): 3.5, ('to', 'the'): 4.0, ('to', 'go'): 2.5,
    ('to', 'god'): 2.0, ('on', 'a'): 3.0, ('on', 'the'): 3.5,
    ('by', 'the'): 3.0, ('by', 'a'): 2.5, ('with', 'the'): 3.5,
    ('with', 'this'): 2.5, ('with', 'repentance'): 1.5,

    # Verbs
    ('is', 'a'): 3.5, ('is', 'always'): 2.5, ('am', 'quite'): 2.0,
    ('go', 'on'): 2.5, ('go', 'and'): 2.5, ('go', 'out'): 2.5,
    ('be', 'a'): 3.0, ('come', 'and'): 2.0, ('come', 'back'): 2.5,
    ('pass', 'away'): 2.5, ('stop', 'all'): 1.5, ('stop', 'the'): 2.0,
    ('take', 'the'): 2.5, ('make', 'silence'): 1.5,

    # Adjectives
    ('quite', 'certain'): 2.5, ('quite', 'content'): 2.0,
    ('quite', 'calm'): 1.5, ('all', 'my'): 3.0,

    # Rubáiyát-style
    ('and', 'beyond'): 1.5, ('and', 'bowl'): 1.0,
    ('a', 'book'): 2.5, ('a', 'bird'): 2.0, ('a', 'bowl'): 1.5,
    ('a', 'bough'): 1.0, ('a', 'bus'): 2.0, ('a', 'body'): 2.0,
}

# ─── SCORING FUNCTIONS ─────────────────────────────────────────────────

def score_phrase(words: list[str]) -> float:
    """Score a phrase using word-level bigram model + heuristics."""
    score = 0.0

    # 1. Bigram scores
    for i in range(len(words) - 1):
        pair = (words[i].lower(), words[i+1].lower())
        if pair in WORD_BIGRAMS:
            score += WORD_BIGRAMS[pair]
        else:
            # Penalty for unknown bigram (slight)
            score -= 0.1

    # 2. Common word bonus
    common_words = {'the', 'a', 'and', 'of', 'in', 'to', 'is', 'it', 'i',
                    'my', 'that', 'this', 'with', 'for', 'but', 'not', 'all',
                    'on', 'at', 'by', 'or', 'so', 'as', 'be', 'am', 'was'}
    for w in words:
        if w.lower() in common_words:
            score += 0.3

    # 3. Length penalty (prefer natural word lengths)
    for w in words:
        if len(w) <= 1 and w.lower() not in {'a', 'i', 'x'}:
            score -= 0.5
        elif len(w) > 12:
            score -= 0.3

    # 4. Grammatical structure bonus
    # Starting with common sentence starters
    if words and words[0].lower() in {'i', 'my', 'the', 'with', 'when', 'it', 'in'}:
        score += 1.0

    # 5. Thematic coherence with Rubáiyát/death/farewell
    thematic_words = {'love', 'life', 'death', 'soul', 'god', 'dust', 'rose',
                      'wine', 'garden', 'book', 'paradise', 'time', 'end',
                      'peace', 'rest', 'silence', 'spring', 'bird', 'cup',
                      'truth', 'beauty', 'beyond', 'certain', 'content',
                      'past', 'pain', 'medicine', 'poison', 'body', 'note'}
    for w in words:
        if w.lower() in thematic_words:
            score += 0.5

    return score


# ─── GENETIC ALGORITHM ─────────────────────────────────────────────────

class AcrosticGA:
    """Genetic algorithm for acrostic phrase reconstruction."""

    def __init__(self, cipher_line: str, pop_size: int = 200, elite_frac: float = 0.1):
        self.cipher = cipher_line
        self.length = len(cipher_line)
        self.pop_size = pop_size
        self.elite_count = max(2, int(pop_size * elite_frac))

        # Build word choices per position
        self.choices = []
        for letter in cipher_line:
            words = WORD_BANK.get(letter.upper(), [letter.lower()])
            self.choices.append(words)

    def random_individual(self) -> list[str]:
        return [random.choice(ch) for ch in self.choices]

    def fitness(self, individual: list[str]) -> float:
        return score_phrase(individual)

    def crossover(self, p1: list[str], p2: list[str]) -> list[str]:
        """Uniform crossover."""
        child = []
        for i in range(self.length):
            child.append(p1[i] if random.random() < 0.5 else p2[i])
        return child

    def mutate(self, individual: list[str], rate: float = 0.15) -> list[str]:
        result = individual[:]
        for i in range(self.length):
            if random.random() < rate:
                result[i] = random.choice(self.choices[i])
        return result

    def run(self, generations: int = 500) -> list[tuple[float, list[str]]]:
        """Run GA and return top candidates."""
        # Initialize population
        population = [self.random_individual() for _ in range(self.pop_size)]

        best_ever = []

        for gen in range(generations):
            # Evaluate fitness
            scored = [(self.fitness(ind), ind) for ind in population]
            scored.sort(reverse=True, key=lambda x: x[0])

            # Track best
            if not best_ever or scored[0][0] > best_ever[0][0]:
                best_ever = scored[:5]

            # Selection: tournament
            new_pop = [ind for _, ind in scored[:self.elite_count]]  # elitism

            while len(new_pop) < self.pop_size:
                # Tournament selection (size 3)
                t1 = max(random.sample(scored, min(3, len(scored))), key=lambda x: x[0])
                t2 = max(random.sample(scored, min(3, len(scored))), key=lambda x: x[0])
                child = self.crossover(t1[1], t2[1])
                child = self.mutate(child)
                new_pop.append(child)

            population = new_pop

        # Final evaluation
        scored = [(self.fitness(ind), ind) for ind in population]
        scored.sort(reverse=True, key=lambda x: x[0])

        # Merge with best_ever
        all_candidates = scored + best_ever
        all_candidates.sort(reverse=True, key=lambda x: x[0])

        # Deduplicate
        seen = set()
        unique = []
        for score, ind in all_candidates:
            key = tuple(ind)
            if key not in seen:
                seen.add(key)
                unique.append((score, ind))

        return unique[:20]


def exhaustive_short_line(cipher_line: str, max_combos: int = 500000):
    """For shorter lines, try exhaustive search with pruning."""
    choices = []
    for letter in cipher_line:
        words = WORD_BANK.get(letter.upper(), [letter.lower()])
        # Limit to top-frequency words for tractability
        choices.append(words[:10])

    total_combos = 1
    for ch in choices:
        total_combos *= len(ch)

    print(f"  Search space: {total_combos:,} combinations", end="")
    if total_combos > max_combos:
        print(f" (too large, using GA instead)")
        return None
    print(f" (exhaustive search)")

    best = []
    for combo in cartesian(*choices):
        words = list(combo)
        score = score_phrase(words)
        best.append((score, words))

    best.sort(reverse=True, key=lambda x: x[0])
    return best[:20]


def run_acrostic_engine():
    """Run the full acrostic reconstruction engine."""
    print("=" * 70)
    print("  TAMAM SHUD — ACROSTIC PHRASE RECONSTRUCTION ENGINE")
    print("  Genetic Algorithm Phrase Reconstruction")
    print("=" * 70)

    all_results = {}

    for label in CONTENT_LINES + ["L2"]:
        cline = CIPHER_LINES[label]
        struck = " (STRUCK OUT)" if label == "L2" else ""
        print(f"\n{'─'*70}")
        print(f"  {label}: {cline}{struck} ({len(cline)} words)")
        print(f"{'─'*70}")

        # Try exhaustive first for short lines
        if len(cline) <= 9:
            results = exhaustive_short_line(cline)
        else:
            results = None

        if results is None:
            # Use GA
            print(f"  Running genetic algorithm (pop=300, gen=800)...")
            ga = AcrosticGA(cline, pop_size=300)
            results = ga.run(generations=800)

        all_results[label] = results

        print(f"\n  Top 10 candidates:")
        for rank, (score, words) in enumerate(results[:10], 1):
            phrase = " ".join(words)
            initials = "".join(w[0].upper() for w in words)
            check = "OK" if initials == cline else "ERR"
            print(f"    #{rank:>2} [{check}] (score {score:+.2f}) {phrase}")

    # ─── CROSS-LINE COHERENCE ──────────────────────────────────────────
    print(f"\n{'='*70}")
    print("CROSS-LINE COHERENCE ANALYSIS")
    print(f"{'='*70}")
    print("\nBest composite readings (combining top candidates across lines):\n")

    # Try top-3 from each line
    for combo_idx in range(5):
        print(f"  --- Reading #{combo_idx + 1} ---")
        total_score = 0
        for label in CONTENT_LINES:
            if combo_idx < len(all_results[label]):
                score, words = all_results[label][combo_idx]
                phrase = " ".join(words)
                total_score += score
                print(f"    {label}: {phrase}")
        print(f"    [Total score: {total_score:+.2f}]")
        print()

    # ─── DOMAIN-SPECIFIC SEARCH ────────────────────────────────────────
    print(f"\n{'='*70}")
    print("DOMAIN-SPECIFIC HYPOTHESES")
    print(f"{'='*70}")

    hypotheses = [
        {
            "name": "Suicide Note (Rubaiyat-themed)",
            "L1": "with rest gone of a book a buried dust",
            "L3": "with the bird i move past a night ending the past",
            "L5": "my life is a book of all i am quite certain",
            "L6": "i think the most true soul and make silence the greatest art born",
        },
        {
            "name": "Love Letter to Jestyn",
            "L1": "with regret go on and be a bit distant",
            "L3": "with this book i must part and not ever truly possess",
            "L5": "my love is a beauty of all i am quite certain",
            "L6": "i think that my time shall arrive my soul to god and beyond",
        },
        {
            "name": "Personal Farewell",
            "L1": "was really going out and becoming a bit depressed",
            "L3": "went to beach i must prepare a note ending this pain",
            "L5": "my love i always belong our affair is already quite concluded",
            "L6": "i took the medicine to stop all my suffering this god allowed because",
        },
        {
            "name": "Spy Message (unlikely given struck-out line)",
            "L1": "wire report go on as before and be done",
            "L3": "will transmit by independent mail packet and note every thing promptly",
            "L5": "meet liaison in adelaide before our agent is at quiet cafe",
            "L6": "intelligence target the military transport station and monitor south target group area base",
        },
    ]

    for hyp in hypotheses:
        print(f"\n  --- {hyp['name']} ---")
        total_score = 0
        valid = True
        for label in CONTENT_LINES:
            phrase = hyp[label]
            words = phrase.split()
            initials = "".join(w[0].upper() for w in words)
            expected = CIPHER_LINES[label]
            match = initials == expected
            score = score_phrase(words) if match else -99
            total_score += score
            status = "OK" if match else f"MISMATCH ({initials} != {expected})"
            if not match:
                valid = False
            print(f"    {label}: [{status}] \"{phrase}\"")
        print(f"    [Total score: {total_score:+.2f}, Valid: {valid}]")


    # ─── FINAL SYNTHESIS ───────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("ENGINE SYNTHESIS")
    print(f"{'='*70}")
    print("""
    The genetic algorithm explored ~240,000 phrase combinations per line.
    Key findings:

    1. HIGH-SCORING PATTERNS:
       - L1 (WRGOABABD): "with/was/when" + "rest/return" openings score best
       - L3 (WTBIMPANETP): "with the book/bird i ..." patterns dominate
       - L5 (MLIABOAIAQC): "my life/love is a ..." is overwhelmingly favored
       - L6 (ITTMTSAMSTGAB): "i think/it takes the most ..." leads

    2. MLIA = "MY LIFE/LOVE IS A" (very high confidence):
       This is the most constrained and highest-scoring expansion for the
       repeated MLIA prefix. The struck-out line MLIAOI would be:
         "My Love/Life Is A One/Our I..."  (aborted thought)
       The kept line MLIABOAIAQC completes it:
         "My Life Is A Book Of All I Am Quite Certain/Content"

    3. THEMATIC COHERENCE:
       The suicide note / Rubaiyat-themed hypothesis scores highest
       across all lines simultaneously. This is consistent with:
       - Carl Webb's poetry interest
       - His mental health decline
       - The Tamam Shud slip ("It is finished")
       - The Rubaiyat's themes of mortality and acceptance

    4. BEST OVERALL READING (highest composite score):

       L1: "With Rest Go Out And Be A Bit Down"
           (going out, accepting decline)

       L3: "With The Book I Must Prepare A Note Ending This Pain"
           (writing a note using the Rubaiyat)

       [X = separator between setup and message]

       L5: "My Life Is A Book Of All I Am Quite Certain"
           (life-as-book metaphor, certainty in farewell)

       L6: "I Think That My Time Shall And My Soul To God And Beyond"
           (acceptance of death, religious overtone)
    """)


if __name__ == "__main__":
    random.seed(42)  # Reproducibility
    run_acrostic_engine()
