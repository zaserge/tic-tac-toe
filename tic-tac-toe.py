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

table = {
    7: 7, 8: 8, 9: 9,
    4: 4, 5: 5, 6: 6,
    1: 1, 2: 2, 3: 3,
}

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

    @return None
    """
    print("┌───────┐")
    print(f"│ {table[7]} {table[8]} {table[9]} │")
    print(f"│ {table[4]} {table[5]} {table[6]} │")
    print(f"│ {table[1]} {table[2]} {table[3]} │")
    print("└───────┘")


def check_all_lines(mark: str) -> list:
    """Check all lines

    @param mark {str} Mark to search at table

    @return List of tuples (number line, matched marks number)
    """
    return [
        (n, sum([table[cell] == mark for cell in line]))
        for n, line in enumerate(winning_lines)
    ]


def is_winner(mark: str) -> int:
    """Check if any line contains 3 matches

    @param mark {str} Mark to search at table

    @return Line number or None
    """
    sorted_lines = sorted(
        check_all_lines(mark), key=lambda item: item[N_MARKS], reverse=True
    )
    return sorted_lines[0][LINE] if sorted_lines[0][N_MARKS] == 3 else None


def proceed_turn(choice: int, gamer: dict) -> bool:
    """Do game

    @param choice {int} Gamer's choice
    @param gamer {dict} Gamer's name and mark

    @return True if game ends otherwise False
    """
    if choice == 0:
        draw_table()
        print(f"{gamer['name']} gave up")
        return True
    else:
        table[choice] = gamer["mark"]

        if (l := is_winner(gamer["mark"])) is not None:
            for cell in winning_lines[l]:
                table[cell] = gamer["mark"].upper()
            draw_table()
            print(f"{gamer['name']} is winner!!!")
            return True

    # if no free cell then a draw
    # else let's continue

    if [cell for cell in table.values() if cell == EMPTY]:
        return False
    else:
        draw_table()
        print("A draw")
        return True


def user_turn() -> int:
    """Read user choice and do some basic checks

    @return Choice
    """
    while True:
        choice = input("You choice (1-9 for turn, 0 for exit):")

        if not choice.isdigit():
            print("Wrong action, use only digits.")
            continue
        choice = int(choice)

        if choice == 0:
            return choice
        elif not (0 < choice <= 9):
            print("Wrong action, 1-9 or 0.")
            continue
        elif table[choice] != EMPTY:
            print("Cell is occupied, try another.")
            continue
        else:
            return choice


DO_ROBOT_GAVE_UP = False


def robot_turn() -> int:
    """! Make robot choice. very basic ai

    @return Choice
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
            if table[cell] == EMPTY:
                return cell

    # looking for human's 2 marks line and protect
    # also if found a fork it can gave up if flag is set

    protect_cell = None

    for l_number in [line[LINE] for line in sorted_users_lines if line[N_MARKS] == 2]:
        for cell in winning_lines[l_number]:
            if table[cell] == EMPTY:
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

    # TODO: не ставить если есть в линии враги

    # TODO: играть по стратегии "победа или ничья"

    return random.choice(
        [cell[CELL_NUMBER]
            for cell in table.items() if cell[CELL_VALUE] == EMPTY]
    )


#
# Start game
#


print("Hello. Let's play Tic-Tac-Toe")
print("Cells numbered like digits at keyboard")
draw_table()
name = input("Enter your name (or skip to use default):")
if name:
    USER["name"] = name

# init random numbers generator
random.seed(datetime.now().timestamp())
for cell in table.keys():
    table[cell] = EMPTY

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
