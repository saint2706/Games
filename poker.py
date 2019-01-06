import random as r
from collections import Counter
import time
import sys

#Problems:
#Sometimes(very rarely) same card may be dealt twice
#last statement open to malicious input
pot = 0
money1 = 1000
money2 = 1000
playround = 0
check = 0
com_count = 1
pl1_card1 = 0
pl1_card2 = 0
pl2_card1 = 0
pl2_card2 = 0
com1 = 0
com2 = 0
com3 = 0
fold=0
bet1=0
bet2=0
# nop= int(input('No of players(1-4):'))

spade_cards = {1: 'Ace of spades', 2: 'Two of spades', 3: 'three of spades', 4: 'four of spades', 5: 'five of spades'
    , 6: 'six of spades', 7: 'seven of spades', 8: 'eight of spades', 9: 'nine of spades'
    , 10: 'ten of spades', 11: 'jack of spades', 12: 'queen of spades', 13: 'king of spades'}

diamond_cards = {14: 'Ace of diamond', 15: 'Two of diamond', 16: 'three of diamond', 17: 'four of diamond',
                 18: 'five of diamond'
    , 19: 'six of diamond', 20: 'seven of diamond', 21: 'eight of diamond', 22: 'nine of diamond'
    , 23: 'ten of diamond', 24: 'jack of diamond', 25: 'queen of diamond', 26: 'king of diamond'}

heart_cards = {27: 'Ace of heart', 28: 'Two of heart', 29: 'three of heart', 30: 'four of heart', 31: 'five of heart'
    , 32: 'six of heart', 33: 'seven of heart', 34: 'eight of heart', 35: 'nine of heart'
    , 36: 'ten of heart', 37: 'jack of heart', 38: 'queen of heart', 39: 'king of heart'}

clubs_cards = {40: 'Ace of clubs', 41: 'Two of clubs', 42: 'three of clubs', 43: 'four of clubs', 44: 'five of clubs'
    , 45: 'six of clubs', 46: 'seven of clubs', 47: 'eight of clubs', 48: 'nine of clubs'
    , 49: 'ten of clubs', 50: 'jack of clubs', 51: 'queen of clubs', 52: 'king of clubs'}



pok=r'''         |-----------   |-----------|   |     /      |----------    |------------
         |          |   |           |   |   /        |              |           |
         |          |   |           |   |  /         |              |           |
         |----------|   |           |   |/           |              |-----------|
         |              |           |   |\           |-----         |  \  
         |              |           |   |  \         |              |    \
         |              |           |   |   \        |              |     \
         |              |-----------|   |    \       |----------    |      \
'''


for l in pok:
    sys.stdout.write(l)
    sys.stdout.flush()
    time.sleep(0.001)

print('Rules for poker------>')
print('In poker a total of 5 cards are dealt to each player over a period of 4 rounds. The player who has the better hand or better combination of cards wins')
a='''\nBelow are the card combinations that are possible and the probability of getting that combination in order of best-worst\n

Royal Flush: 10,Jack,Queen,King,Ace of the same suit (0.0001% probability)

Straight Flush : All cards in sequence and of the same suit (0.001% probability)

Four of a kind: Four cards of the same rank and one misc card (0.02% probability)

Full House: Three cards of the same rank and Two cards of another rank (0.14% probability)

Flush: All 5 cards of the same suit ,not required to be in sequence (0.2% probability)

Straight: All 5 cards in sequence , not required to be of the same suit (0.4% probability)

Three of kind: Three cards of the same rank (2.1% probability)

Two pair: Two cards of the same rank and another 2 cards of the same rank (4.7% probability)

Single pair: Two cards of the same rank (42.2% probability)

High card: When all of the above combinations do not apply then the value of the greatest card in the deck is considered (50% probability)
 '''

print(a)


print('1.Each player is dealt 2 cards at the beggining of the game.These are know as hole cards')
print('2.After the hole cards are dealt round one begins and each player has the oppurtunity to place a bet,fold or check')
print('Check: It means the player does not wish to place a bet now and play goes on' )
print('Fold: If you think that your cards are not good enough ,you may fold giving the opponent the win.\n You also lose all the money that has been bet till that point')
print('Call: this appears in the later rounds. It means to bet  the same amount as the player before you')
print('Raise:Same as bet')
print('\nPress enter to start!')
start=input()
if start=='':
    print('Welcome! as a starting gift each player is given 1000$')


def player1():
    global playround, bet1_amt, money1, pl1_card1, pl1_card2, pl1_v1, pl1_v2,fold,bet1
    playround += 1
    if fold>0:
        return
    if playround == 1:
        hole1 = r.randrange(1, 53)
        hole2 = r.randrange(1, 53)

        if hole1 >= 1 and hole1 <= 13:
            for k, v in spade_cards.items():
                if k == hole1:
                    print('Player1 your first card is :', v)
                    pl1_card1 = k
                    pl1_v1 = v
        elif hole1 > 13 and hole1 <= 26:
            for k, v in diamond_cards.items():
                if k == hole1:
                    print('Player1 your first card is :', v)
                    pl1_card1 = k
                    pl1_v1 = v
        elif hole1 >= 27 and hole1 <= 39:
            for k, v in heart_cards.items():
                if k == hole1:
                    print('Player1 your first card is :', v)
                    pl1_card1 = k
                    pl1_v1 = v

        elif hole1 >= 40 and hole1 <= 52:
            for k, v in clubs_cards.items():
                if k == hole1:
                    print('Player1 your first card is :', v)
                    pl1_card1 = k
                    pl1_v1 = v

        if hole2 >= 1 and hole2 <= 13:
            for k, v in spade_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :', v)
                    pl1_card2 = k
                    pl1_v2 = v
        elif hole2 > 13 and hole2 <= 26:
            for k, v in diamond_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :', v)
                    pl1_card2 = k
                    pl1_v2 = v
        elif hole2 >= 27 and hole2 <= 39:
            for k, v in heart_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :', v)
                    pl1_card2 = k
                    pl1_v2 = v

        elif hole2 >= 40 and hole2 <= 52:
            for k, v in clubs_cards.items():
                if k == hole2:
                    print('Player1 your second card is :', v)
                    pl1_card2 = k
                    pl1_v2 = v

        # bets
    while playround == 1:
        print()
        bet1 = input('Player1 Would you like to place the initial bet or fold or check(b/f/c)?')
        if bet1 == 'b':
            print('How much is your bet Player1 (1-', money1, ')')
            bet1_amt = int(input())
            if bet1_amt > money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                global pot
                pot += bet1_amt
                money1 -= bet1_amt
                print('The value of the pot currently is:', pot)
                print()
                print('money left:', money1)
                print()
                break


        elif bet1 == 'f':
            #print('We are sorry to see you go ')
            return

        elif bet1 == 'c':
            print('Player1 has decided to check')
            if pot == 0:
                bet1_amt = 0
                time.sleep(2)
                print()
                print('The value of the pot currently is:', pot)
                print()
                break
            else:
                pot += bet1_amt
                print()
                print('The value of the pot currently is:', pot)  # not important because this is only for round 1
                print()
                print('Money left(Player1):', money1)
                print()
                break

    while playround == 3 or playround == 5:
        print()
        bet1 = input('Player1 Would you like to call/fold/raise?')
        if bet1 == 'r':
            print()
            bet1_amt = int(input('How much would you like to raise (1-', money1, ')?'))
            # if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            if bet1_amt > money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                pot += bet1_amt
                money1 -= bet1_amt
                print()
                print('Money left(player1)', money1)
                print()
                print('The value of the pot currently is:', pot)
                break
        elif bet1 == 'c':
            if bet2_amt > money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                print('player 1 has decided to call')
                pot += bet2_amt
                print()
                print('The value of the pot currently is:', pot)
                money1 -= bet2_amt
                bet1_amt = bet2_amt
                print()
                print('money left for player1', money1)
                break

        elif bet1=='f':
            return


def player2():

    global playround, bet2_amt, money2, pl2_card1, pl2_card2, pl2_v1, pl2_v2,fold,bet2

    playround += 1
    if fold>0:
        return
    # print('hello')
    if playround == 2:
        hole1 = r.randrange(1, 53)
        hole2 = r.randrange(1, 53)

        if hole1 >= 1 and hole1 <= 13:
            for k, v in spade_cards.items():
                if k == hole1:
                    print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v
        elif hole1 > 13 and hole1 <= 26:
            for k, v in diamond_cards.items():
                if k == hole1:
                    print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v
        elif hole1 >= 27 and hole1 <= 39:
            for k, v in heart_cards.items():
                if k == hole1:
                    print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v

        elif hole1 >= 40 and hole1 <= 52:
            for k, v in clubs_cards.items():
                if k == hole1:
                    print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v

        if hole2 >= 1 and hole2 <= 13:
            for k, v in spade_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v
        elif hole2 > 13 and hole2 <= 26:
            for k, v in diamond_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v
        elif hole2 >= 27 and hole2 <= 39:
            for k, v in heart_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v

        elif hole2 >= 40 and hole2 <= 52:
            for k, v in clubs_cards.items():
                if k == hole2:
                    print('Player2 your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v

        # bets

    while playround == 2:
        print()
        print()
        bet2 = input('Player2 Would you like to place the initial bet or fold or check(b/f/c)?')

        if bet2 == 'b':
            print('How much is your bet Player2 (1-', money2, ')')
            bet2_amt = int(input())
            if bet2_amt > money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                global pot
                pot += bet2_amt
                money2 -= bet2_amt
                print()
                print('The value of the pot currently is:', pot)
                print()
                print('money left:', money2)
                break

        if bet2 == 'f':
            #print('We are sorry to see you go ')
            return

        if bet2 == 'c':
            print('Player2 has decided to check')
            if pot == 0:
                bet2_amt = 0
                print()
                print('The value of the pot currently is:', pot)
                print()
                return
            else:

                global bet1_amt
                bet2_amt = bet1_amt
                pot += bet2_amt
                print()
                print('The value of the pot currently is:', pot)
                print()
                money2 -= bet2_amt
                print('Money left by player 2 is:', money2)
                print()
                break
    while playround == 4 or playround == 6:
        print()
        bet2 = input('Player2 Would you like to call/fold/raise?')
        if bet2 == 'r':
            print('money left:', money2)
            bet2_amt = int(input('How much would you like to raise:?'))
            # if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            if bet2_amt > money2:
                print('you cant bet what you dont have')
                continue
            else:
                pot += bet2_amt
                print()
                print('The value of the pot currently is:', pot)
                print()
                money2 -= bet2_amt
                print()
                print('Money left by player 2 is:', money2)
                print()
                break
        elif bet2 == 'c':
            if bet1_amt > money2:
                print('you cant bet what you dont have')
                continue
            else:
                print()
                print('player 2 has decided to call')
                print()
                pot += bet1_amt
                print('The value of the pot currently is:', pot)
                bet1_amt = bet2_amt
                money2 -= bet1_amt
                print()
                print('Money left by player 2 is:', money2)
                break
        elif bet2 =='f':
            return


def computer1():

    global playround, bet2_amt, money2, pl2_card1, pl2_card2, pl2_v1, pl2_v2, bet1_amt,fold
    if fold>0:
        return
    playround += 1
    lis = ['b', 'c']
    lis1 = ['r', 'c']
    # print('hello')
    if playround == 2:
        hole1 = r.randrange(1, 53)
        hole2 = r.randrange(1, 53)

        if hole1 >= 1 and hole1 <= 13:
            for k, v in spade_cards.items():
                if k == hole1:
                    # print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v
        elif hole1 > 13 and hole1 <= 26:
            for k, v in diamond_cards.items():
                if k == hole1:
                    # print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v
        elif hole1 >= 27 and hole1 <= 39:
            for k, v in heart_cards.items():
                if k == hole1:
                    # print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v

        elif hole1 >= 40 and hole1 <= 52:
            for k, v in clubs_cards.items():
                if k == hole1:
                    # print('Player2 your first card is :', v)
                    pl2_card1 = k
                    pl2_v1 = v

        if hole2 >= 1 and hole2 <= 13:
            for k, v in spade_cards.items():
                if k == hole2:
                    # print('Player2 Your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v
        elif hole2 > 13 and hole2 <= 26:
            for k, v in diamond_cards.items():
                if k == hole2:
                    # print('Player2 Your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v
        elif hole2 >= 27 and hole2 <= 39:
            for k, v in heart_cards.items():
                if k == hole2:
                    # print('Player2 Your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v

        elif hole2 >= 40 and hole2 <= 52:
            for k, v in clubs_cards.items():
                if k == hole2:
                    # print('Player2 your second card is :', v)
                    pl2_card2 = k
                    pl2_v2 = v

        # bets

    while playround == 2:
        print()
        print('Player2 is thinking.....')
        time.sleep(3)
        if money2 > 500:
            random_choice = r.randrange(0, 2)
        else:
            random_choice = 0
        bet2 = lis[random_choice]
        if bet2 == 'b':
            if money2 < 400:
                bet2_amt = bet1_amt / 2
                print()
                print('Player2 has decided to bet', bet2_amt)
            else:
                if bet1_amt > 1 and bet1_amt < 100:
                    bet2_amt = bet1_amt + 10
                    print()
                    print('Player2 has decided to bet', bet2_amt)
                elif bet1_amt == 0:
                    bet2_amt = 50
                    print()
                    print('Player2 has decided to bet', bet2_amt)
                else:
                    bet2_amt = money2 // 10
                    print()
                    print('Player2 has decided to bet', bet2_amt)
                if bet2_amt > money2:
                    print('You can"t bet what you don''t have ')
                    continue
                else:
                    global pot
                    pot += bet2_amt
                    money2 -= bet2_amt
                    print()
                    print('The value of the pot currently is:', pot)

                    # print('money left:', money2)
                    break

        if bet2 == 'f':
            print('We are sorry to see you go ')
            return

        if bet2 == 'c':
            print()
            print('Player2 has decided to check')
            print()
            if pot == 0:
                bet2_amt = 0
                print()
                print('The value of the pot currently is:', pot)
                return
            else:

                bet2_amt = bet1_amt
                pot += bet2_amt
                print()
                print('The value of the pot currently is:', pot)
                money2 -= bet2_amt
                # print('Money left by player 2 is:', money2)
                break
    while playround == 4 or playround == 6:
        print('Player2 is thinking......')
        time.sleep(3)
        if money2 > 500:
            random_choice = r.randrange(0, 2)
        else:
            random_choice = 0
        bet2 = lis[random_choice]
        if bet2 == 'r':

            #print('Player2 has decided to raise')
            if money2 < 400:
                bet2_amt = bet1_amt // 4
                print()
                print('Player2 has decided to raise', bet2_amt)
            else:
                if bet1_amt > 1 and bet1_amt < 100:
                    bet2_amt = bet1_amt + 10
                    print()
                    print('Player2 has decided to raise', bet2_amt)
                elif bet1_amt == 0:
                    bet2_amt = 50
                    print()
                    print('Player2 has decided to raise', bet2_amt)
                else:
                    bet2_amt = money2 // 10
                    print()
                    print('Player2 has decided to raise', bet2_amt)

            if bet2_amt > money2:
                print('you cant bet what you dont have')
                continue
            else:
                pot += bet2_amt
                print()
                print('The value of the pot currently is:', pot)
                money2 -= bet2_amt
                # print('Money left by player 2 is:', money2)
                break
        elif bet2 == 'c':
            if bet1_amt > money2:
                print('you cant bet what you dont have')
                continue
            else:
                print()
                print('player 2 has decided to call')
                pot += bet1_amt
                print('The value of the pot currently is:', pot)
                bet1_amt = bet2_amt
                money2 -= bet1_amt
                # print('Money left by player 2 is:', money2)
                break


def card1():
    com_card1 = r.randrange(1, 53)

    global com_count, com1, com_v1,fold
    if fold>0:
        return
    if com_count == 1:
        if com_card1 >= 1 and com_card1 <= 13:
            for k, v in spade_cards.items():
                if k == com_card1:
                    print()
                    print()
                    print('The first community card is: :', v)
                    print()
                    print()
                    com1 = k
                    com_v1 = v
        if com_card1 > 13 and com_card1 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card1:
                    print()
                    print()
                    print('The first community card is: :', v)
                    print()
                    print()
                    com1 = k
                    com_v1 = v
        if com_card1 >= 27 and com_card1 <= 39:
            for k, v in heart_cards.items():
                if k == com_card1:
                    print()
                    print()
                    print('The first community card is: :', v)
                    print()
                    print()
                    com1 = k
                    com_v1 = v

        if com_card1 >= 40 and com_card1 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card1:
                    print()
                    print()
                    print('The first community card is: :', v)
                    print()
                    print()
                    com1 = k
                    com_v1 = v
        com_count += 1
        return


def card2():
    com_card2 = r.randrange(1, 53)
    global com_count, com2, com_v2,fold
    if fold>0:
        return
    if com_count == 2:
        if com_card2 >= 1 and com_card2 <= 13:
            for k, v in spade_cards.items():
                if k == com_card2:
                    print()
                    print()
                    print('The second community card is: :', v)
                    print()
                    print()
                    com2 = k
                    com_v2 = v
        if com_card2 > 13 and com_card2 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card2:
                    print()
                    print()
                    print('The second community card is: :', v)
                    print()
                    print()
                    com2 = k
                    com_v2 = v
        if com_card2 >= 27 and com_card2 <= 39:
            for k, v in heart_cards.items():
                if k == com_card2:
                    print()
                    print()
                    print('The second community card is: :', v)
                    print()
                    print()
                    com2 = k
                    com_v2 = v

        if com_card2 >= 40 and com_card2 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card2:
                    print()
                    print()
                    print('The second community card is: :', v)
                    print()
                    print()
                    com2 = k
                    com_v2 = v
        com_count += 1
        return


def card3():
    com_card3 = r.randrange(1, 53)
    global com_count, com3, com_v3,fold
    if fold>0:
        return
    if com_count == 3:
        if com_card3 > 1 and com_card3 <= 13:
            for k, v in spade_cards.items():
                if k == com_card3:
                    print()
                    print()
                    print('The third community card is: :', v)
                    print()
                    print()
                    com3 = k
                    com_v3 = v
        if com_card3 > 13 and com_card3 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card3:
                    print()
                    print()
                    print('The third community card is: :', v)
                    print()
                    print()
                    com3 = k
                    com_v3 = v
        if com_card3 >= 27 and com_card3 <= 39:
            for k, v in heart_cards.items():
                if k == com_card3:
                    print()
                    print()
                    print('The third community card is: :', v)
                    print()
                    print()
                    com3 = k
                    com_v3 = v

        if com_card3 >= 40 and com_card3 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card3:
                    print()
                    print()
                    print('The third community card is: :', v)
                    print()
                    print()
                    com3 = k
                    com_v3 = v
        return

# unl1 is unmodified version of l1 which is modified by four of a kind
def royal_flush():
    global l1, evaluator
    s = sum(l1)

    royal = 0
    l1 = sorted(l1)
    if s <= 65:
        if 1 and 10 in l1:
            for i in range(1, len(l1) - 1):
                if l1[i] - l1[i + 1] == -1:
                    royal += 1
            if royal == 3:
                print('Royal flush')
                evaluator = 1

            else:
                return

    elif s > 65 and s <= 130:
        if 14 and 23 in l1:
            for i in range(1, len(l1) - 1):
                if l1[i] - l1[i + 1] == -1:
                    royal += 1
            if royal == 3:
                print('Royal flush')
                evaluator = 1

            else:
                return

    elif s > 130 and s <= 195:
        if 27 and 36 in l1:
            for i in range(1, len(l1) - 1):
                if l1[i] - l1[i + 1] == -1:
                    royal += 1
            if royal == 3:
                print('Royal flush')
                evaluator = 1

            else:
                return

    elif s > 195 and s <= 260:
        if 40 and 49 in l1:
            for i in range(1, len(l1) - 1):
                if l1[i] - l1[i + 1] == -1:
                    royal += 1
            if royal == 3:
                print('Royal flush')
                evaluator = 1

            else:
                return
    else:
        return


def straight_flush():
    global l1, evaluator
    s = sum(l1)
    l1 = sorted(l1)
    straight = 0
    if s <= 65:
        for i in range(len(l1) - 1):
            if l1[i] - l1[i + 1] == -1:
                straight += 1
                # print('h')
        if straight == 4:
            print('Straight flush')
            evaluator = 2
        else:
            return

    elif s > 65 and s <= 130:
        for i in range(len(l1) - 1):
            if l1[i] - l1[i + 1] == -1:
                straight += 1
        if straight == 4:
            print('Straight flush')
            evaluator = 2
        else:
            return


    elif s > 130 and s <= 195:
        for i in range(len(l1) - 1):
            if l1[i] - l1[i + 1] == -1:
                straight += 1
        if straight == 4:
            print('Straight flush')
            evaluator = 2
        else:
            return

    elif s > 195 and s <= 260:
        for i in range(len(l1) - 1):
            if l1[i] - l1[i + 1] == -1:
                straight += 1
        if straight == 4:
            print('Straight flush')
            evaluator = 2
        else:
            return


def four_of_a_kind():
    # print('four')
    global l1, evaluator
    l1 = sorted(l1)
    four = 0
    i = 0
    while i != 5:
        if l1[i] > 13 and l1[i] < 27:
            l1[i] = l1[i] - 13


        elif l1[i] >= 27 and l1[i] < 40:
            l1[i] = l1[i] - 26

        elif l1[i] >= 40 and l1[i] < 53:
            l1[i] = l1[i] - 39

        # print(l1)
        i += 1

    count = Counter(l1)
    for k, v in count.items():
        if v == 4:
            print('Four of a kind')
            evaluator = 3
            return


def full_house():
    global l1, evaluator
    l1 = sorted(l1)
    full = 0
    full1 = 0
    count = Counter(l1)
    for k, v in count.items():
        if v == 2:
            full += 5
        elif v == 3:
            full += 5
        else:
            break
    else:
        if full == 10:
            print('Full house')
            evaluator = 4
        else:
            return


# problem is l1 is being modified by four so we use diffrent version of list
def flush():
    global un_l1, evaluator
    s = sum(un_l1)
    suit1 = 0
    suit2 = 0
    suit3 = 0
    suit4 = 0
    for i in range(len(un_l1)):
        if un_l1[i] <= 13:
            suit1 += 1
        elif un_l1[i] > 13 and un_l1[i] <= 26:
            suit2 += 1
        elif un_l1[i] > 26 and un_l1[i] <= 29:
            suit3 += 1
        elif un_l1[i] > 39 and un_l1[i] <= 52:
            suit4 += 1
    else:
        if suit1 == 5 or suit2 == 5 or suit3 == 5 or suit4 == 5:
            print('Flush')
            evaluator = 5
        else:
            return


def straight():
    global l1, evaluator
    l1 = sorted(l1)
    straight = 0
    for i in range(len(l1) - 1):
        if l1[i] - l1[i + 1] == -1:
            straight += 1
    else:
        if straight == 4:
            print('Straight')
            evaluator = 6


def three_of_a_kind():
    global l1, evaluator
    three = 0
    count = Counter(l1)
    for k, v in count.items():
        if v == 3:
            three += 3
    else:
        if three == 3:
            print('Three of a kind')
            evaluator = 7


def two_pair():
    global l1, evaluator
    two_pair = 0
    count = Counter(l1)

    for k, v in count.items():
        if v == 2:
            two_pair += 2

    else:
        if two_pair == 4:
            print('Two pair')
            evaluator = 8


def single_pair():
    global l1, evaluator
    two_pair = 0
    count = Counter(l1)

    for k, v in count.items():
        if v == 2:
            two_pair += 2

    else:
        if two_pair == 2:
            print('Single pair')
            evaluator = 9


def high_card():
    global evaluator, un_l1, l1,high
    if evaluator == 0:
        un_l1 = sorted(un_l1)
        for k, v in spade_cards.items():
            if k == un_l1[0]:
                # print('The high card is',v)
                print('High card')
        for k, v in diamond_cards.items():
            if k == un_l1[0]:
                # print('The high card is',v)
                print('High card')
        for k, v in heart_cards.items():
            if k == un_l1[0]:
                # print('The high card is',v)
                print('High card')
        for k, v in clubs_cards.items():
            if k == un_l1[0]:
                # print('The high card is',v)
                print('High card')
        evaluator = 10
        l1 = sorted(l1,reverse=True)
        #print(l1)
        high = l1[0]
        #print('high value',high)

def fold_check_pl1():
    global fold,bet1,money1,money2,pot

    if bet1=='f':
        print('Player2 wins since Player1 has folded')
        money2+=pot
        pot=0
        print('Player2 currently has',money2)
        print('Player1 currently has',money1)
        fold=1
        bet1=0


def fold_check_pl2():
    global fold,bet2,money1,money2,pot

    if bet2=='f':
        print('Player1 wins since Player2 has folded')
        money1+=pot
        pot=0
        print('Player1 currently has',money1)
        print('Player2 currently has',money2)
        fold=2
        bet2=0


play = input('Would you like to play against another player or would you like to play against the computer(p/c)')
while play!='p' and play!='c':
    play = input('Would you like to play against another player or would you like to play against the computer(p/c)')

print()
print()
play_again=0
f=0
while play_again!='q':

    if play == 'p':

        player1()
        fold_check_pl1()
        player2()
        fold_check_pl2()

        card1()

        player1()
        fold_check_pl1()
        player2()
        fold_check_pl2()
        card2()
        player1()
        fold_check_pl1()
        player2()
        fold_check_pl2()
        card3()
        player1()
        player2()

    elif play == 'c':
        player1()
        fold_check_pl1()
        computer1()
        card1()
        player1()
        fold_check_pl1()
        computer1()
        card2()
        player1()
        fold_check_pl1()
        computer1()
        card3()
        player1()
        fold_check_pl1()
        computer1()
    else:
        print('shit')
    if fold==0:
        print()
        print()
        print('player1 cards are:', pl1_v1, ',', pl1_v2, ',', com_v1, ',', com_v2, ',', com_v3)
        print('player2 cards are:', pl2_v1, ',', pl2_v2, ',', com_v1, ',', com_v2, ',', com_v3)
        print()
        print()
        global l1, l2
        un_l1 = l1 = [pl1_card1, pl1_card2, com1, com2, com3]
        l2 = [pl2_card1, pl2_card2, com1, com2, com3]
        evaluator = 0
        i = 0


    if fold ==0:
        while True:
            print()
            print('Player', i + 1, 'has the combination:',end='')
            print()
            royal_flush()
            straight_flush()
            four_of_a_kind()
            full_house()
            flush()
            straight()
            three_of_a_kind()
            two_pair()
            single_pair()
            high_card()
            if i==0 and evaluator==10:
                high1=high
                #print('high1 is',high1)

            elif i==1 and evaluator==10:
                high2=high
                #print('high2 is',high2)

            if i == 0:
                evaluator
                Player1_val = evaluator
                i += 1
                l1 = l2
                evaluator = 0
            elif i == 1:
                player2_val = evaluator
                i += 1
                break
        if Player1_val > player2_val:
            print()
            print('Player 2 wins ')
            money2 += pot
            pot=0
            print('Player 2 you now have', money2)
            print('Player 1 you now have', money1)

        elif player2_val > Player1_val:
            print('Player 1 wins ')
            money1 += pot
            pot=0
            print('Player1 you now have', money1)
            print('Player2 you now have', money2)
        else:
            if evaluator==10:
                if high1>high2:
                    print()
                    print('Player 1 wins since Player1 has higher high card value')
                    money1 += pot
                    pot = 0
                    print('Player1 you now have', money1)
                    print('Player2 you now have', money2)
                elif high2>high1:
                    print()
                    print('Player 2 wins since Player2 has higher high card value')
                    money2 += pot
                    pot = 0
                    print('Player1 you now have', money1)
                    print('Player2 you now have', money2)

                else:
                    print()
                    print('its a draw')
                    money1 += pot / 2
                    money2 += pot / 2
                    pot=0
                    print('the pot is divided')
                    print('Money with player1', money1)
                    print('money with player2', money2)
        play_again = input('Would you like to play another round or quit(p/q)?')
        print()
        print()
        if play_again=='p':
            playround=0
            f += 1
            fold = 0
            continue

        else:
            break
    else:
        play_again = input('Would you like to play another round or quit(p/q)?')
        print()
        print()
        if play_again=='p':
            playround=0
            f += 1
            fold = 0
            continue

        elif play_again=='q':
            print('Thank You for playing!')
            break

        else:
            continue

# print('player1 cards are:',pl1_card1,',',pl1_card2,',',com1,',',com2,',',com3)
# print('player2 cards are:',pl2_card1,pl2_card2,com1,com2,com3)






