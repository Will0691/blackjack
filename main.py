from random import shuffle

# Represents a playing card
class Card():
    def __init__(self, suit, value):
        if value == 1:
            # Blackjack allows the Ace to count as an 11 if it would not cause the value of the hand to exceed 21
            self.name = 'Ace (1 or 11)'
            self.value = 1
        elif value == 11:
            # The Jack, Queen, and King all count as 10 in Blackjack
            self.name = 'Jack (10)'
            self.value = 10
        elif value == 12:
            self.name = 'Queen (10)'
            self.value = 10
        elif value == 13:
            self.name = 'King (10)'
            self.value = 10
        else:
            self.name = str(value)
            self.value = value
        
        self.name = self.name + ' of ' + suit

    def __str__(self):
        return self.name

# Represents a deck of cards
class Deck():
    def __init__(self):
        self.cards = []

        suits = {'Clubs', 'Diamonds', 'Hearts', 'Spades'}
        for suit in suits:
            for i in range(13):
                self.cards.append(Card(suit, i + 1 ))

    def shuffle(self):
        shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop()
        
    # This was for debugging purposes...
    def __str__(self):
        display_string = ', '.join(self.cards)
        return display_string

# Represents the hand of the player or dealer
class Hand():
    def __init__(self):
        self.cards = []

    def addCardToHand(self, deck):
        card = deck.drawCard()
        self.cards.append(card)
        return card

    def getHandValue(self):
        value = 0
        has_ace = False 
        for card in self.cards:
            if 'Ace' in card.name:
                has_ace = True
            value += card.value
        
        # Rules of Blackjack: An ace can count as an 11 if it would not cause the value of your hand to exceed 21
        if has_ace and value + 10 <= 21:
            value += 10
        return value

    def __str__(self):
        display_string = ', '.join([card.name for card in self.cards])
        return display_string

# The game itself
class Game():

    def __init__(self):
        self.game_over = False
        self.player_has_hit = False # Used to track if the player has managed to win on the first deal

        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_hand.addCardToHand(self.deck)
        self.player_hand.addCardToHand(self.deck)

        self.dealer_hand.addCardToHand(self.deck)
        self.dealer_hand.addCardToHand(self.deck)

        # The number in which dealers will continue to draw varies by place
        while (self.dealer_hand.getHandValue() < 16):
            self.dealer_hand.addCardToHand(self.deck)
    
    def getPlayerChoice(self):
        has_chosen = False
        choices = ['hit', 'stand']
        choice = ''
        stand = False

        while choice not in choices:
            if has_chosen:
                print('That wasn\'t a valid choice')
            choice = input('What will you do: Hit or Stand? >> ').lower()
            has_chosen = True
        
        if choice == choices[0]:
            card = self.player_hand.addCardToHand(self.deck)
            print(f'{card} was added to your hand')
        else:
            stand = True

        return stand

    def play(self):
        while not self.game_over:
            player_hand_value = self.player_hand.getHandValue()

            print(f'The dealer\'s hand contains {len(self.dealer_hand.cards)} cards')
            print(f'One of the dealer\'s cards is: {self.dealer_hand.cards[0]}')
            print(f'Your Hand: {self.player_hand}')

            if player_hand_value > 21:
                print(f'BUST! The value of your hand is {player_hand_value}')
                self.game_over = True
                print()
                break
            elif player_hand_value == 21 and not self.player_has_hit:
                print('You reached 21 on the first deal!')
                print('BLACKJACK')
                self.game_over = True
                print()
                break

            stand = self.getPlayerChoice()
            self.player_has_hit = True
            if stand:
                dealer_hand_value = self.dealer_hand.getHandValue()

                print(f'Your Hand: {self.player_hand} - Total Value {player_hand_value}')
                print(f'Dealer\'s Hand: {self.dealer_hand} - Total Value {dealer_hand_value}')

                if dealer_hand_value > 21:
                    print('Looks like the dealer busted, you win!')
                elif player_hand_value > dealer_hand_value:
                    print('You win!')
                elif player_hand_value == dealer_hand_value:
                    print('It\'s a Draw!')
                elif player_hand_value < dealer_hand_value:
                    print('You lose!')
                self.game_over = True

    def gameOver(self):
        if not self.game_over:
            return False

        player_choice = input('Would you like to play again? Y / N >> ').upper()
        if player_choice == 'Y':
            print()
            self.reset()
            return False
        elif player_choice == 'N':
            return True
        else:
            print('Invalid choice! Please try again')
        
        return False

    def reset(self):
        self.__init__()


game = Game()
while not game.gameOver():
    game.play()

print('Thank you for playing!')