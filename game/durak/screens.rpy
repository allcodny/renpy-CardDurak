################################################################################
##### made by AllCodny
################################################################################

init offset = -9

# File with screens for the mini-game "Durak"
# For settings (changing phrases and other things) use the file durak/settings.rpy
# The main code of the mini-game is in the file durak/durak.rpy
# To start the game, use call durak_game,
# after the game is finished, the variable who_win_ will return with the value 0 (the opponent won), 1 (draw) or 2 (the player won)

# Screens use classes and functions defined in the file durak.rpy

define text_size_ = 40 if renpy.variant("small") else 35

## Main screen for the game #######################################################################
screen durak_card_game(): 
    zorder 50

    # beaten
    if len(discard_pile) > 0:
        add 'backcard' at discard_pile_atl(-0.1, 0.66, -7)
    if len(discard_pile) > 1:
        add 'backcard' at discard_pile_atl(-0.1, 0.66, 5)

    # Deck of cards and the bottom trump
    $ qt = len(card_deck_) # number of cards in a deck
    # shows the bottom trump if the deck is not empty
    if qt > 0: 
        add card_deck_[-1].image() xalign -0.06 yalign 0.2 rotate 110 zoom 1.2
    # shows the reversed card and the number of cards if there is more than 1 card in the deck
    if qt > 1: 
        add 'backcard' xalign -0.1 yalign 0.17 rotate 200 zoom 1.2
        text '[qt]' xanchor 0.5 xpos 90 yalign 0.13 size 45:
            outlines [ (1.5, "#0000005b", 2, 2), (1.2, "#000000ff", 0, 0)]

    # names of the current move
    text '[durak_step_name[durak_step]]' xalign 0.5 yalign 0.01 size 40:
        outlines [ (1.5, "#0000005b", 1, 1), (1.2, "#000000ff", 0, 0)]

    # "options" button
    if button_options_show_:
        frame:
            xalign 0.02 yalign 0.03
            padding (10, 5)
            textbutton _("{size=33}[button_options_]{/size}") action ShowMenu('preferences')

    # button on the playing field for a player to attack
    button:
        xalign 0.4 yalign 0
        xsize 1200
        ysize 700
        
        if select_card_ is not None and durak_step in ['player', 'player_throw']:
            action [Function(playing_field_.player_attack, select_card_, False), SetVariable('select_card_', None)]

    # buttons for beat
    if durak_step == 'player_beat':
        $ card = 0
        for y in [0.14, 0.52]:
            for x in [0.45, 0.25, 0.65]:
                $ card += 1
                if playing_field_.number_cards_attack >= card and playing_field_.cards_beat[card-1] is None:
                    $ c = playing_field_.cards_attack[card-1]
                    button:
                        padding (0, 0, 0, 0)
                        yalign y xalign x
                        add 'card_null' zoom 1.2 rotate -7
                        if select_card_ is not None and ((select_card_.suit == c.suit and select_card_.value > c.value) or (select_card_.trump and not c.trump)):
                            action [Function(playing_field_.player_beat, select_card_, card-1), SetVariable('select_card_', None)] #Notify(card)


    on "show" action Show('s_durak_player_cards')


# Screen with cards in attack
screen card_in_attack():

    for i in range(0, 6):
        if playing_field_.number_cards_attack > i: # attacking
            if playing_field_.state == 'normal':
                $ durak_sca = durak_scap[i] if playing_field_.cards_attack_from[i] else durak_scan[i]
                add playing_field_.im(i) at durak_sca
            else:
                $ durak_sca = {'npc_take': npc_take_attack_atl,
                'beat': beat_card_atl_attack,
                'take': take_cards_atl_attack}
                add playing_field_.im(i) at durak_sca[playing_field_.state][i]
        if len(playing_field_.cards_beat) > i and playing_field_.cards_beat[i] is not None: # beating
            if playing_field_.state == 'normal':
                $ durak_scb = durak_scbp[i] if playing_field_.cards_beat_from[i] else durak_scbn[i]
                add playing_field_.im_beat(i) at durak_scb
            else:
                $ durak_sca = {'npc_take': npc_take_beat_atl,
                'beat': beat_card_atl_beat,
                'take': take_cards_atl_beat}
                add playing_field_.im_beat(i) at durak_sca[playing_field_.state][i]


# player cards screen
screen durak_player_cards():

    zorder 60

    default past_select = None

    for rows in [24, 12, 0]:

        if len(player_cards_.set()) > rows:

            $ x = -15 if rows == 24 else (-30 if rows == 12 else -45)
            $ y = 0.9 if rows == 24 else (1.07 if rows == 12 else 1.27)
            $ size_ = 130 if rows == 24 else (140 if rows == 12 else 150)

            hbox at player_cards:
                xalign 0.5
                yalign y
                for p_card in player_cards_.set(start=rows, end=rows+12):

                    $ card_states = {hide_player_card: player_card_hide,
                    select_card_: player_card_select,
                    past_select: player_card_past}

                    $ atl = card_states.get(p_card, player_card)

                    $ trow = durak_step == 'player_throw' and p_card.value in playing_field_.value
                    $ trans = durak_step == 'player_beat' and playing_field_.number_beat_attack == 0 and p_card.value in playing_field_.value and npc_cards_.qt() >= len(playing_field_.cards_attack)+1 <= 6
                    $ beat = durak_step == 'player_beat' and any(((c.suit == p_card.suit and c.value < p_card.value) or (not c.trump and p_card.trump)) and playing_field_.cards_beat[playing_field_.cards_attack.index(c)] is None for c in playing_field_.cards_attack)

                    button at atl:
                        xoffset x
                        xsize size_
                        add p_card.image() zoom 1.7 xalign 0.5 yoffset -45 rotate -4 xoffset 45
                        
                        if select_card_ != p_card and (durak_step == 'player' or trow or trans or beat):
                            action [SetLocalVariable('past_select', select_card_), SetVariable('select_card_', p_card)]


screen s_durak_player_cards():

    hbox at s_player_card_:
        xalign 0.5
        yalign 1.27
        for p_card in player_cards_.set(end=12):
            button:
                xoffset -45
                xsize 150
                add p_card.image() zoom 1.7 xalign 0.5 yoffset -45 rotate -4 xoffset 45

    if not renpy.get_screen('phrase_modal'):
        timer 0.01 action [Show('durak_player_cards'), Show('card_in_attack'), Hide('s_durak_player_cards')]
        if durak_step == 'npc' :
            timer 0.005 action [Function(npc_emotion_.change, 'thinks'), Show('npc_attack_t')]


## Image of a character with inscriptions in the upper right corner and buttons #######################################################################
screen durak_character_image():

    zorder 150

    # Position depending on what is shown on the screen
    $ y_card = 0.32 if show_character_image_ else 0.17
    $ x_card = 0.83 if show_character_image_ else 0.93
    $ y_text = 0.345 if show_character_image_ else 0.21
    $ x_text = 1547 if show_character_image_ else 1725
    $ y_buttons = 0.51 if show_character_image_ else 0.32

    $ qt_npc = npc_cards_.qt() # number of cards the opponent has
    # displays one card reversed
    if qt_npc > 0: 
        add 'backcard' zoom 0.7 xalign x_card yalign y_card at dissolve_extra_
    # displays the second card turned over and the number of cards if the opponent has more than 1 card
    if qt_npc > 1: 
        add 'backcard' zoom 0.7 xalign x_card yalign y_card rotate -10 at dissolve_extra_
        text '[qt_npc]' xanchor 0.5 xpos x_text yalign y_text size 40 at dissolve_extra_:
            outlines [ (1.5, "#0000005b", 2, 2), (1.2, "#000000ff", 0, 0)]

    # image of a character with inscriptions
    vbox at dissolve_extra_:
        xalign 0.97 yalign 0.035
        if show_character_name_: # displayed name
            frame:
                padding (0, 3)
                yoffset 3
                xsize 252
                text '[character_name_]' xalign 0.5 size 33
        if show_character_image_: # displayed image
            frame:
                xsize 252 ysize 372
                add npc_emotion_.image()
        if show_character_emotion_: # displayed emotion
            frame:
                padding (0, 3)
                yoffset -3
                xsize 252
                text npc_emotion_.name() xalign 0.5 size 33

    # buttons
    vbox at dissolve_extra_:
        xalign 0.97 yalign y_buttons
        frame: # pass
            padding (0, 0)
            xsize 252
            if durak_step == 'player_throw':
                textbutton "{size=33}[button_pass_]{/size}" xalign 0.5 action [Function(playing_field_.beat_durak, 'p', 'npc')]
            else:
                textbutton "{size=33}[button_pass_]{/size}" xalign 0.5
        frame: # take
            padding (0, 0)
            xsize 252
            yoffset -3
            if durak_step == 'player_beat':
                textbutton "{size=33}[button_take_]{/size}" xalign 0.5 action [Function(playing_field_.player_take), Function(npc_emotion_.change, 'happy')]
            else:
                textbutton "{size=33}[button_take_]{/size}" xalign 0.5
        frame: # translate
            padding (0, 0)
            xsize 252
            yoffset -5
            if durak_step == 'player_beat' and select_card_ is not None and playing_field_.number_beat_attack == 0 and select_card_.value in playing_field_.value and npc_cards_.qt() >= len(playing_field_.cards_attack)+1 <= 6:
                textbutton "{size=33}[button_translation]{/size}" xalign 0.5 action [Function(playing_field_.player_translation, select_card_), SetVariable('select_card_', None)]
            else:
                textbutton "{size=33}[button_translation]{/size}" xalign 0.5


## Notifications #######################################################################
screen durak_noti(message, time=0):

    zorder 100

    text '{color=[color_noti_durak]}[message]{/color}' xalign 0.5 yalign 0.055 size 60 at noti_atl:
        outlines [ (2, "#0000005b", 1, 1), (1.7, "#000000ff", 0, 0)]

    timer noti_time_+time action Hide("durak_noti")

screen durak_noti_small(message, time=0):

    text '{color=#fff}[message]{/color}' xalign 0.5 yalign 0.13 size 30 at noti_atl:
        outlines [ (1.4, "#0000005b", 1, 1), (1.2, "#000000ff", 0, 0)]

    timer noti_time_+time action Hide("durak_noti_small")


## Screen for the phrase that interrupts the game #######################################################################

# main screen phrase with window and character
screen phrase_modal(message, image, act=None, extra=None, fast=False):
    modal True
    zorder 100

    add '#000' at black_bg_atl
    add image at phrase_chr_atl
    add phrase_window_ at phrase_window_atl
    
    if fast:
        timer 0.01 action Show('phrase_modal_text', message=message, act=act, extra=extra) # text appears quickly
    else:
        timer 0.7 action Show('phrase_modal_text', message=message, act=act, extra=extra) # the text appears only after the animation is finished


# output text
screen phrase_modal_text(message, act=None, spot_step=False, extra=None):
    zorder 100
    button:
        xfill True yfill True
        vbox at dissolve_hide_:
            xsize 1000 xcenter 0.5 ycenter 0.61
            text """[message]""" xcenter 0.5:
                size text_size_
                textalign 0.5
                layout "subtitle"
                slow_cps cps_phrase_
        if spot_step:
            action [Show(act, spot_step=True), Hide('phrase_modal_text')]
        elif act == 'end':
            # if the action is equal to end, then the game ends
            action Jump('end_card_game')
        elif act == 'hide':
            # if the action is hide the window with the phrase is hidden
            action [Hide('phrase_modal', transition=Dissolve(.2)), Show('durak_character_image'), Hide('phrase_modal_text', transition=Dissolve(.2))]
        elif act == 'hide_add':
            # the window with the phrase is hidden and the player is given a card
            action [Function(player_cards_.add_cards, extra), Hide('phrase_modal', transition=Dissolve(.2)), Show('durak_character_image'), Hide('phrase_modal_text', transition=Dissolve(.2))]
        elif act == 'hide_':
            # additional hiding without showing the character image
            action [Hide('phrase_modal', transition=Dissolve(.2)), Hide('phrase_modal_text', transition=Dissolve(.2))]
        elif act is not None:
            # window shown after clicking
            action [Show(act), Hide('phrase_modal_text')]


# screen with answer about trump
screen choice_trump_modal():
    zorder 100
    style_prefix 'choice_modal'
    vbox at ctm_atl:
        xsize 1000 xcenter 0.5 ycenter 0.61
        spacing 30
        hbox:
            xcenter 0.5
            spacing 50 
            if player_cards_.lesser_trump() is not None:
                $ card = player_cards_.lesser_trump().value_name().title()
                $ n = player_cards_.lesser_trump().value 
                textbutton '[card]' action [Function(trump_phrase), Hide('trump_choice_list'), Hide('choice_trump_modal')]
            else:
                textbutton no_trump_ action [Function(trump_phrase, n=0), Hide('trump_choice_list'),  Hide('choice_trump_modal')]


# screen phrases during the game
screen durak_phrase_(text='Text'):
    zorder 90
    style_prefix 'durak_phrase_st'
    window at durak_phrase_atl:
        id 'window'
        xanchor 1.0 xpos 1600 ypos 50
        text "[text]"


screen durak_phrase_hide():
    timer durak_phrase_t action [Hide('durak_phrase_'), Hide('durak_phrase_hide')]




## Screens when a player deals cards #######################################################################

# main
screen takes_cards():

    # refreshes the screen for correct operation
    timer 0.1 action Function(renpy.restart_interaction) repeat True

    add TakesCards() # display object to detect click

    if starting_cards[1] > 0:
        text '{size=45}[starting_cards[1]]{/size}' xalign 0.64 yalign 0.52 at dissolve_fast_text_:
            outlines [ (3, "#0000005b", 1, 1), (1.7, "#000000ff", 0, 0)]
    if starting_cards[0] > 0:
        text '{size=45}[starting_cards[0]]{/size}' xalign 0.4 yalign 0.2 at dissolve_fast_text_:
            outlines [ (3, "#0000005b", 1, 1), (1.7, "#000000ff", 0, 0)]

screen takes_cards_plus(who, how):

    if who == 1:
        text '{size=20}+[how]{/size}' xalign 0.657 yalign 0.51 at text_plus_cards:
            outlines [ (1.5, "#0000005b", 1, 1), (1, "#000000ff", 0, 0)]
    else:
        text '{size=20}+[how]{/size}' xalign 0.417 yalign 0.2 at text_plus_cards:
            outlines [ (1.5, "#0000005b", 1, 1), (1, "#000000ff", 0, 0)]

    

## Other screens ####################################################################

# Changes the player's cards
screen change_player_cards(act, card=None, t=0.2, extra=None):
    timer t action Hide('durak_player_cards')
    if act in ['attack', 'trans', 'beat', 'hide']:
        $ t2 = renpy.random.random()
        timer t+0.05 action [Function(player_cards_.remove_card, card), Show('durak_player_cards', transition=Dissolve(.2)), SetVariable('hide_player_card', None)]
        if act == 'attack':
            timer 1+t2*1.8 action [Function(playing_field_.npc_beats, card), Hide('change_player_cards')]
        elif act == 'trans':
            timer 1+t2*2 action [Function(playing_field_.npc_beats_more), Hide('change_player_cards')]
        elif act == 'beat':
            timer t+0.3 action [extra, Hide('change_player_cards')]
        else:
            timer t+0.05 action Hide('change_player_cards')
    else:
        timer t+0.05 action [Function(player_cards_.add_cards, card), Show('durak_player_cards', transition=Dissolve(.2)), Hide('change_player_cards')]

# resets the value on the field
screen reset_field(t=1.5, last='p', next='player', who_cant=None):
    timer t action [Function(playing_field_.reset), Function(end_move, last, next, who_cant), Hide('reset_field')]

# used to deal cards
screen issue_card(who, t, name):
    $ f = card_deck_remove if who == 'p' else npc_cards_.add_cards_from_dec
    if len(card_deck_) != 1:
        $ atl_ = issue_cards_player if who == 'p' else issue_cards_npc
        $ im = 'backcard'
    else:
        $ atl_ = issue_last_cards_player if who == 'p' else issue_last_cards_npc
        $ im = card_deck_[-1].image()
    timer t action [Show('card_issue', _tag=name, t=t+1.5, atl=atl_, name=name), Function(f, 1), Play(channel='sound', file=["<silence .03>", audio.take_], relative_volume=sound_card_valume)]

screen card_issue(t, atl, name):
    zorder 55
    add 'backcard' at atl
    timer t action Hide(name)

# resets the enemy's emotion
screen reset_emotion_npc():
    $ t = renpy.random.randint(1, 8)
    timer t action [Function(npc_emotion_.reset), Hide('reset_emotion_npc')]

# changes the course of the game with a timer
screen change_durak_move(move, t=0.01):
    if move == 'npc':
        timer t action [SetVariable('durak_step', move), Show('npc_attack_t'), Function(npc_emotion_.change, 'thinks'), Hide('change_durak_move')]
    else:
        timer t action [SetVariable('durak_step', move), Hide('change_durak_move')]

# enemy attack with timer
screen npc_attack_t():
    $ t = renpy.random.random()
    timer t*2 action [Function(playing_field_.npc_attack), Hide('npc_attack_t')]

screen npc_toss_t():
    $ t = renpy.random.random()
    timer t*2 action [Function(playing_field_.npc_toss), Hide('npc_toss_t')]




################################################################################
## Transformations
################################################################################

transform durak_phrase_atl:
    yoffset 50 alpha 0.0
    easein_quart 0.5 yoffset 0 alpha 1.0
    on hide:
        ease 0.2 alpha 0.0

transform durak_show_card_attack_p(x, y):
    xalign 0.5 yalign 1.5 zoom 1.2 rotate 70
    pause 0.2
    easein_quint 1 xalign x yalign y rotate -7

transform durak_show_card_attack_n(x, y):
    xalign 0.5 yalign -0.5 zoom 1.2 rotate 70
    easein_quint 1 xalign x yalign y rotate -7

transform durak_show_card_beat_n(x, y):
    xalign 0.5 yalign -0.5 zoom 1.2 rotate 70
    easein_quint 1 xalign x yalign y rotate 5

transform durak_show_card_beat_p(x, y):
    xalign 0.5 yalign 1.5 zoom 1.2 rotate 70
    easein_quint 1 xalign x yalign y rotate 5

define durak_scap = [durak_show_card_attack_p(0.45, 0.14), durak_show_card_attack_p(0.25, 0.14), durak_show_card_attack_p(0.65, 0.14),
durak_show_card_attack_p(0.45, 0.52), durak_show_card_attack_p(0.25, 0.52), durak_show_card_attack_p(0.65, 0.52)]

define durak_scan = [durak_show_card_attack_n(0.45, 0.14), durak_show_card_attack_n(0.25, 0.14), durak_show_card_attack_n(0.65, 0.14),
durak_show_card_attack_n(0.45, 0.52), durak_show_card_attack_n(0.25, 0.52), durak_show_card_attack_n(0.65, 0.52)]

define durak_scbn = [durak_show_card_beat_n(0.47, 0.18), durak_show_card_beat_n(0.27, 0.18), durak_show_card_beat_n(0.67, 0.18),
durak_show_card_beat_n(0.47, 0.56), durak_show_card_beat_n(0.27, 0.56), durak_show_card_beat_n(0.67, 0.56)]

define durak_scbp = [durak_show_card_beat_p(0.47, 0.18), durak_show_card_beat_p(0.27, 0.18), durak_show_card_beat_p(0.67, 0.18),
durak_show_card_beat_p(0.47, 0.56), durak_show_card_beat_p(0.27, 0.56), durak_show_card_beat_p(0.67, 0.56)]

transform npc_take_atl(x, y, r):
    alpha 1.0 zoom 1.2 xalign x yalign y rotate r
    easein_quint 1 yalign -0.4 xalign 0.45

define npc_take_attack_atl = [npc_take_atl(0.45, 0.14, -7), npc_take_atl(0.25, 0.14, -7), npc_take_atl(0.65, 0.14, -7),
npc_take_atl(0.45, 0.52, -7), npc_take_atl(0.25, 0.52, -7), npc_take_atl(0.65, 0.52, -7)]

define npc_take_beat_atl = [npc_take_atl(0.47, 0.18, 5), npc_take_atl(0.27, 0.18, 5), npc_take_atl(0.67, 0.18, 5),
npc_take_atl(0.47, 0.56, 5), npc_take_atl(0.27, 0.56, 5), npc_take_atl(0.67, 0.56, 5)]

transform beat_card_atl(x, y, r):
    parallel:
        zoom 1.2 xalign x yalign y rotate r
        beat_card_warper 0.8 xalign -0.1 yalign 0.66
    parallel:
        pause 0.3
        'backcard' with Dissolve(0.1)
    parallel:
        pause 0.8
        alpha 0.0

define beat_card_atl_attack = [beat_card_atl(0.45, 0.14, -7), beat_card_atl(0.25, 0.14, -7), beat_card_atl(0.65, 0.14, -7),
beat_card_atl(0.45, 0.52, -7), beat_card_atl(0.25, 0.52, -7), beat_card_atl(0.65, 0.52, -7)]

define beat_card_atl_beat = [beat_card_atl(0.47, 0.18, 5), beat_card_atl(0.27, 0.18, 5), beat_card_atl(0.67, 0.18, 5),
beat_card_atl(0.47, 0.56, 5), beat_card_atl(0.27, 0.56, 5), beat_card_atl(0.67, 0.56, 5)]

transform take_cards_atl(x, y, r):
    zoom 1.2 xalign x yalign y rotate r
    easein_quad 0.8 xalign 0.45 yalign 1.5

define take_cards_atl_beat = [take_cards_atl(0.45, 0.14, -7), take_cards_atl(0.25, 0.14, -7), take_cards_atl(0.65, 0.14, -7),
take_cards_atl(0.45, 0.52, -7), take_cards_atl(0.25, 0.52, -7), take_cards_atl(0.65, 0.52, -7)]

define take_cards_atl_attack = [take_cards_atl(0.45, 0.14, -7), take_cards_atl(0.25, 0.14, -7), take_cards_atl(0.65, 0.14, -7),
take_cards_atl(0.45, 0.52, -7), take_cards_atl(0.25, 0.52, -7), take_cards_atl(0.65, 0.52, -7)]

transform discard_pile_atl(x, y, r):
    xalign x yalign y rotate r zoom 1.2 alpha 0.0
    pause 0.8
    alpha 1.0

transform issue_cards_player:
    xalign -0.1 yalign 0.17 rotate 200 zoom 1.2
    easein_quint 1.5 xalign 0.4 yalign 1.5 rotate 0

transform issue_last_cards_player:
    xalign -0.06 yalign 0.2 rotate 110 zoom 1.2
    easein_quint 1.5 xalign 0.4 yalign 1.5 rotate 0

transform issue_cards_npc:
    xalign -0.1 yalign 0.17 rotate 200 zoom 1.2
    easein_quint 1.5 xalign 0.4 yalign -0.5 rotate 0

transform issue_last_cards_npc:
    xalign -0.06 yalign 0.2 rotate 110 zoom 1.2
    easein_quint 1.5 xalign 0.4 yalign -0.5 rotate 0

transform dissolve_extra_:
    on show:
        alpha 0.0
        linear 0.1 alpha 1.0
    on hide:
        linear 0.1 alpha 0.0

transform text_plus_cards:
    parallel:
        alpha 0.0 
        linear 0.1 alpha 1.0
        pause 0.18
        linear 0.12 alpha 0.0
    parallel:
        yoffset 0
        linear 0.2 yoffset -8
        linear 0.2 yoffset -16


transform dissolve_fast_text_:
    alpha 0.0
    linear 0.05 alpha 1.0
    on hide:
        linear 0.05 alpha 0.0

transform ctm_atl:
    on show:
        alpha 0.0
        ease 0.3 alpha 1.0
    on hide:
        ease 0.1 alpha 0.0
        

transform dissolve_hide_:
    on hide:
        ease 0.3 alpha 0.0

transform phrase_chr_atl:
    parallel:
        xalign 1.0 yalign 0.1 zoom 1.5
        easein_circ 0.7 xalign 0.5 yalign 0.2 
    parallel:
        alpha 0.0
        pause 0.05 
        linear 0.4 alpha 1.0

transform phrase_window_atl:
    xalign 0 yalign 0.0 alpha 0.0 zoom 0.7 rotate -2
    easein_circ 0.7 xalign 0.5 yalign 0.1 alpha 1.0

transform black_bg_atl:
    alpha 0
    linear .3 alpha .5

transform player_card:
    on hover:
        easein 0.2 yoffset -50
    on idle:
        easein 0.2 yoffset 0

transform player_card_past:
    yoffset -100
    on hover:
        easein 0.2 yoffset -50
    on idle:
        easein 0.2 yoffset 0

transform player_card_select:
    yoffset -50
    easein 0.2 yoffset -100

transform player_cards:
    on hide:
        alpha 1.0
        linear 0.2 alpha 0

transform s_player_card_:
    on show:
        yoffset 300
        easein_cubic 1 yoffset 0

transform player_card_hide:
    yoffset -100
    ease 0.4 yoffset 300

transform noti_atl:
    on show:
        alpha 0.0
        ease 0.15 alpha 1.0
    on hide:
        alpha 1.0
        ease 0.15 alpha 0.0
        


################################################################################
## Styles
################################################################################


style choice_modal_button_text:
    color '#b7b7b7'
    hover_color '#fff'
    size text_size_

style choice_modal_text:
    color '#fff'
    size text_size_

style durak_phrase_st_window is empty

style durak_phrase_st_window:
    xpadding 30
    top_padding 25
    bottom_padding 25
    background Frame("phrase bubble", 55, 55, 55, 55)

style durak_phrase_st_text:
    color '#000'
    size 35


################################################################################
##### made by AllCodny
################################################################################
