# Copyright (c) 2022 zaserge@gmail.com

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import random
from datetime import datetime

VERSION = "0.2"

USER = {"name": "Human", "mark": "x"}
ROBOT = {"name": "Robot", "mark": "o"}

LINE = 0
N_MARKS = 1

CELL_NUMBER = 0
CELL_VALUE = 1

# EMPTY = "·"
EMPTY = "."

# init game table. put number of cell in each cell
TABLE = {n: n for n in range(1, 10)}

winning_lines = [
    {7, 8, 9},  # up row
    {4, 5, 6},  # center row
    {1, 2, 3},  # bottom row

    {7, 4, 1},  # left column
    {8, 5, 2},  # center column
    {9, 6, 3},  # right column

    {7, 5, 3},  # first diagonal
    {9, 5, 1},  # second diagonal
]


def draw_table():
    """Draw game's table
    """
    print("┌───────┐")
    print(f"│ {TABLE[7]} {TABLE[8]} {TABLE[9]} │")
    print(f"│ {TABLE[4]} {TABLE[5]} {TABLE[6]} │")
    print(f"│ {TABLE[1]} {TABLE[2]} {TABLE[3]} │")
    print("└───────┘")


def check_all_lines(mark: str) -> list:
    """Check all lines for matching with player's mark

    Args:
        mark (str): Player's mark

    Returns:
        list: List of tuples (number line, matched marks number)
    """
    return [
        (n, sum([TABLE[cell] == mark for cell in line]))
        for n, line in enumerate(winning_lines)
    ]


def is_winner(mark: str) -> int:
    """Check if any line contains 3 matches

    Args:
        mark (str): Player's mark

    Returns:
        int: Line number or None
    """
    sorted_lines = sorted(
        check_all_lines(mark), key=lambda item: item[N_MARKS], reverse=True
    )
    return sorted_lines[0][LINE] if sorted_lines[0][N_MARKS] == 3 else None


def proceed_turn(choice: int, player: dict) -> bool:
    """Do game

    Args:
        choice (int): Player's move/choice
        player (dict): Player's name and mark

    Returns:
        bool: True if game ends otherwise False
    """
    if choice == 0:
        draw_table()
        print(f"{player['name']} gave up")
        return True
    else:
        TABLE[choice] = player["mark"]

        if (line_number := is_winner(player["mark"])) is not None:
            for cell in winning_lines[line_number]:
                TABLE[cell] = player["mark"].upper()
            draw_table()
            print(f"{player['name']} wins!!!")
            return True

    # if no free cell then a draw
    # else let's continue

    if [cell for cell in TABLE.values() if cell == EMPTY]:
        return False
    else:
        draw_table()
        print("A draw")
        return True


def user_turn() -> int:
    """Read user input and do some basic checks

    Returns:
        int: User's move/choice
    """
    while True:
        choice = input("You choice (1-9 for turn, 0 for exit):")

        if not choice.isdigit():
            print("Wrong action, use only digits.")
            continue
        choice = int(choice)

        if choice == 0:
            return choice
        elif not 0 < choice <= 9:
            print("Wrong action, 1-9 or 0.")
            continue
        elif TABLE[choice] != EMPTY:
            print("Cell is occupied, try another.")
            continue
        else:
            return choice


DO_ROBOT_GAVE_UP = False


def robot_turn() -> int:
    """Make robot choice. very basic ai

    Returns:
        int: Robor's move/choice
    """
    sorted_users_lines = sorted(
        check_all_lines(USER["mark"]), key=lambda item: item[1], reverse=True
    )
    sorted_robots_lines = sorted(
        check_all_lines(ROBOT["mark"]), key=lambda item: item[1], reverse=True
    )

    # looking for robot's 2 marks line and win

    for l_number in [line[LINE] for line in sorted_robots_lines if line[N_MARKS] == 2]:
        for cell in winning_lines[l_number]:
            if TABLE[cell] == EMPTY:
                return cell

    # looking for human's 2 marks line and protect
    # also if found a fork it can gave up if flag is set

    protect_cell = None

    for l_number in [line[LINE] for line in sorted_users_lines if line[N_MARKS] == 2]:
        for cell in winning_lines[l_number]:
            if TABLE[cell] == EMPTY:
                if DO_ROBOT_GAVE_UP:
                    if protect_cell:
                        return 0
                    else:
                        protect_cell = cell
                else:
                    return cell
    if protect_cell:
        return protect_cell

    # make choice to random free cell

    # TODO: не ставить если есть в линии враги  # pylint: disable=fixme

    # TODO: играть по стратегии "победа или ничья"

    return random.choice(
        [cell[CELL_NUMBER]
            for cell in TABLE.items() if cell[CELL_VALUE] == EMPTY]
    )


#
# Start game
#

def main():
    """
    Start game
    """
    print("Hello. Let's play Tic-Tac-Toe")
    print("Cells numbered like digits at keyboard")
    draw_table()
    name = input("Enter your name (or skip to use default):")
    if name:
        USER["name"] = name

    # init random numbers generator
    random.seed(datetime.now().timestamp())
    for cell in TABLE.keys():
        TABLE[cell] = EMPTY

    turn = 1
    while True:
        draw_table()

        print(f"Turn #{turn}: {USER['name']}")
        choice = user_turn()
        if proceed_turn(choice, USER):
            break

        choice = robot_turn()
        if proceed_turn(choice, ROBOT):
            break

        turn += 1


if __name__ == '__main__':
    main()
