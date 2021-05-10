# Import Modules and Define Variables

import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack(10)", "Queen(10)", "King(10)", "Ace(10)")
values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
          "10": 10, "Jack(10)": 10, "Queen(10)": 10, "King(10)": 10, "Ace(10)": 10}

Playing = True

# Classes

class Card:  # Creates all the cards

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " " + "of " + self.suit


class Deck:  # Creates a deck of cards

    def __init__(self):
        self.deck = []  # No deck yet
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n " + card.__str__()
        return "The deck has:" + deck_comp

    def shuffle(self):  # Shuffle all the cards in the deck
        random.shuffle(self.deck)

    def deal(self):  # Pick out a card from the deck
        single_card = self.deck.pop()
        return single_card


class Hand:  # Show All cards Dealer and Player have

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # keep track of aces

    def add_card(self, card):  # add a card to the Player's or Dealer's hand
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace(10)":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 21:
            self.value -= 10
            self.aces -= 1


class Chips:  # Keep track fo chips

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Functions

def take_bet(chips):  # ask for user's bet

    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet?"))

        except (ValueError, IndexError):
            print("Sorry please type a number")

        else:
            if chips.bet > chips.total:
                print("Can't exceed 100!")
            else:
                break


def hit(deck1, hand):
    hand.add_card(deck1.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck1, hand):  # hit or stand
    global Playing

    while True:

        try:
            ask = input("\nWould you like to hit or stand? please enter 'h' or 's':")
            if ask[0].lower() == "h":
                print("player hits, Dealer is playing")
                hit(deck1, hand)
            elif ask[0].lower() == "s":
                print("player Stands, Dealer is playing")
                Playing = False
            else:
                print("Only press 'h' or 's' please try again!")
            break

        except (ValueError, IndexError):
            print("Only press 'h' or 's' please try again!")


def show_some(player, dealer):
    print("\nDealer's hand:")
    print(" <Card hidden>")
    print("", dealer.cards[1])
    print("\nPlayer's hand:", *player.cards, sep="\n ")


def show_all(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep="\n ")
    print(" Dealer's hand =", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep="\n ")
    print("Player's hand=", player.value)


# game ending

def player_busts(player, dealer, chips):
    print("Player Bust!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def Dealer_busts(player, dealer, chips):
    print("Dealer Bust!")
    chips.win_bet()


def Dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("Its a push! Player and Dealer tie!")


def end_game():
    global new_game

    while True:
        try:
            new_game = input("Would you like to play again? Enter 'y' or 'n': ")
            if new_game[0].lower() == "y":
                break
            if new_game[0].lower() == "n":
                print("\nThank you for playing Tomer's BlackJack!")
                break
            else:
                print("Only press 'y' or 'n' please")
                continue

        except (ValueError, IndexError):
            print("Sorry please 'y' or 'n' please")

# GamePlay


while True:

    print("Welcome to Tomer's BlackJAck!")
    # create and shuffle deck

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    New_Name = str(input("What is your name?:"))
    if New_Name.lower() == "tomer" or New_Name.lower() == "rami" or New_Name[0].lower() == "b":
        print("Hello" + " " + New_Name + "!")
        print("You have a Beautiful name!")
    else:
        print("Hello" + " " + New_Name + "!")

    # set up the player's chips
    player_chips = Chips()

    # ask player for bet
    take_bet(player_chips)

    # show cards
    show_some(player_hand, dealer_hand)

    while Playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            Dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            Dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

    print("\nPlayer's Chips stands at", player_chips.total)
    global new_game
    end_game()
    if new_game[0].lower() == "n":
        break
