import random
import os
import colorama
import platform

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
# from torpydo.telemetryclient import TelemetryClient

print("Starting")

myFleet = []
enemyFleet = []

def main():
    # TelemetryClient.init()
    # TelemetryClient.trackEvent('ApplicationStarted', {'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    if (platform.system().lower() == "windows"):
        cmd = 'cls'
    else:
        cmd = 'clear'
    os.system(cmd)
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()

    start_game()

def start_game():
    global myFleet, enemyFleet
    # clear the screen
    if(platform.system().lower()=="windows"):
        cmd='cls'
    else:
        cmd='clear'   
    os.system(cmd)
    print(r'''
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
   |      _  /
   |     /_\
    \    \_/
     """"""""''')

    while True:
        print()
        print(Fore.WHITE + ("-" * 80) + Style.RESET_ALL)
        print(Fore.YELLOW + "Player, it's your turn" + Style.RESET_ALL)
        position = parse_position(input(Fore.BLUE + "Enter coordinates for your shot :" + Style.RESET_ALL))
        is_hit = GameController.check_is_hit(enemyFleet, position)
        if is_hit:
            print(Fore.GREEN + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)

        print(Fore.GREEN + "Yeah ! Nice hit !" + Style.RESET_ALL if is_hit else Fore.RED + "Miss" + Style.RESET_ALL)
        enemy_ships_sunk, enemy_ships_not_sunk = split_ship_by_status(enemyFleet)
        print(Fore.YELLOW + "Enemy ships sunk: " + Fore.GREEN + ",".join((ship.name for ship in enemy_ships_sunk)) + Style.RESET_ALL)
        print(Fore.YELLOW + "Enemy ships not sunk: " + Fore.RED + ",".join((ship.name for ship in enemy_ships_not_sunk)) + Style.RESET_ALL)

        # TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print()
        print(f"Computer shoot in {str(position)} and {Fore.RED + 'hit your ship!' if is_hit else Fore.GREEN + 'miss'}" + Style.RESET_ALL)
        # TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})
        if is_hit:
            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)


def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    position = Position(letter, number)

    return Position(letter, number)

def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position

def initialize_game():
    initialize_myFleet()

    initialize_enemyFleet()

def initialize_myFleet():
    global myFleet

    myFleet = GameController.initialize_ships()

    print("Please position your fleet (Game board has size from A to H and 1 to 8) :")

    for ship in myFleet:
        print()
        print(f"Please enter the positions for the {ship.name} (size: {ship.size})")

        for i in range(ship.size):
            position_input = input(Fore.BLUE + "Enter position " + str(i+1) + " of " + str(ship.size) + " (i.e A3):" + Style.RESET_ALL)
            ship.add_position(position_input)
            # TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})

def initialize_enemyFleet():
    global enemyFleet

    enemyFleet = GameController.initialize_ships()

    enemyFleet[0].positions.append(Position(Letter.B, 4))
    enemyFleet[0].positions.append(Position(Letter.B, 5))
    enemyFleet[0].positions.append(Position(Letter.B, 6))
    enemyFleet[0].positions.append(Position(Letter.B, 7))
    enemyFleet[0].positions.append(Position(Letter.B, 8))

    enemyFleet[1].positions.append(Position(Letter.E, 6))
    enemyFleet[1].positions.append(Position(Letter.E, 7))
    enemyFleet[1].positions.append(Position(Letter.E, 8))
    enemyFleet[1].positions.append(Position(Letter.E, 9))

    enemyFleet[2].positions.append(Position(Letter.A, 3))
    enemyFleet[2].positions.append(Position(Letter.B, 3))
    enemyFleet[2].positions.append(Position(Letter.C, 3))

    enemyFleet[3].positions.append(Position(Letter.F, 8))
    enemyFleet[3].positions.append(Position(Letter.G, 8))
    enemyFleet[3].positions.append(Position(Letter.H, 8))

    enemyFleet[4].positions.append(Position(Letter.C, 5))
    enemyFleet[4].positions.append(Position(Letter.C, 6))

def split_ship_by_status(ships: list):
    ships_sunk = []
    ships_not_sunk = []
    for ship in ships:
        if ship.is_sunk:
            ships_sunk.append(ship)
        else:
            ships_not_sunk.append(ship)
    return ships_sunk, ships_not_sunk


if __name__ == '__main__':
    main()
