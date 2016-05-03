# Cartiernan-Bot
A custom bot I wrote for my final project in COMPSCI 383: Artificial Intellegence. It is based off the python3 starter bot provided by rbtcs on [ The AI Games Website](http://theaigames.com/competitions/ai-block-battle/getting-started).


This is a hueristic based agent that makes classifications based off all possible board configuration two Trominoes in advance. Feature weights are learned via a genetic algorithm.

---

### Running The Bot
1. Download the server code from [The AI Games Github page](https://github.com/theaigames/blockbattle-engine)
2. Download my [bot's source code](https://github.com/CDTiernan/Block-Bot)
3. Move the bash script run, found in Extras/, to the root directory of the server code downloaded in 1
4. Edit the bash script run, changing the <PATH> to the full path of BotRun.py, found in the root directory of my bot's source code downloaded in 2
5. Exectute the run command. Game data will be printed to a file named out.txt in the root folder of the server code

### Generating New Feature Weights With Botvelution
1.  Move the Botvelution, found in Extras/, to the root directory of the server code
2.  Call the class using python3
3.  Data will be displayed printed on generation data and performance. Additionally, the top 5 couples and their features will be [pickled](https://wiki.python.org/moin/UsingPickle) every generation. 

----

### Strategy Descriptions
##### 1. CTStrategy
CTStrategy looks one Tromino in advance to make decisions. Features and weights are derived from [Yiyuan Lee's Near Perfect Tetris AI](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/).
##### 2. CTStrategyTwoBlock
CTStrategyTwoBlock looks two Trominoes in advance to make decisions. Features are similar but modified from Yiyuan Lee's, and weights are learned using a genetic algorithm.

CTStrategyTwoBlock also takes advantage of more optimized piece projection and can recognize covered positions and other Tromino positions that cannot be dropped into. This is done using TetrisGraph, which is a best first search algorihtm that finds valid moves for Trominos.
