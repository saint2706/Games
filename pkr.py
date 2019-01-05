# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 09:28:23 2018

@author: student
"""


#%%
#poker
import random as r
from collections import Counter

pot=0
money1=10
money2=10
playround=0
check=0
com_count=1
pl1_card1=0
pl1_card2=0
pl2_card1=0
pl2_card2=0
com1=0
com2=0
com3=0

#nop= int(input('No of players(1-4):'))

spade_cards={1:'Ace of spades',2:'Two of spades',3:'three of spades',4:'four of spades',5:'five of spades'
       ,6:'six of spades',7:'seven of spades',8:'eight of spades',9:'nine of spades'
       ,10:'ten of spades',11:'jack of spades',12:'queen of spades',13:'king of spades'}

 
diamond_cards={14:'Ace of diamond',15:'Two of diamond',16:'three of diamond',17:'four of diamond',18:'five of diamond'
      ,19:'six of diamond',20:'seven of diamond',21:'eight of diamond',22:'nine of diamond'
      ,23:'ten of diamond',24:'jack of diamond',25:'queen of diamond',26:'king of diamond'}


heart_cards={27:'Ace of heart',28:'Two of heart',29:'three of heart',30:'four of heart',31:'five of heart'
      ,32:'six of heart',33:'seven of heart',34:'eight of heart',35:'nine of heart'
      ,36:'ten of heart',37:'jack of heart',38:'queen of heart',39:'king of heart'}
    
 
clubs_cards={40:'Ace of clubs',41:'Two of clubs',42:'three of clubs',43:'four of clubs',44:'five of clubs'
      ,45:'six of clubs',46:'seven of clubs',47:'eight of clubs',48:'nine of clubs'
      ,49:'ten of clubs',50:'jack of clubs',51:'queen of clubs',52:'king of clubs'}

print('Welcome! as a starting gift each player is given 10$')

def player1():
    #print('pl1')
    '''print('Would you like to start?')
    yes=input()
    if yes == 'yes':
        pass
    else:
        return'''
        

    
    global  playround,bet1_amt,money1,pl1_card1,pl1_card2,pl1_v1,pl1_v2
    playround+=1

    
    if playround==1:
        hole1= r.randrange(1,53)
        hole2 =r.randrange(1,53)


        if hole1>=1 and hole1<=13:
            for k,v in spade_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
                    pl1_card1=k
                    pl1_v1=v
        elif hole1>13 and hole1<=26:
            for k,v in diamond_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
                    pl1_card1 = k
                    pl1_v1 = v
        elif hole1>=27 and hole1<=39:
            for k,v in heart_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
                    pl1_card1 = k
                    pl1_v1 = v
                                            
        elif hole1>=40 and hole1<=52:
            for k,v in clubs_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
                    pl1_card1 = k
                    pl1_v1 = v
 
        

        if hole2>=1 and hole2<=13:
            for k,v in spade_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
                    pl1_card2=k
                    pl1_v2 = v
        elif hole2>13 and hole2<=26:
            for k,v in diamond_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
                    pl1_card2 = k
                    pl1_v2 = v
        elif hole2>=27 and hole2<=39:
            for k,v in heart_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
                    pl1_card2 = k
                    pl1_v2 = v
    
        elif hole2>=40 and hole2<=52:
            for k,v in clubs_cards.items():
                if k == hole2:
                    print('Player1 your second card is :',v)
                    pl1_card2 = k
                    pl1_v2 = v
                    
        
        

        #bets
    while playround == 1:

        bet1=input('Player1 Would you like to place the initial bet or fold or check(b/f/c)?')
        if bet1=='b':
            print('How much is your bet Player1 (1-',money1,')')
            bet1_amt=int(input())
            if bet1_amt>money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                global pot
                pot+=bet1_amt
                money1-=bet1_amt
                print('The value of the pot currently is:',pot)
                print('money left:',money1)
                break


        elif bet1=='f':
            print('We are sorry to see you go ')
            return

        elif bet1=='c':
            print('Player1 has decided to check')
            if pot==0:
                bet1_amt=0
                print('The value of the pot currently is:', pot)
                break
            else:
                pot+=bet1_amt
                print('The value of the pot currently is:', pot) #not important because this is only for round 1
                print('money left:',money1)
                break

    while playround==3:
        bet1= input('Player1 Would you like to check/fold/raise?')
        if bet1=='r':
            print('money left:',money1)
            bet1_amt=int(input('How much would you like to raise:?'))
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            if bet1_amt>money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                pot+=bet1_amt
                money1-=bet1_amt
                print('money left for player1',money1)
                print('The value of the pot currently is:', pot)
                break
        if bet1=='c':
            if bet2_amt>money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                print('player 1 has decided to check')
                pot+=bet2_amt
                print('The value of the pot currently is:', pot)
                money1-=bet2_amt
                bet1_amt=bet2_amt
                print('money left for player1',money1)
                break
            

    while playround==5:
        bet1= input('Player1 Would you like to check/fold/raise?')
        if bet1=='r':
            print('money left:',money1)
            bet1_amt=int(input('How much would you like to raise:?'))
            if bet1_amt>money1:
                print('You cant bet with what you dont have')
                continue
            else:
                #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
                pot+=bet1_amt
                print('The value of the pot currently is:', pot)
                break
        elif bet1=='c':
            if bet2_amt>money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                print('player 1 has decided to check')
                pot+=bet2_amt
                print('The value of the pot currently is:', pot)
                money1-=bet2_amt
                bet1_amt=bet2_amt
                print('money left for player1',money1)
                break


            

def player2():
    '''print('Would you like to start?')
    yes=input()
    if yes == 'yes':
        pass
    else:
        return'''
        
    global playround,bet2_amt,money2,pl2_card1,pl2_card2,pl2_v1,pl2_v2
    playround+=1

    #print('hello')
    if playround==2:
        hole1= r.randrange(1,53)
        hole2 =r.randrange(1,53)
        
        if hole1>=1 and hole1<=13:
            for k,v in spade_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
                    pl2_card1=k
                    pl2_v1=v
        elif hole1>13 and hole1<=26:
            for k,v in diamond_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
                    pl2_card1 = k
                    pl2_v1 = v
        elif hole1>=27 and hole1<=39:
            for k,v in heart_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
                    pl2_card1 = k
                    pl2_v1 = v
                                            
        elif hole1>=40 and hole1<=52:
            for k,v in clubs_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
                    pl2_card1 = k
                    pl2_v1 = v
 
        

        if hole2>=1 and hole2<=13:
            for k,v in spade_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
                    pl2_card2=k
                    pl2_v2 = v
        elif hole2>13 and hole2<=26:
            for k,v in diamond_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
                    pl2_card2 = k
                    pl2_v2 = v
        elif hole2>=27 and hole2<=39:
            for k,v in heart_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
                    pl2_card2 = k
                    pl2_v2 = v
    
        elif hole2>=40 and hole2<=52:
            for k,v in clubs_cards.items():
                if k == hole2:
                    print('Player2 your second card is :',v)
                    pl2_card2 = k
                    pl2_v2 = v
                    
        
        

        #bets

    while playround==2:

        bet2=input('Player2 Would you like to place the initial bet or fold or check(b/f/c)?')
        if bet2=='b':
            print('How much is your bet Player2 (1-',money2,')')
            bet2_amt=int(input())
            if bet2_amt>money1:
                print('You can"t bet what you don''t have ')
                continue
            else:
                global pot
                pot+=bet2_amt
                money2 -= bet2_amt
                print('The value of the pot currently is:',pot)
                print('money left:',money2)
                break


        if bet2=='f':
            print('We are sorry to see you go ')
            return

        if bet2=='c':
            print('Player2 has decided to check')
            if pot==0:
                bet2_amt=0
                print('The value of the pot currently is:', pot)
                return
            else:

                global bet1_amt
                bet2_amt=bet1_amt
                pot+=bet2_amt
                print('The value of the pot currently is:', pot)
                money2 -= bet2_amt
                print('Money left by player 2 is:',money2)
                break
    while playround==4:
        bet2= input('Player2 Would you like to check/fold/raise?')
        if bet2=='r':
            print('money left:',money2)
            bet2_amt=int(input('How much would you like to raise:?'))
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            if bet2_amt>money2:
                print('you cant bet what you dont have')
                continue
            else:
                pot+=bet2_amt
                print('The value of the pot currently is:', pot)
                money2 -= bet2_amt
                print('Money left by player 2 is:',money2)
                break
        elif bet2=='c':
            if bet1_amt>money2:
                print('you cant bet what you dont have')
                continue
            else:
                print('player 2 has decided to check')
                pot+=bet1_amt
                print('The value of the pot currently is:', pot)
                bet1_amt=bet2_amt
                money2 -= bet1_amt
                print('Money left by player 2 is:',money2)
                break
    
    
    
    
    while playround==6:
        bet2= input('Player2 Would you like to check/fold/raise?')
        if bet2=='r':
            print('money left:',money2)
            bet2_amt=int(input('How much would you like to raise:?'))
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            if bet2_amt>money2:
                print('You cant bet what you dont have')
                continue
            else:
                pot+=bet2_amt
                print('The value of the pot currently is:', pot)
                money2 -= bet2_amt
                print('Money left by player 2 is:',money2)
                break
        elif bet2=='c':
            if bet1_amt>money2:
                print('You cant bet what you dont have')
                continue
            else:
                print('player 2 has decided to check')
                pot+=bet1_amt
                print('The value of the pot currently is:', pot)
                bet1_amt=bet2_amt
                money2 -= bet1_amt
                print('Money left by player 2 is:',money2)
                break

    



def card1():
    com_card1= r.randrange(1,53)

    global com_count,com1,com_v1
    if com_count==1:
        if com_card1 >= 1 and com_card1 <= 13:
            for k, v in spade_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
                    com1=k
                    com_v1=v
        if com_card1 > 13 and com_card1 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
                    com1 = k
                    com_v1 = v
        if com_card1 >= 27 and com_card1 <= 39:
            for k, v in heart_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
                    com1 = k
                    com_v1 = v

        if com_card1 >= 40 and com_card1 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
                    com1 = k
                    com_v1 = v
        com_count+=1
        return

def card2():
    com_card2 = r.randrange(1, 53)
    global com_count,com2,com_v2
    if com_count == 2:
        if com_card2 >= 1 and com_card2 <= 13:
            for k, v in spade_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
                    com2 = k
                    com_v2 = v
        if com_card2 > 13 and com_card2 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
                    com2 = k
                    com_v2 = v
        if com_card2 >= 27 and com_card2 <= 39:
            for k, v in heart_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
                    com2 = k
                    com_v2 = v

        if com_card2 >= 40 and com_card2 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
                    com2 = k
                    com_v2 = v
        com_count+=1
        return

def card3():
    com_card3 = r.randrange(1, 53)
    global com_count,com3,com_v3
    if com_count == 3:
        if com_card3 > 1 and com_card3 <= 13:
            for k, v in spade_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
                    com3=k
                    com_v3 = v
        if com_card3 > 13 and com_card3 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
                    com3 = k
                    com_v3 = v
        if com_card3 >= 27 and com_card3<= 39:
            for k, v in heart_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
                    com3 = k
                    com_v3 = v

        if com_card3 >= 40 and com_card3<= 52:
            for k, v in clubs_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
                    com3 = k
                    com_v3 = v
        return



play= input('Would you lie to play against another player or would you like to play against the computer(p/c)')

if play=='p':

    player1()
    player2()

    card1()
    player1()
    player2()
    card2()
    player1()
    player2()
    card3()
    player1()
    player2()
elif play=='c':
    print('its coming')

print('player1 cards are:',pl1_card1,pl1_card2,com1,com2,com3)
print('player2 cards are:',pl2_card1,pl2_card2,com1,com2,com3)

print('player1 cards are:',pl1_v1,pl1_v2,com_v1,com_v2,com_v3)
print('player2 cards are:',pl2_v1,pl2_v2,com_v1,com_v2,com_v3)




f=0

global l1,l2
un_l1=l1=[pl1_card1,pl1_card2,com1,com2,com3]
l2=[pl2_card1,pl2_card2,com1,com2,com3]
royal=0
evaluator=0
#unl1 is unmodified version of l1 which is modified by four of a kind
def royal_flush():
    global l1, evaluator
    s=sum(l1)

    royal=0
    l1=sorted(l1)
    if s<=65:
        if 1 and 10 in l1:
            for i in range(1,len(l1)-1):
                if l1[i]-l1[i+1]==-1:
                    royal+=1
            if royal==3:
                print('It is a royal flush')
                evaluator=1

            else:
                return

    elif s>65 and s<=130:
        if 14 and 23 in l1:
            for i in range(1,len(l1)-1):
                if l1[i]-l1[i+1]==-1:
                    royal+=1
            if royal==3:
                print('It is a royal flush')
                evaluator=1

            else:
                return

    elif s>130 and s<=195:
        if 27 and 36 in l1:
            for i in range(1,len(l1)-1):
                if l1[i]-l1[i+1]==-1:
                    royal+=1
            if royal==3:
                print('It is a royal flush')
                evaluator=1

            else:
                return

    elif s>195 and s<=260:
        if 40 and 49 in l1:
            for i in range(1,len(l1)-1):
                if l1[i]-l1[i+1]==-1:
                    royal+=1
            if royal==3:
                print('It is a royal flush')
                evaluator=1

            else:
                return
    else:
        return

def straight_flush():
    global l1,evaluator
    s=sum(l1)
    l1=sorted(l1)
    straight=0
    if s <= 65:
        for i in range(len(l1)-1):
            if l1[i]-l1[i+1]==-1:
                straight+=1
                #print('h')
        if straight==4:
            print('it is a straight flush')
            evaluator=2
        else:
            return

    elif s > 65 and s <= 130:
        for i in range(len(l1)-1):
            if l1[i]-l1[i+1]==-1:
                straight+=1
        if straight==4:
            print('it is a straight flush')
            evaluator=2
        else:
            return


    elif s > 130 and s <= 195:
        for i in range(len(l1)-1):
            if l1[i]-l1[i+1]==-1:
                straight+=1
        if straight==4:
            print('it is a straight flush')
            evaluator=2
        else:
            return

    elif s > 195 and s <= 260:
        for i in range(len(l1)-1):
            if l1[i]-l1[i+1]==-1:
                straight+=1
        if straight==4:
            print('it is a straight flush')
            evaluator=2
        else:
            return

def four_of_a_kind():
    #print('four')
    global l1,evaluator
    l1=sorted(l1)
    four=0
    i=0
    while i!=5:
        if l1[i]>13 and l1[i]<27:
            l1[i]=l1[i]-13


        elif l1[i]>=27 and l1[i]<40:
            l1[i]=l1[i]-26

        elif l1[i]>=40 and l1[i]<53:
            l1[i]=l1[i]-39

        print(l1)
        i+=1

    '''for i in range(len(l1)-1):
        if l1[i]==l1[i+1]:
            four+=1
        else:
            pass
    else:
        if four==3:
            evaluator=3
            print('it is four of kind')
        else:
            return'''
    count= Counter(l1)
    for k,v in count.items():
        if v==4:
            print('it is four of a kind')
            evaluator=3
            return

def full_house():
    global l1, evaluator
    l1 = sorted(l1)
    full = 0
    full1=0
    i = 0
    '''while i != 4:
        if l1[i] > 13 and l1[i] < 27:
            l1[i] = l1[i] - 13

        elif l1[i] >= 27 and l1[i] < 40:
            l1[i] = l1[i] - 26

        elif l1[i] >= 40 and l1[i] < 53:
            l1[i] = l1[i] - 39
        print(l1)
        i += 1'''
    count= Counter(l1)
    for k,v in count.items():
        if v==2:
            full+=5
        elif v==3:
            full+=5
        else:
            break
    else:
        if full==10:
            print('it is a full house')
            evaluator=4
        else:
            return
#problem is l1 is being modified by four so we use diffrent version of list
def flush():
    global un_l1,evaluator
    s= sum(un_l1)
    suit1=0
    suit2=0
    suit3=0
    suit4=0
    for i in range(len(un_l1)):
        if un_l1[i]<=13:
            suit1+=1
        elif un_l1[i]>13 and un_l1[i]<=26:
            suit2+=1
        elif un_l1[i]>26 and un_l1[i]<=29:
            suit3+=1
        elif un_l1[i]>39 and un_l1[i]<=52:
            suit4+=1
    else:
        if suit1==5 or suit2==5 or suit3==5 or suit4==5:
            print('It is a flush')
            evaluator=5
        else:
            return

def straight():
    global l1,evaluator
    l1=sorted(l1)
    straight=0
    for i in range(len(l1)-1):
        if l1[i]-l1[i+1]==-1:
            straight+=1
    else:
        if straight==4:
            print('it is a straight')
            evaluator=6

def three_of_a_kind():
    global l1,evaluator
    three=0
    count= Counter(l1)
    for k,v in count.items():
        if v==3:
            three+=3
    else:
        if three==3:
            print('it is three of a kind')
            evaluator=7

def two_pair():
    global l1,evaluator
    two_pair=0
    count=Counter(l1)

    for k,v in count.items():
        if v==2:
            two_pair+=2

    else:
        if two_pair==4:
            print('it is a two pair')
            evaluator=8

def single_pair():
    global l1,evaluator
    two_pair=0
    count=Counter(l1)

    for k,v in count.items():
        if v==2:
            two_pair+=2

    else:
        if two_pair==2:
            print('it is a single pair')
            evaluator=9

def high_card():
    global evaluator,un_l1,l1
    if evaluator==0:
        un_l1=sorted(un_l1)
        for k,v in spade_cards.items():
            if k== un_l1[0]:
                print('The high card is',v)
        for k,v in diamond_cards.items():
            if k== un_l1[0]:
                print('The high card is',v)
        for k,v in heart_cards.items():
            if k== un_l1[0]:
                print('The high card is',v)
        for k,v in clubs_cards.items():
            if k== un_l1[0]:
                print('The high card is',v)
        evaluator=10
        l1=sorted(l1)
        high=l1[0]
        print('high value',high)
i=0
while True:
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

    if i==0:
        evaluator
        Player1_val=evaluator
        i+=1
        l1=l2
        evaluator=0
    elif i==1:
        player2_val=evaluator
        i+=1
        break

print(Player1_val,player2_val)

if Player1_val>player2_val:
    print('Player 2 wins')
    money2+=pot
    print('you now have',money2)
elif player2_val>Player1_val:
    print('Player 1 wins')
    money1+=pot
    print('Player1 you now have',money1)
else:
    print('its a draw')
    money1+=pot/2
    money2+=pot/2
    print('the pot is divided')
    print('Money with player1',money1)
    print('money with player2',money2)


#TODO add the final comparing of cards and also minus the money1 and 2 vars which is currently not being done
#TODO Work on fold but do it in the end basic card comparing comes first
#TODO make it such that if everyone checks on the first round then the community cards are directly unveiled
#add playround 7 and 6
#add all if statements in while loop so that continue can be used for going back when bet_amt is greater than money
#lower redundancy in code by merging diffrent rounds in player1 and player2
