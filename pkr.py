# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 09:28:23 2018

@author: student
"""

#%%
#poker
import random as r
pot=0
money1=10
money2=10
playround=0
check=0
com_count=1
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
    print('pl1')
    '''print('Would you like to start?')
    yes=input()
    if yes == 'yes':
        pass
    else:
        return'''
        

    
    global  playround,bet1_amt,bet1,money1
    playround+=1
    print('value of playground is',playround)
    
    if playround==1:
        hole1= r.randrange(1,53)
        hole2 =r.randrange(1,53)

        print(hole2)
        if hole1>=1 and hole1<=13:
            for k,v in spade_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
        elif hole1>13 and hole1<=26:
            for k,v in diamond_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
        elif hole1>=27 and hole1<=39:
            for k,v in heart_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
                                            
        elif hole1>=40 and hole1<=52:
            for k,v in clubs_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
 
        

        if hole2>=1 and hole2<=13:
            for k,v in spade_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
        elif hole2>13 and hole2<=26:
            for k,v in diamond_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
        elif hole2>=27 and hole2<=39:
            for k,v in heart_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
    
        elif hole2>=40 and hole2<=52:
            for k,v in clubs_cards.items():
                if k == hole2:
                    print('Player1 your second card is :',v)
                    
        
        

        #bets
    if playround == 1:
        while True:

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
                    return


            elif bet1=='f':
                print('We are sorry to see you go ')
                return

            elif bet1=='c':
                print('Player1 has decided to check')
                if pot==0:
                    bet1_amt=0
                    print('The value of the pot currently is:', pot)
                    return
                else:
                    pot+=bet1_amt
                    print('The value of the pot currently is:', pot) #not important because this is only for round 1
                    print('money left:',money1)
                    return

    if playround==3:
        bet1= input('Player1 Would you like to check/fold/raise?')
        if bet1=='r':
            print('money left:',money1)
            bet1_amt=int(input('How much would you like to raise:?'))
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            pot+=bet1_amt
            money1-=bet1_amt
            print('money left for player1',money1)
            print('The value of the pot currently is:', pot)
        if bet1=='c':
            if bet2_amt>money1:
                print('You can"t bet what you don''t have ')
            else:
                print('player 1 has decided to check')
                pot+=bet2_amt
                print('The value of the pot currently is:', pot)
                money1-=bet2_amt
                bet1_amt=bet2_amt
                print('money left for player1',money1)
            

    if playround==5:
        bet1= input('Player1 Would you like to check/fold/raise?')
        if bet1=='r':
            print('money left:',money1)
            bet1_amt=int(input('How much would you like to raise:?'))
            if bet1_amt>money1:
                print('You cant bet with what you dont have')
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            pot+=bet1_amt
            print('The value of the pot currently is:', pot)
        if bet2_amt>money1:
            print('You can"t bet what you don''t have ')
        else:
            print('player 1 has decided to check')
            pot+=bet2_amt
            print('The value of the pot currently is:', pot)
            money1-=bet2_amt
            bet1_amt=bet2_amt
            print('money left for player1',money1)
            

            

def player2():
    '''print('Would you like to start?')
    yes=input()
    if yes == 'yes':
        pass
    else:
        return'''
        
    global playround,bet2,bet2_amt,money2
    playround+=1
    print('value of playground is',playround)
    print('hello')
    if playround==2:
        hole1= r.randrange(1,53)
        hole2 =r.randrange(1,53)
        
        if hole1>=1 and hole1<=13:
            for k,v in spade_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
        elif hole1>13 and hole1<=26:
            for k,v in diamond_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
        elif hole1>=27 and hole1<=39:
            for k,v in heart_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
                                            
        elif hole1>=40 and hole1<=52:
            for k,v in clubs_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
 
        

        if hole2>=1 and hole2<=13:
            for k,v in spade_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
        elif hole2>13 and hole2<=26:
            for k,v in diamond_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
        elif hole2>=27 and hole2<=39:
            for k,v in heart_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
    
        elif hole2>=40 and hole2<=52:
            for k,v in clubs_cards.items():
                if k == hole2:
                    print('Player2 your second card is :',v)
                    
        
        

        #bets
    if playround == 2:
        while True:

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
                    return


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
                    return
    if playround==4:
        bet1= input('Player2 Would you like to check/fold/raise?')
        if bet2=='r':
            print('money left:',money2)
            bet2_amt=int(input('How much would you like to raise:?'))
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            pot+=bet2_amt
            print('The value of the pot currently is:', pot)
            money2 -= bet2_amt
            print('Money left by player 2 is:',money2)
        if bet1=='c':
            print('player 2 has decided to check')
            pot+=bet1_amt
            print('The value of the pot currently is:', pot)
            bet1_amt=bet2_amt
            money2 -= bet1_amt
            print('Money left by player 2 is:',money2)
    
    
    
    
    if playround==6:
        bet1= input('Player2 Would you like to check/fold/raise?')
        if bet2=='r':
            print('money left:',money2)
            bet2_amt=int(input('How much would you like to raise:?'))
            #if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh
            pot+=bet2_amt
            print('The value of the pot currently is:', pot)
            money2 -= bet2_amt
            print('Money left by player 2 is:',money2)
        if bet1=='c':
            print('player 1 has decided to check')
            pot+=bet1_amt
            print('The value of the pot currently is:', pot)
            bet1_amt=bet2_amt
            money2 -= bet1_amt
            print('Money left by player 2 is:',money2)
    



def card1():
    com_card1= r.randrange(1,53)

    global com_count
    if com_count==1:
        if com_card1 >= 1 and com_card1 <= 13:
            for k, v in spade_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
        if com_card1 > 13 and com_card1 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
        if com_card1 >= 27 and com_card1 <= 39:
            for k, v in heart_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)

        if com_card1 >= 40 and com_card1 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
        com_count+=1
        return

def card2():
    com_card2 = r.randrange(1, 53)
    global com_count
    if com_count == 2:
        if com_card2 >= 1 and com_card2 <= 13:
            for k, v in spade_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
        if com_card2 > 13 and com_card2 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
        if com_card2 >= 27 and com_card2 <= 39:
            for k, v in heart_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)

        if com_card2 >= 40 and com_card2 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
        com_count+=1
        return

def card3():
    com_card3 = r.randrange(1, 53)
    global com_count
    if com_count == 3:
        if com_card3 > 1 and com_card3 <= 13:
            for k, v in spade_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
        if com_card3 > 13 and com_card3 <= 26:
            for k, v in diamond_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
        if com_card3 >= 27 and com_card3<= 39:
            for k, v in heart_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)

        if com_card3 >= 40 and com_card3<= 52:
            for k, v in clubs_cards.items():
                if k == com_card3:
                    print('The third community card is: :', v)
        return

    

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
#TODO add the final comparing of cards and also minus the money1 and 2 vars which is currently not being done
#TODO Work on fold but do it in the end basic card comparing comes first
#TODO make it such that if everyone checks on the first round then the community cards are directly unveiled
#add playround 7 and 6
#add all if statements in while loop so that continue can be used for going back when bet_amt is greater than money
