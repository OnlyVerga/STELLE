import pygame
import math
from copy import deepcopy

G = 0.0000000000667
normalization = 1
deltaT = 0.1

class Vector:
    def __init__(self, x: float, y: float, z: float = 0):
        self.mat = [x, y, z]
        self.mag = math.sqrt(pow(self.mat[0], 2) + pow(self.mat[1], 2) + pow(self.mat[2], 2))

    def __add__(self, other):
        return Vector(self.mat[0] + other.mat[0], self.mat[1] + other.mat[1], self.mat[2] + other.mat[2])

    def __sub__(self, other):
        return Vector(self.mat[0] - other.mat[0], self.mat[1] - other.mat[1], self.mat[2] - other.mat[2])

    def __mul__(self, other: int):
        return Vector(self.mat[0] * other, self.mat[1] * other, self.mat[2] * other)

    def __repr__(self):
        return f"[{self.mat[0]},\n{self.mat[1]},\n{self.mat[2]}]"

    def dotprod(self, other):
        return self.mat[0] * other.mat[0] + self.mat[1] * other.mat[1] + self.mat[2] * other.mat[2]

    def crossprod(self, other):
        return Vector(self.mat[1] * other.mat[2] - self.mat[2] * other.mat[1],
                      self.mat[2] * other.mat[0] - self.mat[0] * other.mat[2],
                      self.mat[0] * other.mat[2] - self.mat[2] * other.mat[0])

    def normalize(self):
        return Vector(self.mat[0] / self.mag,
                      self.mat[1] / self.mag,
                      self.mat[2] / self.mag)


class Obj:
    def __init__(self, pos: Vector, vel: Vector, mass: int = 0, length: int = 600):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.acc = Vector(0, 0, 0)
        self.traj = [self.pos]
        self.length = length

    def draw(self, window, img):
        for i in self.traj:
            i *= (1 / normalization)
            pygame.draw.circle(window, (255, 255, 255), i.mat[0:2], 1)
        img = pygame.transform.scale(img, (30, 30))
        window.blit(img, (self.pos.mat[0] / normalization - 15, self.pos.mat[1] / normalization - 15))

    def dist(self, other):
        return math.sqrt(pow((self.pos.mat[0] - other.pos.mat[0]), 2) + pow((self.pos.mat[1] - other.pos.mat[1]), 2) +
                         pow((self.pos.mat[2] - other.pos.mat[2]), 2))

    def update(self, other):
        self.acc = Vector(0, 0, 0)
        acc = -G * other.mass / pow(self.dist(other), 2)
        try:
            accx = acc * abs(self.pos.mat[0] - other.pos.mat[0]) / self.dist(other)
        except ZeroDivisionError:
            accx = 0
        try:
            accy = acc * abs(self.pos.mat[1] - other.pos.mat[1]) / self.dist(other)
        except ZeroDivisionError:
            accy = 0
        if self.pos.mat[0] - other.pos.mat[0] < 0:
            accx = -accx
        if self.pos.mat[1] - other.pos.mat[1] < 0:
            accy = -accy
        self.acc = Vector(accx, accy, 0)
        self.vel += self.acc
        self.pos += self.vel * deltaT
        self.traj.append(self.pos)
        if len(self.traj) >= self.length:
            self.traj.pop(0)


def show_text(Text, X, Y, wl, Font, surface, scaling=1, overflow='normal', Spacing=1):
    Text += ' '
    OriginalX = X
    OriginalY = Y
    X = 0
    Y = 0
    CurrentWord = ''
    WidthLimit = wl / scaling + OriginalX
    if overflow == 'normal':
        for char in Text:
            if char not in [' ', '\n']:
                try:
                    Image = Font[str(char)][1]
                    Image = pygame.transform.scale(Image, (Image.get_width() * scaling, Image.get_height() * scaling))
                    Image.set_colorkey((255, 255, 255))
                    CurrentWord += str(char)
                    surface.blit(
                        Image,
                        (X * scaling + OriginalX, Y * scaling + OriginalY))
                except KeyError:
                    pass
            else:
                WordTotal = 0
                for char2 in CurrentWord:
                    WordTotal += Font[char2][0]
                    WordTotal += Spacing
                if WordTotal+X+OriginalX > WidthLimit:
                    X = 0
                    Y += Font['Height']
                for char2 in CurrentWord:
                    Image = Font[str(char2)][1]
                    surface.blit(pygame.transform.scale(Image, (Image.get_width()*scaling, Image.get_height()*scaling)),
                                 (X * scaling + OriginalX, Y * scaling + OriginalY))
                    X += Font[char2][0]
                    X += Spacing
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                else:
                    X = 0
                    Y += Font['Height']
                CurrentWord = ''
            if X+OriginalX > WidthLimit:
                X = 0
                Y += Font['Height']
        return X, Y
    elif overflow == 'cut all':
        for char in Text:
            if char not in [' ', '\n']:
                try:
                    Image = Font[str(char)][1]
                    surface.blit(pygame.transform.scale(Image, (Image.get_width()*scaling, Image.get_height()*scaling)),
                                 (X*scaling, Y*scaling))
                    X += Font[str(char)][0]
                    X += Spacing
                except KeyError:
                    pass
            else:
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                if char == '\n':
                    X = 0
                    Y += Font['Height']
                CurrentWord = ''
            if X+OriginalX > WidthLimit:
                X = 0
                Y += Font['Height']
        return X, Y


def generate_font(FontImage, FontSpacingMain, TileSize, TileSizeY, color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
                    ,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y'
                    ,'z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=',
                 '\\','[',']','*','"','<','>',';']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(), FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((0, 0, 0))
    NewSurf.blit(FontImage, (0, 0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((255, 255, 255))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize+1)*num), 0, TileSize, TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing
