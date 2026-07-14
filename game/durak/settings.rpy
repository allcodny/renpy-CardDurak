################################################################################
##### made by AllCodny
################################################################################

init offset = -11

# Here are the settings for "Durak" on renpy
# The main code of the mini-game is in the file dursk/durak.rpy, the screens used are in durak/screens.rpy
# To start the game, use call durak_game,
# after the game is finished, the variable who_win_ will return with the value 0 (the opponent won), 1 (a draw) or 2 (the player won)

# Default values ​​are defined here, but you can change them before calling the mini-game (before writing call durak_game)


## Basic settings #######################################################################

# Who deals the cards
# False - the opponent deals the cards
# True - the player deals the cards
define player_takes_cards_ = False

# Who goes first
# 0 - determined by the lowest trump
# 1 - Player
# 2 - Opponent
define first_step_ = 0

# Who goes first if no one has trumps
# 0 - Randomly selected
# 1 - Player
# 2 - Opponent
define who_step_ = 0



# Color of notifications
define color_noti_durak = '#99ccff'

# how long does the notification stay on the screen
define noti_time_ = 2.5

# Card suit names
# Change only the value (the line after the colon)
define suits_name_ = {'hearts': 'Heart',
'diamonds': 'Diamond',
'spades': 'Spade',
'clubs': 'Club'}

# Name of the card value
# Change only the value (the string after the colon)
define value_name_ = {'6': 'six',
'7': 'seven',
'8': 'eight',
'9': 'nine',
'10': 'ten',
'11': 'jack',
'12': 'queen',
'13': 'king',
'14': 'ace'}

# Player has no trump cards (name when selected)
define no_trump_ = 'No trump cards'

# Name of moves
# Change only the value (the string after the colon)
define durak_step_name = {'player': 'Your move',
'npc_beats': 'Opponent beats',
'player_throw': 'Throw cards',
'npc': "Opponent's move",
'player_beat': 'You beat',
'npc_throw': 'Opponent throws',
'wait': 'Wait'}

# Notifications
define durak_noti_name = {'player_takes': 'You deal cards!',
'trump': ' trump!', # results in "[suit name] trump!"
'npc_take': 'The opponent took cards!',
'player_take': 'You took cards!',
'beat': 'End of turn!',
'translation': 'Transfer the move!'
}

# whether to show the "options" button
define button_options_show_ = False

# The name of the "options" button in the upper left corner
define button_options_ = 'Опции'

# Button name "Pass"
define button_pass_ = 'Pass'

# Button name "Take"
define button_take_ = 'Take'

# Button name "Translate"
define button_translation = 'Translate'




## Conditions when the opponent beats the player's card #######################################################################

# Conditions when there are still cards in the deck

# 1 (the number before the colon) - conditions for the case when there are more cards in the deck than this number
# 2 (the first after the colon) - if the player threw a trump card and it is higher in value than this number, then the opponent will take the cards
# 3 (the second after the colon) - less than what non-trump card the opponent can beat with
# 4 - less than what trump card the opponent can beat with
# 5 - If the opponent has more cards in his hand than this number, then he can beat with stronger cards
# 6 - less than what non-trump card the opponent can beat with (if condition 5 is met)
# 7 - less than what trump card the opponent can beat with (if condition 5 is met)

# If there are more than [1 number] cards in the deck, then...
# If the player threw a trump card greater than [2 numbers], the opponent will take.
# If the opponent's card is less than [3 numbers] and not a trump or a trump and less than [4 numbers], then the opponent can beat with this card.
# However, if the opponent has more than [5 numbers] cards and the opponent's card is less than [6 numbers] and not a trump or a trump and less than [7 numbers], then the opponent can beat with this card.

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define npc_condition_beat1 = {15: (9, 12, 11, 9, 12, 11),
6:  (10, 13, 11, 9, 13, 12),
0:  (11, 13, 12, 8, 14, 13)}


# Conditions when there are no more cards in the deck

# 1 - Conditions for the case if the opponent has more cards than this number
# 2 - if the player threw a trump and it is more than this number in denomination, then the opponent will take the cards
# 3 - Less than what card the opponent can beat
# 4 - How many strong cards are needed for the opponent to spend the last trump
# 5 - If the player has less than this number of cards, then the opponent will beat with any card

# If the opponent has less than [1 number] cards
# If the opponent threw a trump, more than [2 number], then he will take
# If the card is less than [3 number], then the opponent will beat with this card
# If there are more big cards than [4 number], then the opponent can beat with the last trump
# If the player has less than [5 number], then the opponent will beat with any card

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in ascending order
# By analogy you can add an additional line with values
define npc_condition_beat2 = {4: (13, 15, 1, 3),
6: (12, 13, 2, 4)
}



# Conditions for transferring cards when there are cards in the deck

# 1 - conditions for the case if there are more than this number of cards in the deck
# 2 - if the value of the suitable card is less than this number and is not a trump, then the opponent will transfer this card
# 3 - if the value of the suitable card is less than this number and is a trump, then the opponent will transfer this card

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define npc_condition_transfer1 = {15: (11, 0),
6: (12, 7),
0: (12, 8)}


# Conditions for transferring cards when there are no cards in the deck

# 1 - conditions for the case if the player has more cards than this number
# 2 - if the value of the suitable card is less than this number and is not a trump, then the opponent will transfer this card
# 3 - if the value of the suitable card is less than this number and is a trump, then the opponent will transfer this card

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define npc_condition_transfer2 = {6: (12, 8),
4: (12, 8),
2: (13, 11),
0: (14, 15)}



# Conditions for discarding several cards on the first move, when there are still cards in the deck

# 1 - conditions for the case if there are more than this number of cards in the deck
# 2 - can discard several cards less than this value
# 3 - see point 4
# 4 - can discard several cards less than this value, if there are more such cards [number 3]

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define condition_more_attack1 = {18: (9, 4, 11),
12: (10, 3, 11),
6: (11, 4, 12),
0: (11, 3, 12)}


# Conditions for discarding several cards on the first move when there are no cards in the deck

# 1 - conditions for the case if the opponent has cards more than this number
# 2 - can discard several cards less than this value
# 3 - see point 4
# 4 - can discard several cards less than this value if there are more such cards [number 3]

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define condition_more_attack2 = {6: (11, 3, 13),
3: (13, 3, 15),
0: (15, 1, 15)}




# Conditions for the opponent to throw up cards

# 1 - conditions for the case if there are more than this number of cards in the deck
# 2 - throwing up a lower value is not a trump
# 4 - throwing up a lower value is a trump

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define condition_pass1 = {12: (10, 0),
0: (11, 8)}


# Conditions for the opponent to throw cards when the deck is empty

# 1 - conditions for the case if the opponent has cards more than this number
# 2 - throwing a lower value is not a trump
# 4 - throwing a lower value is a trump

# You can change any numbers, but do not change the structure, it is also important that the numbers go from top to bottom in descending order
# By analogy, you can add an additional line with values
define condition_pass2 = {6: (11, 8),
3: (12, 11),
0: (15, 13)}





## Character images, name and emotions in the upper right corner #######################################################################
#
# The images used here are defined by ATL (their code is written at the end of this file due to their volume)
# but the files for them are in the images/durak/ folder, you can change them or delete them and define new ones
# The character image in the upper left corner must have an extension of 240*360

# Is the character image displayed?
define show_character_image_ = True

# Specifies which character images will be used
# Change only the value (the line after the colon)
define character_image_ = {'normal': 'eileen normal durak',
'happy': 'eileen happy durak',
'sad': 'eileen sad durak',
'thinks': 'eileen thinks durak'}

# Is the character name displayed?
define show_character_name_ = True 

# What character name is displayed
define character_name_ = 'Eileen' 

# Is the character's emotion displayed?
define show_character_emotion_ = True

# Character emotion names
# Change only the value (the string after the colon)
define character_emotions_ = {'normal': 'Calm',
'happy': 'Happy',
'sad': 'Sad',
'thinks': 'Thinking'}

# what emotion will the character have at the beginning of the game
# Can only take values ​​'normal', 'happy', 'sad', 'thinks'
define character_emotions_default = 'normal' 





## Phrase and Phrase Screen Settings #######################################################################

# The image that displays the phrase at the beginning of the game
define phrase_window_ = "phrase window"

# A number indicating how fast the text of the phrase is printed
# Set to 0 if you want to disable
define cps_phrase_ = 25



# Special phrases are an object of the NPCPhraseSpecial class, take three attributes in the following order:
# 1. Whether this phrase is displayed (True or False)
# 2. The phrase that the character says, the \n sign denotes a line break
# 3. The image that is displayed
# If the first is False, the other two attributes can be omitted
# General form: NPCPhraseSpecial(displayed?, phrase, image)

# Phrase at the beginning of the game if the first player goes
define pc_start_phrase_ = NPCPhraseSpecial(True, "Well, let's start the game.\nGo!", 'eileen normal phrase')

# Phrase at the beginning of the game if the opponent goes first
define npc_start_phrase_ = NPCPhraseSpecial(True, "Let's start the game!\nThe first move is mine", 'eileen happy phrase')

# The phrase at the beginning of the game, if the first player to go is the one with the lowest trump card, the designation |num| denotes the opponent's lowest trump card, for correct operation |num| must be in the phrase
define start_phrase_ = NPCPhraseSpecial(True, "Let's start the game!\nI have the lowest trump card, which is |num|.\nWhat do you have?", 'eileen happy phrase')




# Other Phrases
# These phrases usually come after other phrases and their display depends on whether the phrase they follow is shown or not
#
# Phrases are an object of the Phrase class and take two attributes:
# 1. The text of the phrase
# 2. The image of the character at the time of the phrase
# General form: Phrase(text, image)


# Phrase at the beginning of the game if the move is determined by the trump card and the opponent has no trump cards
define no_npc_trump_phrase = Phrase('Oh, I have no trump cards..\nWhat do you have?', 'eileen normal phrase')

# A phrase used when a player has a lower trump card than his opponent.
define lesser_trump_phrase = Phrase('Okay, you have the lower trump card,\nYour move!', 'eileen normal phrase')

# Phrase when the opponent has a lower trump card
define bigger_trump_phrase = Phrase("Great, I have less, so I'm leading!", 'eileen happy phrase')

# A phrase used when the opponent does not have a trump card, but the player does
define npc_no_trump_phrase = Phrase('Oh, okay, your move.', 'eileen normal phrase')

# A phrase used when a player does not have a trump card and the opponent does
define player_no_trump_phrase = Phrase("Great, guess I'll go then!", 'eileen happy phrase')

# Phrase when no one has trumps and the opponent moves
define n_no_trump_phrase = Phrase("Oh, you too...\nThen I go!", 'eileen happy phrase')

# Phrase when no one has trumps and it is the player's turn
define p_no_trump_phrase = Phrase("Oh, you don't have one either...\nThen you go.", 'eileen normal phrase')



# Phrases during the game
# These phrases appear during the game itself next to the character image when the enemy's emotion changes

# Show phrases during the game?
define durak_phrase_show = True

# after how many seconds the phrase disappears
define durak_phrase_t = 2

# Chance that the phrase will be said when the enemy's emotion changes
define durak_phrase_chance = 0.3

# Phrases are selected randomly from the list after the colon, you can add as many as you like, but don't make them too long
define durak_phrases = {'happy': ["Great!", "He-he", "Watch your turn!", "Victory is mine!"],
'sad': ["Well...", "Oh...", "That's sad..."],
'thinks': ["Hmm...", "I need to think..."]}




## Music and sounds #######################################################################
#
# To change music and sounds, it is best to simply replace existing files
# All audio files are in the durak folder

# music that plays in the background during the minigame
define audio.durak = 'durak/durak_loop.ogg'

# music volume
define durak_music_valume = 0.6

# sounds for cards
define audio.slide_ = 'durak/card_slide.flac' # the card is moving
define audio.take_ = 'durak/card_take.flac' # the card is taken from the deck

# volume of sounds for cards, set to 0 to disable
define sound_card_valume = 1.0

# sound of window appearing with phrase
define audio.woosh = 'durak/woosh.flac'










## Image Definition via ATL #######################################################################
#
# This definition is more of an introductory nature, you can use it to define your images
# or completely erase it by specifying a different image value in the variables


# This image definition makes the image blink (if happy it blinks faster, if sad it keeps its eyes closed longer)
# Also the background is immediately added to the image
image eileen normal durak:
    contains:
        'bg durak chr'
    contains:
        'eileen normal0'
        choice:
            pause 2.3
        choice:
            pause 2.8
        choice:
            pause 2.0
        choice:
            pause 2.5
        'eileen normal1'
        choice:
            pause 0.12
        choice:
            pause 0.15
        choice:
            pause 0.2
        repeat

image eileen thinks durak:
    contains:
        'bg durak chr'
    contains:
        'eileen thinks0'
        choice:
            pause 2.3
        choice:
            pause 2.8
        choice:
            pause 2.0
        choice:
            pause 2.5
        'eileen thinks1'
        choice:
            pause 0.12
        choice:
            pause 0.15
        choice:
            pause 0.2
        repeat

image eileen happy durak:
    contains:
        'bg durak chr'
    contains:
        'eileen happy0'
        choice:
            pause 1.5
        choice:
            pause 1.0
        choice:
            pause 2.0
        choice:
            pause 0.5
        'eileen happy1'
        choice:
            pause 0.1
        choice:
            pause 0.12
        choice:
            pause 0.2
        repeat

image eileen sad durak:
    contains:
        'bg durak chr'
    contains:
        'eileen sad0'
        choice:
            pause 2.3
        choice:
            pause 2.8
        choice:
            pause 2.0
        choice:
            pause 2.5
        'eileen sad1'
        choice:
            pause 0.3
        choice:
            pause 0.35
        choice:
            pause 0.25
        repeat

image eileen happy phrase:
    'eileen happy0'
    choice:
        pause 1.5
    choice:
        pause 1.0
    choice:
        pause 2.0
    choice:
        pause 0.5
    'eileen happy1'
    choice:
        pause 0.1
    choice:
        pause 0.12
    choice:
        pause 0.2
    repeat

image eileen normal phrase:
    'eileen normal0'
    choice:
        pause 1.5
    choice:
        pause 1.0
    choice:
        pause 2.0
    choice:
        pause 0.5
    'eileen normal1'
    choice:
        pause 0.1
    choice:
        pause 0.12
    choice:
        pause 0.2
    repeat

image eileen sad phrase:
    'eileen sad0'
    choice:
        pause 1.5
    choice:
        pause 1.0
    choice:
        pause 2.0
    choice:
        pause 0.5
    'eileen sad1'
    choice:
        pause 0.1
    choice:
        pause 0.12
    choice:
        pause 0.2
    repeat

################################################################################
##### made by AllCodny
################################################################################
