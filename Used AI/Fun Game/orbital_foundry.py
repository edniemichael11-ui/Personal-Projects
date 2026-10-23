"""
ORBITAL FOUNDRY
A single-file Pygame management / incremental strategy game.

Requirements:
    pip install pygame-ce
Run:
    python orbital_foundry.py

Controls:
    Mouse: click buttons and tabs
    Space: collect a quick batch of scrap
    1-4: switch tabs
    F5: save
    F9: load
    Esc: quit

The game is designed around interacting production systems:
scrap -> alloys -> components -> modules -> orbital infrastructure.
Automation keeps production running, while research and milestones unlock
new ways to expand. No external images or audio are required.
"""

import pygame
import json
import os
import time

pygame.init()

WIDTH = 1120
HEIGHT = 760
FPS = 60
SAVE_FILE = "orbital_foundry_save.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ORBITAL FOUNDRY")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 17)
SMALL = pygame.font.SysFont("consolas", 14)
MEDIUM = pygame.font.SysFont("consolas", 22, bold=True)
BIG = pygame.font.SysFont("consolas", 34, bold=True)

BG = (12, 17, 29)
PANEL = (22, 31, 49)
PANEL2 = (29, 42, 64)
EDGE = (57, 82, 112)
WHITE = (229, 239, 250)
MUTED = (147, 166, 190)
CYAN = (69, 220, 231)
GREEN = (100, 224, 151)
YELLOW = (255, 205, 91)
ORANGE = (255, 151, 91)
RED = (240, 100, 111)
PURPLE = (178, 145, 255)

# Resource order is important: every resource is stored in the same list.
RESOURCE_NAMES = ["Scrap", "Alloy", "Circuits", "Modules", "Energy",
                  "Research", "Credits", "Data"]
RESOURCE_COLORS = [YELLOW, ORANGE, CYAN, PURPLE, GREEN, CYAN, YELLOW, PURPLE]


def fmt(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 10_000:
        return f"{value / 1000:.1f}k"
    if value >= 100:
        return f"{value:.0f}"
    return f"{value:.1f}"


def draw_text(surface, text, x, y, color=WHITE, font=FONT):
    image = font.render(str(text), True, color)
    surface.blit(image, (x, y))


def panel(surface, rect, color=PANEL, border=EDGE, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 1, border_radius=radius)


class Button:
    def __init__(self, rect, label, action, detail="", color=PANEL2):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action
        self.detail = detail
        self.color = color
        self.enabled = True

    def draw(self, surface, mouse):
        hover = self.rect.collidepoint(mouse)
        fill = self.color if self.enabled else (35, 39, 49)
        if hover and self.enabled:
            fill = (45, 67, 91)
        pygame.draw.rect(surface, fill, self.rect, border_radius=7)
        pygame.draw.rect(surface, CYAN if hover and self.enabled else EDGE,
                         self.rect, 1, border_radius=7)
        label_color = WHITE if self.enabled else MUTED
        draw_text(surface, self.label, self.rect.x + 10, self.rect.y + 7,
                  label_color, SMALL)
        if self.detail:
            draw_text(surface, self.detail, self.rect.x + 10,
                      self.rect.y + 27, MUTED, SMALL)

    def clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        self.resources = [35.0, 0.0, 0.0, 0.0, 20.0, 0.0, 0.0, 0.0]
        self.buildings = [0] * 12
        self.upgrades = [False] * 16
        self.research_done = [False] * 12
        self.tab = 0
        self.buttons = []
        self.message = "Welcome, Director. The station is waiting."
        self.message_timer = 6.0
        self.elapsed = 0.0
        self.total_scrap = 0.0
        self.total_modules = 0.0
        self.total_exports = 0.0
        self.total_research = 0.0
        self.contract_progress = 0.0
        self.contract_index = 0
        self.last_save = "Never"
        self.game_won = False
        self.paused = False
        self.speed = 1.0
        self.stage = 0

        # Building names and base costs: scrap, alloy, circuits, modules, credits.
        self.building_names = [
            "Scrap Drone", "Solar Array", "Smelter", "Assembler",
            "Research Lab", "Data Scanner", "Trade Beacon", "Battery Bank",
            "Orbital Dock", "Nanoforge", "Habitat Printer", "Gate Anchor"
        ]
        self.building_costs = [
            [18, 0, 0, 0, 0], [12, 3, 0, 0, 0], [25, 0, 0, 0, 0],
            [30, 8, 0, 0, 0], [25, 5, 2, 0, 0], [40, 10, 5, 0, 0],
            [55, 15, 4, 0, 0], [30, 8, 0, 0, 0],
            [120, 45, 20, 4, 0], [180, 70, 45, 8, 0],
            [240, 90, 60, 12, 0], [500, 180, 120, 30, 0]
        ]
        self.upgrade_names = [
            "Efficient Sorting", "Reinforced Belts", "Solar Tracking",
            "Induction Furnaces", "Precision Assembly", "Parallel Computing",
            "Deep Scan Arrays", "Market Algorithms", "High-Density Cells",
            "Orbital Logistics", "Microfabrication", "Self-Repairing Hull",
            "Quantum Routing", "Matter Compression", "Stellar Harvest",
            "Singularity Blueprint"
        ]
        self.upgrade_costs = [
            [25, 0, 0, 0], [55, 8, 0, 0], [40, 8, 0, 0],
            [75, 15, 2, 0], [100, 20, 8, 0], [130, 25, 15, 0],
            [150, 30, 20, 0], [180, 45, 25, 0],
            [200, 55, 30, 0], [250, 70, 45, 4],
            [300, 90, 60, 6], [350, 110, 70, 8],
            [420, 140, 100, 10], [500, 170, 120, 15],
            [650, 220, 160, 20], [900, 300, 240, 35]
        ]
        self.research_names = [
            "Automated Sorting", "Basic Metallurgy", "Circuit Theory",
            "Modular Construction", "Orbital Engineering", "Predictive Models",
            "Long-Range Scanning", "Interplanetary Commerce",
            "Nanotechnology", "Adaptive Materials", "Quantum Networks",
            "The Foundry Protocol"
        ]
        self.research_costs = [12, 25, 45, 75, 110, 150, 210, 280, 380, 500, 700, 1000]
        self.contract_names = [
            "Supply Run: export 20 Alloy",
            "Circuit Order: export 15 Circuits",
            "Habitat Order: export 8 Modules",
            "Research Grant: earn 100 Research",
            "Deep Space Contract: export 30 Modules"
        ]
        self.contract_targets = [20, 15, 8, 100, 30]
        self.contract_rewards = [35, 60, 100, 100, 300]
        self.feed = []
        self.add_feed("Station boot sequence complete.")

    def add_feed(self, text):
        self.feed.insert(0, text)
        self.feed = self.feed[:6]

    def say(self, text):
        self.message = text
        self.message_timer = 4.0
        self.add_feed(text)

    def amount(self, index):
        return self.resources[index]

    def has_cost(self, costs):
        # Costs are [scrap, alloy, circuits, modules, credits].
        indexes = [0, 1, 2, 3, 6]
        for i in range(5):
            if self.resources[indexes[i]] < costs[i]:
                return False
        return True

    def pay(self, costs):
        indexes = [0, 1, 2, 3, 6]
        if not self.has_cost(costs):
            return False
        for i in range(5):
            self.resources[indexes[i]] -= costs[i]
        return True

    def scaled_build_cost(self, index):
        cost = self.building_costs[index]
        count = self.buildings[index]
        scale = 1.0 + count * 0.48
        return [max(1, int(v * scale)) if v else 0 for v in cost]

    def build(self, index):
        if index >= 8 and self.stage < 1:
            self.say("That blueprint needs Orbital Engineering.")
            return
        if index >= 10 and self.stage < 2:
            self.say("That blueprint is still classified.")
            return
        cost = self.scaled_build_cost(index)
        if self.pay(cost):
            self.buildings[index] += 1
            self.say(self.building_names[index] + " constructed.")
        else:
            self.say("Not enough resources for that construction.")

    def buy_upgrade(self, index):
        if self.upgrades[index]:
            return
        if index >= 9 and self.stage < 2:
            self.say("This upgrade requires orbital infrastructure.")
            return
        cost = self.upgrade_costs[index]
        indexes = [0, 1, 2, 3]
        for i in range(4):
            if self.resources[indexes[i]] < cost[i]:
                self.say("Insufficient resources for upgrade.")
                return
        for i in range(4):
            self.resources[indexes[i]] -= cost[i]
        self.upgrades[index] = True
        self.say("Upgrade installed: " + self.upgrade_names[index])

    def research(self, index):
        if self.research_done[index]:
            return
        if index >= 4 and self.stage < 1:
            self.say("Research the earlier fields first.")
            return
        if index >= 8 and self.stage < 2:
            self.say("Advanced research requires an orbital network.")
            return
        cost = self.research_costs[index]
        if self.resources[5] < cost:
            self.say("Not enough Research Points.")
            return
        self.resources[5] -= cost
        self.research_done[index] = True
        self.say("Research completed: " + self.research_names[index])
        if index == 3:
            self.stage = max(self.stage, 1)
            self.say("MILESTONE: Orbital construction unlocked!")
        if index == 7:
            self.stage = max(self.stage, 2)
            self.say("MILESTONE: Nanotechnology unlocked!")
        if index == 11:
            self.stage = max(self.stage, 3)
            self.say("MILESTONE: The Foundry Protocol is online!")

    def collect_scrap(self):
        gain = 4.0
        if self.upgrades[0]:
            gain *= 1.5
        self.resources[0] += gain
        self.total_scrap += gain
        self.say("Salvage team recovered " + fmt(gain) + " Scrap.")

    def rates(self):
        # Per-second production. Energy is consumed by industrial buildings.
        scrap = self.buildings[0] * 1.25
        energy = self.buildings[1] * 2.0
        alloy = self.buildings[2] * 0.72
        circuits = self.buildings[3] * 0.34
        research = self.buildings[4] * 0.55
        data = self.buildings[5] * 0.22
        credits = self.buildings[6] * 0.18
        energy += self.buildings[7] * 0.35
        modules = self.buildings[8] * 0.12
        circuits += self.buildings[9] * 0.24
        modules += self.buildings[10] * 0.20
        data += self.buildings[11] * 0.10

        if self.upgrades[1]:
            scrap *= 1.35
        if self.upgrades[2]:
            energy *= 1.5
        if self.upgrades[3]:
            alloy *= 1.5
        if self.upgrades[4]:
            circuits *= 1.5
        if self.upgrades[5]:
            research *= 1.65
        if self.upgrades[6]:
            data *= 1.8
        if self.upgrades[7]:
            credits *= 1.8
        if self.upgrades[8]:
            energy += self.buildings[1] * 0.8
        if self.upgrades[10]:
            modules *= 1.65
        if self.upgrades[14]:
            scrap *= 1.5
            energy *= 1.5
        return [scrap, alloy, circuits, modules, energy, research, credits, data]

    def update(self, dt):
        if self.paused:
            return
        dt *= self.speed
        self.elapsed += dt
        if self.message_timer > 0:
            self.message_timer -= dt

        rate = self.rates()
        # Producers use energy. If energy is low, industrial output slows down.
        demand = (self.buildings[2] * 0.45 + self.buildings[3] * 0.65 +
                  self.buildings[4] * 0.25 + self.buildings[5] * 0.20 +
                  self.buildings[8] * 0.9 + self.buildings[9] * 1.0 +
                  self.buildings[10] * 1.2 + self.buildings[11] * 1.5)
        available = self.resources[4] + rate[4] * dt
        factor = 1.0
        if demand > 0:
            factor = min(1.0, available / (demand * dt + 0.0001))
        # Apply production and material consumption.
        scrap_gain = rate[0] * dt
        self.resources[0] += scrap_gain
        self.total_scrap += scrap_gain

        alloy_rate = rate[1] * factor
        alloy_need = alloy_rate * 0.9
        scrap_used = min(self.resources[0], alloy_need * dt)
        self.resources[0] -= scrap_used
        self.resources[1] += min(alloy_rate * dt, scrap_used / 0.9)

        circuit_rate = rate[2] * factor
        alloy_used = min(self.resources[1], circuit_rate * 0.65 * dt)
        self.resources[1] -= alloy_used
        self.resources[2] += min(circuit_rate * dt, alloy_used / 0.65)

        module_rate = rate[3] * factor
        circuit_used = min(self.resources[2], module_rate * 0.55 * dt)
        alloy_used2 = min(self.resources[1], module_rate * 0.35 * dt)
        self.resources[2] -= circuit_used
        self.resources[1] -= alloy_used2
        actual_modules = min(module_rate * dt, circuit_used / 0.55,
                             alloy_used2 / 0.35)
        self.resources[3] += actual_modules
        self.total_modules += actual_modules

        self.resources[4] = max(0, self.resources[4] + rate[4] * dt - demand * factor * dt)
        self.resources[5] += rate[5] * factor * dt
        self.total_research += rate[5] * factor * dt
        self.resources[6] += rate[6] * dt
        self.resources[7] += rate[7] * factor * dt

        # The trade beacon converts surplus manufactured goods into credits.
        if self.buildings[6] > 0:
            alloy_export = min(self.resources[1], self.buildings[6] * 0.12 * dt)
            circuit_export = min(self.resources[2], self.buildings[6] * 0.05 * dt)
            module_export = min(self.resources[3], self.buildings[6] * 0.025 * dt)
            self.resources[1] -= alloy_export
            self.resources[2] -= circuit_export
            self.resources[3] -= module_export
            earned = alloy_export * 1.3 + circuit_export * 3.0 + module_export * 8.0
            self.resources[6] += earned
            self.total_exports += alloy_export + circuit_export + module_export

        # Contract progress is tied to real production / exports.
        if self.contract_index == 0:
            self.contract_progress += alloy_export if self.buildings[6] else 0
        elif self.contract_index == 1:
            self.contract_progress += circuit_export if self.buildings[6] else 0
        elif self.contract_index in (2, 4):
            self.contract_progress += module_export if self.buildings[6] else 0
        else:
            self.contract_progress += rate[5] * factor * dt

        if self.contract_progress >= self.contract_targets[self.contract_index]:
            reward = self.contract_rewards[self.contract_index]
            self.resources[6] += reward
            self.contract_index = (self.contract_index + 1) % len(self.contract_names)
            self.contract_progress = 0
            self.say("Contract completed! +" + str(reward) + " Credits.")

        # Stage progression also checks accumulated production.
        if self.stage == 0 and self.total_scrap >= 500 and self.total_research >= 15:
            self.say("Your operation is growing. Research Modular Construction.")
        if self.stage >= 3 and self.total_modules >= 250 and self.resources[7] >= 100:
            if not self.game_won:
                self.game_won = True
                self.say("THE FOUNDRY IS COMPLETE. You built a self-expanding orbital network!")

    def resource_rate_text(self, index):
        r = self.rates()[index]
        return f"+{r:.2f}/s"

    def save(self):
        data = [
            self.resources, self.buildings, self.upgrades, self.research_done,
            self.tab, self.elapsed, self.total_scrap, self.total_modules,
            self.total_exports, self.total_research, self.contract_progress,
            self.contract_index, self.stage, self.game_won
        ]
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file)
            self.last_save = time.strftime("%H:%M:%S")
            self.say("Game saved.")
        except OSError:
            self.say("Save failed. Check folder permissions.")

    def load(self):
        if not os.path.exists(SAVE_FILE):
            self.say("No save file found yet.")
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.resources = data[0]
            self.buildings = data[1]
            self.upgrades = data[2]
            self.research_done = data[3]
            self.tab = data[4]
            self.elapsed = data[5]
            self.total_scrap = data[6]
            self.total_modules = data[7]
            self.total_exports = data[8]
            self.total_research = data[9]
            self.contract_progress = data[10]
            self.contract_index = data[11]
            self.stage = data[12]
            self.game_won = data[13]
            self.say("Save loaded.")
        except (OSError, ValueError, IndexError):
            self.say("Save file could not be loaded.")

    def add_button(self, x, y, w, h, label, detail, action, enabled=True):
        button = Button((x, y, w, h), label, action, detail)
        button.enabled = enabled
        self.buttons.append(button)

    def draw_header(self):
        panel(screen, (18, 14, WIDTH - 36, 82), PANEL)
        draw_text(screen, "ORBITAL FOUNDRY", 36, 27, CYAN, BIG)
        stage_names = ["SCRAP YARD", "ORBITAL INDUSTRY", "NANOTECH ERA", "FOUNDRY PROTOCOL"]
        draw_text(screen, "SECTOR: " + stage_names[min(self.stage, 3)],
                  39, 66, MUTED, SMALL)
        draw_text(screen, "TIME  " + self.format_time(), 790, 27, WHITE, MEDIUM)
        draw_text(screen, "F5 SAVE   F9 LOAD   SPACE SALVAGE", 790, 57, MUTED, SMALL)

    def format_time(self):
        seconds = int(self.elapsed)
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def draw_resources(self):
        panel(screen, (18, 106, WIDTH - 36, 94), PANEL)
        for i in range(8):
            col = i % 4
            row = i // 4
            x = 34 + col * 270
            y = 118 + row * 39
            draw_text(screen, RESOURCE_NAMES[i].upper(), x, y, RESOURCE_COLORS[i], SMALL)
            draw_text(screen, fmt(self.resources[i]), x + 105, y - 1, WHITE, FONT)
            draw_text(screen, self.resource_rate_text(i), x + 180, y, MUTED, SMALL)

    def draw_tabs(self):
        labels = ["INDUSTRY", "RESEARCH", "UPGRADES", "MISSIONS"]
        self.buttons = []
        for i, label in enumerate(labels):
            rect = pygame.Rect(18 + i * 174, 214, 164, 38)
            fill = (40, 75, 96) if self.tab == i else PANEL2
            pygame.draw.rect(screen, fill, rect, border_radius=7)
            pygame.draw.rect(screen, CYAN if self.tab == i else EDGE, rect, 1, border_radius=7)
            draw_text(screen, label, rect.x + 40, rect.y + 10, WHITE, SMALL)
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.buttons.append(Button(rect, label, lambda n=i: self.set_tab(n)))

    def set_tab(self, index):
        self.tab = index

    def draw_industry(self):
        panel(screen, (18, 264, 710, 440), PANEL)
        draw_text(screen, "PRODUCTION FACILITIES", 38, 280, CYAN, MEDIUM)
        draw_text(screen, "Build a supply chain. Facilities work automatically while powered.",
                  38, 310, MUTED, SMALL)
        descriptions = [
            "Finds scrap every second", "Generates clean energy",
            "Turns Scrap into Alloy", "Turns Alloy into Circuits",
            "Produces Research Points", "Finds digital Data",
            "Exports goods for Credits", "Stores and supplies power",
            "Builds Modules from parts", "Advanced circuit production",
            "High-output module printer", "Generates advanced Data"
        ]
        for i in range(12):
            col = i // 6
            row = i % 6
            x = 36 + col * 350
            y = 345 + row * 56
            cost = self.scaled_build_cost(i)
            cost_text = f"S{cost[0]} A{cost[1]} C{cost[2]} M{cost[3]}"
            locked = (i >= 8 and self.stage < 1) or (i >= 10 and self.stage < 2)
            affordable = self.has_cost(cost) and not locked
            detail = descriptions[i] + " | " + cost_text
            self.add_button(x, y, 326, 49,
                            self.building_names[i] + "  x" + str(self.buildings[i]),
                            detail, lambda n=i: self.build(n), affordable)
            if locked:
                draw_text(screen, "LOCKED", x + 270, y + 5, RED, SMALL)

        panel(screen, (746, 264, 356, 440), PANEL)
        draw_text(screen, "OPERATIONS", 766, 280, CYAN, MEDIUM)
        draw_text(screen, "Power demand", 766, 326, MUTED, SMALL)
        demand = (self.buildings[2] * .45 + self.buildings[3] * .65 +
                  self.buildings[4] * .25 + self.buildings[5] * .20 +
                  self.buildings[8] * .9 + self.buildings[9] +
                  self.buildings[10] * 1.2 + self.buildings[11] * 1.5)
        draw_text(screen, f"{demand:.2f} / sec", 966, 324, WHITE, FONT)
        draw_text(screen, "Power supply", 766, 356, MUTED, SMALL)
        draw_text(screen, f"{self.rates()[4]:.2f} / sec", 966, 354, GREEN, FONT)
        draw_text(screen, "Total scrap recovered", 766, 399, MUTED, SMALL)
        draw_text(screen, fmt(self.total_scrap), 966, 397, WHITE, FONT)
        draw_text(screen, "Total modules made", 766, 429, MUTED, SMALL)
        draw_text(screen, fmt(self.total_modules), 966, 427, WHITE, FONT)
        draw_text(screen, "Total goods exported", 766, 459, MUTED, SMALL)
        draw_text(screen, fmt(self.total_exports), 966, 457, WHITE, FONT)
        self.add_button(766, 500, 310, 46, "SEND SALVAGE TEAM",
                        "Collect a quick batch of Scrap", self.collect_scrap, True)
        self.add_button(766, 557, 145, 42, "PAUSE" if not self.paused else "RESUME",
                        "Toggle simulation", self.toggle_pause, True)
        self.add_button(930, 557, 146, 42, "SPEED x" + str(self.speed),
                        "Cycle simulation speed", self.cycle_speed, True)
        draw_text(screen, "Tip: energy shortages slow production.", 766, 625, YELLOW, SMALL)
        draw_text(screen, "Build Solar Arrays before over-expanding.", 766, 647, MUTED, SMALL)

    def toggle_pause(self):
        self.paused = not self.paused
        self.say("Simulation paused." if self.paused else "Simulation resumed.")

    def cycle_speed(self):
        speeds = [1.0, 2.0, 3.0]
        self.speed = speeds[(speeds.index(self.speed) + 1) % len(speeds)]
        self.say("Simulation speed: x" + str(self.speed))

    def draw_research(self):
        panel(screen, (18, 264, 1084, 440), PANEL)
        draw_text(screen, "RESEARCH TREE", 38, 280, CYAN, MEDIUM)
        draw_text(screen, "Research points are generated by Research Labs. Unlock fields in order.",
                  38, 310, MUTED, SMALL)
        for i in range(12):
            col = i // 6
            row = i % 6
            x = 38 + col * 520
            y = 348 + row * 56
            done = self.research_done[i]
            locked = (i >= 4 and self.stage < 1) or (i >= 8 and self.stage < 2)
            previous_missing = i > 0 and not self.research_done[i - 1]
            can_buy = not done and not locked and not previous_missing and self.resources[5] >= self.research_costs[i]
            detail = "COST: " + str(self.research_costs[i]) + " RP"
            if done:
                detail = "COMPLETED"
            elif locked or previous_missing:
                detail = "Complete the previous field first"
            self.add_button(x, y, 480, 48,
                            ("✓ " if done else "") + self.research_names[i],
                            detail, lambda n=i: self.research(n), can_buy)
        draw_text(screen, "Milestones: Modular Construction -> Orbital Engineering -> Nanotechnology -> Foundry Protocol",
                  38, 686, YELLOW, SMALL)

    def draw_upgrades(self):
        panel(screen, (18, 264, 1084, 440), PANEL)
        draw_text(screen, "SYSTEM UPGRADES", 38, 280, CYAN, MEDIUM)
        draw_text(screen, "Permanent improvements to your entire production network.",
                  38, 310, MUTED, SMALL)
        for i in range(16):
            col = i // 8
            row = i % 8
            x = 38 + col * 520
            y = 342 + row * 43
            cost = self.upgrade_costs[i]
            done = self.upgrades[i]
            locked = i >= 9 and self.stage < 2
            affordable = (not done and not locked and
                          self.resources[0] >= cost[0] and
                          self.resources[1] >= cost[1] and
                          self.resources[2] >= cost[2] and
                          self.resources[3] >= cost[3])
            detail = f"S{cost[0]} A{cost[1]} C{cost[2]} M{cost[3]}"
            if done:
                detail = "INSTALLED"
            elif locked:
                detail = "Requires Nanotechnology"
            self.add_button(x, y, 480, 38,
                            ("✓ " if done else "") + self.upgrade_names[i],
                            detail, lambda n=i: self.buy_upgrade(n), affordable)

    def draw_missions(self):
        panel(screen, (18, 264, 1084, 440), PANEL)
        draw_text(screen, "CONTRACTS & DIRECTIVES", 38, 280, CYAN, MEDIUM)
        draw_text(screen, "Complete recurring contracts to earn Credits for construction.",
                  38, 310, MUTED, SMALL)
        draw_text(screen, "ACTIVE CONTRACT", 42, 365, YELLOW, SMALL)
        draw_text(screen, self.contract_names[self.contract_index], 42, 397, WHITE, MEDIUM)
        target = self.contract_targets[self.contract_index]
        progress = min(1.0, self.contract_progress / target)
        pygame.draw.rect(screen, PANEL2, (42, 442, 650, 22), border_radius=8)
        pygame.draw.rect(screen, CYAN, (42, 442, int(650 * progress), 22), border_radius=8)
        draw_text(screen, f"{fmt(self.contract_progress)} / {target}", 710, 443, WHITE, SMALL)
        draw_text(screen, "REWARD: " + str(self.contract_rewards[self.contract_index]) + " Credits",
                  42, 483, GREEN, FONT)
        draw_text(screen, "DIRECTIVES", 42, 550, YELLOW, SMALL)
        directives = [
            ("Build 3 Scrap Drones", self.buildings[0] >= 3),
            ("Build 2 Solar Arrays", self.buildings[1] >= 2),
            ("Complete Modular Construction", self.research_done[3]),
            ("Reach the Nanotech Era", self.stage >= 2),
            ("Complete The Foundry Protocol", self.game_won)
        ]
        for i, item in enumerate(directives):
            draw_text(screen, ("✓ " if item[1] else "○ ") + item[0],
                      42, 578 + i * 23, GREEN if item[1] else MUTED, SMALL)
        if self.game_won:
            draw_text(screen, "NETWORK STATUS: SELF-SUSTAINING", 720, 590, GREEN, MEDIUM)

    def draw_footer(self):
        panel(screen, (18, 716, WIDTH - 36, 30), PANEL)
        status = self.message if self.message_timer > 0 else "Systems nominal. Expand carefully, Director."
        draw_text(screen, status, 32, 722, CYAN if self.message_timer > 0 else MUTED, SMALL)

    def draw(self):
        screen.fill(BG)
        self.draw_header()
        self.draw_resources()
        self.draw_tabs()
        if self.tab == 0:
            self.draw_industry()
        elif self.tab == 1:
            self.draw_research()
        elif self.tab == 2:
            self.draw_upgrades()
        else:
            self.draw_missions()
        self.draw_footer()

        mouse = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(screen, mouse)

        if self.game_won:
            draw_text(screen, "FOUNDRY NETWORK COMPLETE", 710, 675, GREEN, SMALL)
        pygame.display.flip()


game = Game()
game.load() if os.path.exists(SAVE_FILE) else None

running = True
while running:
    dt = min(clock.tick(FPS) / 1000.0, 0.08)
    game.update(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                game.collect_scrap()
            elif event.key == pygame.K_F5:
                game.save()
            elif event.key == pygame.K_F9:
                game.load()
            elif event.key == pygame.K_1:
                game.set_tab(0)
            elif event.key == pygame.K_2:
                game.set_tab(1)
            elif event.key == pygame.K_3:
                game.set_tab(2)
            elif event.key == pygame.K_4:
                game.set_tab(3)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Reverse order means the topmost button receives the click first.
            for button in reversed(game.buttons):
                if button.clicked(event.pos):
                    button.action()
                    break

    game.draw()

pygame.quit()
