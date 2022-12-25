from random import shuffle

# All possible playing cards, with their names and values
cards = dict()

# The shuffled deck of cards to be dealt to the player and dealer during the game
game_deck = []

# The player and dealer have a list of card name, which correspond to keys in the cards dict
# This is so the game can nicely present the names of the cards
player_cards = []
dealer_cards = []

# Creates all 52 possible cards for the game
def initCards():
    suits = {'Clubs', 'Diamonds', 'Hearts', 'Spades'}
    for suit in suits:
        for i in range(13):
            card_value = i + 1
            
            if card_value == 1:
                # Blackjack allows the Ace to count as an 11 if it would not cause the value of the hand to exceed 21
                card_name = 'Ace (1 or 11)'
            elif card_value == 11:
                # The Jack, Queen, and King all count as 10 in Blackjack
                card_name = 'Jack (10)'
                card_value = 10
            elif card_value == 12:
                card_name = 'Queen (10)'
                card_value = 10
            elif card_value == 13:
                card_name = 'King (10)'
                card_value = 10
            else:
                card_name = str(card_value)

            card_name = card_name + " of " + suit

            cards[card_name] = card_value

# Shuffles a fresh deck of cards for the game
def shuffleDeck():
    if not cards:
        initCards()
    
    game_deck.clear()
    game_deck.extend(list(cards.keys()))
    shuffle(game_deck)

def getHandValue(hand: list):
    value = 0
    has_ace = False 
    for card_name in hand:
        if 'Ace' in card_name:
            has_ace = True
        value += cards[card_name]
    
    # Rules of Blackjack: An ace can count as an 11 if it would not cause the value of your hand to exceed 21
    if has_ace and value + 10 <= 21:
        value += 10
    return value

def addCardToHand(hand: list):
    card = game_deck.pop()
    hand.append(card)
    return card

# Gets a nice, clean string to display the hand instead of displaying the raw list with those ugly []
def getHandDisplayString(hand: list):
    display_string = ', '.join(hand)
    return display_string

def getPlayerChoice():
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
        card = addCardToHand(player_cards)
        print(f'{card} was added to your hand')
    else:
        stand = True

    return stand

quit = False
shuffleDeck()

# Each iteration of this loop is a seperate game
game_over = False
while not quit:
    player_has_hit = False # Used to track if the player has managed to win on the first deal
    while not game_over:
        while len(dealer_cards) < 2:
            addCardToHand(dealer_cards)
        while len(player_cards) < 2:
            addCardToHand(player_cards)

        player_hand_value = getHandValue(player_cards)

        print(f'One of the dealer\'s cards is: {dealer_cards[0]}')
        print(f'Your Hand: {getHandDisplayString(player_cards)}')

        if player_hand_value > 21:
            print(f'BUST! The value of your hand is {player_hand_value}')
            game_over = True
            break
        elif player_hand_value == 21 and not player_has_hit:
            print('You reached 21 on the first deal!')
            print('BLACKJACK')
            game_over = True
            break

        stand = getPlayerChoice()
        player_has_hit = True
        if stand:
            dealer_value = getHandValue(dealer_cards)

            print(f'Your Hand: {getHandDisplayString(player_cards)} - Total Value {player_hand_value}')
            print(f'Dealer\'s Hand: {getHandDisplayString(dealer_cards)} - Total Value {dealer_value}')

            if dealer_value > 21:
                print('Looks like the dealer busted, you win!')
            elif player_hand_value > dealer_value:
                print('You win!')
            elif player_hand_value == dealer_value:
                print('It\'s a Draw!')
            elif player_hand_value < dealer_value:
                print('You lose!')
            game_over = True
        

    player_choice = input('Would you like to play again? Y / N >> ').upper()
    if player_choice == 'Y':
        game_over = False
        shuffleDeck()
        player_cards = []
        dealer_cards = []
    elif player_choice == 'N':
        quit = True
    else:
        print('Invalid choice! Please try again')

print('Thank you for playing!')