import itertools
from sklearn.utils import shuffle
from random import randrange

#Inner class represent agent
class agent(object):

    def __init__(self, number):
        self._cards = []
        self._number = number
        self._bid = 0
        self._win = 0
        self.b_wallet = 0

    def get_cards(self):
        return self._cards

    def get_number(self):
        return self._number

    def get_bid(self):
        return self._bid

    def get_win(self):
        return self._win

    def get_b_wallet(self):
        return self.b_wallet
    def get_win(self):
        return self._win

    def set_cards(self, new_hand):
        if new_hand is not None:
            self._cards = new_hand

    def set_number(self, value):
        if value >= 0:
            self._number = value
        else:
            self._number = 0

    def set_bid(self, new_bid):
        if new_bid >= 0:
            self._bid = new_bid
        else:
            self._bid = 0

    def set_win(self,num):
        if num > 0:
            self._win = num

    def set_b_wallet(self, new_amount):
        if new_amount >=0:
            self.b_wallet = self.b_wallet + new_amount

    cards = property(get_cards, set_cards)
    number = property(get_number, set_number)
    bid = property(get_bid, set_bid)
    win = property(get_win, set_win)
    wallet = property(get_b_wallet, set_b_wallet)

###########################################################################

agent1 = agent(1)
agent2 = agent(2)
phase1 = 1
phase2 = 1
deck = []
win1=0
win2=0


# Randomly generate two hands of n cards
def generate_2hands(nn_card=3):
    Shuffling = shuffle(deck, n_samples = nn_card)
    for x in Shuffling:
        deck.remove(x)
    return Shuffling

def new_deck():
    global deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['s', 'c', 'h', 'd']
    deck = list(''.join(card) for card in itertools.product(ranks, suits))

def check_cards(digit):
    if digit == 'T':
        digit =10
        return digit
    elif digit == 'J':
        digit = 11
        return digit
    elif digit == 'Q':
        digit = 12
        return digit
    elif digit == 'K':
        digit =13
        return digit
    elif digit == 'A':
        digit = 14
        return digit
    else:
        return digit

def sum_cards(c_list):
    arr = []
    for x in range(3):
        arr.append(int(check_cards(c_list[x][0])))
    return sum(arr)

# identify hand category using IF-THEN rule
def hand_identifying(hand):
    for x in hand:
        for i in hand:
            if ((x[1] < i[1] and x[0] == i[0])):
                yield dict(name = 'pair', rank = x[0], suit1=x[1], suit2=i[1])
            for y in hand:
                if(x[0] == i[0] == y[0]) and (x[1] < i[1] < y[1]):
                    yield dict(name = 'three', rank = x[0], suit1 = x[1], suit2 = i[1], suit3 = y[1])
                    return

def hand_analysing(hand):
    hand_category = None
    for cat in hand_identifying(hand):
        print('Category: ')
        for key in "name rank suit1 suit2".split():
            print
            var = key, "=", cat[key],
        print
        hand_category = cat

    if hand_category is not None:
        return hand_category
    else:
        return None

def randomAgent():
    agent1 = randrange(0, 50)
    return agent1

def fixAgent():
    bid = [10, 20, 30]
    return bid

def reflex_Agent(card):
    if hand_analysing(card) is not None:
        if hand_analysing(card).__getitem__('name') == 'three':
            cards = "strong "
        elif sum_cards(card) >= 30 and hand_analysing(card).__getitem__('name') == 'three':
            cards = "very strong "
        elif hand_analysing(card).__getitem__('name') == 'pair':
            cards = "medium"
        else:
            cards = 'weak'
    else:
        if sum_cards(card) > 24:
            cards = 'medium'
        else:
            cards = 'weak'

    if cards == 'strong':
        return randrange(40, 48)
    elif cards == 'very strong':
        return 50
    elif cards == 'medium':
        return randrange(30,39)
    elif cards =='weak':
        return randrange(0,25)

#########################
# phase 1: Card Dealing #
#########################
coins = []
for x in range(50):
    new_deck()
    coins.clear()
    agent1.cards = generate_2hands(3)
    agent2.cards = generate_2hands(3)
    print("Agent{0.number} has cards:{0.cards}".format(agent1) + "\n" + "Agent{0.number} has cards:{0.cards}".format(agent2))

    #########################
    # phase 2:   Bidding    #
    #########################

    for i in range(3):
        print("\n" + "Bidding phase", phase1)
        agent1.bid = randomAgent()
        agent2.bid = reflex_Agent(agent2.cards)
        coins.append(agent1.bid+agent2.bid)
        print("Agent{0.number} bids: ${0.bid}".format(agent1) + "\n" + "Agent{0.number} bids: ${0.bid}".format(agent2))
        phase1 = phase1 + 1

    #########################
    # phase 2:   Showdown   #
    #########################

    analyse1 = hand_analysing(agent1.cards)
    analyse2 = hand_analysing(agent2.cards)

    if analyse1 is not None: 
        if analyse1.__getitem__('name') == 'pair':
            print("Agent one wins this round")
            agent1.win = agent1.win + 1
            agent1.wallet = (sum(coins))
        elif analyse1.__getitem__('name') == 'three':
            print("Agent one wins this round")
            agent1.win = agent1.win + 1
            agent1.wallet = (sum(coins))

    elif analyse2 is not None: 
        if analyse2.__getitem__('name') == 'pair':
            print("Agent two wins this round")
            agent2.win = agent2.win + 1
            agent2.wallet = (sum(coins))
        elif analyse2.__getitem__('name') == 'three':
            print("Agent one wins this round")
            agent2.win = agent2.win + 1
            agent2.wallet = (sum(coins))

    elif analyse1 == None and analyse2 == None: 
        if sum_cards(agent2.cards) < sum_cards(agent1.cards):
            print("Agent one wins this round")
            agent1.win = agent1.win + 1
            agent1.wallet = (sum(coins))
        else:
            print("Agent two wins this round")
            agent2.win = agent2.win + 1
            agent2.wallet=(sum(coins))

    elif analyse1 is not None and analyse2 is not None: 
        if analyse1.__getitem__('name') == 'pair' and analyse2.__getitem__('name') == 'pair':
             if analyse1.__getitem__('rank') > analyse2.__getitem__('rank'):
                 print("Agent one wins this round")
                 agent1.win = agent1.win + 1
                 agent1.wallet=(sum(coins))
             else:
                 print("Agent two wins this round")
                 agent2.win = agent2.win + 1
                 agent2.wallet=(sum(coins))
        elif analyse1.__getitem__('name') == 'three' or analyse2.__getitem__('name') == 'three':
            if analyse1.__getitem__('name') == 'three' and analyse2.__getitem__('name') == 'pair':
                print("Agent one wins this round")
                agent1.win = agent1.win + 1
                agent1.wallet=(sum(coins))
            elif analyse1.__getitem__('name') == 'pair' and analyse2.__getitem__('name') == 'three':
                print("Agent two wins this round")
                agent2.win = agent2.win + 1
                agent2.wallet=(sum(coins))
            elif analyse1.__getitem__('name') == 'three' and analyse2.__getitem__('name') == 'three':
                if analyse1.__getitem__('rank') > analyse2.__getitem__('rank'):
                    print("Agent one wins this round")
                    agent1.win = agent1.win + 1
                    agent1.wallet=(sum(coins))
                else:
                    print("Agent two wins this round")
                    agent2.win = agent2.win + 1
                    agent2.wallet=(sum(coins))
    
    phase1 = 1

print("\n" + "Agent{0.number} won {0.win} rounds and ${0.wallet}".format(agent1) + " money" + "\n" + "Agent{0.number} won {0.win} rounds and ${0.wallet}".format(agent2) + " money")