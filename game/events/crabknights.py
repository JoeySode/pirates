import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class CrabKnights (event.Event):
    '''
    A combat encounter with a crew of drowned pirate zombies.
    When the event is drawn, creates a combat encounter with 2 to 6 drowned pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " crab knights stand guard"

    def process (self, world):
        '''Process the event. Populates a combat with Drowned monsters. The first Drowned may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the crab knights are defeated!"
        monsters = []
        min = 2
        uplim = 3
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(combat.CrabKnight("Crab knight "+str(n)))
            n += 1
        announce ("A group of crab knights stand guard!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
