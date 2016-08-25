# Battleship
# ===============
#
# The Classic Game
#
# Author: Miguel de Luis
# Start Date: August, the 18th 2016


# Constants

SHIP_INFO = {"Aircraft Carrier": 5,
             "Battleship": 4,
             "Submarine": 3,
             "Cruiser": 3,
             "Patrol Boat": 2}

SHIP_NAMES = ["Aircraft Carrier",
              "Battleship",
              "Submarine",
              "Cruiser",
              "Patrol Boat"]

BOARD_SIZE = 10

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'

DECORATION_LINE = "\t" + ("-" * 66) + "\n"

NUM_PLAYERS = 2  # Just for code clarity
FLEETS = ["Red", "Blue"]  # Naming the fleets


# Auxiliary functions
def clear_screen():
    # Treehouse code
    print("\033c", end="")


def pass_player_screen(player_name):
    ### Allows to switch turns without revealing sensible data on the screen :)
    clear_screen()
    print("\a\n")
    print(DECORATION_LINE * 2)
    print("\tAdmiral {}, please report to the bridge\n".format(player_name))
    print(DECORATION_LINE * 2)
    print("")
    wait = input("\tAdmiral {}, please press enter when ready.".format(player_name))
    clear_screen()


# Global variables

players = []  # players is a list to contain both gamers

boards = []  # list to contain players' main boards

tracking_boards = []  # list to contain players' tracking boards

ships = [[], []]  # list to contain players' tracking ships


# Classes

class Gamer:
    """
    Gamer class containing the name, remaining ship, the id number (number) and the rival's id number
    The id numbers are the indexes of the players, boards and tracking_boards list
    """

    def __init__(self, name, number):
        self.name = name
        self.remaining_ships = 5
        self.number = number
        self.rival = 1 if self.number == 0 else 0


class Board:
    # Board class map being a list of characters, initailized with the character for empty
    def __init__(self, tracking):
        self.tracking = tracking  # True if it's a tracking board
        self.map = []
        for i in range(BOARD_SIZE):
            self.map.append([EMPTY] * BOARD_SIZE)

    def print_board_heading(self):
        # Treehouse code with minor modifications to include board type
        print("\v")  # Vertical tab, just some white space
        if self.tracking:
            print("Tracking Board".center(40))
            print(("-" * len("Tracking Board")).center(40))
        else:
            print("Main Board".center(40))
            print(("-" * len("Main Board")).center(40))
        print("\n\t   " + " ".join([chr(c) for c in range(ord('A'), ord('A')
                                                          + BOARD_SIZE)]))

    def print_board(self):
        # Treehouse code
        self.print_board_heading()

        row_num = 1
        for row in self.map:
            print("\t" + str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1


class Ship:
    """
    Ship contains the ship's name, its size and hits.
    While hits was not strictly needed, I included it for clarity.
    """

    def __init__(self, ship_name):
        self.locations = []
        self.name = ship_name
        self.size = SHIP_INFO[ship_name]
        self.hits = SHIP_INFO[ship_name]


### Game Start-Up functions

def ask_for_name(prompt, raw_players):
    """
    Asks for name, insuring one unique name will be entered for each player
    """
    raw_player_name = input(prompt).strip().title()
    if raw_player_name == "":
        raw_player_name = ask_for_name("\a\v\t*** Sorry sir, I am afraid I was not able to understand your name.",
                                       raw_players)
    else:
        for player in raw_players:
            if player.name == raw_player_name:
                raw_player_name = ask_for_name(
                    "\a\v\t*** Sorry sir, I am afraid your rival stole your name. Please choose another one that would live in history",
                    raw_players)
                break
    return raw_player_name


def welcome_screen():
    """
    Displays a welcome screen
    """
    clear_screen()
    print("\n" + DECORATION_LINE)
    print("\t *** Welcome to Battleship ***".center(66))
    print("\t the classic game".center(66))
    print("")
    print(DECORATION_LINE)
    print("\v")
    print("\tThe war has left the world in ruins; all that remains are two")
    print("\tsmall fleets that are about to meet in a decisive battle at sea.")
    print("\tThe name of the admirals will live in history, yet only the winner")
    print("\twill determine the fate of humankind.")
    print("\v")


def generate_players(prompt):
    """
    Asks for players names and initializes players
    """
    raw_players = []
    for i in range(NUM_PLAYERS):
        raw_players.append(
            Gamer(ask_for_name(prompt.format(FLEETS[i]), raw_players), i
                  ))
    return raw_players


def generate_ship_location(coordinates, horizontal, ship_size):
    """
    Generates a coordinates list (indexes) containing all the 'squares' occupied by the ship
    :param coordinates: list of coordinates
    :param horizontal: True if ship to be placed horizontally
    :param ship_size: Integer
    :return: coordinates_list
    """
    coordinate_list = []
    if horizontal:
        for i in range(ship_size):
            coordinate_list.append([coordinates[0], coordinates[1] + i])
    else:
        for i in range(ship_size):
            coordinate_list.append([coordinates[0] + i, coordinates[1]])

    return coordinate_list


def validate_ship_location(ship_location, board):
    """
    Returns a Tuple 
    Tulpe [0] >> 
    True if ship's location does not conflict with any other ship location
    or if the ship is to be placed outside the board
    
    Tuple[1] = Error message if any
    
    :param ship_location: list of coordinates for each 'square' occupied by the ship
    :param board: board where the ship is to be placed
    :return: Tuple (Boolean, Error Message)
    """
    for coordinate in ship_location:
        for i in coordinate:  # new code insures no ship placed outside the board
            if i > 9 or i < 0:
                return False, ("\a\v\t\t*** Sir, I am sorry but given those coordinates part of our {}"
                               "\n\twould lay outside of the battle area.")
        if board.map[coordinate[0]][coordinate[1]] != EMPTY:
            return False, ("\a\v\t\t*** Excuse me Sir, I cannot place our {} there"
                           "\n\tas there's other ship in the same area.")
    return True, ""


def set_ship_in_board(ship_location, board, horizontal):
    """
    Updates the board with the appropiate character for each square that the ship is to occupy
    :param ship_location: coordinate list [[x,y], [x1,y1] ... ]
    :param board: Board
    :param horizontal: Boolean
    :return: Board
    """
    if horizontal:
        character = HORIZONTAL_SHIP
    else:
        character = VERTICAL_SHIP

    for coordinate in ship_location:
        x = coordinate[0]
        y = coordinate[1]
        board.map[x][y] = character

    return board


def parse_coordinates(raw_coordinates):
    """
    1. Validates coordinates
    2. Transforms coordinates given as (a,1) into indexes
    :param raw_coordinates:
    :return: list containing two ints and, optionally, an error message
    """
    letters = "abcdefghij"  # only those in our coordinates
    digits = "0123456789"
    parsed_coordinates = []
    coordinate_letter = ""
    coordinate_number = ""

    for character in raw_coordinates.lower():
        # sorts valid characters and numbers into two variable, discarding illegal characters (k-z, etc)
        if character in letters:
            coordinate_letter += character
        elif character in digits:
            coordinate_number += character

    if len(coordinate_number) == 0:
        parsed_coordinates.append("\a\v\t*** Error, Bad coordinates, need one number, please")
    elif int(coordinate_number) > 10 or int(coordinate_number) < 1:
        parsed_coordinates.append("\a\v\t*** Error, Need a number 1 to 10")
    else:
        parsed_coordinates.append(int(coordinate_number) - 1)

    if len(coordinate_letter) == 0:
        parsed_coordinates.append("\a\v\t*** Error, Bad coordinates, missing A-J coordinates")
    elif len(coordinate_letter) > 1:
        parsed_coordinates.append("\a\v\t*** Error, Bad coordinates, only one A-J coordinate, please")
    else:
        parsed_coordinates.append(letters.index(coordinate_letter))

    return parsed_coordinates


def enter_coordinates(message):
    """
    Asks the player for coordinates, returns the parsed values as a list of ints [x,y]
    :param message: A string with a message for the player
    :return: [int]
    """
    validates = True
    raw_coordinates = input("\v" + message)
    parsed_coordinates = parse_coordinates(raw_coordinates)

    for i in parsed_coordinates:
        if isinstance(i, str):  # There's an error message, so it should be printed and not validate
            print(i)
            validates = False

    if validates:
        return parsed_coordinates
    else:
        return enter_coordinates("\a" + message)


def ask_coordinates_for_ship(ship, error_message, player):
    """
    Ship placement interface
    :param ship: Ship to be placed
    :param error_message: str with an error message, if any
    :param player: Gamer
    :return: Board once the ship has been placed
    """

    clear_screen()
    print("\v")
    boards[player.number].print_board()

    if error_message:
        print(error_message)

    print("\v\tAdmiral {} place your {}, ({} spaces).".
          format(player.name, ship.name, ship.size))

    ship_location_bow = enter_coordinates(
        "\tEnter the coordinates for the bow (front) of the {}: ".format(ship.name))
    horizontal = input("\tPlace your ship horizontally or Vertically H/v?: ")

    if horizontal.lower().startswith("v"):
        horizontal = False
    else:
        horizontal = True

    raw_ship_locations = generate_ship_location(ship_location_bow, horizontal, ship.size)

    ship_validation_tuple = validate_ship_location(raw_ship_locations, boards[player.number])
    ship_location_is_valid = ship_validation_tuple[0]

    if ship_location_is_valid:
        boards[player.number] = set_ship_in_board(raw_ship_locations, boards[player.number], horizontal)
        ship.locations = raw_ship_locations
    else:
        error_message = ship_validation_tuple[1]
        clear_screen()
        print("\v")
        boards[player.number].print_board()
        ask_coordinates_for_ship(ship, error_message.format(ship.name), player)

    return boards[player.number]


def set_up_board(player):
    """
    Asks the player to place each ship, returning the board once the player has placed all its ships
    :param player: Gamer
    :return: Board
    """

    pass_player_screen(player.name)

    for ship in ships[player.number]:
        boards_player = ask_coordinates_for_ship(ship, "", player)

    return boards_player


# Main game functions

def sink_ship(sank_ship, t_board, rival_board):
    """
   Updates the players tracting board and the rival's main board with the character for a SUNK vessel '#'
   :param sank_ship: Ship that has been sunk
   :param t_board: Board (tracking)
   :param rival_board: Board (rival's main board)
   :return: Both boards
   """
    for location in sank_ship.locations:
        x = location[0]
        y = location[1]
        t_board[x][y] = SUNK
        rival_board[x][y] = SUNK
    return t_board, rival_board


def hit_ship(gun_aim, rival):
    """
    1. Decrements ship hits
    2. Checks if ship has been sunk. In that case decrements the rivals remaining ship
   :param gun_aim: [int] coordinates as indexes
   :param rival: Gamer
   :return: Ship that has been sunk or None
   """
    for ship in ships[rival.number]:
        if gun_aim in ship.locations:
            ship.hits -= 1
            if ship.hits == 0:
                rival.remaining_ships -= 1
                return ship
            else:
                return None


def print_main_and_tracking_boards(player_number):
    """
    :param player_number: int with the players index
    :return: None
    """
    boards[player_number].print_board()  # cannot print whatever.map as it's the class which owns the method
    tracking_boards[player_number].print_board()


def shoot(player, players, boards, tracking_boards):
    """
    Displays boards, ask the player for coordinates, sinks ships and checks if there's a winner, declaring it
    :param player: Gamer
    :param players: [Gamer]
    :param boards: [Board] main board
    :param tracking_boards: [Board], of the tracking kind
    :return: None or Winner's name
    """

    # auxiliary variables, to shorten code
    rival_board = boards[player.rival].map
    my_board = boards[player.number].map
    t_board = tracking_boards[player.number].map
    rival = players[player.rival]

    print_main_and_tracking_boards(player.number)

    we_must_fire = True

    while we_must_fire:
        gun_aim = enter_coordinates("\tAdmiral {}, please enter the coordinates for your gun: ".format(player.name))
        if t_board[gun_aim[0]][gun_aim[1]] in ".#*":
            print(
                "\a\v\t*** Admiral {}, you might consider firing somewhere else, as we had already fired there.".format(
                    player.name))
        else:
            we_must_fire = False

    if rival_board[gun_aim[0]][gun_aim[1]] in "-|":
        t_board[gun_aim[0]][gun_aim[1]] = HIT
        rival_board[gun_aim[0]][gun_aim[1]] = HIT
        sank_ship = hit_ship(gun_aim, rival)
        if sank_ship:
            t_board, rival_board = sink_ship(sank_ship, t_board, rival_board)
            if rival.remaining_ships:
                print("\v\tCongratulations, Admiral {0}, you sank the {1}! ".format(player.name, sank_ship.name))
            else:
                return player.name
        else:
            print("Hit!")


    else:
        t_board[gun_aim[0]][gun_aim[1]] = MISS
        rival_board[gun_aim[0]][gun_aim[1]] = MISS
        print("Miss!")

    boards[player.rival].map = rival_board
    tracking_boards[player.number].map = t_board
    boards[player.number].map = my_board

    print_main_and_tracking_boards(player.number)

    waiting = input("\v\tAdmiral {}, press enter to end your turn ".format(player.name))


def turn(player, players, boards, tracking_boards):
    """
    Swiches turns between players until there's a winner, returning its name
    :param player: Gamer
    :param players: [Gamer]
    :param boards: [Board] main boards
    :param tracking_boards: [Board] tracking boards
    :return: str winners name
    """
    pass_player_screen(player.name)
    winner = shoot(player, players, boards, tracking_boards)
    rival = players[player.rival]
    if winner:
        return winner
    else:
        return turn(rival, players, boards, tracking_boards)


def main():
    """
    Main function
    :return:
    """
    welcome_screen()
    players = generate_players(
        """\n\tGreetings, Admiral of the {} fleet!
        \t\tMay I have the honor of knowing your name?: """
    )

    # generates boards and ships for both players
    for i in range(NUM_PLAYERS):
        boards.append(Board(tracking=False))
        tracking_boards.append(Board(tracking=True))

        for ship_name in SHIP_NAMES:
            ships[i].append(Ship(ship_name))

        boards[i] = set_up_board(players[i])

    winner = turn(players[0], players, boards, tracking_boards)

    clear_screen()

    print("\v" + DECORATION_LINE)
    print("\v\tCongratulations Admiral {}, you have won this battle!".format(winner))
    print("\v" + DECORATION_LINE)

    for i in range(NUM_PLAYERS):
        print("\v\t\tThis is the most secret information regarding Admiral " + players[i].name)
        boards[i].print_board()

    print("\v")


main()
