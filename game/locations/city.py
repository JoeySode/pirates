
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import random

class City (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "city"
        self.symbol = 'C'
        self.visitable = True
        self.starting_location = CityDock(self)
        self.locations = {}
        self.locations["city dock"] = self.starting_location
        self.locations["city gate"] = CityGate(self)
        self.locations["city streets"] = CityStreets(self)
        self.locations["castle gate"] = CastleGate(self)
        self.locations["castle chest"] = CastleChest(self)

    def enter (self, ship):
        print ("arrived at a city")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class CityDock (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "city dock"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append (crabknights.CrabKnights())

    def enter (self):
        announce ("Arrive at the dock. Your ship is at anchor to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["city gate"]
        elif (verb == "east" or verb == "west"):
            announce ("There is nothing in that direction.")


class CityGate (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "city gate"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['guess'] = self

        self.event_chance = 100

        self.code = []
        for i in range(5):
            self.code.append(random.randint(2, 10))
        self.answer = self.get_answer()

        self.locked = True

    def enter (self):
      if self.locked:
        announce ("You approach the gate to the city")
        announce (f"It presents you with the following: {self.code}")
        announce ("It reads: The sum of all parts divided and rounded by the weakeset within...")
        announce ("There is a pad to enter numbers in. Use 'guess' to enter a guess")
      else:
        announce ("You approach the city's open gate.")

    def process_verb (self, verb, cmd_list, nouns):
      if verb == "south":
          config.the_player.next_loc = self.main_location.locations["city dock"]
      elif verb == "west" or verb == "east":
          announce ("There is nothing in that direction.")
      elif verb == "north":
          if self.locked:
              announce ("The gate is locked.")
          else:
              config.the_player.next_loc = self.main_location.locations["city streets"]
      else:
          guess = 0
          try:
              guess = int(input("What is your guess? "))
              if guess == self.answer:
                  announce ("Correct! The gate is unlocked!")
                  self.locked = False
              else:
                  announce ("Incorrect.")
          except:
            announce ("Invalid input")
            

    def get_answer(self):
        # The sum of all values divided by the smallest in the list
        return sum(self.code) // sorted(self.code)[0]

    
class CityStreets (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "city streets"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 100

        self.depth = 0

    def enter (self):
      announce ("You enter the city's vast streets. It may take multiple north trips to exit.")
      self.depth = 0

    def process_verb (self, verb, cmd_list, nouns):
      if verb == "south":
          config.the_player.next_loc = self.main_location.locations["city gate"]
      elif verb == "west" or verb == "east":
            announce ("You proceed in the streets")
      elif verb == "north":
          if self.should_pass():
            announce ("You have reached the end of the streets. A castle is ahead.")
            config.the_player.next_loc = self.main_location.locations["castle gate"]
          else:
            announce ("You proceed in the streets")
            self.depth += 2

    def should_pass(self):
        # True if the player should advance past the streets
        return random.randint(1, 9 - self.depth) == 1
    

class CastleGate (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "castle gate"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['guess'] = self

        self.event_chance = 100

        self.code = []
        self.answer = 0

        self.gen_puzzle()

        self.locked = True

    def enter (self):
      if self.locked:
        announce ("You approach the castle's gate. It reads:")
        announce (f"To enter the castle, you must give the next number in the squence {self.code}")
        announce ("There is a pad to enter numbers in. Use 'guess' to enter a guess")
      else:
        announce ("You approach the castle's open gate.")

    def process_verb (self, verb, cmd_list, nouns):
      if verb == "south": 
          config.the_player.next_loc = self.main_location.locations["city streets"]
      elif verb == "west" or verb == "east":
          announce ("There is nothing in that direction.")
      elif verb == "north":
          if self.locked:
              announce ("The gate is locked.")
          else:
              config.the_player.next_loc = self.main_location.locations["castle chest"]
      else:
          guess = 0
          try:
              guess = int(input("What is your guess? "))
              if guess == self.answer:
                  announce ("Correct! The gate is unlocked!")
                  self.locked = False
              else:
                  announce ("Incorrect.")
          except:
            announce ("Invalid input")

    def gen_puzzle(self):
        # A sequence with a starting value and a step value. The palyer must guess the next in the sequence
        num = random.randint(3, 5)

        start = random.randint(0, 50)
        step = random.randint(1, 20)

        for i in range(num):
            self.code.append(start + (step * i))
        
        self.answer = start + (step * num)


class CastleChest (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "castle chest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['open'] = self

        self.event_chance = 100

        self.opened = False

    def enter (self):
      if not self.opened:
          announce ("You approach a chest inside the castle. Use 'open' to take its treasure.")
      else:
          announce ("You approach the opened castle chest.")

    def process_verb (self, verb, cmd_list, nouns):
      if verb == "south": 
          config.the_player.next_loc = self.main_location.locations["castle gate"]
      elif verb == "west" or verb == "east" or verb == "north":
          announce ("There is nothing in that direction.")
      else:
          if self.opened:
              announce ("You already looted the chest.")
          else:
              announce ("You find and take a golden idol and a golden blade.")
              config.the_player.inventory.append(items.GoldenBlade())
              config.the_player.inventory.append(items.GoldenIdol())
              self.opened = True