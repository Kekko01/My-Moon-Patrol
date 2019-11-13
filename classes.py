#!/usr/bin/env python3
'''
@author  Francesco Ciociola - https://kekko01.altervista.org/blog/
@from Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

from random import choice, randrange
from actor import Actor, Arena


class Rover(Actor):
    def __init__(self, arena, pos, player):
        self._x, self._y = pos
        self._w, self._h = 31, 23
        self._player = player
        self._speed = 10
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._gravity=0.6
        self._plane=55
        arena.add(self)

    def move(self):
        ARENA_W, ARENA_H = self._arena.size()
        self._ARENA_H=ARENA_H
        self._dy+=self._gravity
        self._y += self._dy
        self._x += self._dx
        if self._y < 0:
            self._y = 0
        elif self._y > ARENA_H - self._h-self._plane:
            self._y = ARENA_H - self._h-self._plane

#        self._x += self._dx
#        if self._x < 0:
#            self._x = 0
#        elif self._x > ARENA_W - self._w:
#            self._x = ARENA_W - self._w

    def go_left(self):
        if self._x>0:
            self._dx-=3

    def go_right(self):
        if self._x+self._w<480:
            self._dx+=3

    def go_up(self):
        if self._y + self._h >= self._ARENA_H - self._plane - 5:
            self._dx, self._dy = 0, -self._speed

    def go_down(self):
        self._dx, self._dy = 0, +self._speed

    def stay(self):
        self._dx, self._dy = 0, 0

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._player == 1:
            if self._y + self._h <= self._ARENA_H - self._plane and self._dy < 0:
                return 49, 150, self._w, self._h
            elif self._y + self._h <= self._ARENA_H - self._plane and self._dy > 0 and self._y + self._h != self._ARENA_H - self._plane:
                return 82 , 153 , self._w, self._h
            return 249, 158, self._w, self._h
        elif self._player == 2:
            if self._y + self._h <= self._ARENA_H - self._plane and self._dy < 0:
                return 47, 103, self._w, self._h
            elif self._y + self._h <= self._ARENA_H - self._plane and self._dy > 0 and self._y + self._h != self._ARENA_H - self._plane:
                return 80 , 104 , self._w, self._h
            return 212, 158, self._w, self._h

    def drop(self):
        if self._y<self._ARENA_H:
            self._dy+=self._gravity/2
            self._y += self._dy

    def drop_symbol(self):
        return 167,100,41,34

    def x_position(self):
        return self._x+self._w

    def y_position(self):
        return self._y+self._h/2

class Background:
    """docstring for Background."""

    def __init__(self, pos, speed, image, dimensions):
        self._image_x,self._image_y=image
        self._startpoint=pos[0]
        self._x, self._y = pos
        self._w, self._h = dimensions
        self._speed = speed
        self._dx = self._speed

    def move(self):
        if self._x+self._w<=self._startpoint:
            self._x=self._startpoint
        self._x -= self._dx

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self, other):
        pass

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

class Hole(Arena):
    """docstring for Hole."""

    def __init__(self, arena, image, pos):
        self._x,self._y=480,300
        self._w,self._h=22,27
        self._image_x,self._image_y=image
        self._speed = 6
        self._dx = self._speed
        arena.add(self)

    def move(self):
        self._x -= self._dx

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self,other):
        x,y,w,h=other.position()
        if x + w > self._x and y + h > self._y and x < self._x + self._w:
            return True
        else:
            return False

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x+self._w

class Hill(Arena):
    """docstring for Hill."""

    def __init__(self, arena, image, dimension, life):
        self._w,self._h=dimension
        self._x,self._y=480,305-self._h
        self._image_x,self._image_y=image
        self._speed = 6
        self._dx = self._speed
        self._life=life
        arena.add(self)

    def move(self):
        self._x -= self._dx

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self,other):
        x,y,w,h=other.position()
        if isinstance(other,Rover):
            if y + h >= self._y and self._x <= x + w and x< self._x + self._w:
                return True
            else:
                return False
        elif isinstance(other,Bullet):
            if x + w >= self._x and y >= self._y :
                return True
            else:
                return False

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x+self._w

    def get_life(self):
        return self._life

    def take_life(self):
        self._life-=1

class Alien(Arena):
    """docstring for Hole."""

    def __init__(self, arena):
        self._x,self._y=480,100
        self._w,self._h=17,10
        self._image_x,self._image_y=67,229
        self._speed = 3
        self._dx = self._speed
        arena.add(self)

    def move(self):
        self._dy = choice((-1,-0.5,0,0.5,1))
        self._y += self._dy
        self._x -= self._dx

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self,other):
        x,y,w,h=other.position()
        if isinstance(other,Bullet):
            if y + h <= self._y and self._x <= x <= self._x + self._w:
                return True
            else:
                return False

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x+self._w

    def y_position(self):
        return self._y+self._h

    def delete(self):
        self._x=-1000


class AlienBullet(Arena):
    """docstring for AlienBullet."""

    def __init__(self, arena, pos):
        self._x,self._y=pos
        self._x-=3
        self._speed=5
        self._w,self._h=5,6
        self._image_x,self._image_y=213,231
        arena.add(self)

    def move(self):
        self._y+=self._speed

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self,other):
        x,y,w,h=other.position()
        if isinstance(other,Rover):
            if x<=self._x<=x+w and self._y+self._h>=y:
                return True
            else:
                return False

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x

    def y_position(self):
        return self._y

class Bullet(Arena):
    """docstring for Bullet."""

    def __init__(self, arena, x, y, dir):
        self._x,self._y=x,y
        self._w,self._h=8,8
        self._image_x,self._image_y=269,142
        self._speed = 8
        if dir==0:
            self._dx = self._speed
            self._dy = 0
        elif dir==1:
            self._dy = self._speed
            self._dx = 0
        arena.add(self)

    def collide(self, other):
        pass
#        x,y,w,h=other.position()
#        if self._x + self._w >= x and self._y >= y :
#            return True
#        else:
#            return False

    def move(self):
        self._x += self._dx
        self._y -= self._dy

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x + self._w

    def y_position(self):
        return self._y + self._h

class Robot(Arena):
    """docstring for Hole."""

    def __init__(self, arena):
        self._x,self._y=480,290
        self._w,self._h=16,16
        self._image_x,self._image_y=109,246
        self._speed = 4
        self._dx = self._speed
        arena.add(self)

    def move(self):
        self._x -= self._dx

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self,other):
        x,y,w,h=other.position()
        if isinstance(other,Bullet):
            if self._y + self._h >= y >= self._y and self._x <= x + w <= self._x + self._w:
                return True
        elif isinstance(other,Rover):
            if self._y < y + h and self._x <= x + w <= self._x + self._w:
                return True
        return False

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x+self._w

    def y_position(self):
        return self._y+self._h

    def delete(self):
        self._x=-100

class RobotBullet(Arena):
    """docstring for AlienBullet."""

    def __init__(self, arena, pos):
        self._x,self._y=pos
        self._y-=15
        self._x-=15
        self._speed=7
        self._w,self._h=4,1
        self._image_x,self._image_y=94,248
        arena.add(self)

    def move(self):
        self._x-=self._speed

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self,other):
        x,y,w,h=other.position()
        if isinstance(other,Rover):
            if x<=self._x<=x+w and y+h>=self._y:
                return True
            else:
                return False

    def symbol(self):
        return self._image_x, self._image_y, self._w, self._h

    def x_position(self):
        return self._x

    def y_position(self):
        return self._y

##class BounceGame:
##    def __init__(self):
##        self._arena = Arena(320, 240)
##        Ball(self._arena, 40, 80)
##        Ball(self._arena, 80, 40)
##        Ghost(self._arena, 120, 80)
##        self._hero = Turtle(self._arena, 80, 80)
##
##    def arena(self) -> Arena:
##        return self._arena
##
##    def hero(self) -> Turtle:
##        return self._hero


def print_arena(arena):
    pass
#    for a in arena.actors():
#        print(type(a).__name__, '@', a.position())
