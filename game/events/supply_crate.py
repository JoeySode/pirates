
from game import event
import random
import game.config as config

class SupplyCrate (event.Event):
    '''This event picks one pirate to have a lucky day, setting their "lucky" bool to True. By itself this has no effect, but a variety of things check lucky.'''
    def __init__ (self):
        self.name = " found a supply crate"

    def process (self, world):
        num_food = random.randrange(5, 10)
        msg = f"{num_food} food was found in a stray supply crate"

        config.the_player.ship.take_food(-num_food)

        result = {}
        result["message"] = msg
        result["newevents"] = [ self ]
        return result
