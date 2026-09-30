# Kingdom of Ash — Expanded Edition
# Text-based medieval fantasy RPG
# Requires Python 3.10+ and Tkinter

import tkinter as tk
from tkinter import messagebox
import json
import os
import random

SAVE_FILE = "kingdom_of_ash_save.json"


# ============================================================
# GAME DATA
# ============================================================

ITEMS = {
    "Potion": {
        "type": "consumable",
        "price": 25,
        "description": "Restores 40 HP."
    },
    "Elixir": {
        "type": "consumable",
        "price": 60,
        "description": "Restores 100 HP."
    },
    "Mana Tonic": {
        "type": "consumable",
        "price": 45,
        "description": "Restores 35 MP."
    },
    "Antidote": {
        "type": "consumable",
        "price": 30,
        "description": "Cures poison."
    },

    "Iron Sword": {
        "type": "weapon",
        "price": 80,
        "strength": 3,
        "description": "A dependable iron sword."
    },
    "Knight's Longsword": {
        "type": "weapon",
        "price": 180,
        "strength": 8,
        "description": "A finely balanced knight's blade."
    },
    "Moonsteel Blade": {
        "type": "weapon",
        "price": 350,
        "strength": 14,
        "magic": 4,
        "description": "A blade forged from pale moonsteel."
    },
    "Dragonfang": {
        "type": "weapon",
        "price": 700,
        "strength": 22,
        "magic": 8,
        "description": "A legendary blade forged after the dragon wars."
    },

    "Traveler's Coat": {
        "type": "armor",
        "price": 60,
        "defense": 2,
        "description": "Light armor worn by travelers."
    },
    "Guard Armor": {
        "type": "armor",
        "price": 150,
        "defense": 6,
        "description": "Standard royal guard armor."
    },
    "Runic Plate": {
        "type": "armor",
        "price": 300,
        "defense": 12,
        "magic": 3,
        "description": "Heavy armor covered in protective runes."
    },
    "Dragon Mail": {
        "type": "armor",
        "price": 650,
        "defense": 20,
        "magic": 7,
        "description": "Armor designed to withstand dragonfire."
    }
}


SPELLS = {
    "Ember": {
        "cost": 5,
        "power": 18,
        "description": "A quick burst of flame."
    },
    "Frost Lance": {
        "cost": 8,
        "power": 28,
        "description": "A piercing bolt of ice."
    },
    "Thunder": {
        "cost": 12,
        "power": 42,
        "description": "Calls down a powerful lightning strike."
    },
    "Mending Light": {
        "cost": 10,
        "heal": 45,
        "description": "Restores HP."
    },
    "Flame Wall": {
        "cost": 15,
        "power": 35,
        "burn": True,
        "description": "Damages the enemy and may burn them."
    },
    "Starfall": {
        "cost": 25,
        "power": 75,
        "description": "A devastating late-game spell."
    }
}


ENEMIES = {
    "Dire Wolf": {
        "hp": 45,
        "attack": 9,
        "defense": 2,
        "xp": 20,
        "gold": 12
    },
    "Cave Spider": {
        "hp": 60,
        "attack": 11,
        "defense": 4,
        "xp": 30,
        "gold": 18,
        "poison": True
    },
    "Forest Bandit": {
        "hp": 70,
        "attack": 13,
        "defense": 5,
        "xp": 40,
        "gold": 30
    },
    "Highwayman": {
        "hp": 85,
        "attack": 15,
        "defense": 7,
        "xp": 55,
        "gold": 40
    },
    "Ash Cultist": {
        "hp": 90,
        "attack": 16,
        "defense": 8,
        "xp": 65,
        "gold": 50
    },
    "Ruined Shade": {
        "hp": 110,
        "attack": 18,
        "defense": 10,
        "xp": 80,
        "gold": 65
    },
    "Fallen Knight": {
        "hp": 140,
        "attack": 21,
        "defense": 13,
        "xp": 110,
        "gold": 80
    },
    "Stone Golem": {
        "hp": 190,
        "attack": 25,
        "defense": 20,
        "xp": 160,
        "gold": 110
    },
    "Ash Warlord": {
        "hp": 250,
        "attack": 29,
        "defense": 18,
        "xp": 250,
        "gold": 180
    },
    "Cinder Witch": {
        "hp": 220,
        "attack": 32,
        "defense": 15,
        "xp": 230,
        "gold": 160
    },
    "Royal Enforcer": {
        "hp": 180,
        "attack": 27,
        "defense": 17,
        "xp": 190,
        "gold": 130
    },
    "Ancient Knight": {
        "hp": 300,
        "attack": 34,
        "defense": 24,
        "xp": 350,
        "gold": 250
    },
    "The Ash Dragon": {
        "hp": 450,
        "attack": 42,
        "defense": 28,
        "xp": 600,
        "gold": 500,
        "boss": True,
        "no_flee": True
    },
    "Elder Ash Dragon": {
        "hp": 650,
        "attack": 50,
        "defense": 34,
        "xp": 1000,
        "gold": 1000,
        "boss": True,
        "no_flee": True
    }
}


# ============================================================
# STORY
# ============================================================

S = {

    "intro": {
        "title": "Kingdom of Ash",
        "text": (
            "The kingdom of Eldoria was once known for its golden towers, "
            "quiet forests, and ancient knights.\n\n"
            "Then the bells began to ring.\n\n"
            "Ash started falling from the sky.\n"
            "Villages disappeared.\n"
            "And somewhere beyond the northern mountains, something ancient awakened.\n\n"
            "You are a wandering warrior with little more than a sword and a name.\n"
            "Tonight, your journey begins in the village of Blackthorne."
        ),
        "choices": [
            ("Enter Blackthorne", "chapter1")
        ]
    },

    "chapter1": {
        "title": "Chapter I — The Bell of Blackthorne",
        "text": (
            "You arrive at Blackthorne just before sunset.\n\n"
            "The village is strangely quiet.\n"
            "A huge bell hangs above the town square, but no one is ringing it.\n\n"
            "An old woman approaches you.\n\n"
            "\"Stranger... if you have a sword, we need you.\""
        ),
        "choices": [
            ("Ask what happened", "chapter1_question"),
            ("Offer to help immediately", "chapter1_help"),
            ("Ask for payment", "chapter1_payment")
        ]
    },

    "chapter1_question": {
        "title": "The Ashmark",
        "text": (
            "The woman explains that several villagers vanished during the night.\n\n"
            "Before they disappeared, strange symbols appeared on their doors.\n\n"
            "She points toward the forest.\n\n"
            "\"The mark came from there.\""
        ),
        "choices": [
            ("Investigate the forest", "chapter2"),
            ("Search the village first", "village_search")
        ]
    },

    "chapter1_help": {
        "title": "A Promise",
        "text": (
            "You agree to help.\n\n"
            "The woman smiles with relief.\n\n"
            "\"Then perhaps Eldoria still has heroes.\""
        ),
        "choices": [
            ("Enter the forest", "chapter2")
        ],
        "effects": [
            ("flag", "helped", True)
        ]
    },

    "chapter1_payment": {
        "title": "A Mercenary's Question",
        "text": (
            "The woman looks disappointed.\n\n"
            "\"Gold is scarce. But if you survive the forest, "
            "perhaps the village can repay you.\""
        ),
        "choices": [
            ("Accept", "chapter2"),
            ("Refuse and leave", "bad_end")
        ]
    },

    "village_search": {
        "title": "Searching Blackthorne",
        "text": (
            "You search the village before leaving.\n\n"
            "Behind the old chapel, you discover a hidden cellar.\n\n"
            "Inside is a small chest containing supplies and an old map."
        ),
        "choices": [
            ("Take the supplies", "chapter2")
        ],
        "effects": [
            ("item", "Potion", 2),
            ("gold", 30)
        ]
    },

    "chapter2": {
        "title": "Chapter II — The Forest Road",
        "text": (
            "The forest grows darker with every step.\n\n"
            "Ash covers the leaves.\n\n"
            "Then you hear a growl."
        ),
        "battle": "Dire Wolf",
        "choices": [
            ("Continue", "forest_after_battle")
        ]
    },

    "forest_after_battle": {
        "title": "A Stranger in the Woods",
        "text": (
            "After the battle, you discover another traveler nearby.\n\n"
            "Her name is Mara.\n\n"
            "She carries a bow and wears the crest of the old royal scouts.\n\n"
            "\"You should not be here,\" she says."
        ),
        "choices": [
            ("Trust Mara", "mara_trust"),
            ("Keep your distance", "mara_doubt"),
            ("Ask about the royal crest", "mara_question")
        ]
    },

    "mara_trust": {
        "title": "Mara",
        "text": (
            "Mara agrees to travel with you.\n\n"
            "\"Whatever is happening in Eldoria, "
            "we are going to find the truth.\""
        ),
        "choices": [
            ("Travel together", "chapter3")
        ],
        "effects": [
            ("flag", "mara", True)
        ]
    },

    "mara_doubt": {
        "title": "Two Paths",
        "text": (
            "Mara watches you carefully.\n\n"
            "\"Fair enough. We can still travel in the same direction.\""
        ),
        "choices": [
            ("Continue", "chapter3")
        ]
    },

    "mara_question": {
        "title": "The Royal Scouts",
        "text": (
            "Mara explains that the royal scouts disappeared years ago.\n\n"
            "\"Someone has been using their old routes to move soldiers "
            "through the forest.\""
        ),
        "choices": [
            ("Ask who is behind it", "chapter3"),
            ("Move on", "chapter3")
        ],
        "effects": [
            ("flag", "truth", True)
        ]
    },

    "chapter3": {
        "title": "Chapter III — The Ashen Ruins",
        "text": (
            "Deep inside the forest you discover ancient ruins.\n\n"
            "A cracked stone door leads underground.\n\n"
            "The walls are covered with paintings of dragons."
        ),
        "choices": [
            ("Enter the ruins", "ruins_enter"),
            ("Search the outside", "ruins_search")
        ]
    },

    "ruins_search": {
        "title": "The Fallen Shrine",
        "text": (
            "Behind the ruins you find a small shrine.\n\n"
            "Inside is a glowing crystal."
        ),
        "choices": [
            ("Take the crystal", "ruins_enter")
        ],
        "effects": [
            ("item", "Potion", 1),
            ("flag", "crystal", True)
        ]
    },

    "ruins_enter": {
        "title": "The Ruins Below",
        "text": (
            "You descend into the ruins.\n\n"
            "A shadow moves between the pillars."
        ),
        "battle": "Ruined Shade",
        "choices": [
            ("Continue deeper", "ruins_deep")
        ]
    },

    "ruins_deep": {
        "title": "The Dragon Tablet",
        "text": (
            "At the center of the chamber stands a stone tablet.\n\n"
            "It describes an ancient pact between the royal family "
            "and the dragons of Eldoria.\n\n"
            "The pact was broken generations ago."
        ),
        "choices": [
            ("Study the tablet", "chapter4"),
            ("Destroy the tablet", "chapter4")
        ],
        "effects": [
            ("flag", "pact", True)
        ]
    },

    "chapter4": {
        "title": "Chapter IV — City of Crowns",
        "text": (
            "You arrive at the capital city.\n\n"
            "The gates are heavily guarded.\n\n"
            "The royal banners still fly above the walls, "
            "but something about the city feels wrong."
        ),
        "choices": [
            ("Enter through the main gate", "capital_gate"),
            ("Sneak through the old tunnels", "capital_stealth")
        ]
    },

    "capital_gate": {
        "title": "The Royal Guard",
        "text": (
            "The guards stop you.\n\n"
            "\"State your business.\""
        ),
        "choices": [
            ("Tell the truth", "capital_truth"),
            ("Lie about being a messenger", "capital_lie")
        ]
    },

    "capital_truth": {
        "title": "A Dangerous Truth",
        "text": (
            "You tell the guards about the ruins.\n\n"
            "Their expressions change.\n\n"
            "One guard quietly says:\n\n"
            "\"You need to speak with Lord Varick.\""
        ),
        "choices": [
            ("Meet Lord Varick", "chapter5")
        ]
    },

    "capital_lie": {
        "title": "The Messenger",
        "text": (
            "Your story almost works.\n\n"
            "But one guard notices the ash on your equipment."
        ),
        "battle": "Royal Enforcer",
        "choices": [
            ("Escape into the city", "chapter5")
        ]
    },

    "capital_stealth": {
        "title": "The Old Tunnels",
        "text": (
            "You use an abandoned tunnel beneath the city walls.\n\n"
            "The tunnel leads directly beneath the royal palace."
        ),
        "choices": [
            ("Enter the palace", "chapter5")
        ],
        "effects": [
            ("flag", "stealth", True)
        ]
    },

    "chapter5": {
        "title": "Chapter V — The King's Secret",
        "text": (
            "Lord Varick meets you in a private chamber.\n\n"
            "\"The king is dead,\" he says.\n\n"
            "\"But that is not the greatest danger.\""
        ),
        "choices": [
            ("Ask about the dragons", "dragon_secret"),
            ("Ask about the missing villagers", "villager_secret"),
            ("Demand the truth", "truth_secret")
        ]
    },

    "dragon_secret": {
        "title": "The Dragon Pact",
        "text": (
            "Varick reveals that the royal family once controlled "
            "the dragons through an ancient pact.\n\n"
            "\"Someone is trying to restore that pact.\""
        ),
        "choices": [
            ("Continue", "chapter6")
        ],
        "effects": [
            ("flag", "secret", True)
        ]
    },

    "villager_secret": {
        "title": "The Missing",
        "text": (
            "The villagers were taken because someone believes "
            "they carry traces of an ancient royal bloodline."
        ),
        "choices": [
            ("Continue", "chapter6")
        ],
        "effects": [
            ("flag", "document", True)
        ]
    },

    "truth_secret": {
        "title": "The Hidden Heir",
        "text": (
            "Varick finally reveals the secret.\n\n"
            "\"The royal bloodline did not end with the king.\""
        ),
        "choices": [
            ("Ask who the heir is", "heir_secret")
        ]
    },

    "heir_secret": {
        "title": "The Heir",
        "text": (
            "Varick looks directly at you.\n\n"
            "\"You are standing in front of them.\""
        ),
        "choices": [
            ("Accept your heritage", "chapter6"),
            ("Reject the crown", "chapter6")
        ],
        "effects": [
            ("flag", "heir", True)
        ]
    },

    "chapter6": {
        "title": "Chapter VI — War of Ash",
        "text": (
            "The capital falls into chaos.\n\n"
            "Ash storms roll across the sky.\n\n"
            "An army marches toward the city."
        ),
        "choices": [
            ("Defend the city", "war_defend"),
            ("Seek the source of the attack", "war_source"),
            ("Escape the city", "war_escape")
        ]
    },

    "war_defend": {
        "title": "The City Gate",
        "text": (
            "You stand at the gate as the enemy approaches."
        ),
        "battle": "Ash Warlord",
        "choices": [
            ("Continue", "chapter7")
        ]
    },

    "war_source": {
        "title": "The Witch of Cinders",
        "text": (
            "You track the magic behind the ash storms to an ancient tower."
        ),
        "battle": "Cinder Witch",
        "choices": [
            ("Continue", "chapter7")
        ]
    },

    "war_escape": {
        "title": "Leaving the Capital",
        "text": (
            "You escape through the eastern road.\n\n"
            "Behind you, the capital disappears beneath the ash."
        ),
        "choices": [
            ("Keep going", "chapter7")
        ]
    },

    "chapter7": {
        "title": "Chapter VII — The Elder",
        "text": (
            "Beyond the mountains lies a forgotten temple.\n\n"
            "An ancient dragon waits inside.\n\n"
            "It speaks without moving its mouth.\n\n"
            "\"The kingdom has forgotten its promise.\""
        ),
        "choices": [
            ("Listen", "elder_listen"),
            ("Attack", "elder_attack")
        ]
    },

    "elder_listen": {
        "title": "The Old Pact",
        "text": (
            "The dragon explains that the royal family broke the ancient pact.\n\n"
            "Now the dragons are deciding whether humanity deserves another chance."
        ),
        "choices": [
            ("Accept the dragon's terms", "chapter8"),
            ("Reject the pact", "chapter8")
        ],
        "effects": [
            ("flag", "dragon_pact", True)
        ]
    },

    "elder_attack": {
        "title": "Ancient Guardian",
        "text": (
            "The guardian awakens.\n\n"
            "Its power fills the temple."
        ),
        "battle": "Ancient Knight",
        "choices": [
            ("Continue", "chapter8")
        ]
    },

    "chapter8": {
        "title": "Chapter VIII — The Last Bell",
        "text": (
            "You return to the ruins beneath the capital.\n\n"
            "At the center of the chamber is the final bell.\n\n"
            "The bell can either restore the kingdom's ancient pact "
            "or break it forever."
        ),
        "choices": [
            ("Ring the bell", "ending_dragon"),
            ("Destroy the bell", "ending_ruler"),
            ("Let the council decide", "ending_council"),
            ("Walk away", "ending_guardian")
        ]
    },

    "ending_dragon": {
        "title": "Ending — The Dragon Crown",
        "text": (
            "You ring the bell.\n\n"
            "The sound travels across Eldoria.\n\n"
            "Dragons descend from the mountains, but they do not attack.\n\n"
            "The ancient pact is restored.\n\n"
            "Eldoria enters a new age where humans and dragons "
            "must learn to live beside one another."
        ),
        "choices": [
            ("Face the final guardian", "final_dragon")
        ]
    },

    "ending_ruler": {
        "title": "Ending — The New Crown",
        "text": (
            "You destroy the bell.\n\n"
            "The old magic fades.\n\n"
            "Without the ancient pact, the kingdom becomes free "
            "from the influence of the dragons.\n\n"
            "But someone must rebuild Eldoria."
        ),
        "choices": [
            ("Face the final guardian", "final_dragon")
        ]
    },

    "ending_council": {
        "title": "Ending — The Council",
        "text": (
            "You refuse to decide the fate of the kingdom alone.\n\n"
            "The surviving nobles and villagers form a council.\n\n"
            "For the first time in generations, Eldoria is ruled "
            "through cooperation rather than a single crown."
        ),
        "choices": [
            ("Face the final guardian", "final_dragon")
        ]
    },

    "ending_guardian": {
        "title": "Ending — The Wandering Guardian",
        "text": (
            "You leave the ruins behind.\n\n"
            "You never take the throne.\n\n"
            "Instead, you travel from village to village, "
            "protecting people from the dangers left behind by the war."
        ),
        "choices": [
            ("Face the final guardian", "final_dragon")
        ]
    },

    "final_dragon": {
        "title": "The Final Battle",
        "text": (
            "A final roar shakes the chamber.\n\n"
            "The Elder Ash Dragon descends from the darkness.\n\n"
            "There will be no more running."
        ),
        "battle": "Elder Ash Dragon",
        "choices": [
            ("Continue", "true_ending")
        ]
    },

    "true_ending": {
        "title": "Kingdom of Ash — The End",
        "text": (
            "The dragon falls silent.\n\n"
            "The ash storm finally clears.\n\n"
            "Sunlight returns to Eldoria.\n\n"
            "Your journey is over...\n\n"
            "but the kingdom's story has only just begun."
        ),
        "choices": [
            ("Return to Main Menu", "menu")
        ]
    },

    "bad_end": {
        "title": "Ending — The Road Ends",
        "text": (
            "You turn away from Blackthorne.\n\n"
            "The forest disappears behind you.\n\n"
            "Whatever was happening in Eldoria continues without you."
        ),
        "choices": [
            ("Return to Main Menu", "menu")
        ]
    }
}


# ============================================================
# GAME STATE
# ============================================================

def new_game():
    return {
        "name": "Hero",

        "level": 1,
        "xp": 0,

        "hp": 100,
        "max_hp": 100,

        "mp": 40,
        "max_mp": 40,

        "strength": 10,
        "defense": 5,
        "magic": 5,

        "gold": 100,

        "inventory": {
            "Potion": 3,
            "Mana Tonic": 2
        },

        "equipment": {
            "weapon": "Iron Sword",
            "armor": "Traveler's Coat"
        },

        "spells": [
            "Ember",
            "Mending Light"
        ],

        "companions": [],

        "achievements": [],

        "flags": {},

        "chapter": 1,

        "settings": {
            "sound": True,
            "music": True
        }
    }


game = new_game()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def strength():
    value = game["strength"]

    weapon = game["equipment"].get("weapon")

    if weapon in ITEMS:
        value += ITEMS[weapon].get("strength", 0)

    return value


def defense():
    value = game["defense"]

    armor = game["equipment"].get("armor")

    if armor in ITEMS:
        value += ITEMS[armor].get("defense", 0)

    return value


def magic_power():
    value = game["magic"]

    weapon = game["equipment"].get("weapon")
    armor = game["equipment"].get("armor")

    if weapon in ITEMS:
        value += ITEMS[weapon].get("magic", 0)

    if armor in ITEMS:
        value += ITEMS[armor].get("magic", 0)

    return value


def add_item(item, amount=1):
    game["inventory"][item] = game["inventory"].get(item, 0) + amount


def remove_item(item, amount=1):
    if game["inventory"].get(item, 0) < amount:
        return False

    game["inventory"][item] -= amount

    if game["inventory"][item] <= 0:
        del game["inventory"][item]

    return True


def add_xp(amount):
    game["xp"] += amount

    while game["xp"] >= game["level"] * 100:
        game["xp"] -= game["level"] * 100
        game["level"] += 1

        game["max_hp"] += 15
        game["max_mp"] += 5
        game["strength"] += 2
        game["defense"] += 2
        game["magic"] += 1

        game["hp"] = game["max_hp"]
        game["mp"] = game["max_mp"]

        unlock_achievement("Seasoned Adventurer")

        messagebox.showinfo(
            "LEVEL UP!",
            f"You reached Level {game['level']}!"
        )


def unlock_achievement(name):
    if name not in game["achievements"]:
        game["achievements"].append(name)


def apply_effects(effects):
    if not effects:
        return

    for effect in effects:

        kind = effect[0]

        if kind == "flag":
            game["flags"][effect[1]] = effect[2]

        elif kind == "item":
            add_item(effect[1], effect[2])

        elif kind == "gold":
            game["gold"] += effect[1]

        elif kind == "xp":
            add_xp(effect[1])

        elif kind == "strength":
            game["strength"] += effect[1]

        elif kind == "defense":
            game["defense"] += effect[1]

        elif kind == "magic":
            game["magic"] += effect[1]

        elif kind == "chapter":
            game["chapter"] = effect[1]


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Kingdom of Ash")
root.geometry("1200x760")
root.minsize(950, 650)
root.configure(bg="#111111")


TITLE_FONT = ("Georgia", 26, "bold")
HEADING_FONT = ("Georgia", 18, "bold")
BODY_FONT = ("Georgia", 13)
BUTTON_FONT = ("Georgia", 11, "bold")
SMALL_FONT = ("Georgia", 10)


story_frame = tk.Frame(root, bg="#171717")
story_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


side_frame = tk.Frame(
    root,
    bg="#202020",
    width=270
)

side_frame.pack(
    side="right",
    fill="y",
    padx=(0, 15),
    pady=15
)

side_frame.pack_propagate(False)


title_label = tk.Label(
    story_frame,
    text="KINGDOM OF ASH",
    font=TITLE_FONT,
    bg="#171717",
    fg="#d7b56d"
)

title_label.pack(pady=(15, 5))


scene_title = tk.Label(
    story_frame,
    text="",
    font=HEADING_FONT,
    bg="#171717",
    fg="#caa86a"
)

scene_title.pack(pady=10)


story_text = tk.Text(
    story_frame,
    wrap="word",
    font=BODY_FONT,
    bg="#111111",
    fg="#eeeeee",
    insertbackground="white",
    relief="flat",
    padx=25,
    pady=20
)

story_text.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

story_text.configure(state="disabled")


choice_frame = tk.Frame(
    story_frame,
    bg="#171717"
)

choice_frame.pack(
    fill="x",
    padx=20,
    pady=10
)


# ============================================================
# SIDE PANEL
# ============================================================

stats_title = tk.Label(
    side_frame,
    text="CHARACTER",
    font=HEADING_FONT,
    bg="#202020",
    fg="#d7b56d"
)

stats_title.pack(pady=(15, 5))


stats_label = tk.Label(
    side_frame,
    text="",
    justify="left",
    anchor="w",
    font=SMALL_FONT,
    bg="#202020",
    fg="#eeeeee"
)

stats_label.pack(
    fill="x",
    padx=20,
    pady=10
)


def update_stats():

    weapon = game["equipment"].get("weapon", "None")
    armor = game["equipment"].get("armor", "None")

    text = (
        f"Level: {game['level']}\n"
        f"XP: {game['xp']}/{game['level'] * 100}\n\n"

        f"HP: {game['hp']} / {game['max_hp']}\n"
        f"MP: {game['mp']} / {game['max_mp']}\n\n"

        f"Strength: {strength()}\n"
        f"Defense: {defense()}\n"
        f"Magic: {magic_power()}\n\n"

        f"Gold: {game['gold']}\n\n"

        f"Weapon:\n{weapon}\n\n"
        f"Armor:\n{armor}"
    )

    stats_label.config(text=text)


def clear_choices():

    for widget in choice_frame.winfo_children():
        widget.destroy()


def write_story(title, text):

    scene_title.config(text=title)

    story_text.configure(state="normal")
    story_text.delete("1.0", "end")
    story_text.insert("end", text)
    story_text.configure(state="disabled")

    story_text.see("1.0")

    update_stats()


# ============================================================
# SAVE / LOAD
# ============================================================

def save_game():

    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(game, f, indent=4)

        messagebox.showinfo(
            "Game Saved",
            "Your progress has been saved."
        )

    except Exception as e:
        messagebox.showerror(
            "Save Error",
            str(e)
        )


def load_game():

    global game

    if not os.path.exists(SAVE_FILE):
        messagebox.showwarning(
            "No Save",
            "No save file was found."
        )
        return

    try:

        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            game = json.load(f)

        update_stats()

        show_scene("intro")

    except Exception as e:

        messagebox.showerror(
            "Load Error",
            str(e)
        )


# ============================================================
# STORY SYSTEM
# ============================================================

def show_scene(scene_id):

    clear_choices()

    if scene_id == "menu":
        show_main_menu()
        return

    scene = S.get(scene_id)

    if not scene:
        write_story(
            "Error",
            f"Scene '{scene_id}' does not exist."
        )
        return

    apply_effects(scene.get("effects"))

    write_story(
        scene["title"],
        scene["text"]
    )

    if "battle" in scene:

        battle_button = tk.Button(
            choice_frame,
            text=f"⚔ Fight {scene['battle']}",
            command=lambda: start_battle(
                scene["battle"],
                scene.get("choices", [])
            ),
            font=BUTTON_FONT,
            bg="#6b2c2c",
            fg="white",
            activebackground="#8c3d3d",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=10
        )

        battle_button.pack(
            fill="x",
            pady=5
        )

        return

    for text, destination in scene.get("choices", []):

        button = tk.Button(
            choice_frame,
            text=text,
            command=lambda d=destination: show_scene(d),
            font=BUTTON_FONT,
            bg="#303030",
            fg="#eeeeee",
            activebackground="#4a4a4a",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=9
        )

        button.pack(
            fill="x",
            pady=4
        )


# ============================================================
# COMBAT
# ============================================================

current_battle = None


def start_battle(enemy_name, after_choices):

    global current_battle

    enemy_template = ENEMIES[enemy_name]

    current_battle = {
        "name": enemy_name,
        "hp": enemy_template["hp"],
        "max_hp": enemy_template["hp"],
        "attack": enemy_template["attack"],
        "defense": enemy_template["defense"],
        "xp": enemy_template["xp"],
        "gold": enemy_template["gold"],
        "poison": enemy_template.get("poison", False),
        "boss": enemy_template.get("boss", False),
        "no_flee": enemy_template.get("no_flee", False),
        "weakened": False,
        "burn": 0
    }

    show_battle_screen(after_choices)


def show_battle_screen(after_choices):

    clear_choices()

    enemy = current_battle

    write_story(
        f"Battle — {enemy['name']}",
        (
            f"You face {enemy['name']}!\n\n"
            f"Enemy HP: {enemy['hp']} / {enemy['max_hp']}\n"
            f"Your HP: {game['hp']} / {game['max_hp']}\n"
            f"Your MP: {game['mp']} / {game['max_mp']}"
        )
    )

    actions = [
        ("⚔ Sword Strike", lambda: player_attack(after_choices)),
        ("💥 Power Slash", lambda: power_slash(after_choices)),
        ("🛡 Guard Break", lambda: guard_break(after_choices)),
        ("✨ Spells", lambda: spell_menu(after_choices)),
        ("🛡 Defend", lambda: defend_turn(after_choices)),
        ("🎒 Items", lambda: item_menu(after_choices)),
        ("🏃 Flee", lambda: flee_battle(after_choices))
    ]

    for text, command in actions:

        button = tk.Button(
            choice_frame,
            text=text,
            command=command,
            font=BUTTON_FONT,
            bg="#303030",
            fg="#eeeeee",
            activebackground="#4a4a4a",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )


def enemy_turn(after_choices):

    enemy = current_battle

    if enemy is None:
        return

    if enemy["hp"] <= 0:
        return

    damage = random.randint(
        max(1, enemy["attack"] - 5),
        enemy["attack"] + 5
    )

    damage -= defense() // 3

    if damage < 1:
        damage = 1

    game["hp"] -= damage

    if enemy["poison"] and random.random() < 0.25:

        game["hp"] -= 3

        poison_text = (
            f"\n\nThe {enemy['name']} leaves you poisoned!"
        )

    else:
        poison_text = ""

    if game["hp"] <= 0:

        game["hp"] = 0

        update_stats()

        messagebox.showinfo(
            "Defeat",
            "You were defeated.\n\n"
            "Your journey ends here."
        )

        show_main_menu()
        return

    show_battle_screen(after_choices)


def player_attack(after_choices):

    enemy = current_battle

    damage = random.randint(
        max(1, strength() - 4),
        strength() + 8
    )

    critical = random.random() < 0.12

    if critical:
        damage *= 2

    damage -= enemy["defense"] // 2

    if damage < 1:
        damage = 1

    enemy["hp"] -= damage

    if enemy["hp"] <= 0:

        enemy["hp"] = 0

        win_battle(after_choices)

        return

    enemy_turn(after_choices)


def power_slash(after_choices):

    if game["mp"] < 5:

        messagebox.showwarning(
            "Not Enough MP",
            "You need 5 MP."
        )

        return

    game["mp"] -= 5

    enemy = current_battle

    damage = random.randint(
        strength() + 5,
        strength() + 15
    )

    damage -= enemy["defense"] // 2

    if damage < 1:
        damage = 1

    enemy["hp"] -= damage

    if enemy["hp"] <= 0:

        enemy["hp"] = 0
        win_battle(after_choices)

        return

    enemy_turn(after_choices)


def guard_break(after_choices):

    enemy = current_battle

    damage = random.randint(
        max(1, strength() - 5),
        strength() + 3
    )

    enemy["hp"] -= damage

    enemy["weakened"] = True
    enemy["defense"] = max(
        0,
        enemy["defense"] - 5
    )

    if enemy["hp"] <= 0:

        enemy["hp"] = 0
        win_battle(after_choices)

        return

    enemy_turn(after_choices)


def defend_turn(after_choices):

    enemy = current_battle

    damage = random.randint(
        max(1, enemy["attack"] - 5),
        enemy["attack"] + 5
    )

    damage -= defense() // 2

    damage //= 2

    if damage < 1:
        damage = 1

    game["hp"] -= damage

    if game["hp"] <= 0:

        game["hp"] = 0

        messagebox.showinfo(
            "Defeat",
            "You were defeated."
        )

        show_main_menu()
        return

    show_battle_screen(after_choices)


def spell_menu(after_choices):

    clear_choices()

    for spell_name in game["spells"]:

        spell = SPELLS.get(spell_name)

        if not spell:
            continue

        button = tk.Button(
            choice_frame,
            text=(
                f"{spell_name} "
                f"({spell.get('cost', 0)} MP)"
            ),
            command=lambda s=spell_name:
            cast_spell(s, after_choices),
            font=BUTTON_FONT,
            bg="#3d3057",
            fg="white",
            activebackground="#564275",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=lambda: show_battle_screen(after_choices),
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def cast_spell(spell_name, after_choices):

    spell = SPELLS[spell_name]

    cost = spell.get("cost", 0)

    if game["mp"] < cost:

        messagebox.showwarning(
            "Not Enough MP",
            "You do not have enough mana."
        )

        return

    game["mp"] -= cost

    if "heal" in spell:

        amount = spell["heal"] + magic_power()

        game["hp"] = min(
            game["max_hp"],
            game["hp"] + amount
        )

        enemy_turn(after_choices)
        return

    enemy = current_battle

    damage = spell.get("power", 0)

    damage += magic_power()

    damage = random.randint(
        max(1, damage - 8),
        damage + 8
    )

    damage -= enemy["defense"] // 3

    if damage < 1:
        damage = 1

    enemy["hp"] -= damage

    if spell.get("burn"):

        enemy["burn"] = 3

    if enemy["hp"] <= 0:

        enemy["hp"] = 0
        win_battle(after_choices)

        return

    enemy_turn(after_choices)


def item_menu(after_choices):

    clear_choices()

    usable = False

    for item_name, amount in list(
        game["inventory"].items()
    ):

        item = ITEMS.get(item_name)

        if not item:
            continue

        if item["type"] != "consumable":
            continue

        usable = True

        button = tk.Button(
            choice_frame,
            text=f"{item_name} x{amount}",
            command=lambda i=item_name:
            use_item(i, after_choices),
            font=BUTTON_FONT,
            bg="#304b3a",
            fg="white",
            activebackground="#3d604b",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )

    if not usable:

        label = tk.Label(
            choice_frame,
            text="You have no usable items.",
            font=BODY_FONT,
            bg="#171717",
            fg="#bbbbbb"
        )

        label.pack(pady=10)

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=lambda: show_battle_screen(after_choices),
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def use_item(item_name, after_choices):

    if not remove_item(item_name):
        return

    if item_name == "Potion":

        game["hp"] = min(
            game["max_hp"],
            game["hp"] + 40
        )

    elif item_name == "Elixir":

        game["hp"] = min(
            game["max_hp"],
            game["hp"] + 100
        )

    elif item_name == "Mana Tonic":

        game["mp"] = min(
            game["max_mp"],
            game["mp"] + 35
        )

    elif item_name == "Antidote":
        pass

    enemy_turn(after_choices)


def flee_battle(after_choices):

    enemy = current_battle

    if enemy.get("no_flee"):

        messagebox.showwarning(
            "Cannot Escape",
            "There is nowhere to run!"
        )

        return

    if random.random() < 0.65:

        messagebox.showinfo(
            "Escaped",
            "You escaped from the battle."
        )

        show_scene("chapter2")

    else:

        enemy_turn(after_choices)


def win_battle(after_choices):

    global current_battle

    enemy = current_battle

    reward_xp = enemy["xp"]
    reward_gold = enemy["gold"]

    game["gold"] += reward_gold

    add_xp(reward_xp)

    unlock_achievement("First Blood")

    if enemy["boss"]:
        unlock_achievement("Boss Breaker")

    if enemy["name"] in (
        "The Ash Dragon",
        "Elder Ash Dragon"
    ):
        unlock_achievement("Dragon's Shadow")

    current_battle = None

    update_stats()

    messagebox.showinfo(
        "Victory!",
        (
            f"You defeated {enemy['name']}!\n\n"
            f"XP gained: {reward_xp}\n"
            f"Gold gained: {reward_gold}"
        )
    )

    if after_choices:

        # Continue using the first choice
        next_scene = after_choices[0][1]

        show_scene(next_scene)

    else:

        show_main_menu()


# ============================================================
# INVENTORY
# ============================================================

def show_inventory():

    clear_choices()

    write_story(
        "Inventory",
        "Your current equipment and items."
    )

    for item_name, amount in game["inventory"].items():

        button = tk.Button(
            choice_frame,
            text=f"{item_name} x{amount}",
            command=lambda i=item_name:
            inspect_item(i),
            font=BUTTON_FONT,
            bg="#303030",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )

    button = tk.Button(
        choice_frame,
        text="⚔ Equipment",
        command=show_equipment,
        font=BUTTON_FONT,
        bg="#4a3a25",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    button.pack(
        fill="x",
        pady=8
    )

    button = tk.Button(
        choice_frame,
        text="← Back",
        command=show_main_menu,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    button.pack(
        fill="x"
    )


def inspect_item(item_name):

    item = ITEMS.get(item_name)

    if not item:
        return

    description = item.get(
        "description",
        "No description."
    )

    messagebox.showinfo(
        item_name,
        description
    )


def show_equipment():

    clear_choices()

    weapon = game["equipment"].get("weapon")
    armor = game["equipment"].get("armor")

    write_story(
        "Equipment",
        (
            f"Weapon:\n{weapon}\n\n"
            f"Armor:\n{armor}\n\n"
            "You can equip purchased equipment below."
        )
    )

    for item_name in game["inventory"]:

        item = ITEMS.get(item_name)

        if not item:
            continue

        if item["type"] not in (
            "weapon",
            "armor"
        ):
            continue

        button = tk.Button(
            choice_frame,
            text=f"Equip {item_name}",
            command=lambda i=item_name:
            equip_item(i),
            font=BUTTON_FONT,
            bg="#303030",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_inventory,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def equip_item(item_name):

    item = ITEMS.get(item_name)

    if not item:
        return

    if item["type"] == "weapon":

        game["equipment"]["weapon"] = item_name

    elif item["type"] == "armor":

        game["equipment"]["armor"] = item_name

    update_stats()

    messagebox.showinfo(
        "Equipped",
        f"You equipped {item_name}."
    )

    show_equipment()


# ============================================================
# TOWN / SHOPS
# ============================================================

def show_town():

    clear_choices()

    write_story(
        "Town of Blackthorne",
        (
            "The town is recovering from the events of the story.\n\n"
            "You can visit several shops here."
        )
    )

    buttons = [
        ("⚒ Blacksmith", show_blacksmith),
        ("⚕ Apothecary", show_apothecary),
        ("🔮 Mage's Shop", show_mage_shop),
        ("🐉 Dragonforge", show_dragonforge),
        ("🏨 Inn", rest_at_inn),
        ("← Back", show_main_menu)
    ]

    for text, command in buttons:

        button = tk.Button(
            choice_frame,
            text=text,
            command=command,
            font=BUTTON_FONT,
            bg="#303030",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )


def buy_item(item_name):

    item = ITEMS[item_name]

    price = item["price"]

    if game["gold"] < price:

        messagebox.showwarning(
            "Not Enough Gold",
            f"You need {price} gold."
        )

        return

    game["gold"] -= price

    add_item(item_name)

    if item["type"] == "weapon":
        unlock_achievement("Master Trader")

    update_stats()

    messagebox.showinfo(
        "Purchased",
        f"You purchased {item_name}."
    )


def shop_button(item_name):

    item = ITEMS[item_name]

    return tk.Button(
        choice_frame,
        text=f"{item_name} — {item['price']} gold",
        command=lambda i=item_name: buy_item(i),
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )


def show_blacksmith():

    clear_choices()

    write_story(
        "Blacksmith",
        "Weapons forged for adventurers and knights."
    )

    for item in (
        "Iron Sword",
        "Knight's Longsword",
        "Moonsteel Blade"
    ):

        button = shop_button(item)
        button.pack(
            fill="x",
            pady=3
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_town,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def show_apothecary():

    clear_choices()

    write_story(
        "Apothecary",
        "Potions and supplies for adventurers."
    )

    for item in (
        "Potion",
        "Elixir",
        "Mana Tonic",
        "Antidote"
    ):

        button = shop_button(item)

        button.pack(
            fill="x",
            pady=3
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_town,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def show_mage_shop():

    clear_choices()

    write_story(
        "Mage's Shop",
        "Ancient spells and magical knowledge."
    )

    spells_for_sale = {
        "Frost Lance": 100,
        "Thunder": 200,
        "Flame Wall": 250,
        "Starfall": 500
    }

    for spell_name, price in spells_for_sale.items():

        button = tk.Button(
            choice_frame,
            text=f"{spell_name} — {price} gold",
            command=lambda s=spell_name, p=price:
            buy_spell(s, p),
            font=BUTTON_FONT,
            bg="#3d3057",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_town,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def buy_spell(spell_name, price):

    if spell_name in game["spells"]:

        messagebox.showinfo(
            "Already Known",
            f"You already know {spell_name}."
        )

        return

    if game["gold"] < price:

        messagebox.showwarning(
            "Not Enough Gold",
            f"You need {price} gold."
        )

        return

    game["gold"] -= price
    game["spells"].append(spell_name)

    unlock_achievement("Arcane Student")

    update_stats()

    messagebox.showinfo(
        "Spell Learned",
        f"You learned {spell_name}!"
    )


def show_dragonforge():

    clear_choices()

    write_story(
        "Dragonforge",
        (
            "A legendary forge sits at the edge of town.\n\n"
            "Only the strongest adventurers can afford its equipment."
        )
    )

    for item in (
        "Runic Plate",
        "Dragon Mail",
        "Dragonfang"
    ):

        button = shop_button(item)

        button.pack(
            fill="x",
            pady=3
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_town,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def rest_at_inn():

    cost = 20

    if game["gold"] < cost:

        messagebox.showwarning(
            "Not Enough Gold",
            "The inn costs 20 gold."
        )

        return

    game["gold"] -= cost

    game["hp"] = game["max_hp"]
    game["mp"] = game["max_mp"]

    update_stats()

    messagebox.showinfo(
        "Rested",
        "You feel completely refreshed."
    )


# ============================================================
# COMPANIONS
# ============================================================

def show_companions():

    clear_choices()

    if not game["companions"]:

        write_story(
            "Companions",
            (
                "You currently have no permanent companions.\n\n"
                "Some story choices can unlock companions."
            )
        )

    else:

        write_story(
            "Companions",
            "\n".join(game["companions"])
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_main_menu,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


# ============================================================
# ACHIEVEMENTS
# ============================================================

ACHIEVEMENTS = [
    "First Blood",
    "Seasoned Adventurer",
    "Veteran of Eldoria",
    "Well Funded",
    "Collector",
    "Arcane Student",
    "Boss Breaker",
    "Dragon's Shadow",
    "A Helping Hand",
    "Master Trader",
    "Still Standing"
]


def update_achievements():

    if game["level"] >= 5:
        unlock_achievement("Veteran of Eldoria")

    if game["gold"] >= 500:
        unlock_achievement("Well Funded")

    if len(game["inventory"]) >= 8:
        unlock_achievement("Collector")

    if game["flags"].get("helped"):
        unlock_achievement("A Helping Hand")

    if game["hp"] > 0:
        unlock_achievement("Still Standing")


def show_achievements():

    clear_choices()

    update_achievements()

    completed = len(game["achievements"])
    total = len(ACHIEVEMENTS)

    text = (
        f"Achievements unlocked: "
        f"{completed}/{total}\n\n"
    )

    for achievement in ACHIEVEMENTS:

        if achievement in game["achievements"]:
            text += f"✓ {achievement}\n"
        else:
            text += f"○ {achievement}\n"

    write_story(
        "Achievements",
        text
    )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_main_menu,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


# ============================================================
# CHAPTER SELECT
# ============================================================

def chapter_select():

    clear_choices()

    write_story(
        "Chapter Select",
        (
            "Choose a chapter to replay.\n\n"
            "Chapter Select creates a prepared character "
            "so you can jump directly into later content."
        )
    )

    chapters = [
        ("Chapter I", "intro"),
        ("Chapter II", "chapter2"),
        ("Chapter III", "chapter3"),
        ("Chapter IV", "chapter4"),
        ("Chapter V", "chapter5"),
        ("Chapter VI", "chapter6"),
        ("Chapter VII", "chapter7"),
        ("Chapter VIII", "chapter8")
    ]

    for name, scene in chapters:

        button = tk.Button(
            choice_frame,
            text=name,
            command=lambda s=scene:
            start_chapter(s),
            font=BUTTON_FONT,
            bg="#303030",
            fg="white",
            relief="flat",
            padx=10,
            pady=8
        )

        button.pack(
            fill="x",
            pady=2
        )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_main_menu,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def start_chapter(scene):

    global game

    game = new_game()

    game["level"] = 5
    game["max_hp"] = 160
    game["hp"] = 160
    game["max_mp"] = 80
    game["mp"] = 80

    game["strength"] = 18
    game["defense"] = 12
    game["magic"] = 12

    game["gold"] = 500

    add_item("Knight's Longsword")
    add_item("Guard Armor")
    add_item("Potion", 5)
    add_item("Elixir", 2)
    add_item("Mana Tonic", 3)

    game["equipment"]["weapon"] = "Knight's Longsword"
    game["equipment"]["armor"] = "Guard Armor"

    game["spells"] = [
        "Ember",
        "Mending Light",
        "Frost Lance",
        "Thunder"
    ]

    show_scene(scene)


# ============================================================
# SETTINGS
# ============================================================

def show_settings():

    clear_choices()

    sound_status = (
        "ON"
        if game["settings"]["sound"]
        else "OFF"
    )

    music_status = (
        "ON"
        if game["settings"]["music"]
        else "OFF"
    )

    write_story(
        "Settings",
        (
            "Game settings.\n\n"
            f"Sound: {sound_status}\n"
            f"Music: {music_status}\n\n"
            "Audio support can be expanded later."
        )
    )

    sound_button = tk.Button(
        choice_frame,
        text=f"Toggle Sound ({sound_status})",
        command=toggle_sound,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    sound_button.pack(
        fill="x",
        pady=3
    )

    music_button = tk.Button(
        choice_frame,
        text=f"Toggle Music ({music_status})",
        command=toggle_music,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    music_button.pack(
        fill="x",
        pady=3
    )

    back = tk.Button(
        choice_frame,
        text="← Back",
        command=show_main_menu,
        font=BUTTON_FONT,
        bg="#303030",
        fg="white",
        relief="flat",
        padx=10,
        pady=8
    )

    back.pack(
        fill="x",
        pady=8
    )


def toggle_sound():

    game["settings"]["sound"] = not game["settings"]["sound"]

    show_settings()


def toggle_music():

    game["settings"]["music"] = not game["settings"]["music"]

    show_settings()


# ============================================================
# MAIN MENU
# ============================================================

def show_main_menu():

    clear_choices()

    write_story(
        "Kingdom of Ash",
        (
            "Welcome to Eldoria.\n\n"
            "Your choices shape the story.\n"
            "Your equipment changes how you fight.\n"
            "Your decisions determine which ending you reach.\n\n"
            "Choose an option below."
        )
    )

    buttons = [
        ("⚔ Start New Game", start_new_game),
        ("▶ Continue", load_game),
        ("📖 Chapter Select", chapter_select),
        ("🎒 Inventory", show_inventory),
        ("👥 Companions", show_companions),
        ("🏆 Achievements", show_achievements),
        ("🏘 Town / Shops", show_town),
        ("⚙ Settings", show_settings),
        ("💾 Save Game", save_game),
        ("✕ Quit", quit_game)
    ]

    for text, command in buttons:

        button = tk.Button(
            choice_frame,
            text=text,
            command=command,
            font=BUTTON_FONT,
            bg="#303030",
            fg="#eeeeee",
            activebackground="#4a4a4a",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8
        )

        button.pack(
            fill="x",
            pady=3
        )


def start_new_game():

    global game

    game = new_game()

    show_scene("intro")


def quit_game():

    result = messagebox.askyesno(
        "Quit",
        "Are you sure you want to quit?"
    )

    if result:
        root.destroy()


# ============================================================
# START GAME
# ============================================================

update_stats()

show_main_menu()

root.mainloop()