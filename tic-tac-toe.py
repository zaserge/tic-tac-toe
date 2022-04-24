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

VERSION = "0.1"

USER = {'name': "Human", 'mark': 'x'}
ROBOT = {'name': "Robot", 'mark': 'o'}

LINE = 0
N_MARKS = 1

CELL_NUMBER = 0
CELL_VALUE = 1

EMPTY = ' '

table = {7: EMPTY, 8: EMPTY, 9: EMPTY, 
         4: EMPTY, 5: EMPTY, 6: EMPTY, 
         1: EMPTY, 2: EMPTY, 3: EMPTY}

wining_lines = [
    {7, 8, 9}, # up row 
    {4, 5, 6}, # center row
    {1, 2, 3}, # bottom row
    {7, 4, 1}, # left column
    {8, 5, 2}, # center column
    {9, 6, 3}, # right column
    {7, 5, 3}, # first diagonal
    {9, 5, 1}  # second diagonal
]

def draw_table():
    """! Draw game's table

    @return None
    """
    print("  1 2 3")
    print(f"1 {table[7]} {table[8]} {table[9]}")
    print(f"2 {table[4]} {table[5]} {table[6]}")
    print(f"3 {table[1]} {table[2]} {table[3]}")
    

def check_all_lines(mark: str) -> list:
    """! check all lines 

    @return List of tuples (number line, matched marks number)
    """
    return [
        (n, sum([table[cell] == mark for cell in line]))
        for n, line in enumerate(wining_lines)
        ]


def is_winner(mark: str) -> int:
    """! Check if any line contains 3 matches
    
    @return Line number or None
    """
    sorted_lines = sorted(check_all_lines(mark), key=lambda item : item[N_MARKS], reverse=True)
    return sorted_lines[0][LINE] if sorted_lines[0][N_MARKS] == 3 else None


def proceed_turn(choice: int, gamer: set) -> bool:
    """! Do game

    @return True if game ends otherwise False
    """
    if choice == 0:
        draw_table()
        print (f"{gamer['name']} gave up")
        return True
    else:
        table[choice] = gamer['mark']

        if (l := is_winner(gamer['mark'])) is not None:
            for cell in wining_lines[l]:
                table[cell] = gamer['mark'].upper()
            draw_table()
            print (f"{gamer['name']} is winner!!!")
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
    """! Read user choice and do some basic checks

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
    sorted_users_lines = sorted(check_all_lines(USER['mark']), key=lambda item : item[1], reverse=True)
    sorted_robots_lines = sorted(check_all_lines(ROBOT['mark']), key=lambda item : item[1], reverse=True)

    # loking for robot's 2 marks line and win

    for l_number in [line[LINE] for line in sorted_robots_lines if line[N_MARKS] == 2]:
        for cell in wining_lines[l_number]:
            if table[cell] == EMPTY:
                return cell

    # loking for human's 2 marks line and protect
    # also if found a fork it can gave up if flag is set

    defeat_cell = None

    for l_number in [line[LINE] for line in sorted_users_lines if line[N_MARKS] == 2]:
        for cell in wining_lines[l_number]:
            if table[cell] == EMPTY:
                if DO_ROBOT_GAVE_UP:
                    if defeat_cell:
                        return 0
                    else:
                        defeat_cell = cell
                else:
                    return cell
    if defeat_cell:
        return defeat_cell

    # make choice to random free cell

    return random.choice([cell[CELL_NUMBER] for cell in table.items() if cell[CELL_VALUE] == EMPTY])





#
# Start game 
#
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
