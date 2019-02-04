# Name: Anisah Alahmed
# Date: 2/4/2019
# Description: A program that performs a variable number of matches consisting of a user-defined number of coin flips, and prints statistics

from random import randint

# get user input for number of games and coin flips per game
games = int(input("How many games?"))
coinFlips = int(input("How many coin tosses per game?"))

# the outcome of each game is recorded here
groupAWins = 0
groupBWins = 0
profWins = 0

# play each game
for game in range(games):

    # the outcome of each flip is recorded here for a game
    bothHeads = 0
    bothTails = 0
    headsAndTails = 0

    print("Game {}:".format(game))
    for toss in range(coinFlips):

        # 0 is heads, 1 is tails
        coinA = randint(0,1)
        coinB = randint(0,1)

        # if heads
        if coinA == 0 and coinB == 0:

            bothHeads += 1

        # if tails
        elif coinA == 1 and coinB == 1:

            bothTails += 1

        # if different
        else:

            headsAndTails += 1

    # calculate percentages for the game and print results
    groupAFlipPercent = bothHeads / coinFlips * 100
    groupBFlipPercent = bothTails / coinFlips * 100
    profFlipPercent = headsAndTails / coinFlips * 100
    print("\tGroup A: {} ({}%); Group B: {} ({}%); Prof: {} ({}%)".format(bothHeads, groupAFlipPercent, bothTails, groupBFlipPercent, headsAndTails, profFlipPercent))

    # determine game winner
    if bothHeads > bothTails and bothHeads > headsAndTails:

        groupAWins += 1

    elif bothTails > bothHeads and bothTails > headsAndTails:

        groupBWins += 1

    else:

        profWins += 1

# calculate percentages accross all games and print results
groupAWinsPercent = groupAWins / games * 100
groupBWinsPercent = groupBWins / games * 100
profWinsPercent = profWins / games * 100
# i want to win sometimes... why do you always have to win??? ;_;
print("Wins: Group A={} ({}%); Group B={} ({}%); Prof={} ({}%)".format(groupAWins, groupAWinsPercent, groupBWins, groupBWinsPercent, profWins, profWinsPercent))
