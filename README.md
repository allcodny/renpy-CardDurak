# Card Durak for Ren'Py
[![eng](https://img.shields.io/badge/lang-en-en)](https://github.com/allcodny/renpy-CardDurak/blob/master/README.md)
[![rus](https://img.shields.io/badge/lang-ru-ru?color=DCDCDC)](https://github.com/allcodny/renpy-CardDurak/blob/master/README-ru.md)

![gif](https://github.com/user-attachments/assets/97af9c01-c0fe-47d1-b55c-3df574f8f7e3)

## About
"Durak" is a classic Russian card game, a throw-in and translation version for Ren'Py games.

The `ruls.rpy` file describes the rules of the game.

The main feature of this code compared to the rest is the character's interactivity during the game: an image is displayed, emotions change, phrases are pronounced with some chance. However, if necessary, all this can be disabled in the `settings.rpy` file. Also, with the help of this file, you can easily change various settings (phrases, texts, character behavior, who goes first, etc.).

After the game is over, the `who_win_` variable is returned with a value of 0 (the opponent won), 1 (draw) or 2 (the player won)

## How to use
To use the card "Durak" in your game, place the `durak` folder in the `game` directory of your Ren'Py game, and copy all the files from `images` to the corresponding folder of your project.

You can customize the game to your needs using the `settings.rpy` file. Each setting has detailed comments.

To call the game, use `call durak_game`:
```
    e "Let's play the card durak!"

    call durak_game

    # here are the actions after the game, we need to show the background and sprites again
    scene room
    show eileen

    if who_win_ == 0:
        # opponent wins
        e "Hehe, I win~"
    elif who_win_ == 1:
        # draw
        e "We have a draw!"
    else:
        # player wins
        e "Wow, you won! Congratulations!"

    e "And here is the general continuation of the plot."
```

## Possible problems
A known possible problem: a conflict of variables from the game with variables of your project. Although the variables are named more specifically, it is impossible to protect yourself from this completely. In case of such conflicts, you just need to rename either your variables or variables in the durak files (`durak\durak.rpy`, `durak\screens.rpy`, `durak\settings.rpy`).

## About the code itself
Initially, the game was planned to add the ability to cheat on the player's side and on the opponent's side. In the end, I abandoned this idea, but its beginnings are visible in the code and because of this, the code may seem strange in places. In general, I can't say that the code is 100% done correctly, but it works good (including on mobile devices) and that's the main thing.

The comments in the code may be a little crooked, as I don't know English very well, but it's still clear.
