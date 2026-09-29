import os
import json
import time
import random

SAVE_FILE = "kingdom_of_ash_save.json"


# ============================================================
#                    UTILITY FUNCTIONS
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress ENTER to continue...")


def slow(text, delay=0.012):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def title(text):
    clear()
    print("=" * 72)
    print(text.center(72))
    print("=" * 72)
    print()


def choose(prompt, options):
    while True:
        print()
        print(prompt)

        for i, option in enumerate(options, 1):
            print(f"  [{i}] {option}")

        answer = input("\n> ").strip()

        if answer.isdigit():
            number = int(answer)
            if 1 <= number <= len(options):
                return number

        print("Please enter one of the listed numbers.")


def wait():
    time.sleep(0.8)


# ============================================================
#                    PLAYER DATA
# ============================================================

def new_game():
    return {
        "chapter": 1,
        "name": "",
        "health": 100,
        "gold": 20,

        "strength": 1,
        "cunning": 1,
        "honor": 1,

        "inventory": [],

        "met_mara": False,
        "trusted_mara": False,
        "helped_mara": False,

        "knows_secret": False,
        "has_ring": False,
        "has_sword": False,
        "has_letter": False,

        "saved_villager": False,
        "saved_knight": False,
        "killed_knight": False,

        "allied_wolves": False,
        "allied_rebels": False,
        "allied_crown": False,

        "betrayed_crown": False,
        "betrayed_rebels": False,

        "ghost_warning": False,
        "opened_crypt": False,

        "duel_won": False,
        "dragon_awakened": False,

        "ending": None
    }


# ============================================================
#                    SAVE / LOAD
# ============================================================

def save_game(game):
    with open(SAVE_FILE, "w") as file:
        json.dump(game, file, indent=4)

    print("\nGame saved.")


def load_game():
    if not os.path.exists(SAVE_FILE):
        print("\nNo save file exists.")
        pause()
        return None

    try:
        with open(SAVE_FILE, "r") as file:
            game = json.load(file)

        print("\nGame loaded.")
        pause()
        return game

    except Exception:
        print("\nThe save file could not be loaded.")
        pause()
        return None


# ============================================================
#                    STATUS SCREEN
# ============================================================

def status(game):
    title("CHARACTER")

    print(f"Name:       {game['name']}")
    print(f"Health:     {game['health']}/100")
    print(f"Gold:       {game['gold']}")
    print()
    print(f"Strength:   {game['strength']}")
    print(f"Cunning:    {game['cunning']}")
    print(f"Honor:      {game['honor']}")
    print()

    print("Inventory:")

    if game["inventory"]:
        for item in game["inventory"]:
            print(f"  - {item}")
    else:
        print("  Empty")

    pause()


# ============================================================
#                    RANDOM EVENTS
# ============================================================

def damage(game, amount):
    game["health"] -= amount

    if game["health"] < 0:
        game["health"] = 0


def heal(game, amount):
    game["health"] += amount

    if game["health"] > 100:
        game["health"] = 100


def add_item(game, item):
    if item not in game["inventory"]:
        game["inventory"].append(item)


def has_item(game, item):
    return item in game["inventory"]


# ============================================================
#                    CHAPTER 1
# ============================================================

def chapter_1(game):
    game["chapter"] = 1

    title("CHAPTER I — THE BELL OF BLACKTHORNE")

    slow(
        "The first bell rings at midnight.\n\n"
        "You are standing in the rain outside the village of Blackthorne, "
        "a forgotten settlement pressed between the King's Road and the "
        "ancient forest known as the Hollowwood."
    )

    slow(
        "\nThe second bell rings.\n\n"
        "Every candle in the village goes out."
    )

    slow(
        "\nThen comes the third bell."
    )

    slow(
        "\nSomething screams from inside the forest."
    )

    slow(
        "\nYou have heard stories about Blackthorne."
        "\nSoldiers vanish here."
        "\nTravelers disappear."
        "\nChildren claim they see a pale woman walking among the trees."
        "\nThe royal court says these are peasant superstitions."
    )

    slow(
        "\nYou came here looking for work."
        "\nInstead, you find a village preparing for war."
    )

    print("\nA frightened man runs toward you.")

    slow(
        "\n\"You! Stranger! If you've got a sword, now would be the time "
        "to admit it!\""
    )

    choice = choose(
        "What do you do?",
        [
            "Draw your weapon and demand answers.",
            "Calmly ask what happened.",
            "Ignore him and enter the village.",
            "Offer to help immediately."
        ]
    )

    if choice == 1:
        game["strength"] += 1

        slow(
            "\nThe man freezes when he sees your hand on your weapon."
            "\n\n\"Easy! Easy! We're not the enemy.\""
        )

    elif choice == 2:
        game["cunning"] += 1

        slow(
            "\nYou keep your voice calm."
            "\n\nThe man takes a breath."
            "\n\n\"Three knights rode into the Hollowwood yesterday. "
            "Only their horses came back.\""
        )

    elif choice == 3:
        slow(
            "\nYou walk past him."
            "\n\nHe shouts something after you, but you ignore it."
            "\n\nInside the village, you immediately notice the people "
            "watching you from their windows."
        )

    else:
        game["honor"] += 1
        game["gold"] += 5

        slow(
            "\nThe man looks surprised."
            "\n\n\"Gods bless you. Maybe there's still hope.\""
        )

    slow(
        "\nBefore you can ask another question, a woman steps out from "
        "beneath a wooden awning."
    )

    slow(
        "\nShe wears a dark green cloak and carries a shortbow."
        "\n\n\"Don't listen to the villagers,\" she says."
        "\n\nHer eyes meet yours."
        "\n\n\"If you truly want to know what's happening, come with me.\""
    )

    choice = choose(
        "Do you follow the mysterious woman?",
        [
            "Follow her.",
            "Refuse and investigate the village yourself.",
            "Ask her name first."
        ]
    )

    if choice == 1:
        game["met_mara"] = True
        game["trusted_mara"] = True

        slow(
            "\nShe leads you behind the chapel."
            "\n\n\"My name is Mara,\" she says."
            "\n\n\"And the knights did not vanish.\""
        )

        slow(
            "\nShe looks toward the forest."
            "\n\n\"They were taken.\""
        )

    elif choice == 2:
        game["cunning"] += 1

        slow(
            "\nYou decide not to trust strangers."
            "\n\nThe woman smiles faintly."
            "\n\n\"Wise.\""
            "\n\nThen she disappears into the rain."
        )

    else:
        game["met_mara"] = True

        slow(
            "\nShe smiles."
            "\n\n\"Mara.\""
            "\n\nShe pauses."
            "\n\n\"Remember it. You may hear my name again.\""
        )

    slow(
        "\nLater that night, while searching an abandoned stable, "
        "you find a wounded royal knight hiding beneath the floorboards."
    )

    slow(
        "\nHis armor is covered in black mud."
        "\n\nA strange symbol has been burned into his breastplate:"
        "\nA crown split down the middle."
    )

    choice = choose(
        "The knight is barely conscious. What do you do?",
        [
            "Help him.",
            "Question him before helping.",
            "Take his equipment and leave him.",
            "Report him to the village."
        ]
    )

    if choice == 1:
        game["saved_knight"] = True
        game["honor"] += 1
        game["has_sword"] = True
        add_item(game, "Royal Knight's Sword")

        slow(
            "\nYou bind his wounds."
            "\n\nBefore passing out, he grabs your arm."
            "\n\n\"The king... has been betrayed...\""
        )

    elif choice == 2:
        game["cunning"] += 1

        slow(
            "\n\"Who attacked you?\" you ask."
            "\n\nThe knight whispers:"
            "\n\n\"Not men.\""
        )

        slow(
            "\nHe passes out."
        )

        game["saved_knight"] = True
        add_item(game, "Royal Knight's Sword")

    elif choice == 3:
        game["gold"] += 25
        game["has_sword"] = True
        add_item(game, "Royal Knight's Sword")

        slow(
            "\nYou take his sword and leave."
            "\n\nAs you step outside, you hear a whisper."
            "\n\n\"Coward.\""
        )

    else:
        slow(
            "\nYou call the villagers."
            "\n\nBut before they arrive, the knight disappears."
        )

    slow(
        "\nAt dawn, the village bell rings again."
    )

    slow(
        "\nThis time, nobody rings it."
    )

    slow(
        "\nYou look toward the Hollowwood."
        "\n\nA column of black smoke rises between the trees."
    )

    pause()


# ============================================================
#                    CHAPTER 2
# ============================================================

def chapter_2(game):
    game["chapter"] = 2

    title("CHAPTER II — THE HOLLOWWOOD")

    slow(
        "The forest seems to breathe."
        "\n\nEvery step deeper into the Hollowwood makes the village "
        "behind you feel more distant."
    )

    if game["met_mara"]:
        slow(
            "\nMara walks ahead of you."
            "\n\n\"There is an old ruin somewhere beyond these trees,\" "
            "she says."
            "\n\n\"If the stories are true, that's where they took the knights.\""
        )
    else:
        slow(
            "\nYou travel alone."
            "\n\nThe forest is unnaturally quiet."
        )

    slow(
        "\nAfter an hour, you discover three paths."
    )

    choice = choose(
        "Which path do you take?",
        [
            "The old stone road.",
            "The narrow hunter's trail.",
            "The path covered in black flowers."
        ]
    )

    if choice == 1:
        game["strength"] += 1

        slow(
            "\nThe stone road leads to a ruined watchtower."
            "\n\nInside, you find an old shield bearing the crest "
            "of House Valen."
        )

        add_item(game, "Valen Shield")

    elif choice == 2:
        game["cunning"] += 1

        slow(
            "\nThe hunter's trail is difficult to follow."
            "\n\nBut you discover footprints."
            "\n\nHuman."
            "\n\nAnd very fresh."
        )

        add_item(game, "Hunter's Map")

    else:
        game["knows_secret"] = True

        slow(
            "\nThe flowers whisper when you walk past them."
            "\n\nYou hear a woman's voice."
            "\n\n\"The crown is lying.\""
        )

        slow(
            "\nYou turn."
            "\n\nNobody is there."
        )

        game["ghost_warning"] = True

    slow(
        "\nEventually, you reach a clearing."
        "\n\nThree armed men surround a young prisoner."
    )

    choice = choose(
        "What do you do?",
        [
            "Attack the guards.",
            "Sneak behind them.",
            "Talk your way past them.",
            "Leave them alone."
        ]
    )

    if choice == 1:
        game["strength"] += 1
        damage(game, 15)

        slow(
            "\nSteel clashes against steel."
            "\n\nYou defeat the guards, but one escapes."
        )

        game["saved_villager"] = True

    elif choice == 2:
        game["cunning"] += 2
        game["saved_villager"] = True

        slow(
            "\nYou circle behind the guards."
            "\n\nA quick strike drops the first."
            "\n\nThe others flee."
        )

    elif choice == 3:
        game["cunning"] += 1

        slow(
            "\nYou claim to be a royal messenger."
            "\n\nThe guards hesitate."
            "\n\nYou point toward the forest."
            "\n\n\"Orders from the castle. Move.\""
            "\n\nSurprisingly, they believe you."
        )

        game["saved_villager"] = True

    else:
        game["honor"] -= 1

        slow(
            "\nYou walk away."
            "\n\nThe prisoner's screams follow you through the trees."
        )

    slow(
        "\nBeyond the clearing stands a ruined fortress."
        "\n\nIts gates are open."
        "\n\nInside, you see banners bearing the royal crest."
    )

    slow(
        "\nBut beneath them hangs another banner."
        "\n\nA black crown."
    )

    pause()


# ============================================================
#                    CHAPTER 3
# ============================================================

def chapter_3(game):
    game["chapter"] = 3

    title("CHAPTER III — THE BLACK CROWN")

    slow(
        "The ruined fortress was once called Greymarch."
        "\n\nNow it belongs to something else."
    )

    slow(
        "\nYou enter the great hall."
        "\n\nAt the far end sits a man wearing battered royal armor."
    )

    slow(
        "\nHe looks directly at you."
        "\n\n\"You shouldn't have come here.\""
    )

    if game["saved_knight"]:
        slow(
            "\nThe knight you rescued is mentioned."
            "\n\nThe man laughs bitterly."
            "\n\n\"Then you already know too much.\""
        )

    choice = choose(
        "How do you respond?",
        [
            "Demand the truth.",
            "Pretend you know nothing.",
            "Threaten him.",
            "Ask about the black crown."
        ]
    )

    if choice == 1:
        game["honor"] += 1

        slow(
            "\n\"Enough games. Tell me what is happening.\""
            "\n\nThe man sighs."
            "\n\n\"King Aldric has been dead for six months.\""
        )

    elif choice == 2:
        game["cunning"] += 2

        slow(
            "\nYou pretend confusion."
            "\n\nThe man studies you."
            "\n\n\"Interesting.\""
        )

    elif choice == 3:
        game["strength"] += 1

        slow(
            "\nYour hand moves toward your weapon."
            "\n\nThe man smiles."
            "\n\n\"You have courage. Or stupidity.\""
        )

    else:
        game["knows_secret"] = True

        slow(
            "\nThe man's expression changes."
            "\n\n\"You saw it.\""
            "\n\n\"The crown.\""
        )

    slow(
        "\nHe explains that the kingdom has been ruled by a council "
        "since the king's supposed death."
    )

    slow(
        "\nBut someone has been controlling that council."
        "\n\nSomeone who calls themselves..."
        "\n\nTHE ASH KING."
    )

    slow(
        "\nBefore you can ask more, arrows slam into the windows."
    )

    slow(
        "\nSoldiers have arrived."
    )

    choice = choose(
        "You need to escape.",
        [
            "Fight through the front gate.",
            "Escape through the crypt.",
            "Climb the tower.",
            "Hide and wait."
        ]
    )

    if choice == 1:
        damage(game, 25)
        game["strength"] += 1

        slow(
            "\nYou charge."
            "\n\nThe battle is brutal."
            "\n\nBut you break through."
        )

    elif choice == 2:
        game["opened_crypt"] = True

        slow(
            "\nYou descend beneath the fortress."
            "\n\nThe crypt is filled with ancient statues."
        )

        if game["ghost_warning"]:
            slow(
                "\nA pale woman appears between the statues."
                "\n\n\"Do not wake what sleeps beneath the crown.\""
            )

    elif choice == 3:
        game["cunning"] += 1

        slow(
            "\nYou climb the tower."
            "\n\nFrom the roof, you see hundreds of soldiers "
            "marching toward the fortress."
        )

        slow(
            "\nYou also see a road leading north."
            "\n\nToward the capital."
        )

    else:
        slow(
            "\nYou hide."
            "\n\nHours pass."
            "\n\nEventually, the soldiers leave."
        )

    slow(
        "\nBefore escaping, you discover a sealed letter."
    )

    add_item(game, "Sealed Letter")
    game["has_letter"] = True

    slow(
        "\nThe letter is addressed to you."
    )

    slow(
        "\nThere is no signature."
    )

    pause()


# ============================================================
#                    CHAPTER 4
# ============================================================

def chapter_4(game):
    game["chapter"] = 4

    title("CHAPTER IV — THE CAPITAL")

    slow(
        "Three days later, you reach the capital city of Valoria."
        "\n\nIts walls are enormous."
        "\n\nBut the city feels strangely quiet."
    )

    slow(
        "\nSoldiers patrol every street."
        "\n\nPosters cover the walls."
    )

    slow(
        "\nWANTED."
        "\n\nYOUR DESCRIPTION."
    )

    slow(
        "\nSomeone has accused you of treason."
    )

    choice = choose(
        "How do you enter the city?",
        [
            "Sneak through the sewer.",
            "Bribe the gate guards.",
            "Pretend to be a soldier.",
            "Enter openly."
        ]
    )

    if choice == 1:
        game["cunning"] += 2
        game["gold"] -= 5

        slow(
            "\nThe sewer smells like death."
            "\n\nBut you reach the city unnoticed."
        )

    elif choice == 2:
        if game["gold"] >= 10:
            game["gold"] -= 10

            slow(
                "\nThe guards take your money."
                "\n\n\"Welcome to Valoria,\" one says."
            )
        else:
            slow(
                "\nYou don't have enough gold."
                "\n\nYou have to find another way."
            )
            damage(game, 10)

    elif choice == 3:
        game["cunning"] += 1

        slow(
            "\nYou steal a soldier's cloak."
            "\n\nNobody questions you."
        )

    else:
        game["honor"] += 2

        slow(
            "\nYou walk directly through the gate."
            "\n\nA guard recognizes you."
            "\n\nBefore he can raise the alarm, another soldier whispers:"
            "\n\n\"Go. Quickly.\""
        )

    slow(
        "\nInside the city, you discover three factions."
    )

    slow(
        "\nThe Crown Guard."
        "\nThe Ashen Rebels."
        "\nThe Wolf Company."
    )

    slow(
        "\nEach claims to be fighting for the kingdom."
    )

    choice = choose(
        "Who do you approach?",
        [
            "The Crown Guard.",
            "The Ashen Rebels.",
            "The Wolf Company.",
            "None. Investigate alone."
        ]
    )

    if choice == 1:
        game["allied_crown"] = True

        slow(
            "\nThe Crown Guard takes you to their commander."
            "\n\n\"If you truly possess evidence of treason,\" she says,"
            "\n\"bring it to the palace.\""
        )

    elif choice == 2:
        game["allied_rebels"] = True

        slow(
            "\nThe rebels bring you into an underground chamber."
            "\n\nTheir leader removes his hood."
        )

        slow(
            "\nIt is Prince Rowan."
        )

        slow(
            "\n\"My father is alive,\" he says."
            "\n\n\"And someone is trying to make sure he stays hidden.\""
        )

    elif choice == 3:
        game["allied_wolves"] = True

        slow(
            "\nThe Wolf Company offers you a drink."
            "\n\nTheir captain laughs."
            "\n\n\"We don't care who wears the crown.\""
            "\n\n\"We care who pays us.\""
        )

        game["gold"] += 15

    else:
        game["cunning"] += 1

        slow(
            "\nYou trust nobody."
            "\n\nYou begin investigating the palace yourself."
        )

    pause()


# ============================================================
#                    CHAPTER 5
# ============================================================

def chapter_5(game):
    game["chapter"] = 5

    title("CHAPTER V — THE PALACE OF GLASS")

    slow(
        "That night, you enter the royal palace."
        "\n\nThe palace is beautiful."
        "\n\nAlmost too beautiful."
    )

    slow(
        "\nEvery wall is covered in mirrors."
        "\n\nEvery hallway seems to reflect another hallway."
    )

    slow(
        "\nYou eventually reach the throne room."
    )

    slow(
        "\nA man sits upon the throne."
        "\n\nHe wears the crown of Valoria."
    )

    slow(
        "\nHe looks exactly like King Aldric."
    )

    slow(
        "\nBut you know the king is supposed to be dead."
    )

    choice = choose(
        "What do you do?",
        [
            "Approach him.",
            "Hide and observe.",
            "Attack immediately.",
            "Search the throne room."
        ]
    )

    if choice == 1:
        slow(
            "\nYou step forward."
            "\n\nThe king smiles."
            "\n\n\"Finally.\""
        )

        slow(
            "\n\"I've been waiting for you.\""
        )

    elif choice == 2:
        game["cunning"] += 1

        slow(
            "\nYou hide behind a pillar."
            "\n\nTwo ministers enter."
            "\n\nThey kneel before the king."
        )

        slow(
            "\n\"My lord Ash King,\" one says."
        )

        game["knows_secret"] = True

    elif choice == 3:
        game["strength"] += 1

        slow(
            "\nYou draw your weapon."
            "\n\nThe king does not move."
            "\n\n\"You really are your father's child.\""
        )

    else:
        slow(
            "\nYou search the room."
            "\n\nBehind the throne, you discover a hidden door."
        )

        add_item(game, "Ancient Key")

    slow(
        "\nThe king rises."
        "\n\n\"Do you know why you were brought here?\""
    )

    slow(
        "\nYou realize something."
        "\n\nThe stranger in Blackthorne."
        "\nThe letter."
        "\nThe missing knights."
        "\nThe black crown."
        "\n\nThey were all connected."
    )

    if game["has_letter"]:
        slow(
            "\nYou open the sealed letter."
            "\n\nInside is a single sentence:"
            "\n\n\"THE BLOOD OF THE OLD KINGS STILL RUNS IN YOUR VEINS.\""
        )

        game["knows_secret"] = True

    slow(
        "\nThe king removes his crown."
        "\n\nHis face changes."
        "\n\nNot magically."
        "\n\nHis skin simply falls away like ash."
    )

    slow(
        "\nBeneath it is a pale, ancient face."
    )

    slow(
        "\n\"The kingdom was never meant for men,\" he says."
    )

    slow(
        "\n\"It was built upon something older.\""
    )

    slow(
        "\nThe floor shakes."
    )

    game["dragon_awakened"] = True

    slow(
        "\nSomething enormous moves beneath the palace."
    )

    pause()


# ============================================================
#                    CHAPTER 6
# ============================================================

def chapter_6(game):
    game["chapter"] = 6

    title("CHAPTER VI — WAR OF THE ASHEN CROWN")

    slow(
        "The capital erupts into chaos."
        "\n\nThe palace burns."
        "\n\nThe city gates close."
    )

    slow(
        "\nThree armies clash beneath the walls."
    )

    slow(
        "\nThe Crown Guard."
        "\nThe Ashen Rebels."
        "\nThe Wolf Company."
    )

    slow(
        "\nAnd beneath them all..."
        "\n\nSomething ancient wakes."
    )

    choice = choose(
        "What is your priority?",
        [
            "Save the civilians.",
            "Find Prince Rowan.",
            "Find the Crown Guard commander.",
            "Search for the source of the creature."
        ]
    )

    if choice == 1:
        game["honor"] += 2
        game["saved_villager"] = True

        slow(
            "\nYou guide civilians through the burning streets."
            "\n\nSeveral soldiers join you."
            "\n\nBy dawn, hundreds have escaped."
        )

    elif choice == 2:
        game["allied_rebels"] = True

        slow(
            "\nYou find Prince Rowan fighting in the western square."
            "\n\n\"You're alive!\" he shouts."
            "\n\n\"Then perhaps we're not doomed yet.\""
        )

    elif choice == 3:
        game["allied_crown"] = True

        slow(
            "\nThe commander gives you a royal seal."
            "\n\n\"If I die, take this to the northern fortress.\""
        )

        add_item(game, "Royal Seal")

    else:
        game["opened_crypt"] = True

        slow(
            "\nYou descend beneath the palace."
            "\n\nAt the bottom is a gigantic stone door."
            "\n\nA symbol has been carved into it."
            "\n\nThe same split crown."
        )

        slow(
            "\nBehind the door, something breathes."
        )

    slow(
        "\nSuddenly, the palace tower collapses."
    )

    damage(game, 20)

    slow(
        "\nA black dragon rises from the ruins."
        "\n\nIts scales glow like burning coal."
    )

    slow(
        "\nIt looks directly at you."
    )

    slow(
        "\nAnd kneels."
    )

    pause()


# ============================================================
#                    CHAPTER 7
# ============================================================

def chapter_7(game):
    game["chapter"] = 7

    title("CHAPTER VII — THE LAST KING")

    slow(
        "The dragon speaks."
        "\n\nIts voice shakes the stones."
    )

    slow(
        "\n\"Blood of Valen.\""
    )

    slow(
        "\n\"You carry the mark.\""
    )

    slow(
        "\nYou realize the truth."
        "\n\nYour family was not merely noble."
        "\n\nYour ancestors founded Valoria."
        "\n\nAnd they made a pact with the creatures beneath the kingdom."
    )

    if game["knows_secret"]:
        slow(
            "\nThe whispers you heard in the forest finally make sense."
        )

    choice = choose(
        "The dragon offers you a choice.",
        [
            "Command the dragon.",
            "Destroy the ancient pact.",
            "Accept the crown.",
            "Ask the dragon for the truth."
        ]
    )

    if choice == 1:
        game["strength"] += 2

        slow(
            "\nYou place your hand upon the dragon's head."
            "\n\n\"Serve me.\""
        )

        slow(
            "\nThe dragon lowers its head."
            "\n\n\"As you command, my king.\""
        )

    elif choice == 2:
        game["honor"] += 2

        slow(
            "\n\"No more kings ruling through fear.\""
            "\n\nThe dragon's eyes narrow."
            "\n\n\"Then the pact must end.\""
        )

    elif choice == 3:
        game["honor"] -= 1

        slow(
            "\nYou take the crown."
            "\n\nThe entire kingdom falls silent."
        )

        slow(
            "\nFor the first time in centuries, the crown recognizes "
            "its true bloodline."
        )

    else:
        game["cunning"] += 1

        slow(
            "\nYou ask the dragon why the pact was created."
        )

        slow(
            "\nThe dragon tells you the first king feared invasion."
            "\n\nHe traded freedom for protection."
            "\n\nThe kingdom survived."
            "\n\nBut every generation paid the price."
        )

    slow(
        "\nA horn sounds in the distance."
    )

    slow(
        "\nThe final armies are approaching."
    )

    slow(
        "\nYou have one night to decide the fate of Valoria."
    )

    pause()


# ============================================================
#                    CHAPTER 8
# ============================================================

def chapter_8(game):
    game["chapter"] = 8

    title("CHAPTER VIII — DAWN OF VALORIA")

    slow(
        "The final battle begins before sunrise."
        "\n\nThousands gather outside the capital."
    )

    slow(
        "\nThe sky is red."
        "\n\nThe dragon circles overhead."
    )

    if game["allied_rebels"]:
        slow(
            "\nPrince Rowan's rebels stand beside you."
        )

    if game["allied_crown"]:
        slow(
            "\nThe Crown Guard raises your banner."
        )

    if game["allied_wolves"]:
        slow(
            "\nThe Wolf Company waits for your command."
        )

    slow(
        "\nAcross the field stands the Ash King."
    )

    slow(
        "\nHe raises a black sword."
        "\n\n\"Come, heir of Valen.\""
    )

    slow(
        "\n\"Let us decide who deserves this kingdom.\""
    )

    choice = choose(
        "How will you face the Ash King?",
        [
            "Fight him in single combat.",
            "Lead your armies against him.",
            "Use deception.",
            "Try to convince him to surrender."
        ]
    )

    if choice == 1:
        if game["strength"] >= 3 or game["has_sword"]:
            game["duel_won"] = True

            slow(
                "\nThe duel begins."
                "\n\nSteel strikes steel."
                "\n\nThe Ash King is faster than any human."
            )

            slow(
                "\nBut you remember everything."
                "\n\nBlackthorne."
                "\nGreymarch."
                "\nThe palace."
                "\nThe dragon."
            )

            slow(
                "\nYou strike the final blow."
            )

        else:
            damage(game, 60)

            slow(
                "\nYou fight bravely."
                "\n\nBut the Ash King overwhelms you."
            )

    elif choice == 2:
        if game["honor"] >= 3 or game["allied_rebels"] or game["allied_crown"]:
            game["duel_won"] = True

            slow(
                "\nYou raise your weapon."
                "\n\nThousands of soldiers charge."
                "\n\nThe battle shakes the valley."
            )

            slow(
                "\nAt last, the Ash King's army breaks."
            )

        else:
            damage(game, 50)

            slow(
                "\nYour forces are divided."
                "\n\nThe battle becomes chaos."
            )

    elif choice == 3:
        if game["cunning"] >= 3:
            game["duel_won"] = True

            slow(
                "\nYou tell the Ash King that the dragon has abandoned him."
            )

            slow(
                "\nHe turns."
                "\n\nFor one second, he looks toward the sky."
            )

            slow(
                "\nThat second is enough."
            )

            slow(
                "\nYou strike."
            )

        else:
            damage(game, 40)

            slow(
                "\nThe Ash King sees through your deception."
            )

    else:
        slow(
            "\nYou lower your weapon."
            "\n\n\"This kingdom has suffered enough.\""
        )

        slow(
            "\nThe Ash King laughs."
        )

        if game["honor"] >= 3:
            slow(
                "\nBut then something unexpected happens."
                "\n\nThe soldiers lower their weapons."
            )

            slow(
                "\nOne by one."
            )

            slow(
                "\nThe Ash King's power was always built on fear."
                "\n\nAnd fear has finally ended."
            )

            game["duel_won"] = True

        else:
            slow(
                "\nThe Ash King attacks."
            )

            damage(game, 50)

    determine_ending(game)


# ============================================================
#                    ENDINGS
# ============================================================

def determine_ending(game):

    title("THE END")

    if game["health"] <= 0:
        ending = "FALLEN"
        game["ending"] = ending

        slow(
            "Your vision fades."
            "\n\nThe war continues without you."
            "\n\nYears later, songs are still sung about the stranger "
            "who tried to save Valoria."
        )

    elif game["duel_won"] and game["honor"] >= 5:
        ending = "THE JUST KING"
        game["ending"] = ending

        slow(
            "The Ash King falls."
            "\n\nYou refuse the crown."
            "\n\nInstead, you restore the ancient council and return power "
            "to the people."
        )

        slow(
            "\nThe dragon disappears into the northern mountains."
            "\n\nFor the first time in centuries, Valoria is free."
        )

        slow(
            "\nHistorians later call your reign the beginning of the "
            "Golden Age."
        )

    elif game["duel_won"] and game["strength"] >= 4:
        ending = "THE DRAGON KING"
        game["ending"] = ending

        slow(
            "The Ash King falls."
            "\n\nYou take the crown."
            "\n\nThe dragon kneels."
        )

        slow(
            "\nUnder your rule, no kingdom dares attack Valoria."
            "\n\nYour armies become legendary."
        )

        slow(
            "\nBut peace always has a price."
        )

    elif game["duel_won"] and game["cunning"] >= 4:
        ending = "THE SHADOW CROWN"
        game["ending"] = ending

        slow(
            "The Ash King dies believing he has won."
            "\n\nOnly you know the truth."
        )

        slow(
            "\nYou take control from the shadows."
            "\n\nKings rule."
            "\n\nCouncils argue."
            "\n\nBut every important decision eventually reaches you."
        )

        slow(
            "\nNo statue bears your name."
            "\n\nNo song celebrates you."
            "\n\nYet every ruler fears the whisper of the Shadow Crown."
        )

    elif game["duel_won"]:
        ending = "THE RELUCTANT RULER"
        game["ending"] = ending

        slow(
            "The war ends."
            "\n\nThe people demand that you become king."
        )

        slow(
            "\nYou accept."
            "\n\nNot because you want power."
            "\n\nBecause someone must rebuild what was destroyed."
        )

    else:
        ending = "THE BROKEN KINGDOM"
        game["ending"] = ending

        slow(
            "The Ash King survives."
            "\n\nValoria fractures."
        )

        slow(
            "\nThe rebels claim the west."
            "\nThe Crown Guard controls the capital."
            "\nThe Wolf Company rules the roads."
        )

        slow(
            "\nYou disappear into the wilderness."
            "\n\nSome say you became a mercenary."
            "\nSome say you crossed the sea."
            "\nOthers say you are still waiting for the right moment."
        )

    print()
    print("=" * 72)
    print(f"ENDING: {ending}".center(72))
    print("=" * 72)

    pause()


# ============================================================
#                    CHAPTER SELECT
# ============================================================

def chapter_select():

    while True:
        title("CHAPTER SELECT")

        print("Choose a chapter to play from.")
        print()
        print("WARNING: Chapter Select starts that chapter with a")
        print("default character setup. It is mainly for replaying scenes.")
        print()

        choice = choose(
            "Select a chapter:",
            [
                "Chapter I — The Bell of Blackthorne",
                "Chapter II — The Hollowwood",
                "Chapter III — The Black Crown",
                "Chapter IV — The Capital",
                "Chapter V — The Palace of Glass",
                "Chapter VI — War of the Ashen Crown",
                "Chapter VII — The Last King",
                "Chapter VIII — Dawn of Valoria",
                "Back"
            ]
        )

        if choice == 9:
            return

        game = new_game()

        if choice >= 2:
            game["name"] = "Adventurer"
            game["has_sword"] = True
            add_item(game, "Royal Knight's Sword")

        if choice >= 3:
            game["knows_secret"] = True
            game["has_letter"] = True
            add_item(game, "Sealed Letter")

        if choice >= 4:
            game["met_mara"] = True
            game["trusted_mara"] = True

        if choice >= 5:
            game["allied_rebels"] = True

        if choice >= 6:
            game["dragon_awakened"] = True

        if choice >= 7:
            game["strength"] = 3
            game["cunning"] = 3
            game["honor"] = 3

        if choice == 1:
            chapter_1(game)

        elif choice == 2:
            chapter_2(game)

        elif choice == 3:
            chapter_3(game)

        elif choice == 4:
            chapter_4(game)

        elif choice == 5:
            chapter_5(game)

        elif choice == 6:
            chapter_6(game)

        elif choice == 7:
            chapter_7(game)

        elif choice == 8:
            chapter_8(game)

        pause()


# ============================================================
#                    FULL GAME
# ============================================================

def play_game(game=None):

    if game is None:
        game = new_game()

        title("KINGDOM OF ASH")

        slow(
            "Before the story begins, tell me your name."
        )

        name = input("\nName: ").strip()

        if not name:
            name = "The Wanderer"

        game["name"] = name

        title("KINGDOM OF ASH")

        slow(
            f"Your name is {game['name']}."
            "\n\nYou are a wandering sellsword."
            "\n\nYou have no title."
            "\nNo castle."
            "\nNo family name worth remembering."
            "\n\nAt least, that is what you believe."
        )

        pause()

    while game["chapter"] <= 8:

        chapter = game["chapter"]

        if chapter == 1:
            chapter_1(game)

        elif chapter == 2:
            chapter_2(game)

        elif chapter == 3:
            chapter_3(game)

        elif chapter == 4:
            chapter_4(game)

        elif chapter == 5:
            chapter_5(game)

        elif chapter == 6:
            chapter_6(game)

        elif chapter == 7:
            chapter_7(game)

        elif chapter == 8:
            chapter_8(game)
            break

        game["chapter"] += 1

        print()
        save_game(game)


# ============================================================
#                    MAIN MENU
# ============================================================

def main_menu():

    while True:

        title("KINGDOM OF ASH")

        print("                 A MEDIEVAL TEXT ADVENTURE")
        print()
        print("                 ─────────────────────")
        print()

        choice = choose(
            "What would you like to do?",
            [
                "Start Game",
                "Continue Game",
                "Chapter Select",
                "Quit"
            ]
        )

        if choice == 1:
            play_game()

        elif choice == 2:
            game = load_game()

            if game:
                play_game(game)

        elif choice == 3:
            chapter_select()

        elif choice == 4:
            clear()
            print("Thank you for playing Kingdom of Ash.")
            print()
            print("The kingdom remembers...")
            print()
            break


# ============================================================
#                    START GAME
# ============================================================

if __name__ == "__main__":
    main_menu()