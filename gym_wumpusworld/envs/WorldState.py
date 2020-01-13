import random as r
from enum import Enum

class Location:

    def __init__(self,x,y):
        self.x = x
        self.y = y


class Perception:

    def __init__(self):
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False


class Direction(Enum):
    NORTH =0
    EAST =1
    SOUTH = 2
    WEST =3


class Action:
    WALK = 0
    TURNLEFT = 1
    TURNRIGHT = 2
    GRAB = 3
    SHOOT = 4
    CLIMB = 5


class World_State:

    def __init__(self):
        self.world_size = 4
        self.pit_prob = 0.2
        # x , y 
        self.agent_location = Location(0,0)
        self.agent_direction = Direction.EAST
        self.wumpus_location = self.init_wumpus_location()
        self.pit_locations = self.init_pit_locations()
        self.gold_location = self.init_gold_location()
        self.agent_alive = True
        self.has_arrow = True
        self.has_gold = False
        self.in_cave = True
        self.wumpus_alive = True


    def reset(self):
        self.agent_location = Location(0,0)
        self.agent_direction = Direction.EAST
        self.agent_alive = True
        self.has_arrow = True
        self.has_gold = False
        self.in_cave = True
        self.wumpus_alive = True




    def init_wumpus_location(self,x=0,y=0):
        while x == y == 0:
            x ,y = r.randint(0,self.world_size-1), r.randint(0,self.world_size-1)
        return Location(x,y)


    def init_pit_locations(self):
        pits = []
        for x in range(0,self.world_size):
            for y in range(0,self.world_size):
                if x != 0 or y != 0:
                    if r.random() < self.pit_prob:
                        pits.append(Location(x,y))
        return pits

    def init_gold_location(self,x=0,y=0):
        while True:
            if next((False for e in self.pit_locations if e.x == x and e.y == y),True):
                if x !=0 and y != 0:
                    return Location(x,y)
            x ,y = r.randint(0,self.world_size - 1), r.randint(0,self.world_size - 1)


