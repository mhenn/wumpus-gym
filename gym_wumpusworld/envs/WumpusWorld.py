import random as r
import numpy
from gym_wumpusworld.envs.WorldState import *

class Wumpus_World:

    def __init__(self, size):
        self.score = 0
        self.old_score = 0
        self.random_prob = 0.2
        self.state = World_State()
        self.percept = Perception()
        self.update_perception()
    

    def reset(self):
        self.score = 0
        self.old_score = 0
        self.state.reset()
        self.percept = Perception()
        self.update_perception()


    def adjacent(self, l1,l2):
        x1, y1 = l1.x, l1.y
        x2, y2 = l2.x, l2.y

        if x1 == x2 -1 and y1 == y2:
            return True
        elif x1 == x2 +1 and y1 == y2:
            return True
        elif y1 == y2 -1 and x1 == x2:
            return True
        elif y1 == y2 +1 and x1 == x2:
            return True
        return False

    def on_field(self, l1, l2):
        if l1.x == l2.x and l1.y == l2.y:
            return True
        return False


    def get_observation(self):
        obs = {}
        obs['x'] = self.state.agent_location.x 
        obs['y'] = self.state.agent_location.y
        obs['gold'] = self.state.has_gold
        obs['direction'] = self.state.agent_direction
        obs['arrow'] = self.state.has_arrow
        obs['stench'] = self.percept.stench
        obs['breeze'] = self.percept.breeze
        obs['glitter'] = self.percept.glitter
        obs['bump'] = self.percept.bump
        obs['scream'] = self.percept.scream
        return obs

    def get_reward(self):
        r = numpy.diff([self.old_score, self.score])
        return r


    def exec_action(self, action):
         
        self.old_score = self.score
        a_l = self.state.agent_location
        self.score -= 1
        if action < 3:
            self.move(action)
        
        self.update_perception()

        if self.state.wumpus_alive:
            if self.on_field(a_l, self.state.wumpus_location):
                self.state.agent_alive = False
                self.score -= 999
                return False

        if next((True for p_l in self.state.pit_locations if self.on_field(a_l,p_l)),False):
            self.state.agent_alive = False
            self.score -= 999
            return False
        
        if  action == Action.GRAB:
            if not self.state.has_gold and self.on_field(a_l, self.state.gold_location):
                self.state.has_gold = True
        
        if action == Action.SHOOT:
            if self.state.has_arrow:
                self.state.has_arrow = False
                self.shoot()
                self.score -= 9

        if action == Action.CLIMB:
            if self.state.has_gold:
                if self.on_field(a_l, Location(0,0)):
                    self.state.in_cave = False
                    self.score += 1001
                    return False

        return True

    
    def __kill_wumpus(self):
        self.state.wumpus_alive = False
        self.percept.scream = True

    def shoot(self):
        a_d = self.state.agent_direction
        a_l, w_l = self.state.agent_location, self.state.wumpus_location 
        if a_d == Direction.WEST:
            if a_l.x < w_l.x and a_l.y == w_l.y:
                self.__kill_wumpus()
        elif a_d == Direction.SOUTH:
            if a_l.x == w_l.x and a_l.y > w_l.y:
                self.__kill_wumpus()
        elif a_d == Direction.EAST:
            if a_l.x > w_l.x and a_l.y == w_l.y:
                self.__kill_wumpus()
        elif a_d == Direction.NORTH:
            if a_l.x == w_l.x and a_l.y < w_l.y:
                self.__kill_wumpus()
        

    def move(self,action):
        if action == Action.WALK:
            rand = r.random()
            if rand < self.random_prob:
                if rand < self.random_prob / 2:
                    self.turn(Action.TURNLEFT)
                else:
                    self.turn(Action.TURNRIGHT)
            self.go_forward()
        else:
            self.turn(action)

    def turn(self, action):
        if action == Action.TURNLEFT:
            self.state.agent_direction = Direction((self.state.agent_direction.value -1) % len(Direction))
        elif action == Action.TURNRIGHT:
            self.state.agent_direction = Direction((self.state.agent_direction.value +1) % len(Direction))
            

    def go_forward(self):
        a_l = self.state.agent_location
        a_d = self.state.agent_direction
        w_s = self.state.world_size
        self.percept.bump = True
        if a_d == Direction.WEST:
            if a_l.x > 0:
                self.state.agent_location.x -= 1
                self.percept.bump = False
        elif a_d == Direction.SOUTH:
            if a_l.y > 0:
                self.state.agent_location.y -= 1
                self.percept.bump = False
        elif a_d == Direction.EAST:
            if a_l.x < w_s -1:
                self.state.agent_location.x += 1
                self.percept.bump = False
        elif a_d == Direction.NORTH:
            if a_l.y < w_s -1:
                self.state.agent_location.y += 1
                self.percept.bump = False


    def update_perception(self):

        self.percept.glitter = False
        self.percept.stench = False
        self.percept.breeze = False
        a_l = self.state.agent_location

        if self.on_field(a_l, self.state.gold_location):
            if not self.state.has_gold:
                self.percept.glitter = True
        if self.adjacent(a_l, self.state.wumpus_location):
            self.percept.stench = True 
        if next((True for p_l in self.state.pit_locations if self.adjacent(a_l,p_l)),False):
            self.percept.breeze = True

    def print(self):
        size = self.state.world_size
        d = self.state.agent_direction
        print('+', end = '')
        for i in range(size):
            print('---+', end ='')
        print()
        for y in range(size-1,-1,-1):
            print('|', end='')
            for x in range(size):
                if self.on_field(self.state.wumpus_location, Location(x,y)):
                    if self.state.wumpus_alive:
                        print('W', end ='')
                    else:
                        print('X', end= '')
                else:
                    print(' ', end='')
                if next((True for p_l in self.state.pit_locations if self.on_field(Location(x,y),p_l)),False):
                    print('P', end='')
                else:
                    print(' ', end='')
                if not self.state.has_gold and self.on_field(Location(x,y), self.state.gold_location):
                    print('G', end ='')
                else:
                    print(' ', end='')
                print('|', end='')
            print()
            print('|', end='')

            for x in range(size):
                if self.on_field(Location(x,y),self.state.agent_location):
                    if d == Direction.WEST:
                        print(' A<|',end='')
                    elif d == Direction.SOUTH:
                        print(' Av|',end='')
                    elif d == Direction.EAST:
                        print(' A>|',end='')
                    elif d == Direction.NORTH:
                        print(' A^|',end='')
                else:
                    print('   |',end='')
            
            print()
            print('+',end='')
            for x in range(size):
                print('---+',end='')
            print()

        print('Perception [ St: {}, Br: {}, '.format(self.percept.stench,self.percept.breeze),end='')
        print('G: {}, Bu: {}, Sc: {} ]'.format(self.percept.glitter,self.percept.bump, self.percept.scream))
        print('Score : {}'.format(self.score))







        


