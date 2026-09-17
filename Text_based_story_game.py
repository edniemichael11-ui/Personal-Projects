import os
import random
import time

# Auto-install missing packages directly inside your active environment
os.system("pip install pyfiglet rich")

import pyfiglet
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

actions = 0

while True:
    clear_screen()
    
    # 1. MAKE "THE DUNGEON" HEADER MASSIVE USING PYFIGLET + RICH
    raw_title = pyfiglet.figlet_format("THE DUNGEON", font="standard")
    # We strip trailing newlines so the box fits snugly around the art
    styled_title = f"[bold red]{raw_title.rstrip()}[/bold red]"
    
    main_header = Panel(
        Align.center(styled_title),
        border_style="bright_magenta",
        box=box.DOUBLE,
        expand=True
    )
    console.print(main_header)
    print("\n") # Add breathing room below the massive header
    
    # 2. CREATE SMALLER, INDIVIDUAL OPTION BOXES
    # expand=False keeps the boxes sized perfectly to fit their text content
    option_1 = Panel("[bold white]1.[/bold white] [cyan]Start Game[/cyan]", border_style="green", expand=False)
    option_q = Panel("[bold white]Q.[/bold white] [bright_black]Quit Game[/bright_black]", border_style="red", expand=False)
    
    # Print the option boxes
    console.print(option_1)
    console.print(option_q)
    print("\n")
    
    # User input action
    action = input("Action: ").strip().lower()
    
    if action == "1":
        break
    elif action == "q":
        print("\nExiting menu. Goodbye!")
        break
    else:
        print("\nInvalid Entry. Please try again.")
        time.sleep(2)

loading_loop = 0
clear_screen()
print("Hello Adventurer!")
time.sleep(1)
loading_loop = 0
clear_screen()
print("Let Your Adventure Begin")
time.sleep(1)
clear_screen()
while loading_loop <5:
    print("Loading.")
    time.sleep(0.5)
    clear_screen()
    print("Loading..")
    time.sleep(0.5)
    clear_screen()
    print("Loading...")
    time.sleep(0.5)
    clear_screen()
    loading_loop +=1
clear_screen()
        
print("You awake in a flower field!")
print("1. Look Around")
action = ""
while True:
    action = input("What do you do: ").strip()
    if action == "1":
        break
    else:
        print("Invalid Action - Try Again")

clear_screen()
location1 = "Smoke"
flower_field_message = "As you look around you spot a forest, to the North, with with smoke rising above it and to the East you spot what appears to be the roofs of buildings."
while True:
    clear_screen()
    print(flower_field_message)
    print(f"A. Head North - to the {location1}")
    print("B. Head East - Towards the village")
    action = ""

    action =input("Action: ").strip().capitalize()
    map = False

    if action == "A":
        clear_screen()
        print("You head North to the Smoke")
        time.sleep(1)
        clear_screen
        print("As you arrive to the source of the smoke you notice it is a abondend campsite")
        location1 = "Abondend Campsite"
        print("A. Search the Camp")
        print("B. Return to the field")
        action = ""
        action = input("Actions: ").strip().capitalize()
        if action == "A":
            print("You find a Map of the nearby Village") #To be named
            map = True
            print("With this campsite looted and a map in hand you now decide to head to the nearby village")
            break
        elif action == "B":
             flower_field_message = "You arive back to the Flower Field"
             continue
        else:
            print("Invalid Action")
    elif action == "B":
        break

clear_screen()
print("You head to the Village")


