# An AI playing BlackJack

This project has been created by 5 first-year students at Télécom Paristech in 14 days.
We applied the reinforcement learning technique to BlackJack, and more particularly to a symetric version of BlackJack we created to let people try to beat the AI in a balanced game.


## Principle

The AI relies on a system of rewards : although it does not know any rule of the game initially, the AI will gradually improve its decision-making because the matrix of decisions is updated at every end of game.

This matrix has 4 dimensions : Category of hand (see below), Oponent state (the first card of the oponent), Player state (the current hand of the AI) and decision's rating (the index of the highest number gives the best decision).


### Why several categories of hand ?

An as has a special behavior : it can either count as 1 or 11. So we have to consider it as a random variable, and place a hand containing an as (Soft hand) in a different matrix.

A pair allows an extra move : splitting your hand into two hands. We need to add another matrix for this.

Here are the possible values for each category :

Normal | Soft Hand | Pair 
------------------ | ----------------- | --------
`<9` | `A+2` | `A+A` 
`9` | `A+3` | `2+2` 
`10` | `A+4` | `3+3` 
`11` | `A+5` | `4+4` 
`12` | `A+6` | `5+5` 
`13` | `A+7` | `6+6` 
`14` | `A+8` | `7+7` 
`15` | `A+9` | `8+8` 
`16` | `A+10` | `9+9`
`17` |  | `10+10`
`18` |  | 
`19` |  | 
`20` |  |  
`21` |  | 
`>21` |  | 



### Guaranteeing an efficient learning

We have to introduce a bit of random during the learning phase to make sure the matrix eventually converges and every possible state has been explored. The probability of making a random decision is given by a parameter (epsilon) , which has to decrease over time.

We also have to decide how much the result of a game should impact the learning, using another parameter (alpha). The higher alpha is, the greater the impact of the last game becomes. We have also chosen a decreasing alpha, but slower than epsilon.


## Usage

# Learning 

To see what the AI decisions look like, you can check out the excel sheets in the results folders (obtained with openpyxl)


# lauch the main program and play
To launch the main program, open a terminal in the directory GUI and simply write something like
'''
$ python27 GUI_main.py
'''

Make sure you have [python27](https://www.python.org/downloads/) installed on your computer, with the [pygame library](http://pygame.org/download.shtml). 


There are three different modes in this program :
1. **IA against dealer** : in this mode, you are just a spectator, who watchs the Artificial Intelligence playing against a classic dealer
2. **classic game** :  in this mode, you play blackjack against the dealer, like in a casino. Our AI is not used.
3. **symetric game** : in this mode, you play against our AI. Therefore, the rules of blackjack were a little bit modified (see below). Note that this mode needs two different window (on two different screens if possible). Thus, if you want to play a symetric game, you have to launch GUI_main.py **and** GUI_client.py. You will play on the first window, while spectators can see on the other window what the AI is playing. The game ends when both you and the AI are finished.

When a game is finished, you can play again in the same mode by clicking on the button NEXT GAME in the center of the screen. If you want to play in an other mode, press _escape_

## Special rules for a symetric game

Sorry, it is not yet explained...


