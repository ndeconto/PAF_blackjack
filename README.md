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

To see what the AI decisions look like, you can check out the excel sheets in the results folders (obtained with openpyxl)

To play against the computer, 
