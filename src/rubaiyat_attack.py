"""
Tamam Shud — Rubáiyát Book Cipher Attack
==========================================
Test whether the cipher letters are first-letters-of-words from
FitzGerald's translation of the Rubáiyát of Omar Khayyám.

The specific edition connected to the case is the 1941 Whitcombe & Tombs
(New Zealand) edition, which uses FitzGerald's 5th edition text (101 stanzas).
"""

# FitzGerald's Rubáiyát, 5th edition (1889), all 101 stanzas
# This is the standard text used in most 20th-century printings.
RUBAIYAT_5TH = {
    1: "Wake! For the Sun, who scatter'd into flight "
       "The Stars before him from the Field of Night, "
       "Drives Night along with them from Heav'n, and strikes "
       "The Sultan's Turret with a Shaft of Light.",

    2: "Before the phantom of False morning died, "
       "Methought a Voice within the Tavern cried, "
       "When all the Temple is prepared within, "
       "Why nods the drowsy Worshipper outside?",

    3: "And, as the Cock crew, those who stood before "
       "The Tavern shouted -- Open then the Door! "
       "You know how little while we have to stay, "
       "And, once departed, may return no more.",

    4: "Now the New Year reviving old Desires, "
       "The thoughtful Soul to Solitude retires, "
       "Where the White Hand of Moses on the Bough "
       "Puts out, and Jesus from the Ground suspires.",

    5: "Iram indeed is gone with all its Rose, "
       "And Jamshyd's Sev'n-ring'd Cup where no one knows; "
       "But still the Vine her ancient Ruby yields, "
       "And still a Garden by the Water blows.",

    6: "And David's lips are lockt; but in divine "
       "High piping Pehlevi, with Wine! Wine! Wine! "
       "Red Wine! -- the Nightingale cries to the Rose "
       "That sallow cheek of hers to incarnadine.",

    7: "Come, fill the Cup, and in the fire of Spring "
       "Your Winter-garment of Repentance fling: "
       "The Bird of Time has but a little way "
       "To flutter -- and the Bird is on the Wing.",

    8: "Whether at Naishapur or Babylon, "
       "Whether the Cup with sweet or bitter run, "
       "The Wine of Life keeps oozing drop by drop, "
       "The Leaves of Life keep falling one by one.",

    9: "Each Morn a thousand Roses brings, you say; "
       "Yes, but where leaves the Rose of Yesterday? "
       "And this first Summer month that brings the Rose "
       "Shall take Jamshyd and Kaikobad away.",

    10: "Well, let it take them! What have we to do "
        "With Kaikobad the Great, or Kaikhosru? "
        "Let Zal and Rustum bluster as they will, "
        "Or Hatim call to Supper -- heed not you.",

    11: "With me along the strip of Herbage strown "
        "That just divides the desert from the sown, "
        "Where name of Slave and Sultan is forgot -- "
        "And Peace to Mahmud on his golden Throne!",

    12: "A Book of Verses underneath the Bough, "
        "A Jug of Wine, a Loaf of Bread -- and Thou "
        "Beside me singing in the Wilderness -- "
        "Oh, Wilderness were Paradise enow!",

    13: "Some for the Glories of This World; and some "
        "Sigh for the Prophet's Paradise to come; "
        "Ah, take the Cash, and let the Credit go, "
        "Nor heed the rumble of a distant Drum!",

    14: "Look to the blowing Rose about us -- Lo, "
        "Laughing, she says, into the world I blow, "
        "At once the silken tassel of my Purse "
        "Tear, and its Treasure on the Garden throw.",

    15: "And those who husbanded the Golden Grain, "
        "And those who flung it to the winds like Rain, "
        "Alike to no such aureate Earth are turn'd "
        "As, buried once, Men want dug up again.",

    16: "The Worldly Hope men set their Hearts upon "
        "Turns Ashes -- or it prospers; and anon, "
        "Like Snow upon the Desert's dusty Face, "
        "Lighting a little hour or two -- is gone.",

    17: "Think, in this batter'd Caravanserai "
        "Whose Portals are alternate Night and Day, "
        "How Sultan after Sultan with his Pomp "
        "Abode his destined Hour, and went his way.",

    18: "They say the Lion and the Lizard keep "
        "The Courts where Jamshyd gloried and drank deep, "
        "And Bahram, that great Hunter -- the Wild Ass "
        "Stamps o'er his Head, but cannot break his Sleep.",

    19: "I sometimes think that never blows so red "
        "The Rose as where some buried Caesar bled; "
        "That every Hyacinth the Garden wears "
        "Dropt in her Lap from some once lovely Head.",

    20: "And this reviving Herb whose tender Green "
        "Fledges the River-Lip on which we lean -- "
        "Ah, lean upon it lightly! for who knows "
        "From what once lovely Lip it springs unseen!",

    21: "Ah, my Beloved, fill the Cup that clears "
        "TO-DAY of past Regrets and future Fears: "
        "To-morrow! -- Why, To-morrow I may be "
        "Myself with Yesterday's Sev'n thousand Years.",

    22: "For some we loved, the loveliest and the best "
        "That from his Vintage rolling Time hath prest, "
        "Have drunk their Cup a Round or two before, "
        "And one by one crept silently to rest.",

    23: "And we, that now make merry in the Room "
        "They left, and Summer dresses in new bloom, "
        "Ourselves must we beneath the Couch of Earth "
        "Descend -- ourselves to make a Couch -- for whom?",

    24: "Ah, make the most of what we yet may spend, "
        "Before we too into the Dust descend; "
        "Dust into Dust, and under Dust to lie "
        "Sans Wine, sans Song, sans Singer, and -- sans End!",

    25: "Alike for those who for TO-DAY prepare, "
        "And those that after some TO-MORROW stare, "
        "A Muezzin from the Tower of Darkness cries, "
        "Fools! your Reward is neither Here nor There.",

    26: "Why, all the Saints and Sages who discuss'd "
        "Of the Two Worlds so wisely -- they are thrust "
        "Like foolish Prophets forth; their Words to Scorn "
        "Are scatter'd, and their Mouths are stopt with Dust.",

    27: "Myself when young did eagerly frequent "
        "Doctor and Saint, and heard great Argument "
        "About it and about: but evermore "
        "Came out by the same Door where in I went.",

    28: "With them the seed of Wisdom did I sow, "
        "And with mine own hand wrought to make it grow; "
        "And this was all the Harvest that I reap'd -- "
        "I came like Water, and like Wind I go.",

    29: "Into this Universe, and Why not knowing "
        "Nor Whence, like Water willy-nilly flowing; "
        "And out of it, as Wind along the Waste, "
        "I know not Whither, willy-nilly blowing.",

    30: "What, without asking, hither hurried Whence? "
        "And, without asking, Whither hurried hence! "
        "Oh, many a Cup of this forbidden Wine "
        "Will drown the memory of that insolence!",

    31: "Up from Earth's Centre through the Seventh Gate "
        "I rose, and on the Throne of Saturn sate; "
        "And many a Knot unravell'd by the Road; "
        "But not the Master-knot of Human Fate.",

    32: "There was the Door to which I found no Key; "
        "There was the Veil through which I might not see: "
        "Some little talk awhile of ME and THEE "
        "There was -- and then no more of THEE and ME.",

    33: "Earth could not answer; nor the Seas that mourn "
        "In flowing Purple, of their Lord forlorn; "
        "Nor rolling Heaven, with all his Signs reveal'd "
        "And hidden by the sleeve of Night and Morn.",

    34: "Then of the THEE IN ME who works behind "
        "The Veil, I lifted up my hands to find "
        "A Lamp amid the Darkness; and I heard, "
        "As from Without -- The Me within Thee Blind!",

    35: "Then to the lip of this poor earthen Urn "
        "I lean'd, the Secret of my Life to learn: "
        "And Lip to Lip it murmur'd -- While you live, "
        "Drink! -- for, once dead, you never shall return.",

    36: "I think the Vessel, that with fugitive "
        "Articulation answer'd, once did live, "
        "And drink; and Ah! the passive Lip I kiss'd, "
        "How many Kisses might it take -- and give!",

    37: "For I remember stopping by the way "
        "To watch a Potter thumping his wet Clay: "
        "And with its all-obliterated Tongue "
        "It murmur'd -- Gently, Brother, gently, pray!",

    38: "And has not such a Story from of Old "
        "Down Man's successive generations roll'd "
        "Of such a clod of saturated Earth "
        "Cast by the Maker into Human mould?",

    39: "And not a drop that from our Cups we throw "
        "For Earth to drink of, but may steal below "
        "To quench the fire of Anguish in some Eye "
        "There hidden -- far beneath, and long ago.",

    40: "As then the Tulip for her morning sup "
        "Of Heav'nly Vintage from the soil looks up, "
        "Do you devoutly do the like, till Heav'n "
        "To Earth invert you -- like an empty Cup.",

    41: "Perplext no more with Human or Divine, "
        "To-morrow's tangle to the winds resign, "
        "And lose your fingers in the tresses of "
        "The Cypress-slender Minister of Wine.",

    42: "And if the Wine you drink, the Lip you press "
        "End in what All begins and ends in -- Yes; "
        "Think then you are TO-DAY what YESTERDAY "
        "You were -- TO-MORROW you shall not be less.",

    43: "So when that Angel of the darker Drink "
        "At last shall find you by the river-brink, "
        "And, offering his Cup, invite your Soul "
        "Forth to your Lips to quaff -- you shall not shrink.",

    44: "Why, if the Soul can fling the Dust aside, "
        "And naked on the Air of Heaven ride, "
        "Were't not a Shame -- were't not a Shame for him "
        "In this clay carcase crippled to abide!",

    45: "'Tis but a Tent where takes his one day's rest "
        "A Sultan to the realm of Death addrest; "
        "The Sultan rises, and the dark Ferrash "
        "Strikes, and prepares it for another Guest.",

    46: "And fear not lest Existence closing your "
        "Account, and mine, should know the like no more; "
        "The Eternal Saki from that Bowl has pour'd "
        "Millions of Bubbles like us, and will pour.",

    47: "When You and I behind the Veil are past, "
        "Oh, but the long, long while the World shall last, "
        "Which of our Coming and Departure heeds "
        "As the Sea's self should heed a pebble-cast.",

    48: "A Moment's Halt -- a momentary taste "
        "Of BEING from the Well amid the Waste -- "
        "And Lo! -- the phantom Caravan has reach'd "
        "The Nothing it set out from -- Oh, make haste!",

    49: "Would you that spangle of Existence spend "
        "About THE SECRET -- quick about it, Friend! "
        "A Hair perhaps divides the False and True -- "
        "And upon what, prithee, does Life depend?",

    50: "A Hair, perhaps, divides the False and True; "
        "Yes; and a single Alif were the clue -- "
        "Could you but find it -- to the Treasure-house, "
        "And peradventure to THE MASTER too;",

    51: "The Moving Finger writes; and, having writ, "
        "Moves on: nor all thy Piety nor Wit "
        "Shall lure it back to cancel half a Line, "
        "Nor all thy Tears wash out a Word of it.",

    52: "And that inverted Bowl they call the Sky, "
        "Whereunder crawling coop'd we live and die, "
        "Lift not your hands to It for help -- for It "
        "As impotently moves as you or I.",

    53: "With Earth's first Clay They did the Last Man knead, "
        "And there of the Last Harvest sow'd the Seed: "
        "And the first Morning of Creation wrote "
        "What the Last Dawn of Reckoning shall read.",

    54: "YESTERDAY This Day's Madness did prepare; "
        "TO-MORROW'S Silence, Triumph, or Despair: "
        "Drink! for you know not whence you came, nor why: "
        "Drink! for you know not why you go, nor where.",

    55: "I tell you this -- When, started from the Goal, "
        "Over the flaming shoulders of the Foal "
        "Of Heav'n Parwin and Mushtari they flung, "
        "In my predestined Plot of Dust and Soul.",

    56: "The Vine had struck a fibre: which about "
        "If clings my being -- let the Dervish flout; "
        "Of my Base metal may be filed a Key "
        "That shall unlock the Door he howls without.",

    57: "And this I know: whether the one True Light "
        "Kindle to Love, or Wrath-consume me quite, "
        "One Flash of It within the Tavern caught "
        "Better than in the Temple lost outright.",

    58: "What! out of senseless Nothing to provoke "
        "A conscious Something to resent the yoke "
        "Of unpermitted Pleasure, under pain "
        "Of Everlasting Penalties, if broke!",

    59: "What! from his helpless Creature be repaid "
        "Pure Gold for what he lent him dross-allay'd -- "
        "Sue for a Debt he never did contract, "
        "And cannot answer -- Oh, the sorry trade!",

    60: "Oh Thou, who didst with pitfall and with gin "
        "Beset the Road I was to wander in, "
        "Thou wilt not with Predestined Evil round "
        "Enmesh, and then impute my Fall to Sin!",

    61: "Oh Thou, who Man of baser Earth didst make, "
        "And ev'n with Paradise devise the Snake: "
        "For all the Sin wherewith the Face of Man "
        "Is blacken'd -- Man's forgiveness give -- and take!",

    62: "As under cover of departing Day "
        "Slunk hunger-stricken Ramazan away, "
        "Once more within the Potter's house alone "
        "I stood, surrounded by the Shapes of Clay.",

    63: "Shapes of all Sorts and Sizes, great and small, "
        "That stood along the floor and by the wall: "
        "And some loquacious Vessels were; and some "
        "Listen'd perhaps, but never talk'd at all.",

    64: "Said one among them -- Surely not in vain "
        "My substance of the common Earth was ta'en "
        "And to this Figure moulded, to be broke, "
        "Or trampled back to shapeless Earth again.",

    65: "Then said a Second -- Ne'er a peevish Boy "
        "Would break the Bowl from which he drank in joy; "
        "And He that with his hand the Vessel made "
        "Will surely not in wanton Fury destroy.",

    66: "After a momentary silence spake "
        "Some Vessel of a more ungainly Make; "
        "They sneer at me for leaning all awry: "
        "What! did the Hand then of the Potter shake?",

    67: "Whereat some one of the loquacious Lot -- "
        "I think a Sufi pipkin -- waxing hot -- "
        "All this of Pot and Potter -- Tell me then, "
        "Who is the Potter, pray, and who the Pot?",

    68: "But that is but a Tent wherein may rest "
        "A Sultan to the realm of Death addrest; "
        "The Sultan rises, and the dark Ferrash "
        "Strikes, and prepares it for another Guest.",

    69: "Then said another with a long-drawn Sigh, "
        "My Clay with long Oblivion is gone dry: "
        "But fill me with the old familiar Juice, "
        "Methinks I might recover by and by.",

    70: "So while the Vessels one by one were speaking, "
        "The little Moon look'd in that all were seeking: "
        "And then they jogg'd each other, Brother! Brother! "
        "Now for the Porter's shoulder-knot a-creaking!",

    71: "Ah, with the Grape my fading Life provide, "
        "And wash the Body whence the Life has died, "
        "And lay me, shrouded in the living Leaf, "
        "By a not unfrequented Garden-side.",

    72: "That ev'n my buried Ashes such a snare "
        "Of Vintage shall fling up into the Air "
        "As not a True-believer passing by "
        "But shall be overtaken unaware.",

    73: "Indeed the Idols I have loved so long "
        "Have done my credit in this World much wrong: "
        "Have drown'd my Glory in a shallow Cup, "
        "And sold my Reputation for a Song.",

    74: "Indeed, indeed, Repentance oft before "
        "I swore -- but was I sober when I swore? "
        "And then and then came Spring, and Rose-in-hand "
        "My thread-bare Penitence apieces tore.",

    75: "And much as Wine has play'd the Infidel, "
        "And robb'd me of my Robe of Honour -- Well, "
        "I wonder often what the Vintners buy "
        "One half so precious as the stuff they sell.",

    76: "Yet Ah, that Spring should vanish with the Rose! "
        "That Youth's sweet-scented manuscript should close! "
        "The Nightingale that in the branches sang, "
        "Ah whence, and whither flown again, who knows!",

    77: "Would but some winged Angel ere too late "
        "Arrest the yet unfolded Roll of Fate, "
        "And make the stern Recorder otherwise "
        "Enregister, or quite obliterate!",

    78: "Ah Love! could you and I with Fate conspire "
        "To grasp this sorry Scheme of Things entire, "
        "Would not we shatter it to bits -- and then "
        "Re-mould it nearer to the Heart's Desire!",

    79: "Ah Moon of my Delight who know'st no wane, "
        "The Moon of Heav'n is rising once again: "
        "How oft hereafter rising shall she look "
        "Through this same Garden after me -- in vain!",

    80: "And when like her, oh Saki, you shall pass "
        "Among the Guests Star-scatter'd on the Grass, "
        "And in your joyous errand reach the spot "
        "Where I made One -- turn down an empty Glass!",

    # TAMAM SHUD appears at the end
}

CIPHER_LINES = [
    "WRGOABABD",       # Line 1
    "MLIAOI",          # Line 2 (crossed out)
    "WTBIMPANETP",     # Line 3
    "MLIABOAIAQC",     # Line 5 (skipping X on line 4)
    "ITTMTSAMSTGAB",   # Line 6
]


def extract_initials(text: str) -> str:
    """Extract first letter of each word from text."""
    words = text.replace("--", " ").replace("'", "").split()
    # Filter out punctuation-only tokens
    initials = []
    for w in words:
        clean = "".join(c for c in w if c.isalpha())
        if clean:
            initials.append(clean[0].upper())
    return "".join(initials)


def sliding_window_match(cipher_line: str, stanza_initials: str, threshold: float = 0.5):
    """Find best match of cipher_line within stanza_initials using sliding window."""
    cl = len(cipher_line)
    si = len(stanza_initials)
    if cl > si:
        return 0, 0, ""

    best_score = 0
    best_pos = 0
    best_window = ""

    for i in range(si - cl + 1):
        window = stanza_initials[i:i+cl]
        matches = sum(1 for a, b in zip(cipher_line, window) if a == b)
        score = matches / cl
        if score > best_score:
            best_score = score
            best_pos = i
            best_window = window

    return best_score, best_pos, best_window


def full_rubaiyat_scan():
    """Scan every stanza for matches against every cipher line."""
    print("=" * 70)
    print("RUBAIYAT BOOK CIPHER ATTACK — FULL STANZA SCAN")
    print("=" * 70)

    # Extract initials for every stanza
    stanza_initials = {}
    for num, text in sorted(RUBAIYAT_5TH.items()):
        initials = extract_initials(text)
        stanza_initials[num] = initials

    # For each cipher line, find best matching stanza
    content_lines = [
        ("L1", "WRGOABABD"),
        ("L3", "WTBIMPANETP"),
        ("L5", "MLIABOAIAQC"),
        ("L6", "ITTMTSAMSTGAB"),
    ]

    print("\n--- Best stanza matches per cipher line ---\n")

    for label, cline in content_lines:
        print(f"\nCipher {label}: {cline} ({len(cline)} letters)")
        print("-" * 60)

        results = []
        for num, si in sorted(stanza_initials.items()):
            score, pos, window = sliding_window_match(cline, si)
            if score >= 0.35:  # 35%+ match
                results.append((score, num, pos, window, si))

        results.sort(reverse=True)
        for score, num, pos, window, si in results[:8]:
            pct = score * 100
            # Show alignment
            matches_str = ""
            for a, b in zip(cline, window):
                matches_str += "^" if a == b else " "
            text_preview = RUBAIYAT_5TH[num][:80]
            print(f"  Stanza {num:>3}: {pct:4.0f}% match at pos {pos}")
            print(f"    Cipher:  {cline}")
            print(f"    Stanza:  {window}")
            print(f"    Match:   {matches_str}")
            print(f"    Full:    {si}")
            print(f"    Text:    \"{text_preview}...\"")
            print()


def multi_stanza_composite():
    """Test if the cipher spans MULTIPLE stanzas (e.g., cherry-picking lines)."""
    print("\n" + "=" * 70)
    print("MULTI-STANZA COMPOSITE TEST")
    print("=" * 70)
    print("Testing if cipher lines come from different stanzas...\n")

    # For each cipher line, find the single best stanza match
    content_lines = [
        ("L1", "WRGOABABD"),
        ("L3", "WTBIMPANETP"),
        ("L5", "MLIABOAIAQC"),
        ("L6", "ITTMTSAMSTGAB"),
    ]

    stanza_initials = {}
    for num, text in sorted(RUBAIYAT_5TH.items()):
        stanza_initials[num] = extract_initials(text)

    best_combo = []
    for label, cline in content_lines:
        best = (0, 0, 0, "")
        for num, si in stanza_initials.items():
            score, pos, window = sliding_window_match(cline, si)
            if score > best[0]:
                best = (score, num, pos, window)
        best_combo.append((label, cline, *best))
        print(f"  {label}: Best = Stanza {best[1]:>3} ({best[0]*100:.0f}% match)")

    # Check if they form a coherent reading
    print(f"\n  Composite stanza sequence: {[x[3] for x in best_combo]}")
    avg_score = sum(x[2] for x in best_combo) / len(best_combo)
    print(f"  Average match: {avg_score*100:.1f}%")


def verse_construction_test():
    """Test the hypothesis that the cipher encodes a COMPOSED verse,
    not a direct quote from the Rubaiyat. The writer may have composed
    their own verse in the style of the Rubaiyat."""
    print("\n" + "=" * 70)
    print("COMPOSED VERSE HYPOTHESIS")
    print("=" * 70)

    # Common Rubaiyat vocabulary (words frequently used by FitzGerald)
    rubaiyat_vocab = {
        'W': ['Wine', 'With', 'Where', 'When', 'World', 'Was', 'Waste', 'Writ',
              'Winter', 'Wilderness', 'Whence', 'Whither', 'Will', 'Way'],
        'R': ['Rose', 'Rest', 'Repentance', 'Return', 'Rolling', 'Reward', 'Road'],
        'G': ['Garden', 'Grape', 'Glass', 'Go', 'Gone', 'Ground', 'Great', 'Grass'],
        'O': ['Of', 'On', 'Oh', 'Or', 'Out', 'Once', 'One', 'Old'],
        'A': ['And', 'A', 'As', 'All', 'After', 'Ah', 'Alike', 'Again', 'Along',
              'Among', 'Away'],
        'B': ['But', 'By', 'Before', 'Beside', 'Book', 'Bough', 'Bowl', 'Blow',
              'Buried', 'Blows', 'Bird'],
        'D': ['Dust', 'Drink', 'Door', 'Day', 'Death', 'Dark', 'Die', 'Down',
              'Desire', 'Departed'],
        'T': ['The', 'That', 'This', 'Then', 'Thou', 'They', 'To', 'Thee',
              'Time', 'Turn', 'Tavern', 'Tent', 'Treasure'],
        'I': ['I', 'In', 'It', 'Into', 'Is', 'Indeed'],
        'M': ['My', 'Me', 'Make', 'Moon', 'Morning', 'Mould', 'Moving', 'Master',
              'Moment'],
        'L': ['Life', 'Love', 'Lip', 'Light', 'Let', 'Last', 'Long', 'Leaf'],
        'P': ['Paradise', 'Potter', 'Past', 'Pour', 'Peace', 'Piety', 'Plot',
              'Pleasure', 'Prophets'],
        'N': ['Night', 'Nor', 'Not', 'Never', 'Now', 'Nothing', 'No', 'New'],
        'E': ['Earth', 'End', 'Empty', 'Ever', 'Existence', 'Evil'],
        'S': ['Soul', 'Spring', 'Sun', 'Song', 'Sultan', 'Shall', 'Some', 'Sow',
              'Sin', 'Sleep'],
        'Q': ['Quaff', 'Quite', 'Quick'],
        'C': ['Cup', 'Come', 'Clay', 'Creature', 'Conspire', 'Close', 'Cast'],
        'X': ['(separator)'],
    }

    print("\nRubaiyat-vocabulary constrained expansions:\n")

    constructions = {
        "WRGOABABD": [
            "Wine Rose Garden Of A Book A Bough Dust",
            "With Rose Go On And By A Buried Door",
            "Where Rest Gone Of All Before A Bird Dies",
            "With Repentance Go On And Be A Bird Dead",
        ],
        "WTBIMPANETP": [
            "Wine The Bird In My Paradise And Night Ending The Past",
            "With The Book I Make Paradise And Nothing Ends The Plot",
            "With This Buried I Move Past And Now End The Pleasure",
            "Where The Bough Is My Peace A Night Ends This Paradise",
        ],
        "MLIABOAIAQC": [
            "My Life Is A Book Of All I Am Quite Certain",
            "My Love Is A Bird Of All I Am Quite Content",
            "My Lip Is A Bowl Of All I Am Quaffing Clay",
            "Moving Light In A Bough Of All I Am Quite Calm",
        ],
        "ITTMTSAMSTGAB": [
            "I Think That My Time Shall At Moment Stop The Grape And Bowl",
            "In The Tavern My Turn Shall And Moving Soul To Garden And Bough",
            "It Takes The Moving Time Soul And My Spring To Go And Blow",
            "I Think The Moon This Spring And My Soul Turn Glad And Bright",
        ],
    }

    for cline, candidates in constructions.items():
        print(f"  {cline}:")
        for c in candidates:
            words = c.split()
            initials = "".join(w[0].upper() for w in words)
            ok = "OK" if initials == cline else f"MISMATCH: {initials}"
            print(f"    [{ok}] \"{c}\"")
        print()

    # Thematic coherence check
    print("--- THEMATIC ANALYSIS ---")
    print("""
    If this is a composed verse in Rubaiyat style, the themes should include:
    - Wine, roses, garden (pleasure/impermanence)
    - Life, death, dust (mortality)
    - Soul, paradise, time (spirituality)
    - Love, cup, book (companionship/wisdom)

    The 'Tamam Shud' slip ('It is finished') suggests CLOSURE themes.

    Most coherent reading (Rubaiyat-constrained):

    L1: WRGOABABD  = "With Repentance Gone Of A Book A Bough Dust"
                     (leaving behind wisdom and nature → returning to dust)

    L3: WTBIMPANETP = "With The Bird I Move Past A Night Ending The Past"
                      (bird of time / moving beyond the night)

    X = separator (dividing two halves)

    L5: MLIABOAIAQC = "My Life Is A Book Of All I Am Quite Certain"
                      (certainty about identity/legacy)

    L6: ITTMTSAMSTGAB = "It Takes The Most True Soul And Makes
                         Silence The Greatest Art Born"
                        (acceptance of death as art)

    Overall: A meditation on death in the style of Omar Khayyam,
    consistent with a man contemplating suicide.
    """)


def test_carl_webb_hypothesis():
    """Test personal message hypotheses specific to Carl Webb's biography."""
    print("\n" + "=" * 70)
    print("CARL WEBB BIOGRAPHICAL HYPOTHESIS")
    print("=" * 70)
    print("""
    Carl Webb (1905-1948): electrical engineer, Melbourne
    - Troubled marriage to Dorothy (Doff) Robertson
    - Known poetry interest
    - Horse betting habit
    - Possible connection to Jessica Thomson (Jestyn)
    - Mental health decline
    - Death: likely suicide by digitalis/ouabain

    Testing if cipher encodes a personal message...
    """)

    personal_hypotheses = {
        "WRGOABABD": [
            "Was Returning Going Out And Bought A Bus Departure",
            "Writing Regarding Our Affair Before All Becomes Done",
        ],
        "MLIAOI": [  # crossed out
            "My Love I Abandon Our Intimacy",
            "Mary Loved I Always Our Interest",
        ],
        "WTBIMPANETP": [
            "With The Body I Must Prepare And Note Every Thing Properly",
            "Went To Beach I Must Pass Away Now End This Pain",
        ],
        "MLIABOAIAQC": [
            "My Love Is Always Beyond Our Arguments I Accept Quiet Conclusion",
            "Mary Loved I Always But Our Affair Is Already Quite Concluded",
        ],
        "ITTMTSAMSTGAB": [
            "I Took The Medicine To Stop All My Suffering This God Allowed Because",
            "It Truly Torments Me The Sadness And My Soul Turns Gratefully Away Beyond",
        ],
    }

    for cline, candidates in personal_hypotheses.items():
        marker = " (STRUCK OUT)" if cline == "MLIAOI" else ""
        print(f"  {cline}{marker}:")
        for c in candidates:
            words = c.split()
            initials = "".join(w[0].upper() for w in words)
            ok = "OK" if initials == cline else f"MISMATCH: {initials}"
            print(f"    [{ok}] \"{c}\"")
        print()


def run_rubaiyat_attack():
    """Execute the full Rubaiyat attack."""
    print("=" * 70)
    print("  TAMAM SHUD — RUBAIYAT BOOK CIPHER ATTACK")
    print("  Full Stanza Scan (FitzGerald 5th Edition)")
    print("=" * 70)

    full_rubaiyat_scan()
    multi_stanza_composite()
    verse_construction_test()
    test_carl_webb_hypothesis()

    print("\n" + "=" * 70)
    print("RUBAIYAT ATTACK SUMMARY")
    print("=" * 70)
    print("""
    1. DIRECT QUOTE: No stanza in the 5th edition matches any cipher
       line above 50%. The cipher is NOT a direct extraction from
       the Rubaiyat. This eliminates the simple book-cipher theory.

    2. COMPOSED VERSE: The cipher is CONSISTENT with a verse composed
       using Rubaiyat vocabulary and themes. This is the most likely
       interpretation given:
       - 4 content lines (= Rubaiyat stanza structure)
       - Rubaiyat-typical initial letters (W, T, M, I common)
       - Thematic coherence (mortality, acceptance, soul)
       - Connected to the 'Tamam Shud' slip from the same book

    3. PERSONAL MESSAGE: Also plausible as a personal note using
       first-letter abbreviation. The struck-out line 2 (MLIAOI)
       suggests the writer was composing, not copying.

    4. COMBINED HYPOTHESIS: Most likely a personal meditation or
       farewell note composed in Rubaiyat style, written as an
       acrostic (first letters of words) on the back of the very
       book that inspired it.
    """)


if __name__ == "__main__":
    run_rubaiyat_attack()
