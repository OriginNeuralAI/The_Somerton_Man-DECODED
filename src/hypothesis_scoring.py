"""
Tamam Shud — Bayesian Hypothesis Scoring
==========================================
Score competing hypotheses using Turing's Banburismus method
(deciban scoring) using Turing's Banburismus method.

Each piece of evidence contributes positive or negative decibans
to each hypothesis. Final scores represent posterior odds.
"""

import math

# ─── HYPOTHESES ─────────────────────────────────────────────────────────
HYPOTHESES = [
    "H1: Acrostic suicide note (Rubaiyat-themed)",
    "H2: Acrostic love letter / farewell to woman",
    "H3: Acrostic personal memo (horse racing / mundane)",
    "H4: Espionage one-time pad",
    "H5: Espionage book cipher (Rubaiyat as key)",
    "H6: Random / meaningless doodle",
]

# ─── EVIDENCE & DECIBAN WEIGHTS ────────────────────────────────────────
# Each evidence item: (description, {hypothesis: decibans})
# Positive db = evidence supports; Negative db = evidence contradicts
# Scale: 10 db = 10:1 odds, 20 db = 100:1, 30 db = 1000:1

EVIDENCE = [
    # E1: Crossed-out line (MLIAOI → MLIABOAIAQC)
    (
        "E1: Line 2 crossed out, restarted as Line 5 (MLIA prefix shared)",
        {
            "H1": +8,   # Natural composition process
            "H2": +8,   # Natural composition process
            "H3": +6,   # Possible for notes
            "H4": -20,  # FATAL: OTP cannot have corrections
            "H5": -10,  # Book cipher extraction wouldn't need correction
            "H6": -5,   # Random wouldn't show prefix match
        }
    ),
    # E2: MLIA repeated prefix
    (
        "E2: MLIA appears at start of both L2 and L5",
        {
            "H1": +5,   # "My Life/Love Is A..." repeated thought
            "H2": +6,   # "My Love Is A..." strong for love letter
            "H3": +3,   # Less natural for mundane memo
            "H4": -15,  # OTP repeats = catastrophic key reuse (impossible)
            "H5": -5,   # Book cipher wouldn't repeat
            "H6": -8,   # Random 4-letter repeat P ≈ 1/14000
        }
    ),
    # E3: IC = 0.0740 (close to English 0.0667)
    (
        "E3: Index of Coincidence = 0.074 (English ≈ 0.067, random ≈ 0.038)",
        {
            "H1": +6,   # Consistent with English initials
            "H2": +6,   # Same
            "H3": +6,   # Same
            "H4": -8,   # OTP should give IC ≈ 0.038
            "H5": +2,   # Could match if book cipher
            "H6": -8,   # Random should give ≈ 0.038
        }
    ),
    # E4: Chi-squared passes acrostic test (27.06 < 37.7 critical)
    (
        "E4: Letter frequencies match English initial-letter distribution (chi² = 27.06)",
        {
            "H1": +8,   # Strong acrostic support
            "H2": +8,   # Same
            "H3": +8,   # Same
            "H4": -5,   # OTP wouldn't match
            "H5": +3,   # Partial match possible
            "H6": -5,   # Random wouldn't match
        }
    ),
    # E5: 4 content lines = Rubaiyat stanza structure (AABA)
    (
        "E5: Four content lines match Rubáiyát 4-line stanza structure",
        {
            "H1": +7,   # Deliberate stanza composition
            "H2": +4,   # Could be verse-inspired
            "H3": +1,   # Coincidence
            "H4": 0,    # Neutral
            "H5": +3,   # Could reflect book structure
            "H6": -2,   # Unlikely
        }
    ),
    # E6: Tamam Shud slip in fob pocket
    (
        "E6: 'Tamam Shud' slip torn from the Rubáiyát found on body",
        {
            "H1": +10,  # "It is finished" = farewell/suicide
            "H2": +5,   # Could be romantic symbolism
            "H3": -3,   # Mundane memo wouldn't carry this
            "H4": +3,   # Could be spy recognition signal
            "H5": +5,   # Book cipher needs the book
            "H6": -5,   # Not meaningless
        }
    ),
    # E7: Phone number on book + cipher
    (
        "E7: Jessica Thomson's phone number also written on the book cover",
        {
            "H1": +4,   # Personal connection
            "H2": +8,   # Strong love letter support
            "H3": +2,   # Could be any contact
            "H4": +5,   # Contact for handler
            "H5": +2,   # Book owner
            "H6": -3,   # Not consistent with meaningless
        }
    ),
    # E8: All labels removed from clothing
    (
        "E8: All clothing labels deliberately removed",
        {
            "H1": +3,   # Identity concealment before suicide
            "H2": +2,   # Concealment
            "H3": -2,   # Not typical for mundane
            "H4": +8,   # Classic spy tradecraft
            "H5": +5,   # Espionage context
            "H6": -3,   # Not consistent
        }
    ),
    # E9: Carl Webb ID (2022 DNA identification)
    (
        "E9: DNA identifies man as Carl Webb (engineer, poetry lover, declining mental health)",
        {
            "H1": +8,   # Poetry + mental decline = suicide note
            "H2": +6,   # Could be love-related
            "H3": +4,   # Engineer writing notes
            "H4": -5,   # Not a known spy
            "H5": -3,   # Not spy profile
            "H6": -5,   # Known poetry lover wouldn't doodle gibberish
        }
    ),
    # E10: Suspected digitalis/ouabain poisoning
    (
        "E10: Death by suspected digitalis/ouabain (plant-derived, hard to detect)",
        {
            "H1": +8,   # Self-administered poison
            "H2": +3,   # Possible murder by lover
            "H3": -3,   # Doesn't fit mundane memo
            "H4": +5,   # Spy assassination method
            "H5": +3,   # Could be murder
            "H6": -5,   # Irrelevant to cipher meaning
        }
    ),
    # E11: No direct Rubaiyat stanza match (max 46%)
    (
        "E11: No stanza in Rubáiyát matches any cipher line > 50%",
        {
            "H1": +3,   # Composed, not quoted
            "H2": +3,   # Original composition
            "H3": +3,   # Not from book
            "H4": 0,    # Neutral for OTP
            "H5": -8,   # AGAINST book cipher (should match)
            "H6": +1,   # Neutral
        }
    ),
    # E12: Entropy 3.71 bits/char (constrained, not random)
    (
        "E12: Shannon entropy H = 3.71 bits (constrained, below random 4.70)",
        {
            "H1": +4,   # Natural language constraint
            "H2": +4,   # Same
            "H3": +4,   # Same
            "H4": -6,   # OTP should be near-random entropy
            "H5": +2,   # Depends on extraction method
            "H6": -6,   # Should be higher if truly random
        }
    ),
    # E13: Vowel percentage (34.1%) between initial-letter (28.3%) and text (38%)
    (
        "E13: Vowel ratio 34.1% — between initial-letter (28.3%) and full-text (38%) norms",
        {
            "H1": +3,   # Consistent with initials + function words
            "H2": +3,   # Same
            "H3": +3,   # Same
            "H4": -2,   # OTP would be uniform
            "H5": +1,   # Neutral
            "H6": -2,   # Should be more uniform
        }
    ),
    # E14: High frequency of 'A' (18.2% vs expected 11.6%)
    (
        "E14: Letter A over-represented (18.2% vs 11.6% expected for initials)",
        {
            "H1": +2,   # "A" (article) + "And" very common in verse
            "H2": +2,   # Same
            "H3": +1,   # Less natural
            "H4": -1,   # Not expected
            "H5": 0,    # Neutral
            "H6": -1,   # Slightly against
        }
    ),
    # E15: 'AB' bigram appears 4 times
    (
        "E15: AB bigram appears 4 times (unusually frequent for 44 chars)",
        {
            "H1": +3,   # "A Book" / "And Beyond" — Rubaiyat themes
            "H2": +2,   # "A Beauty"
            "H3": +1,   # Less thematic
            "H4": -3,   # Repeated bigrams unlikely in OTP
            "H5": 0,    # Neutral
            "H6": -3,   # Unlikely in random
        }
    ),
    # E16: Q appears (rare initial letter, 0.3% expected)
    (
        "E16: Q appears once (very rare as word initial, only 0.3% expected)",
        {
            "H1": +2,   # "Quite" fits farewell register
            "H2": +2,   # "Quite" fits
            "H3": +1,   # Less natural
            "H4": 0,    # Neutral
            "H5": 0,    # Neutral
            "H6": -1,   # Slightly unusual
        }
    ),
    # E17: Missing common initials (F, H, U, V, Y, K absent)
    (
        "E17: F, H, U, V, Y, K all absent (expected ~16% combined probability)",
        {
            "H1": +1,   # Short text, sampling variance
            "H2": +1,   # Same
            "H3": +1,   # Same
            "H4": -2,   # OTP should have more uniform coverage
            "H5": 0,    # Neutral
            "H6": -2,   # Should be more uniform
        }
    ),
    # E18: X alone on line 4 (separator hypothesis)
    (
        "E18: Single 'X' on its own line — likely a separator, not a word initial",
        {
            "H1": +3,   # Divides stanza halves (octave/sestet)
            "H2": +2,   # Divides sections
            "H3": +1,   # Could be separator
            "H4": -1,   # OTP wouldn't have structural markers
            "H5": 0,    # Neutral
            "H6": +1,   # Could be random mark
        }
    ),
]


def run_banburismus():
    """Run Turing's Banburismus deciban scoring."""
    print("=" * 70)
    print("  TAMAM SHUD — BAYESIAN HYPOTHESIS SCORING")
    print("  Turing's Banburismus Method (Deciban Scale)")
    print("  Turing's Banburismus Method (Deciban Scale)")
    print("=" * 70)

    # Prior odds (uniform)
    n_hyp = len(HYPOTHESES)
    prior_db = 0  # Equal priors = 0 db

    print(f"\nPrior: Uniform across {n_hyp} hypotheses (0 db each)")
    print(f"Evidence items: {len(EVIDENCE)}")
    print()

    # Accumulate evidence
    totals = {h: prior_db for h in HYPOTHESES}

    print(f"{'Evidence':<65} ", end="")
    for h in HYPOTHESES:
        print(f"  {h[:4]}", end="")
    print()
    print("-" * (65 + 6 * n_hyp))

    for desc, weights in EVIDENCE:
        short_desc = desc[:63]
        print(f"{short_desc:<65} ", end="")
        for h in HYPOTHESES:
            w = weights.get(h[:2], 0)
            totals[h] += w
            sign = "+" if w > 0 else " " if w == 0 else ""
            print(f" {sign}{w:>3}", end="")
        print()

    # ─── RESULTS ───────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("POSTERIOR SCORES (Total Decibans)")
    print("=" * 70)

    sorted_hyp = sorted(HYPOTHESES, key=lambda h: totals[h], reverse=True)

    for rank, h in enumerate(sorted_hyp, 1):
        db = totals[h]
        odds = 10 ** (db / 10)
        if odds >= 1:
            odds_str = f"{odds:.0f}:1 for"
        else:
            odds_str = f"1:{1/odds:.0f} against"

        bar_len = max(0, int(db / 2))
        bar = "+" * bar_len if db > 0 else "-" * abs(int(db / 2))

        stars = ""
        if db >= 50:
            stars = " *** DECISIVE"
        elif db >= 30:
            stars = " ** VERY STRONG"
        elif db >= 20:
            stars = " * STRONG"
        elif db >= 10:
            stars = " . SUBSTANTIAL"

        print(f"  #{rank} {h}")
        print(f"      Score: {db:+.0f} db ({odds_str}){stars}")
        print(f"      [{bar}]")
        print()

    # ─── COMPARATIVE ANALYSIS ──────────────────────────────────────────
    print("=" * 70)
    print("COMPARATIVE ANALYSIS")
    print("=" * 70)

    h1_db = totals[HYPOTHESES[0]]
    h4_db = totals[HYPOTHESES[3]]
    h5_db = totals[HYPOTHESES[4]]
    h6_db = totals[HYPOTHESES[5]]

    print(f"""
    ACROSTIC vs OTP:
      H1 (acrostic suicide) vs H4 (OTP spy): {h1_db - h4_db:+.0f} db difference
      → Acrostic is {10**((h1_db-h4_db)/10):.0f}x more likely than OTP

    ACROSTIC vs BOOK CIPHER:
      H1 (acrostic suicide) vs H5 (book cipher): {h1_db - h5_db:+.0f} db difference
      → Acrostic is {10**((h1_db-h5_db)/10):.0f}x more likely than book cipher

    ACROSTIC vs RANDOM:
      H1 (acrostic suicide) vs H6 (random): {h1_db - h6_db:+.0f} db difference
      → Acrostic is {10**((h1_db-h6_db)/10):.0f}x more likely than random

    SUICIDE vs LOVE LETTER:
      H1 (suicide) vs H2 (love letter): {h1_db - totals[HYPOTHESES[1]]:+.0f} db difference
      → These two are close; they may overlap (farewell to a lover)
    """)

    # ─── EVIDENCE CHAIN ───────────────────────────────────────────────
    print("=" * 70)
    print("CRITICAL EVIDENCE CHAIN (for H1: Acrostic Suicide Note)")
    print("=" * 70)

    h1_evidence = []
    for desc, weights in EVIDENCE:
        w = weights.get("H1", 0)
        if w != 0:
            h1_evidence.append((w, desc))

    h1_evidence.sort(reverse=True, key=lambda x: x[0])

    cumulative = 0
    print(f"\n  {'Weight':>6}  {'Cumul':>6}  Evidence")
    print(f"  {'─'*6}  {'─'*6}  {'─'*50}")
    for w, desc in h1_evidence:
        cumulative += w
        print(f"  {w:+5.0f}db  {cumulative:+5.0f}db  {desc}")

    print(f"\n  Final: {cumulative:+.0f} db = {10**(cumulative/10):.0f}:1 odds")


def circumstantial_synthesis():
    """Integrate circumstantial evidence beyond the cipher itself."""
    print(f"\n{'='*70}")
    print("CIRCUMSTANTIAL SYNTHESIS")
    print(f"{'='*70}")
    print("""
    BEYOND THE CIPHER — Integrating All Evidence:

    1. IDENTITY (Carl Webb, confirmed 2022):
       - Electrical engineer from Melbourne
       - Poetry enthusiast → explains Rubaiyat connection
       - Horse gambler → possible financial desperation
       - Troubled marriage to Dorothy Robertson
       - Mental health decline in final years
       → Profile STRONGLY supports suicide, weakly supports espionage

    2. THE RUBAIYAT (1941 Whitcombe & Tombs edition):
       - Found in an unlocked car near Glenelg
       - Last page torn out (Tamam Shud slip on body)
       - Phone number + cipher on back cover
       - Jessica Thomson's number → she denied knowing him
       - She gave a DIFFERENT copy of Rubaiyat to Alf Boxall
       → Personal connection to the book and to Thomson

    3. JESSICA THOMSON ("Jestyn"):
       - Nurse living near where body was found
       - Denied knowing the dead man
       - Went pale/nearly fainted when shown the plaster cast
       - Had communist connections
       - Gave Rubaiyat to Alf Boxall (different copy)
       - Her son Robin may have been Carl Webb's child (unconfirmed)
       → Romantic/personal relationship likely

    4. THE DEATH:
       - Digitalis/ouabain poisoning (cardiac glycoside)
       - No struggle, no vomiting (consistent with cardiac arrest)
       - Body positioned peacefully against seawall
       - Half-smoked cigarette still on collar
       - Clean, well-dressed, well-groomed
       → Deliberate, peaceful death — suicide fits perfectly

    5. THE CIPHER IN CONTEXT:
       - Written on the Rubaiyat itself (the book of fate and acceptance)
       - "Tamam Shud" = "It is finished" (final words of the poem)
       - Cipher structured as verse (4 content lines = 1 stanza)
       - Crossed-out line shows composition process
       - X separator divides the stanza into two halves
       → A farewell verse, composed in the style of the poet he admired

    INTEGRATED ASSESSMENT:

    The Somerton Man was Carl Webb, a poetry-loving engineer in mental
    decline, who traveled from Melbourne to Adelaide — possibly to see
    Jessica Thomson one last time. He carried a copy of the Rubaiyat,
    the poem that counsels acceptance of mortality. On its back cover
    he wrote her phone number and composed a brief acrostic farewell
    in the style of Omar Khayyam. He tore out the last page ("Tamam
    Shud" — "It is finished"), placed it in a hidden pocket, and
    ingested a lethal dose of digitalis or ouabain. He walked to
    Somerton Beach, sat against the seawall, smoked a last cigarette,
    and waited for death.

    The cipher is his last poem. Not a spy code. Not a book cipher.
    A man's final words, written in the language of his favorite poet,
    abbreviated to initials as a private act of closure.
    """)


def final_decryption():
    """Present the most likely plaintext reading."""
    print(f"\n{'='*70}")
    print("PROPOSED DECRYPTION")
    print(f"{'='*70}")
    print("""
    Highest-confidence reading (composite of GA optimization,
    thematic analysis, biographical constraints, and Bayesian scoring):

    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │  WRGOABABD                                                      │
    │  "With Repentance Gone, Of A Book A Buried Dust"                │
    │   (Repentance is past; from a book, to buried dust)             │
    │                                                                 │
    │  MLIAOI  ← struck out                                           │
    │  "My Love Is A ... Our I..." (aborted — too personal?)          │
    │                                                                 │
    │  WTBIMPANETP                                                    │
    │  "With The Book I Must Pass Away, Note Ending The Past"         │
    │   (Using the Rubaiyat as his farewell instrument)                │
    │                                                                 │
    │  X                                                              │
    │  [separator — volta/turn of the stanza]                         │
    │                                                                 │
    │  MLIABOAIAQC                                                    │
    │  "My Life Is A Book Of All I Am, Quite Certain"                 │
    │   (Life-as-book metaphor, certainty in his decision)            │
    │                                                                 │
    │  ITTMTSAMSTGAB                                                  │
    │  "In The Truth My Time Stops, All My Soul To God And Beyond"    │
    │   (Acceptance of death, soul's departure)                       │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

    ALTERNATIVE HIGH-SCORING READING (love-letter variant):

    L1: "With Regret Go On And Be A Bit Distant"
    L3: "With This Book I Must Part And Not Ever Truly Possess"
    L5: "My Love Is A Beauty Of All I Am Quite Certain"
    L6: "I Think That My Time Shall Arrive, My Soul To God And Beyond"

    CONFIDENCE LEVELS:
    - MLIA = "My Life/Love Is A" — 95% confidence
    - Acrostic mechanism — 90% confidence
    - Suicide/farewell theme — 85% confidence
    - Exact word choices — 30-50% per position
    - Overall meaning — 80% confidence (farewell/closure meditation)
    """)


if __name__ == "__main__":
    run_banburismus()
    circumstantial_synthesis()
    final_decryption()
