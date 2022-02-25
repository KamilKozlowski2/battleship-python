import random
import os
from typing import List

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

    game = GameController()
    initialize_game(game)

    start_game(game)


def start_game(game: GameController):
    global myFleet, enemyFleet
    # clear the screen
    if (platform.system().lower() == "windows"):
        cmd = 'cls'
    else:
        cmd = 'clear'
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
        if game.debug:
            display_board = ['.' * game.rows] * game.columns
            for i in range(len(enemyFleet)):
                ship = enemyFleet[i]
                for j in range(len(ship.positions)):
                    pos: Position = ship.positions[j]
                    col = pos.column.value - 1
                    row = pos.row - 1
                    s = display_board[col]
                    char = str(i + 1) if not pos.hit else 'x'
                    display_board[col] = s[:row] + char + s[row + 1:]
            for row in display_board:
                print(row)
        print(Fore.YELLOW + "Player, it's your turn" + Style.RESET_ALL)
        position = query_position(game, Fore.CYAN + "Enter coordinates for your shot :" + Style.RESET_ALL)
        is_hit = GameController.check_is_hit(enemyFleet, position)
        game.process_shot(enemyFleet, position)
        if is_hit:
            # GameController.process_shot(enemyFleet, position)
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
        print(Fore.YELLOW + "Enemy ships sunk: " + Fore.GREEN + ",".join(
            (ship.name for ship in enemy_ships_sunk)) + Style.RESET_ALL)
        print(Fore.YELLOW + "Enemy ships not sunk: " + Fore.RED + ",".join(
            (ship.name for ship in enemy_ships_not_sunk)) + Style.RESET_ALL)

        if len(enemy_ships_not_sunk) == 0:
            win_game()
            return

        # TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position(game)
        print(position)
        is_hit = GameController.check_is_hit(myFleet, position)
        print()
        print(
            f"Computer shoot in {str(position)} and {Fore.RED + 'hit your ship!' if is_hit else Fore.GREEN + 'miss'}" + Style.RESET_ALL)
        # TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})
        if is_hit:
            # GameController.process_shot(enemyFleet, position)

            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)
        game.process_shot(myFleet, position)


def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    if number < 1 or number > 8:
        raise Exception("Must be between 1 and 8 inclusive")
    return Position(letter, number)


def query_position(game: GameController, title: str):
    text = input(title)
    try:
        check_debug_string(game, text)
        return parse_position(text)
    except:
        print(Fore.RED + f"Invalid position, must be between A1 and H8" + Style.RESET_ALL)
        print(f"Got text: {title}")
        return query_position(game, title)


def get_random_position(game: GameController):
    rows = game.rows
    columns = game.columns

    letter = Letter(random.randint(1, columns))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position


def initialize_game(game: GameController):
    initialize_myFleet(game)

    initialize_enemyFleet(game)


def initialize_myFleet(game: GameController):
    global myFleet

    myFleet = GameController.initialize_ships()

    print("Please position your fleet (Game board has size from A to H and 1 to 8) :")

    for ship in myFleet:
        print()
        print(f"Please enter the positions for the {ship.name} (size: {ship.size})")

        for i in range(ship.size):
            position_input = query_position(game, Fore.CYAN + "Enter position " + str(i+1) + " of " + str(ship.size) + " (i.e A3):" + Style.RESET_ALL)
            ship.add_position(position_input)
            # TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})


def initialize_enemyFleet(game: GameController):
    global enemyFleet

    enemyFleet = GameController.initialize_ships()

    for i in range(len(enemyFleet)):
        ship = enemyFleet[i]
        roll_ship(game, enemyFleet, ship)


def roll_ship(game: GameController, all_ships: List[Ship], ship: Ship):
    last_roll_valid = False
    start_pos = get_random_position(game)
    direction = random.randint(0, 3)
    length: int = ship.size
    while not last_roll_valid:
        start_pos = get_random_position(game)
        direction = random.randint(0, 3)
        length: int = ship.size

        last_roll_valid = valid_ship(start_pos, length, all_ships, game, direction)


    for s in all_ships:
        for p in s.positions:
            for i in range(length):
                my_pos = add_dir_len_to_position(start_pos, direction, i)
                if my_pos == p:
                    return False

    for i in range(length):
        ship.positions.append(add_dir_len_to_position(start_pos, direction, i))
    return True

def valid_ship(start_pos, length, all_ships, game, direction):
    end_pos: Position
    try:
        end_pos = add_dir_len_to_position(start_pos, direction, length)
    except:
        return False
    if not in_bounds(start_pos, game):
        return False
    if not in_bounds(end_pos, game):
        return False

    for s in all_ships:
        for p in s.positions:
            for i in range(length):
                my_pos: Position
                try:
                    my_pos = add_dir_len_to_position(start_pos, direction, i)
                except:
                    return False
                if my_pos == p:
                    return False
    return True


def in_bounds(pos: Position, game: GameController):
    if pos.column.value < Letter.A.value:
        return False
    if pos.column.value > Letter.H.value:
        return False
    if pos.row < 1:
        return False
    if pos.row > game.rows + 1:
        return False
    return True


def add_dir_len_to_position(pos: Position, direction: int, length: int):
    if direction == 0:
        return Position(Letter(pos.column.value + length), pos.row)
    elif direction == 1:
        return Position(pos.column, pos.row + length)
    elif direction == 2:
        return Position(Letter(pos.column.value - length), pos.row)
    else:
        return Position(pos.column, pos.row - length)

def split_ship_by_status(ships: list):
    ships_sunk = []
    ships_not_sunk = []
    for ship in ships:
        if ship.is_sunk:
            ships_sunk.append(ship)
        else:
            ships_not_sunk.append(ship)
    return ships_sunk, ships_not_sunk


def check_debug_string(game: GameController, text: str):
    if text.lower() == "debug":
        game.debug = True
    if text.lower() == "norandom":
        random.seed(0)


def win_game():
    print("WIN!")


if __name__ == '__main__':
    main()
