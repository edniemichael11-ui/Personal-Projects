import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import urllib.request
import math


# ============================================================
# WORLD WAR STRATEGY GAME
# Standard library only
#
# Features:
# - Start menu
# - Settings
# - Country selection / country lock
# - World map
# - Click + drag map movement
# - Mouse-wheel zoom
# - Performance-oriented map rendering
# - Map / Economy / Military / Research / Diplomacy systems
# - Provinces
# - Province capture
# - Country annexation
# - Buildings
# - Research
# - Units
# - Wars
#
# No save system yet.
# ============================================================


# ------------------------------------------------------------
# MAP DATA
# ------------------------------------------------------------

COUNTRY_URL = (
    "https://raw.githubusercontent.com/nvkelso/"
    "natural-earth-vector/master/geojson/"
    "ne_110m_admin_0_countries.geojson"
)

PROVINCE_URL = (
    "https://raw.githubusercontent.com/nvkelso/"
    "natural-earth-vector/master/geojson/"
    "ne_10m_admin_1_states_provinces.geojson"
)

COUNTRY_FILE = "world_countries.geojson"
PROVINCE_FILE = "world_provinces.geojson"


# ------------------------------------------------------------
# PLAYABLE COUNTRIES
# ------------------------------------------------------------

COUNTRIES = {
    "United States": {
        "population": 131,
        "industry": 18,
        "steel": 16,
        "oil": 14,
        "food": 18,
        "manpower": 8,
        "army": 12,
        "air": 8,
        "navy": 10,
        "factories": 12,
        "farms": 8,
        "mines": 5,
        "oil_fields": 4,
        "ports": 8,
    },

    "Canada": {
        "population": 11,
        "industry": 5,
        "steel": 6,
        "oil": 4,
        "food": 7,
        "manpower": 2,
        "army": 4,
        "air": 2,
        "navy": 2,
        "factories": 4,
        "farms": 5,
        "mines": 4,
        "oil_fields": 2,
        "ports": 5,
    },

    "Mexico": {
        "population": 20,
        "industry": 3,
        "steel": 2,
        "oil": 5,
        "food": 6,
        "manpower": 2,
        "army": 4,
        "air": 1,
        "navy": 1,
        "factories": 3,
        "farms": 4,
        "mines": 2,
        "oil_fields": 3,
        "ports": 3,
    },

    "Brazil": {
        "population": 41,
        "industry": 4,
        "steel": 4,
        "oil": 2,
        "food": 12,
        "manpower": 4,
        "army": 5,
        "air": 1,
        "navy": 2,
        "factories": 4,
        "farms": 10,
        "mines": 4,
        "oil_fields": 1,
        "ports": 5,
    },

    "Argentina": {
        "population": 13,
        "industry": 3,
        "steel": 2,
        "oil": 1,
        "food": 7,
        "manpower": 2,
        "army": 3,
        "air": 1,
        "navy": 1,
        "factories": 3,
        "farms": 5,
        "mines": 2,
        "oil_fields": 1,
        "ports": 3,
    },

    "United Kingdom": {
        "population": 47,
        "industry": 15,
        "steel": 12,
        "oil": 2,
        "food": 8,
        "manpower": 6,
        "army": 9,
        "air": 8,
        "navy": 12,
        "factories": 11,
        "farms": 5,
        "mines": 6,
        "oil_fields": 0,
        "ports": 10,
    },

    "France": {
        "population": 42,
        "industry": 12,
        "steel": 8,
        "oil": 1,
        "food": 9,
        "manpower": 5,
        "army": 10,
        "air": 4,
        "navy": 5,
        "factories": 9,
        "farms": 7,
        "mines": 4,
        "oil_fields": 0,
        "ports": 5,
    },

    "Germany": {
        "population": 69,
        "industry": 20,
        "steel": 18,
        "oil": 3,
        "food": 10,
        "manpower": 10,
        "army": 20,
        "air": 12,
        "navy": 6,
        "factories": 15,
        "farms": 7,
        "mines": 8,
        "oil_fields": 0,
        "ports": 5,
    },

    "Italy": {
        "population": 43,
        "industry": 7,
        "steel": 5,
        "oil": 1,
        "food": 6,
        "manpower": 5,
        "army": 8,
        "air": 4,
        "navy": 5,
        "factories": 6,
        "farms": 4,
        "mines": 2,
        "oil_fields": 0,
        "ports": 6,
    },

    "Spain": {
        "population": 25,
        "industry": 4,
        "steel": 3,
        "oil": 1,
        "food": 6,
        "manpower": 3,
        "army": 5,
        "air": 2,
        "navy": 2,
        "factories": 4,
        "farms": 5,
        "mines": 2,
        "oil_fields": 0,
        "ports": 3,
    },

    "Poland": {
        "population": 35,
        "industry": 5,
        "steel": 5,
        "oil": 1,
        "food": 7,
        "manpower": 4,
        "army": 8,
        "air": 2,
        "navy": 1,
        "factories": 4,
        "farms": 6,
        "mines": 4,
        "oil_fields": 0,
        "ports": 1,
    },

    "Soviet Union": {
        "population": 170,
        "industry": 17,
        "steel": 20,
        "oil": 15,
        "food": 20,
        "manpower": 18,
        "army": 30,
        "air": 10,
        "navy": 5,
        "factories": 14,
        "farms": 12,
        "mines": 12,
        "oil_fields": 8,
        "ports": 5,
    },

    "Turkey": {
        "population": 18,
        "industry": 3,
        "steel": 3,
        "oil": 1,
        "food": 6,
        "manpower": 3,
        "army": 5,
        "air": 1,
        "navy": 1,
        "factories": 3,
        "farms": 5,
        "mines": 2,
        "oil_fields": 0,
        "ports": 2,
    },

    "Iran": {
        "population": 15,
        "industry": 2,
        "steel": 1,
        "oil": 10,
        "food": 5,
        "manpower": 2,
        "army": 3,
        "air": 0,
        "navy": 0,
        "factories": 2,
        "farms": 4,
        "mines": 1,
        "oil_fields": 6,
        "ports": 2,
    },

    "India": {
        "population": 350,
        "industry": 5,
        "steel": 6,
        "oil": 2,
        "food": 22,
        "manpower": 12,
        "army": 12,
        "air": 3,
        "navy": 2,
        "factories": 5,
        "farms": 18,
        "mines": 5,
        "oil_fields": 1,
        "ports": 5,
    },

    "China": {
        "population": 520,
        "industry": 4,
        "steel": 3,
        "oil": 1,
        "food": 30,
        "manpower": 25,
        "army": 25,
        "air": 3,
        "navy": 1,
        "factories": 4,
        "farms": 25,
        "mines": 4,
        "oil_fields": 0,
        "ports": 4,
    },

    "Japan": {
        "population": 72,
        "industry": 12,
        "steel": 10,
        "oil": 1,
        "food": 7,
        "manpower": 8,
        "army": 16,
        "air": 10,
        "navy": 12,
        "factories": 10,
        "farms": 6,
        "mines": 4,
        "oil_fields": 0,
        "ports": 8,
    },

    "Australia": {
        "population": 7,
        "industry": 4,
        "steel": 5,
        "oil": 1,
        "food": 7,
        "manpower": 2,
        "army": 3,
        "air": 2,
        "navy": 2,
        "factories": 3,
        "farms": 5,
        "mines": 4,
        "oil_fields": 0,
        "ports": 5,
    },

    "South Africa": {
        "population": 11,
        "industry": 3,
        "steel": 5,
        "oil": 0,
        "food": 5,
        "manpower": 2,
        "army": 3,
        "air": 1,
        "navy": 1,
        "factories": 3,
        "farms": 4,
        "mines": 5,
        "oil_fields": 0,
        "ports": 4,
    },
}


# ------------------------------------------------------------
# MAP NAME CONVERSION
# ------------------------------------------------------------

WORLD_TO_GAME = {
    "United States of America": "United States",
    "United States": "United States",
    "Russia": "Soviet Union",
    "Russian Federation": "Soviet Union",
    "Türkiye": "Turkey",
    "Turkey": "Turkey",
    "United Kingdom": "United Kingdom",
    "France": "France",
    "Germany": "Germany",
    "Italy": "Italy",
    "Spain": "Spain",
    "Poland": "Poland",
    "Canada": "Canada",
    "Mexico": "Mexico",
    "Brazil": "Brazil",
    "Argentina": "Argentina",
    "Iran": "Iran",
    "India": "India",
    "China": "China",
    "Japan": "Japan",
    "Australia": "Australia",
    "South Africa": "South Africa",
}


# ------------------------------------------------------------
# COLORS
# ------------------------------------------------------------

COUNTRY_COLORS = {
    "United States": "#4d76a8",
    "Canada": "#c94747",
    "Mexico": "#48a868",
    "Brazil": "#d6b42c",
    "Argentina": "#73a9d8",
    "United Kingdom": "#7a4ea3",
    "France": "#406eb0",
    "Germany": "#555555",
    "Italy": "#3c9660",
    "Spain": "#b88a30",
    "Poland": "#c65c72",
    "Soviet Union": "#a53e3e",
    "Turkey": "#b64c4c",
    "Iran": "#5c9660",
    "India": "#d07c3e",
    "China": "#b34b38",
    "Japan": "#d75b5b",
    "Australia": "#6386a8",
    "South Africa": "#8c6f45",
}

NEUTRAL_COLORS = [
    "#8796a5",
    "#718090",
    "#9a8c7a",
    "#697f78",
    "#8a7c91",
    "#78866b",
]


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def download_if_missing(url, filename):
    if os.path.exists(filename):
        return True

    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        return True
    except Exception as e:
        print("Map download failed:", e)
        return False


def load_geojson(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_feature_name(feature):
    props = feature.get("properties", {})

    for key in (
        "NAME",
        "NAME_EN",
        "ADMIN",
        "name",
        "NAME_LONG",
        "admin",
    ):
        value = props.get(key)
        if value:
            return str(value)

    return "Unknown"


def polygon_rings(geometry):
    if not geometry:
        return []

    geom_type = geometry.get("type")
    coords = geometry.get("coordinates", [])

    if geom_type == "Polygon":
        return coords

    if geom_type == "MultiPolygon":
        rings = []
        for polygon in coords:
            rings.extend(polygon)
        return rings

    return []


def point_in_polygon(x, y, polygon):
    inside = False
    j = len(polygon) - 1

    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        intersects = (
            ((yi > y) != (yj > y))
            and
            (
                x
                < (xj - xi)
                * (y - yi)
                / ((yj - yi) or 0.0000001)
                + xi
            )
        )

        if intersects:
            inside = not inside

        j = i

    return inside


# ------------------------------------------------------------
# GAME LOGIC
# ------------------------------------------------------------

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.country_data = {
            country: data.copy()
            for country, data in COUNTRIES.items()
        }

        self.money = {
            country: 100 + self.country_data[country]["industry"] * 20
            for country in self.country_data
        }

        self.research = {
            country: {
                "industry": 0,
                "infantry": 0,
                "armor": 0,
                "air": 0,
                "naval": 0,
                "logistics": 0,
            }
            for country in self.country_data
        }

        self.units = {
            country: {
                "infantry": self.country_data[country]["army"],
                "armor": 0,
                "aircraft": self.country_data[country]["air"],
                "ships": self.country_data[country]["navy"],
            }
            for country in self.country_data
        }

        self.year = 1939
        self.month = 1

        self.selected = "Germany"
        self.locked = False

        self.wars = set()
        self.annexed = set()

        self.provinces = {}
        self.province_counter = 0

        self.log = [
            "Campaign initialized.",
            "Select a country and lock it in.",
        ]

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    def add_log(self, text):
        self.log.insert(0, text)
        self.log = self.log[:100]

    def pair(self, a, b):
        return tuple(sorted((a, b)))

    def at_war(self, a, b):
        return self.pair(a, b) in self.wars

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    def next_month(self):
        self.month += 1

        if self.month > 12:
            self.month = 1
            self.year += 1

        for country, data in self.country_data.items():
            if country in self.annexed:
                continue

            self.money[country] += (
                20
                + data["factories"] * 9
                + data["industry"] * 2
            )

            data["steel"] += data["mines"]
            data["oil"] += data["oil_fields"]
            data["food"] += data["farms"]

            manpower_gain = max(
                1,
                int(data["population"] * 0.002)
            )

            data["manpower"] += manpower_gain

        self.add_log(
            f"{self.month:02d}/{self.year}: "
            "monthly resources collected."
        )

    # --------------------------------------------------------
    # BUILDINGS
    # --------------------------------------------------------

    def build(self, country, building):
        if country in self.annexed:
            return False, "Country has been annexed."

        costs = {
            "factory": 120,
            "farm": 80,
            "mine": 100,
            "oil": 140,
            "port": 110,
        }

        if building not in costs:
            return False, "Unknown building."

        cost = costs[building]

        if self.money[country] < cost:
            return False, "Not enough money."

        self.money[country] -= cost

        key_map = {
            "factory": "factories",
            "farm": "farms",
            "mine": "mines",
            "oil": "oil_fields",
            "port": "ports",
        }

        self.country_data[country][key_map[building]] += 1

        self.add_log(
            f"{country} constructed a {building}."
        )

        return True, f"{building.title()} constructed."

    # --------------------------------------------------------
    # RESEARCH
    # --------------------------------------------------------

    def research_tech(self, country, tech):
        if tech not in self.research[country]:
            return False, "Unknown technology."

        cost = 80 + self.research[country][tech] * 50

        if self.money[country] < cost:
            return False, "Not enough money."

        self.money[country] -= cost
        self.research[country][tech] += 1

        self.add_log(
            f"{country} researched {tech} level "
            f"{self.research[country][tech]}."
        )

        return True, "Research completed."

    # --------------------------------------------------------
    # UNITS
    # --------------------------------------------------------

    def recruit(self, country, unit):
        costs = {
            "infantry": 35,
            "armor": 100,
            "aircraft": 90,
            "ships": 140,
        }

        manpower_cost = {
            "infantry": 1,
            "armor": 1,
            "aircraft": 0,
            "ships": 0,
        }

        if unit not in costs:
            return False, "Unknown unit."

        cost = costs[unit]

        if self.money[country] < cost:
            return False, "Not enough money."

        if self.country_data[country]["manpower"] < manpower_cost[unit]:
            return False, "Not enough manpower."

        self.money[country] -= cost
        self.country_data[country]["manpower"] -= manpower_cost[unit]

        self.units[country][unit] += 1

        self.add_log(
            f"{country} produced 1 {unit}."
        )

        return True, "Unit produced."

    # --------------------------------------------------------
    # WAR
    # --------------------------------------------------------

    def declare_war(self, attacker, defender):
        if attacker == defender:
            return False, "You cannot declare war on yourself."

        if defender in self.annexed:
            return False, "That country no longer exists."

        key = self.pair(attacker, defender)

        if key in self.wars:
            return False, "Already at war."

        self.wars.add(key)

        self.add_log(
            f"{attacker} declared war on {defender}."
        )

        return True, "War declared."

    # --------------------------------------------------------
    # PROVINCES
    # --------------------------------------------------------

    def register_province(self, owner, rings):
        pid = self.province_counter
        self.province_counter += 1

        self.provinces[pid] = {
            "owner": owner,
            "original_owner": owner,
            "rings": rings,
        }

        return pid

    def capture(self, pid):
        if not self.locked:
            return False, "Lock your country before commanding armies."

        province = self.provinces.get(pid)

        if not province:
            return False, "Province not found."

        owner = province["owner"]

        if owner == self.selected:
            return False, "You already control this province."

        if owner == "Neutral":
            return False, "Neutral provinces cannot currently be invaded."

        if not self.at_war(self.selected, owner):
            return False, f"You are not at war with {owner}."

        if self.units[self.selected]["infantry"] < 2:
            return False, "You need at least 2 infantry."

        if self.country_data[self.selected]["manpower"] < 1:
            return False, "You need manpower."

        self.units[self.selected]["infantry"] -= 2
        self.country_data[self.selected]["manpower"] -= 1

        province["owner"] = self.selected

        self.add_log(
            f"{self.selected} captured a province from {owner}."
        )

        return True, "Province captured."

    # --------------------------------------------------------
    # ANNEXATION
    # --------------------------------------------------------

    def can_annex(self, target):
        if target == self.selected:
            return False

        if target in self.annexed:
            return False

        if not self.at_war(self.selected, target):
            return False

        for province in self.provinces.values():
            if province["original_owner"] == target:
                if province["owner"] == target:
                    return False

        return True

    def annex(self, target):
        if not self.can_annex(target):
            return False, "You must capture all of their provinces first."

        self.annexed.add(target)

        gained_industry = max(
            1,
            self.country_data[target]["industry"] // 2
        )

        self.country_data[self.selected]["industry"] += gained_industry
        self.country_data[self.selected]["factories"] += (
            self.country_data[target]["factories"] // 2
        )

        self.country_data[self.selected]["steel"] += (
            self.country_data[target]["steel"] // 2
        )

        self.country_data[self.selected]["oil"] += (
            self.country_data[target]["oil"] // 2
        )

        for province in self.provinces.values():
            if province["original_owner"] == target:
                province["owner"] = self.selected

        self.add_log(
            f"{self.selected} annexed {target}."
        )

        return True, f"{target} annexed."

    # --------------------------------------------------------
    # DIPLOMACY
    # --------------------------------------------------------

    def end_war(self, target):
        key = self.pair(self.selected, target)

        if key not in self.wars:
            return False, "You are not at war."

        self.wars.remove(key)

        self.add_log(
            f"{self.selected} made peace with {target}."
        )

        return True, "Peace signed."


# ------------------------------------------------------------
# MAIN APP
# ------------------------------------------------------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("WORLD WAR STRATEGY")
        self.root.geometry("1450x900")
        self.root.minsize(1100, 700)

        self.game = Game()

        self.mode = "MAP"

        self.map_detail = "Medium"
        self.show_labels = True
        self.show_grid = False
        self.show_provinces = True
        self.animations = False

        self.map_data = None
        self.province_data = None

        self.map_ready = False

        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0

        self.drag_last_x = 0
        self.drag_last_y = 0
        self.dragging = False

        self.projected_cache = {}
        self.hit_regions = []

        self.draw_after_id = None

        self.canvas_width = 900
        self.canvas_height = 700

        self.download_maps()

        self.show_start_menu()

    # ========================================================
    # MAP FILES
    # ========================================================

    def download_maps(self):
        country_ok = download_if_missing(
            COUNTRY_URL,
            COUNTRY_FILE
        )

        province_ok = download_if_missing(
            PROVINCE_URL,
            PROVINCE_FILE
        )

        if country_ok:
            self.map_data = load_geojson(COUNTRY_FILE)

        if province_ok:
            self.province_data = load_geojson(PROVINCE_FILE)

    # ========================================================
    # START MENU
    # ========================================================

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_menu(self):
        self.clear_window()

        self.root.configure(bg="#17202b")

        outer = tk.Frame(
            self.root,
            bg="#17202b"
        )
        outer.pack(fill="both", expand=True)

        title = tk.Label(
            outer,
            text="WORLD WAR",
            font=("Arial", 48, "bold"),
            fg="#eeeeee",
            bg="#17202b"
        )
        title.pack(pady=(100, 5))

        subtitle = tk.Label(
            outer,
            text="GRAND STRATEGY",
            font=("Arial", 20, "bold"),
            fg="#9aa8b7",
            bg="#17202b"
        )
        subtitle.pack(pady=(0, 50))

        center = tk.Frame(
            outer,
            bg="#202b38",
            bd=1,
            relief="solid"
        )
        center.pack(ipadx=40, ipady=30)

        tk.Label(
            center,
            text="SELECT COUNTRY",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#202b38"
        ).pack(pady=10)

        self.start_country = tk.StringVar(
            value=self.game.selected
        )

        combo = ttk.Combobox(
            center,
            textvariable=self.start_country,
            values=list(COUNTRIES.keys()),
            state="readonly",
            width=30
        )
        combo.pack(pady=10)

        tk.Label(
            center,
            text="MAP DETAIL",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#202b38"
        ).pack(pady=(20, 5))

        self.start_detail = tk.StringVar(
            value=self.map_detail
        )

        detail = ttk.Combobox(
            center,
            textvariable=self.start_detail,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=30
        )
        detail.pack(pady=5)

        tk.Button(
            center,
            text="START CAMPAIGN",
            command=self.start_game,
            font=("Arial", 13, "bold"),
            width=25,
            height=2,
            bg="#3b6e9e",
            fg="white",
            relief="flat"
        ).pack(pady=(30, 10))

        tk.Button(
            center,
            text="SETTINGS",
            command=self.show_settings,
            font=("Arial", 11),
            width=25,
            height=2,
            bg="#394858",
            fg="white",
            relief="flat"
        ).pack(pady=5)

        tk.Button(
            center,
            text="QUIT",
            command=self.root.destroy,
            font=("Arial", 11),
            width=25,
            height=2,
            bg="#633d3d",
            fg="white",
            relief="flat"
        ).pack(pady=5)

        tk.Label(
            outer,
            text="Standard Python / Tkinter edition",
            font=("Arial", 9),
            fg="#697785",
            bg="#17202b"
        ).pack(side="bottom", pady=20)

    # ========================================================
    # SETTINGS
    # ========================================================

    def show_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("430x430")
        win.configure(bg="#202a35")
        win.transient(self.root)
        win.grab_set()

        tk.Label(
            win,
            text="SETTINGS",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#202a35"
        ).pack(pady=20)

        frame = tk.Frame(
            win,
            bg="#202a35"
        )
        frame.pack(fill="x", padx=35)

        detail_var = tk.StringVar(value=self.map_detail)

        tk.Label(
            frame,
            text="Map detail",
            fg="white",
            bg="#202a35"
        ).pack(anchor="w")

        ttk.Combobox(
            frame,
            textvariable=detail_var,
            values=["Low", "Medium", "High"],
            state="readonly"
        ).pack(fill="x", pady=(3, 15))

        labels_var = tk.BooleanVar(value=self.show_labels)
        provinces_var = tk.BooleanVar(value=self.show_provinces)
        grid_var = tk.BooleanVar(value=self.show_grid)
        animations_var = tk.BooleanVar(value=self.animations)

        tk.Checkbutton(
            frame,
            text="Show country labels",
            variable=labels_var,
            fg="white",
            bg="#202a35",
            selectcolor="#303c4a",
            activebackground="#202a35",
            activeforeground="white"
        ).pack(anchor="w")

        tk.Checkbutton(
            frame,
            text="Show province borders",
            variable=provinces_var,
            fg="white",
            bg="#202a35",
            selectcolor="#303c4a",
            activebackground="#202a35",
            activeforeground="white"
        ).pack(anchor="w")

        tk.Checkbutton(
            frame,
            text="Show map grid",
            variable=grid_var,
            fg="white",
            bg="#202a35",
            selectcolor="#303c4a",
            activebackground="#202a35",
            activeforeground="white"
        ).pack(anchor="w")

        tk.Checkbutton(
            frame,
            text="Animations",
            variable=animations_var,
            fg="white",
            bg="#202a35",
            selectcolor="#303c4a",
            activebackground="#202a35",
            activeforeground="white"
        ).pack(anchor="w")

        def apply():
            self.map_detail = detail_var.get()
            self.show_labels = labels_var.get()
            self.show_provinces = provinces_var.get()
            self.show_grid = grid_var.get()
            self.animations = animations_var.get()

            self.invalidate_map()
            win.destroy()

        tk.Button(
            win,
            text="APPLY",
            command=apply,
            width=20,
            height=2,
            bg="#3d709e",
            fg="white",
            relief="flat"
        ).pack(pady=30)

    # ========================================================
    # START GAME
    # ========================================================

    def start_game(self):
        self.game.selected = self.start_country.get()
        self.map_detail = self.start_detail.get()

        self.build_game_interface()

    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def build_game_interface(self):
        self.clear_window()

        self.root.configure(bg="#111820")

        # ----------------------------------------------------
        # TOP MENU
        # ----------------------------------------------------

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(
            menubar,
            tearoff=False
        )

        file_menu.add_command(
            label="New Campaign",
            command=self.new_campaign
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.root.destroy
        )

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        game_menu = tk.Menu(
            menubar,
            tearoff=False
        )

        game_menu.add_command(
            label="Next Month",
            command=self.next_month
        )

        game_menu.add_command(
            label="Lock Country",
            command=self.lock_country
        )

        game_menu.add_command(
            label="Settings",
            command=self.show_settings
        )

        menubar.add_cascade(
            label="Game",
            menu=game_menu
        )

        map_menu = tk.Menu(
            menubar,
            tearoff=False
        )

        map_menu.add_command(
            label="Zoom In",
            command=lambda: self.zoom_map(1.2)
        )

        map_menu.add_command(
            label="Zoom Out",
            command=lambda: self.zoom_map(0.83)
        )

        map_menu.add_command(
            label="Reset View",
            command=self.reset_map_view
        )

        menubar.add_cascade(
            label="Map",
            menu=map_menu
        )

        help_menu = tk.Menu(
            menubar,
            tearoff=False
        )

        help_menu.add_command(
            label="Controls",
            command=self.show_controls
        )

        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.root.config(menu=menubar)

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        top = tk.Frame(
            self.root,
            bg="#202b37",
            height=55
        )
        top.pack(
            fill="x",
            side="top"
        )

        tk.Label(
            top,
            text="WORLD WAR",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#202b37"
        ).pack(
            side="left",
            padx=15
        )

        self.mode_buttons = {}

        for mode in [
            "MAP",
            "ECONOMY",
            "MILITARY",
            "RESEARCH",
            "DIPLOMACY",
        ]:
            button = tk.Button(
                top,
                text=mode,
                command=lambda m=mode: self.change_mode(m),
                font=("Arial", 10, "bold"),
                bg="#303d4b",
                fg="white",
                relief="flat",
                padx=15,
                pady=7
            )
            button.pack(
                side="left",
                padx=2,
                pady=8
            )

            self.mode_buttons[mode] = button

        self.date_label = tk.Label(
            top,
            text="",
            font=("Arial", 11, "bold"),
            fg="#d7e0e8",
            bg="#202b37"
        )

        self.date_label.pack(
            side="right",
            padx=15
        )

        # ----------------------------------------------------
        # MAIN CONTENT
        # ----------------------------------------------------

        body = tk.Frame(
            self.root,
            bg="#111820"
        )
        body.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        left = tk.Frame(
            body,
            width=190,
            bg="#1b252f"
        )
        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="COUNTRIES",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#1b252f"
        ).pack(
            pady=10
        )

        self.country_list = tk.Listbox(
            left,
            bg="#202c38",
            fg="#dfe7ee",
            selectbackground="#426d95",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            font=("Arial", 9)
        )

        self.country_list.pack(
            fill="both",
            expand=True,
            padx=7,
            pady=5
        )

        for country in COUNTRIES:
            self.country_list.insert(
                "end",
                country
            )

        self.country_list.bind(
            "<<ListboxSelect>>",
            self.country_selected
        )

        # ----------------------------------------------------
        # CENTER MAP
        # ----------------------------------------------------

        center = tk.Frame(
            body,
            bg="#111820"
        )

        center.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            center,
            bg="#6d8796",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.canvas.bind(
            "<Configure>",
            self.canvas_resized
        )

        self.canvas.bind(
            "<ButtonPress-1>",
            self.map_press
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.map_drag
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.map_release
        )

        self.canvas.bind(
            "<MouseWheel>",
            self.mouse_wheel
        )

        self.canvas.bind(
            "<Button-4>",
            lambda e: self.zoom_map(1.12, e.x, e.y)
        )

        self.canvas.bind(
            "<Button-5>",
            lambda e: self.zoom_map(0.89, e.x, e.y)
        )

        # ----------------------------------------------------
        # RIGHT PANEL
        # ----------------------------------------------------

        self.right = tk.Frame(
            body,
            width=310,
            bg="#1b252f"
        )

        self.right.pack(
            side="right",
            fill="y"
        )

        self.right.pack_propagate(False)

        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        bottom = tk.Frame(
            self.root,
            height=115,
            bg="#131c24"
        )

        bottom.pack(
            side="bottom",
            fill="x"
        )

        self.log_box = tk.Text(
            bottom,
            bg="#111820",
            fg="#aebdca",
            height=6,
            borderwidth=0,
            font=("Consolas", 9),
            state="disabled"
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=7
        )

        self.update_country_list()
        self.update_date()
        self.change_mode("MAP")

        self.root.after(100, self.initial_map_draw)

    # ========================================================
    # MODE SWITCHING
    # ========================================================

    def change_mode(self, mode):
        self.mode = mode

        for name, button in self.mode_buttons.items():
            if name == mode:
                button.configure(
                    bg="#496f91"
                )
            else:
                button.configure(
                    bg="#303d4b"
                )

        self.update_panel()

        if mode == "MAP":
            self.invalidate_map()

    # ========================================================
    # COUNTRY LIST
    # ========================================================

    def update_country_list(self):
        if not hasattr(self, "country_list"):
            return

        self.country_list.delete(
            0,
            "end"
        )

        for country in COUNTRIES:
            if country in self.game.annexed:
                continue

            self.country_list.insert(
                "end",
                country
            )

        try:
            index = list(
                self.country_list.get(0, "end")
            ).index(
                self.game.selected
            )

            self.country_list.selection_set(index)
            self.country_list.see(index)

        except ValueError:
            pass

    def country_selected(self, event=None):
        if self.game.locked:
            return

        selection = self.country_list.curselection()

        if not selection:
            return

        country = self.country_list.get(
            selection[0]
        )

        self.game.selected = country

        self.update_panel()
        self.invalidate_map()

    # ========================================================
    # LOCK COUNTRY
    # ========================================================

    def lock_country(self):
        self.game.locked = not self.game.locked

        if self.game.locked:
            self.game.add_log(
                f"Country locked: {self.game.selected}."
            )
        else:
            self.game.add_log(
                "Country unlocked."
            )

        self.update_panel()
        self.update_log()

    # ========================================================
    # DATE
    # ========================================================

    def update_date(self):
        if hasattr(self, "date_label"):
            self.date_label.config(
                text=(
                    f"{self.game.month:02d} / "
                    f"{self.game.year}    "
                    f"{self.game.selected}"
                )
            )

    def next_month(self):
        self.game.next_month()

        self.update_date()
        self.update_panel()
        self.update_log()
        self.update_country_list()

    # ========================================================
    # PANEL
    # ========================================================

    def clear_right(self):
        for widget in self.right.winfo_children():
            widget.destroy()

    def make_title(self, text):
        tk.Label(
            self.right,
            text=text,
            font=("Arial", 17, "bold"),
            fg="white",
            bg="#1b252f"
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 8)
        )

    def make_button(
        self,
        text,
        command,
        bg="#344b5f"
    ):
        tk.Button(
            self.right,
            text=text,
            command=command,
            bg=bg,
            fg="white",
            activebackground="#526e86",
            activeforeground="white",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=5,
            pady=7
        ).pack(
            fill="x",
            padx=18,
            pady=3
        )

    def make_info(self, text):
        tk.Label(
            self.right,
            text=text,
            justify="left",
            anchor="nw",
            fg="#cbd5de",
            bg="#1b252f",
            font=("Consolas", 9)
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

    def update_panel(self):
        if not hasattr(self, "right"):
            return

        self.clear_right()

        country = self.game.selected
        data = self.game.country_data[country]

        if self.mode == "MAP":
            self.map_panel(country, data)

        elif self.mode == "ECONOMY":
            self.economy_panel(country, data)

        elif self.mode == "MILITARY":
            self.military_panel(country, data)

        elif self.mode == "RESEARCH":
            self.research_panel(country)

        elif self.mode == "DIPLOMACY":
            self.diplomacy_panel(country)

        self.update_date()

    # ========================================================
    # MAP PANEL
    # ========================================================

    def map_panel(self, country, data):
        self.make_title("MAP")

        self.make_info(
            f"COUNTRY\n"
            f"{country}\n\n"
            f"MONEY       ${self.game.money[country]}\n"
            f"INDUSTRY   {data['industry']}\n"
            f"MANPOWER   {data['manpower']}\n"
            f"ARMY       {self.game.units[country]['infantry']}\n\n"
            f"LOCKED     {'YES' if self.game.locked else 'NO'}"
        )

        self.make_button(
            "LOCK / UNLOCK COUNTRY",
            self.lock_country
        )

        self.make_button(
            "NEXT MONTH",
            self.next_month
        )

        self.make_button(
            "RESET MAP VIEW",
            self.reset_map_view
        )

        self.make_info(
            "MAP CONTROLS\n"
            "Left mouse + drag = move\n"
            "Mouse wheel = zoom\n"
            "Click province = select\n"
            "Capture requires war"
        )

    # ========================================================
    # ECONOMY
    # ========================================================

    def economy_panel(self, country, data):
        self.make_title("ECONOMY")

        self.make_info(
            f"MONEY       ${self.game.money[country]}\n"
            f"INDUSTRY    {data['industry']}\n"
            f"FACTORIES   {data['factories']}\n"
            f"FARMS       {data['farms']}\n"
            f"MINES       {data['mines']}\n"
            f"OIL FIELDS  {data['oil_fields']}\n"
            f"PORTS       {data['ports']}\n\n"
            f"STEEL       {data['steel']}\n"
            f"OIL         {data['oil']}\n"
            f"FOOD        {data['food']}"
        )

        self.make_button(
            "BUILD FACTORY  $120",
            lambda: self.action_build("factory")
        )

        self.make_button(
            "BUILD FARM  $80",
            lambda: self.action_build("farm")
        )

        self.make_button(
            "BUILD MINE  $100",
            lambda: self.action_build("mine")
        )

        self.make_button(
            "BUILD OIL FIELD  $140",
            lambda: self.action_build("oil")
        )

        self.make_button(
            "BUILD PORT  $110",
            lambda: self.action_build("port")
        )

    def action_build(self, building):
        ok, message = self.game.build(
            self.game.selected,
            building
        )

        if not ok:
            messagebox.showwarning(
                "Construction",
                message
            )

        self.update_panel()
        self.update_log()

    # ========================================================
    # MILITARY
    # ========================================================

    def military_panel(self, country, data):
        units = self.game.units[country]

        self.make_title("MILITARY")

        self.make_info(
            f"INFANTRY    {units['infantry']}\n"
            f"ARMOR       {units['armor']}\n"
            f"AIRCRAFT    {units['aircraft']}\n"
            f"SHIPS       {units['ships']}\n\n"
            f"MANPOWER    {data['manpower']}\n"
            f"STEEL       {data['steel']}\n"
            f"OIL         {data['oil']}"
        )

        self.make_button(
            "TRAIN INFANTRY  $35",
            lambda: self.action_recruit("infantry")
        )

        self.make_button(
            "BUILD ARMOR  $100",
            lambda: self.action_recruit("armor")
        )

        self.make_button(
            "BUILD AIRCRAFT  $90",
            lambda: self.action_recruit("aircraft")
        )

        self.make_button(
            "BUILD SHIP  $140",
            lambda: self.action_recruit("ships")
        )

        self.make_button(
            "NEXT MONTH",
            self.next_month
        )

    def action_recruit(self, unit):
        ok, message = self.game.recruit(
            self.game.selected,
            unit
        )

        if not ok:
            messagebox.showwarning(
                "Military",
                message
            )

        self.update_panel()
        self.update_log()

    # ========================================================
    # RESEARCH
    # ========================================================

    def research_panel(self, country):
        self.make_title("RESEARCH")

        techs = self.game.research[country]

        for tech, level in techs.items():
            self.make_info(
                f"{tech.upper():12} LEVEL {level}"
            )

            self.make_button(
                f"RESEARCH {tech.upper()}",
                lambda t=tech: self.action_research(t)
            )

    def action_research(self, tech):
        ok, message = self.game.research_tech(
            self.game.selected,
            tech
        )

        if not ok:
            messagebox.showwarning(
                "Research",
                message
            )

        self.update_panel()
        self.update_log()

    # ========================================================
    # DIPLOMACY
    # ========================================================

    def diplomacy_panel(self, country):
        self.make_title("DIPLOMACY")

        self.make_info(
            "DECLARE WAR\n"
            "Select a country below."
        )

        for target in COUNTRIES:
            if target == country:
                continue

            if target in self.game.annexed:
                continue

            if self.game.at_war(country, target):
                self.make_button(
                    f"PEACE WITH {target}",
                    lambda t=target: self.make_peace(t),
                    "#684b43"
                )
            else:
                self.make_button(
                    f"DECLARE WAR: {target}",
                    lambda t=target: self.make_war(t),
                    "#663f3f"
                )

        self.make_info(
            "\nANNEXATION\n"
            "Capture all provinces of a country,\n"
            "then use Annex when available."
        )

        for target in COUNTRIES:
            if target == country:
                continue

            if target in self.game.annexed:
                continue

            if self.game.can_annex(target):
                self.make_button(
                    f"ANNEX {target}",
                    lambda t=target: self.make_annex(t),
                    "#704d35"
                )

    def make_war(self, target):
        ok, message = self.game.declare_war(
            self.game.selected,
            target
        )

        if not ok:
            messagebox.showwarning(
                "Diplomacy",
                message
            )

        self.update_panel()
        self.update_log()

    def make_peace(self, target):
        ok, message = self.game.end_war(target)

        if not ok:
            messagebox.showwarning(
                "Diplomacy",
                message
            )

        self.update_panel()
        self.update_log()

    def make_annex(self, target):
        ok, message = self.game.annex(target)

        if not ok:
            messagebox.showwarning(
                "Annexation",
                message
            )

        self.update_country_list()
        self.update_panel()
        self.update_log()
        self.invalidate_map()

    # ========================================================
    # LOG
    # ========================================================

    def update_log(self):
        if not hasattr(self, "log_box"):
            return

        self.log_box.configure(
            state="normal"
        )

        self.log_box.delete(
            "1.0",
            "end"
        )

        for item in self.game.log[:15]:
            self.log_box.insert(
                "end",
                item + "\n"
            )

        self.log_box.configure(
            state="disabled"
        )

    # ========================================================
    # MAP DRAWING
    # ========================================================

    def initial_map_draw(self):
        if not hasattr(self, "canvas"):
            return

        self.canvas_width = max(
            300,
            self.canvas.winfo_width()
        )

        self.canvas_height = max(
            300,
            self.canvas.winfo_height()
        )

        self.draw_map()

    def canvas_resized(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height

        self.schedule_map_draw()

    def invalidate_map(self):
        self.projected_cache.clear()
        self.map_ready = False
        self.schedule_map_draw()

    def schedule_map_draw(self):
        if self.draw_after_id:
            try:
                self.root.after_cancel(
                    self.draw_after_id
                )
            except Exception:
                pass

        self.draw_after_id = self.root.after(
            30,
            self.draw_map
        )

    # --------------------------------------------------------
    # GEO PROJECTION
    # --------------------------------------------------------

    def project(self, lon, lat):
        # Equirectangular projection.
        #
        # Keeping this simple is considerably faster than using
        # expensive geographic projection calculations.

        base_scale = min(
            self.canvas_width / 360,
            self.canvas_height / 180
        )

        scale = base_scale * self.zoom

        x = (
            self.canvas_width / 2
            + lon * scale
            + self.pan_x
        )

        y = (
            self.canvas_height / 2
            - lat * scale
            + self.pan_y
        )

        return x, y

    # --------------------------------------------------------
    # DRAW MAP
    # --------------------------------------------------------

    def draw_map(self):
        self.draw_after_id = None

        if not hasattr(self, "canvas"):
            return

        if self.mode != "MAP":
            return

        self.canvas.delete("map")

        self.hit_regions = []

        # ----------------------------------------------------
        # OCEAN
        # ----------------------------------------------------

        self.canvas.create_rectangle(
            0,
            0,
            self.canvas_width,
            self.canvas_height,
            fill="#66808f",
            outline="",
            tags=("map", "ocean")
        )

        # ----------------------------------------------------
        # GRID
        # ----------------------------------------------------

        if self.show_grid:
            self.draw_grid()

        # ----------------------------------------------------
        # COUNTRIES
        # ----------------------------------------------------

        if self.map_data:
            features = self.map_data.get(
                "features",
                []
            )

            for index, feature in enumerate(features):
                self.draw_country_feature(
                    feature,
                    index
                )

        # ----------------------------------------------------
        # PROVINCES
        # ----------------------------------------------------

        if self.show_provinces and self.province_data:
            self.draw_provinces()

        # ----------------------------------------------------
        # LABELS
        # ----------------------------------------------------

        if self.show_labels and self.map_data:
            self.draw_labels()

        self.map_ready = True

    # --------------------------------------------------------
    # COUNTRY FEATURE
    # --------------------------------------------------------

    def draw_country_feature(self, feature, index):
        name = get_feature_name(feature)
        owner = WORLD_TO_GAME.get(
            name,
            "Neutral"
        )

        if owner in self.game.annexed:
            owner = "Neutral"

        color = COUNTRY_COLORS.get(
            owner,
            NEUTRAL_COLORS[index % len(NEUTRAL_COLORS)]
        )

        rings = polygon_rings(
            feature.get("geometry")
        )

        for ring_index, ring in enumerate(rings):
            if len(ring) < 3:
                continue

            points = []

            for lon, lat in ring:
                x, y = self.project(
                    lon,
                    lat
                )

                points.extend(
                    [x, y]
                )

            self.canvas.create_polygon(
                points,
                fill=color,
                outline="#303c44",
                width=1,
                tags=("map", "country")
            )

    # --------------------------------------------------------
    # PROVINCES
    # --------------------------------------------------------

    def draw_provinces(self):
        features = self.province_data.get(
            "features",
            []
        )

        step = 1

        if self.map_detail == "Low":
            step = 5

        elif self.map_detail == "Medium":
            step = 2

        for index in range(
            0,
            len(features),
            step
        ):
            feature = features[index]

            rings = polygon_rings(
                feature.get("geometry")
            )

            owner = self.get_province_owner(
                feature
            )

            color = COUNTRY_COLORS.get(
                owner,
                "#8b9295"
            )

            for ring in rings:
                if len(ring) < 3:
                    continue

                points = []

                min_x = float("inf")
                min_y = float("inf")
                max_x = float("-inf")
                max_y = float("-inf")

                geo_ring = []

                for lon, lat in ring:
                    x, y = self.project(
                        lon,
                        lat
                    )

                    points.extend(
                        [x, y]
                    )

                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

                    geo_ring.append(
                        (lon, lat)
                    )

                if len(points) < 6:
                    continue

                pid = self.game.register_province(
                    owner,
                    [geo_ring]
                )

                self.canvas.create_polygon(
                    points,
                    fill="",
                    outline="#3f4c54",
                    width=1,
                    tags=("map", "province")
                )

                self.hit_regions.append(
                    {
                        "pid": pid,
                        "bbox": (
                            min_x,
                            min_y,
                            max_x,
                            max_y
                        ),
                        "ring": geo_ring,
                    }
                )

        # Prevent province list from growing forever.
        if len(self.game.provinces) > 25000:
            keep = list(
                self.game.provinces
            )[-10000:]

            self.game.provinces = {
                pid: self.game.provinces[pid]
                for pid in keep
            }

    def get_province_owner(self, feature):
        props = feature.get(
            "properties",
            {}
        )

        candidates = [
            props.get("admin"),
            props.get("ADMIN"),
            props.get("name"),
            props.get("NAME"),
            props.get("adm0name"),
            props.get("ADM0NAME"),
        ]

        for value in candidates:
            if value:
                value = str(value)

                if value in WORLD_TO_GAME:
                    return WORLD_TO_GAME[value]

                if value in COUNTRIES:
                    return value

        return "Neutral"

    # --------------------------------------------------------
    # LABELS
    # --------------------------------------------------------

    def draw_labels(self):
        features = self.map_data.get(
            "features",
            []
        )

        for index, feature in enumerate(features):
            name = get_feature_name(feature)

            if name == "Antarctica":
                continue

            rings = polygon_rings(
                feature.get("geometry")
            )

            if not rings:
                continue

            ring = max(
                rings,
                key=len
            )

            if not ring:
                continue

            avg_lon = sum(
                p[0] for p in ring
            ) / len(ring)

            avg_lat = sum(
                p[1] for p in ring
            ) / len(ring)

            x, y = self.project(
                avg_lon,
                avg_lat
            )

            if (
                x < -100
                or x > self.canvas_width + 100
                or y < -100
                or y > self.canvas_height + 100
            ):
                continue

            game_name = WORLD_TO_GAME.get(
                name,
                name
            )

            if game_name in self.game.annexed:
                continue

            self.canvas.create_text(
                x,
                y,
                text=game_name,
                fill="#18232b",
                font=("Arial", 7, "bold"),
                tags=("map", "label")
            )

    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    def draw_grid(self):
        for lon in range(-180, 181, 30):
            x1, _ = self.project(
                lon,
                90
            )

            x2, _ = self.project(
                lon,
                -90
            )

            self.canvas.create_line(
                x1,
                0,
                x2,
                self.canvas_height,
                fill="#8095a0",
                width=1,
                tags=("map", "grid")
            )

        for lat in range(-60, 91, 30):
            _, y = self.project(
                -180,
                lat
            )

            self.canvas.create_line(
                0,
                y,
                self.canvas_width,
                y,
                fill="#8095a0",
                width=1,
                tags=("map", "grid")
            )

    # ========================================================
    # MAP DRAGGING
    # ========================================================

    def map_press(self, event):
        self.drag_last_x = event.x
        self.drag_last_y = event.y
        self.dragging = False

    def map_drag(self, event):
        dx = event.x - self.drag_last_x
        dy = event.y - self.drag_last_y

        if abs(dx) + abs(dy) > 2:
            self.dragging = True

        self.drag_last_x = event.x
        self.drag_last_y = event.y

        # ----------------------------------------------------
        # IMPORTANT PERFORMANCE OPTIMIZATION:
        #
        # Do NOT redraw all country polygons while dragging.
        # Just move the existing canvas items.
        # ----------------------------------------------------

        self.pan_x += dx
        self.pan_y += dy

        self.canvas.move(
            "map",
            dx,
            dy
        )

    def map_release(self, event):
        if self.dragging:
            return

        self.map_click(
            event.x,
            event.y
        )

    # ========================================================
    # MAP CLICK
    # ========================================================

    def map_click(self, x, y):
        if not self.hit_regions:
            return

        # Convert screen coordinates back into approximate
        # geographic coordinates.

        base_scale = min(
            self.canvas_width / 360,
            self.canvas_height / 180
        )

        scale = base_scale * self.zoom

        lon = (
            x
            - self.canvas_width / 2
            - self.pan_x
        ) / scale

        lat = (
            self.canvas_height / 2
            + self.pan_y
            - y
        ) / scale

        for region in reversed(self.hit_regions):
            min_x, min_y, max_x, max_y = region["bbox"]

            # Bboxes need to account for panning because the
            # canvas objects move without rebuilding geometry.

            moved_bbox = (
                min_x + self.pan_x,
                min_y + self.pan_y,
                max_x + self.pan_x,
                max_y + self.pan_y
            )

            if not (
                moved_bbox[0]
                <= x
                <= moved_bbox[2]
                and
                moved_bbox[1]
                <= y
                <= moved_bbox[3]
            ):
                continue

            ring = region["ring"]

            if point_in_polygon(
                lon,
                lat,
                ring
            ):
                pid = region["pid"]

                self.province_selected(
                    pid
                )

                return

    # ========================================================
    # PROVINCE SELECTION
    # ========================================================

    def province_selected(self, pid):
        province = self.game.provinces.get(
            pid
        )

        if not province:
            return

        owner = province["owner"]

        if owner != "Neutral":
            self.game.selected = owner

        # Capture only when locked.
        if (
            self.game.locked
            and owner != self.game.selected
        ):
            ok, message = self.game.capture(
                pid
            )

            if not ok:
                messagebox.showinfo(
                    "Province",
                    message
                )

        self.update_panel()
        self.update_log()

        # Redraw after capture.
        self.invalidate_map()

    # ========================================================
    # ZOOM
    # ========================================================

    def mouse_wheel(self, event):
        if event.delta > 0:
            factor = 1.12
        else:
            factor = 0.89

        self.zoom_map(
            factor,
            event.x,
            event.y
        )

    def zoom_map(
        self,
        factor,
        mouse_x=None,
        mouse_y=None
    ):
        old_zoom = self.zoom

        new_zoom = max(
            0.45,
            min(
                5.0,
                old_zoom * factor
            )
        )

        if new_zoom == old_zoom:
            return

        if mouse_x is None:
            mouse_x = self.canvas_width / 2

        if mouse_y is None:
            mouse_y = self.canvas_height / 2

        # Keep the geographic point underneath the cursor
        # in approximately the same place.

        scale_ratio = new_zoom / old_zoom

        self.pan_x = (
            mouse_x
            - (
                mouse_x
                - self.pan_x
            ) * scale_ratio
        )

        self.pan_y = (
            mouse_y
            - (
                mouse_y
                - self.pan_y
            ) * scale_ratio
        )

        self.zoom = new_zoom

        self.invalidate_map()

    def reset_map_view(self):
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0

        self.invalidate_map()

    # ========================================================
    # NEW CAMPAIGN
    # ========================================================

    def new_campaign(self):
        answer = messagebox.askyesno(
            "New Campaign",
            "Start a new campaign?"
        )

        if not answer:
            return

        self.game.reset()

        self.show_start_menu()

    # ========================================================
    # CONTROLS
    # ========================================================

    def show_controls(self):
        messagebox.showinfo(
            "Controls",
            "MAP\n\n"
            "Left mouse + drag: move map\n"
            "Mouse wheel: zoom\n"
            "Click province: select province\n\n"
            "SYSTEMS\n\n"
            "MAP: map and country overview\n"
            "ECONOMY: buildings and resources\n"
            "MILITARY: army, aircraft and ships\n"
            "RESEARCH: technology\n"
            "DIPLOMACY: wars and annexation\n\n"
            "LOCK COUNTRY\n\n"
            "Lock your country before attempting "
            "military province captures."
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()

    app = App(root)

    root.mainloop()