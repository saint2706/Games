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
        

    
    global  playround,bet1_amt
    playround+=1
    
    if playround==1:
        hole1= r.randrange(1,53)
        hole2 =r.randrange(1,53)
        
        if hole1>1 and hole1<=13:
            for k,v in spade_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
        if hole1>13 and hole1<=126:
            for k,v in diamond_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
        if hole1>27 and hole1<=39:
            for k,v in heart_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
                                            
        if hole1>40 and hole1<=52:
            for k,v in clubs_cards.items():
                if k == hole1:
                    print('Player1 your first card is :',v)
 
        

        if hole2>1 and hole2<=13:
            for k,v in spade_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
        if hole2>13 and hole2<=126:
            for k,v in diamond_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
        if hole2>27 and hole2<=39:
            for k,v in heart_cards.items():
                if k == hole2:
                    print('Player1 Your second card is :',v)
    
        if hole2>40 and hole2<=52:
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
                    return


            if bet1=='f':
                print('We are sorry to see you go ')
                return

            if bet1=='c':
                print('Player1 has decided to check')
                if pot==0:
                    bet1_amt=0
                    print('The value of the pot currently is:', pot)
                    return
                else:
                    pot+=bet1_amt
                    print('The value of the pot currently is:', pot) #not important because this is only for round 1
                    return

    if playround==3 and bet1!='f':
        bet1= input('Would you like to check/fold/raise?')
        if bet1=='r':
            print('money left:',money1)
            bet1_amt=int(input('How much would you like to raise:?'))
            if bet1_amt>bet #it has to be greater than check and also minus from money and put in else if bet>money aghrrh


            

def player2():
    '''print('Would you like to start?')
    yes=input()
    if yes == 'yes':
        pass
    else:
        return'''
        
    global playround,bet2
    playround+=1
    
    print('hello')
    if playround==2:
        hole1= r.randrange(1,53)
        hole2 =r.randrange(1,53)
        
        if hole1>1 and hole1<=13:
            for k,v in spade_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
        if hole1>13 and hole1<=126:
            for k,v in diamond_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
        if hole1>27 and hole1<=39:
            for k,v in heart_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
                                            
        if hole1>40 and hole1<=52:
            for k,v in clubs_cards.items():
                if k == hole1:
                    print('Player2 your first card is :',v)
 
        

        if hole2>1 and hole2<=13:
            for k,v in spade_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
        if hole2>13 and hole2<=126:
            for k,v in diamond_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
        if hole2>27 and hole2<=39:
            for k,v in heart_cards.items():
                if k == hole2:
                    print('Player2 Your second card is :',v)
    
        if hole2>40 and hole2<=52:
            for k,v in clubs_cards.items():
                if k == hole2:
                    print('Player2 your second card is :',v)
                    
        
        

        #bets
    if playround == 2:
        while True:

            bet2=input('Player2 Would you like to place the initial bet or fold or check(b/f/c)?')
            if bet2=='b':
                print('How much is your bet Player2 (1-',money1,')')
                bet2_amt=int(input())
                if bet2_amt>money1:
                    print('You can"t bet what you don''t have ')
                    continue
                else:
                    global pot
                    pot+=bet2_amt
                    money2 -= bet2_amt
                    print('The value of the pot currently is:',pot)
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
                    return



def card1():
    com_card1= r.randrange(1,53)

    global com_count
    if com_count==1:
        if com_card1 > 1 and com_card1 <= 13:
            for k, v in spade_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
        if com_card1 > 13 and com_card1 <= 126:
            for k, v in diamond_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
        if com_card1 > 27 and com_card1 <= 39:
            for k, v in heart_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)

        if com_card1 > 40 and com_card1 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card1:
                    print('The first community card is: :', v)
        com_count+=1
        return

def card2():
    com_card2 = r.randrange(1, 53)
    if com_count == 2:
        if com_card2 > 1 and com_card2 <= 13:
            for k, v in spade_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
        if com_card2 > 13 and com_card2 <= 126:
            for k, v in diamond_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
        if com_card2 > 27 and com_card2 <= 39:
            for k, v in heart_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)

        if com_card2 > 40 and com_card2 <= 52:
            for k, v in clubs_cards.items():
                if k == com_card2:
                    print('The second community card is: :', v)
        return


player1()
player2()
card1()
player1()
card2()
#TODO make it such that if everyone checks on the first round then the community cards are directly unveiled