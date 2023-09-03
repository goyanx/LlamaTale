import pathlib
import sys
from typing import Optional, Generator

import tale
from tale.base import Location
from tale.driver import Driver
from tale.llm_ext import DynamicStory
from tale.main import run_from_cmdline
from tale.player import Player, PlayerConnection
from tale.charbuilder import PlayerNaming
from tale.story import *

class Story(DynamicStory):

    config = StoryConfig()
    config.name = "The Prancing Llama"
    config.author = "Rickard Edén, neph1@github.com"
    config.author_address = "rickard@mindemia.com"
    config.version = tale.__version__
    config.supported_modes = {GameMode.IF, GameMode.MUD}
    config.player_money = 10.5
    config.playable_races = {"human"}
    config.money_type = MoneyType.FANTASY
    config.server_tick_method = TickMethod.TIMER
    config.server_tick_time = 0.5
    config.gametime_to_realtime = 5
    config.display_gametime = True
    config.startlocation_player = "prancingllama.entrance"
    config.startlocation_wizard = "prancingllama.entrance"
    config.zones = ["prancingllama"]
    config.context = "The Prancing Llama is the final outpost high up in a cold, craggy mountain range. It's frequented by adventurers and those looking to avoid attention."
    config.type = "A low level fantasy adventure with focus of character building and interaction."
    
    
    def init(self, driver: Driver) -> None:
        """Called by the game driver when it is done with its initial initialization."""
        self.driver = driver
        self._dynamic_locations = dict() # type: dict(str, [])
        self._dynamic_locations["prancingllama"] = []

    def init_player(self, player: Player) -> None:
        """
        Called by the game driver when it has created the player object (after successful login).
        You can set the hint texts on the player object, or change the state object, etc.
        """
        pass

    def create_account_dialog(self, playerconnection: PlayerConnection, playernaming: PlayerNaming) -> Generator:
        """
        Override to add extra dialog options to the character creation process.
        Because there's no actual player yet, you receive PlayerConnection and PlayerNaming arguments.
        Write stuff to the user via playerconnection.output(...)
        Ask questions using the yield "input", "question?"  mechanism.
        Return True to declare all is well, and False to abort the player creation process.
        """
        age = yield "input", "Custom creation question: What is your age?"
        playernaming.story_data["age"] = int(age)    # will be stored in the database (mud)
        occupation = yield "input", "Custom creation question: What is your trade?"
        playernaming.story_data["occupation"] = str(occupation)    # will be stored in the database (mud)
        return True

    def welcome(self, player: Player) -> str:
        """welcome text when player enters a new game"""
        player.tell("<bright>Hello, %s! Welcome to %s.</>" % (player.title, self.config.name), end=True)
        player.tell("\n")
        player.tell(self.driver.resources["messages/welcome.txt"].text)
        player.tell("\n")
        return ""

    def welcome_savegame(self, player: Player) -> str:
        """welcome text when player enters the game after loading a saved game"""
        player.tell("<bright>Hello %s, welcome back to %s.</>" % (player.title, self.config.name), end=True)
        player.tell("\n")
        player.tell(self.driver.resources["messages/welcome.txt"].text)
        player.tell("\n")
        return ""

    def goodbye(self, player: Player) -> None:
        """goodbye text when player quits the game"""
        player.tell("Goodbye, %s. Please come back again soon." % player.title)
        player.tell("\n")

    def add_location(self, location: Location, zone: str = '') -> None:
        self._dynamic_locations["prancingllama"].append(location)

    def races_for_zone(self, zone: str) -> [str]:
        return ["human", "giant rat", "bat", "balrog", "dwarf", "elf", "gnome", "halfling", "hobbit", "kobold", "orc", "troll", "vampire", "werewolf", "zombie"]

    def items_for_zone(self, zone: str) -> [str]:
        return ["woolly gloves", "ice pick", "fur cap", "rusty sword", "lantern", "food rations"]

    def zone_info(self, zone_name: str, location: str) -> dict():
        return {"description": "A cold, craggy mountain range. Snow covered peaks and uncharted valleys hide and attract all manners of creatures.", 
                "races": self.races_for_zone(''), 
                "drop_items": self.items_for_zone('')}

if __name__ == "__main__":
    # story is invoked as a script, start it in the Tale Driver.
    gamedir = pathlib.Path(__file__).parent
    if gamedir.is_dir() or gamedir.is_file():
        cmdline_args = sys.argv[1:]
        cmdline_args.insert(0, "--game")
        cmdline_args.insert(1, str(gamedir))
        run_from_cmdline(cmdline_args)
