#!/usr/bin/python3
""" Provides MasterMind Game, using digits as input

MasterMind require a digits sequence for guess the secret code.
In output gives you a hint on the number of right digits,
in the right position, and on the number of right digits on wrong position.
"""

import random
import sys
import argparse
from os import system, name
from datetime import datetime


__author__ = "Luca Cappelli"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Luca Cappelli"
__status__ = "Dev"

# default value for configuration

digit = 4        # number of digit to guess
score = 2000        # point for the Game
code_seq = []       # array for input sequence
secret_seq = []     # array for random sequence
num_attempt = 0     # number of attempt for score
rank = False        # boolean ranking mode

# function to clear the screen


def clear():
    """ Clear the screen """

    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def save_rank(player, digit, score):
    """ Save the player on the ranking list """

    with open("rank_"+str(digit)+".txt", "a") as f:
        f.write(player+":"+str(score)+"\n")


def print_rank(digit):
    """ Print the top 10 player list """

    print("\n------------ Top 10 players -------------")
    with open("rank_"+str(digit)+".txt", "r") as f:
        for i, line in enumerate(sorted(f, key=lambda line: line.split(":")[1],
                                 reverse=True)):
            print(line)
            if i == 9:
                break


# parse the argument to check the digit number
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-digit", action="store", dest="digit", type=int,
                    help="number of digits to guess. Default is " + str(digit)
                    )
parser.add_argument(
                    "-rank", action="store_true", dest="rank", default=False,
                    help="Save game score to rank list. Default is no ranking"
                    )

args = parser.parse_args()

# if digit argument is present, assign to digit variable
if args.digit:
    digit = args.digit

if args.rank:
    rank = args.rank

# clear the screen before print output
clear()

print(
    "*******    Welcome to Mastermind    *******"
    "\n------- To quit program use CTRL+c -------\n\n"
)


# define the secret random sequence
for secret in range(digit):
    secret_seq.append(random.randint(0, 9))

# input the player name if rank switch is enabled
if rank:
    try:
        player = input('Enter your name : ')
        print("")
    except (KeyboardInterrupt, SystemExit):
        # CTRL+C pressed, exit
        print("\nbye bye. The secret sequence is :"+str(secret_seq))
        quit()

print("Insert your sequence of " + str(digit) + " digits")

# save the timestamp for score if rank switch is enabled
if rank:
    start_time = datetime.now().timestamp()

# loop until CTRL+C or guess the secret sequence
while True:
    try:
        digit_input = input('>: ')
        digit_input_int = int(digit_input)
    except (KeyboardInterrupt, SystemExit):
        # CTRL+C pressed, exit
        print("\nbye bye. The secret sequence is :"+str(secret_seq))
        break

    except EOFError:
        # CTRL+D pressed, continue
        print("")
        pass

    except ValueError:
        # sequence is not syntactically correct
        print("Error! This is not a digit sequence. Try again.")
    else:
        # if the provided sequence is syntactically correct
        n_digit = len(digit_input)

        # if the number of digit input is the same of configured,
        # check against secret sequence
        if n_digit == digit:
            same_pos = 0
            diff_pos = 0

            code_seq = [int(x) for x in digit_input]

            for number in range(digit):
                if secret_seq[number] == code_seq[number]:
                    same_pos += 1
                elif code_seq[number] in secret_seq:
                    diff_pos += 1

            if same_pos == digit:
                print("\nYou win! The secret sequence is :" + str(secret_seq))
                if rank:
                    time_interval = datetime.now().timestamp() - start_time
                    score = int(score - (num_attempt + time_interval))
                    if score < 0:
                        score = 0
                    print("\nYour score is :" + str(score))
                    save_rank(player, digit, score)
                    print_rank(digit)
                break
            else:
                num_attempt += 1
                print(
                    "Same position: "+str(same_pos) + "\n"
                    "Different position: " + str(diff_pos) + "\n"
                    "---------------------------------"
                )

        else:
            print(
                "Error! The sequence should be " + str(digit) +
                " digit lenght"
            )
