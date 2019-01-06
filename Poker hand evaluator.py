from collections import Counter


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
global l1,l2
un_l1=l1=[11,23,10,32,23]
l2=[1,23,23,11,17]
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
    print(count)
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
    #print(count)
    for k,v in count.items():
        if v==2:
            two_pair+=2

    else:
        if two_pair==2:
            print('it is a single pair')
            evaluator=8

def high_card():
    global evaluator,un_l1
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
        evaluator=8














print(evaluator)

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
