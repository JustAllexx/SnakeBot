import discord
from random import randint
from discord.ext import commands
import asyncio
import time

class INFO():
    def __init__(self):

        self.playerlist = {}
        self.serverlist = []
        self.highscores = eval(open('highscores.txt').read())
        self.savedgames = eval(open('savedgames.txt').read())
        self.version = '**1.2.6**'

        self.HELP = discord.Embed(title="Snake Game Help", color=0x32cd32)
        self.HELP.add_field(name="Start A Game", value="""To start a game of snake, use the command **s/start** or alternatively **s/snake**, you will be presented with a `10 by 10` grid that looks like this

        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛\U0001f34e⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

        ⬜ is the player character, he can be controlled by the player. You need to direct this white square to the apple to increase your score

        \U0001f34e is an apple and the primary way of increasing your score, touch the apple with your player character and the score will increment by one and a new apple will be placed on the grid
        """)
        self.HELP.add_field(name="How do I control the Character?", value="""Before the Game begins the directional emojis are added as reactions

        ⬅ **LEFT**
        ⬆ **UP**
        ⬇ **DOWN**
        ➡ **RIGHT**

        Click on the emoji that corresponds to the direction you want to move
        `Note; Unless on 1 score, moving opposite to the direction you are facing results in an immediate failure`
        """)
        self.HELP.add_field(name="How Is the Game Played", value="""The Aim of the game is to get the highest number of points possible by collecting as many apples as you can without Dying, the challenge increases as the more apples you collect the longer your tail becomes and the likelihood of you running into it increases

        The Ways Of Dying Are As Follows;
        **Running Into A Wall**

        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛\U0001f34e⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        `You were killed with a score of 4`
        Running into any one of the 4 walls of the grid is a Game Over

        **Running Into Yourself**

        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛\U0001f34e⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬜⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬜⬜⬜⬛
        ⬛⬛⬛⬛⬛⬛⬜⬛⬜⬛
        ⬛⬛⬛⬛⬛⬛⬜⬜⬜⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
        `You were killed with a score of 9`
        Running into yourself is a Over
        """)

        self.PAUSED ="""
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬜⬜⬛⬛⬛⬛⬜⬜⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
"""
        self.HELP.add_field(name="How do I pause the game?", value="""
You can use the command s/pause to pause the game, the game will freeze for 60 seconds or until you use the command s/unpause.
The game screen will become a pause sign such as this;

{}

Once you unpause the game or 60 seconds have passed the game will continue as normal with a grace period of 3 seconds after you've unpaused.
`NOTE; You can only pause the game once and the game will continue without you if left for more than 60 seconds`
""".format(self.PAUSED))
        self.HELP.add_field(name="Loop Mode", value = """
Loop mode is activated when a user uses the command 's/start loop', this mode means that the game is no longer ended by running into walls.
Instead, the player character will pop out the other end such as below

⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛
⬛⬛\U0001f34e⬛⬛⬛⬛⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛
⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜
⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛



`Note; because of the unfair advantage given to users who use this gamemode, highscores will not be saved in this gamemode; aswell as, this gamemode is compatible with the 's/save' and 's/pause' features, however the gamemode cannot be turned off until the game is finished`
""")
        self.HELP.add_field(name="Why Is the Game so *Slow*?", value="To conform with Discords API policy, the game is limited to changing the game once every second, aswell as if the game is being used a lot at once that can put pressure on the game and it can slow down")
        self.HELP.add_field(name="Who Is the Creator? and what is the Version", value="Use the command **s/creator** for my @player, and you can find the version by doing **s/version** or **s/v**")
        self.HELP.add_field(name="How do I quit the game?", value="The command 's/quit' allows you to leave a game at any time `Note; Your score will not be saved and the original message will not be deleted`")
        self.HELP.add_field(name="How do I get my highscore?", value="You can use the command s/highscore to retrieve the your highscore")
        self.HELP.add_field(name="Can I save my game and continue it later?", value="Yes, by using the command 's/save' your game can be continued at any time by using the command s/start and you will begin exactly where you left off going in the same direction. `Note; Your game can be continued in any guild after you've saved it")
        self.HELP.set_footer(text="Use s/invite or s/inv to get the link to invite Snake to your server")

info = INFO()
