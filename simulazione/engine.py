from copy import deepcopy
import pygame

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 255, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
grey = (127, 127, 127)

font_dat = {'A': [3], 'B': [3], 'C': [3], 'D': [3], 'E': [3], 'F': [3], 'G': [3], 'H': [3], 'I': [3], 'J': [3],
            'K': [3], 'L': [3], 'M': [5], 'N': [3], 'O': [3], 'P': [3], 'Q': [3], 'R': [3], 'S': [3], 'T': [3],
            'U': [3], 'V': [3], 'W': [5], 'X': [3], 'Y': [3], 'Z': [3],
            'a': [3], 'b': [3], 'c': [3], 'd': [3], 'e': [3], 'f': [3], 'g': [3], 'h': [3], 'i': [1], 'j': [2],
            'k': [3], 'l': [3], 'm': [5], 'n': [3], 'o': [3], 'p': [3], 'q': [3], 'r': [2], 's': [3], 't': [3],
            'u': [3], 'v': [3], 'w': [5], 'x': [3], 'y': [3], 'z': [3],
            '.': [1], '-': [3], ',': [2], ':': [1], '+': [3], '\'': [1], '!': [1], '?': [3],
            '0': [3], '1': [3], '2': [3], '3': [3], '4': [3], '5': [3], '6': [3], '7': [3], '8': [3], '9': [3],
            '(': [2], ')': [2], '/': [3], '_': [5], '=': [3], '\\': [3], '[': [2], ']': [2], '*': [3], '"': [3],
            '<': [3], '>': [3], ';': [1]}

pygame.init()

Monitor = pygame.display.Info()



def show_text(Text, X, Y, wl, Font, surface, scaling=1, overflow='normal', Spacing=1, box=False):
    if box != False:
        lenght = 0
        for letter in Text:
            if letter not in [' ', '\n']:
                lenght += Font[letter][0]
                lenght += Spacing
            else:
                lenght += Font["a"][1].get_width()
        X = ((box[1].x - box[0].x) - lenght * scaling) / 2 + box[0].x
        Y = ((box[1].y - box[0].y) - Font["a"][1].get_height() * scaling) / 2 + box[0].y
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
                    Image.set_colorkey((255, 255, 255))
                    CurrentWord += str(char)
                except KeyError:
                    pass
            else:
                WordTotal = 0
                for char2 in CurrentWord:
                    WordTotal += Font[char2][0]
                    WordTotal += Spacing
                if WordTotal + X + OriginalX > WidthLimit:
                    X = 0
                    Y += Font['Height']
                for char2 in CurrentWord:
                    Image = Font[str(char2)][1]
                    Image.set_colorkey((255, 255, 255))
                    surface.blit(
                        pygame.transform.scale(Image, (Image.get_width() * scaling, Image.get_height() * scaling)),
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
            if X + OriginalX > WidthLimit:
                X = 0
                Y += Font['Height']
        return X, Y
    elif overflow == 'cut all':
        for char in Text:
            if char not in [' ', '\n']:
                try:
                    Image = Font[str(char)][1]
                    Image.set_colorkey((255, 255, 255))
                    surface.blit(
                        pygame.transform.scale(Image, (Image.get_width() * scaling, Image.get_height() * scaling)),
                        (X * scaling, Y * scaling))
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
            if X + OriginalX > WidthLimit:
                X = 0
                Y += Font['Height']
        return X, Y


def generate_font(FontImage, FontSpacingMain, TileSize, TileSizeY, color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?',
                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"',
                 '<', '>', ';']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(), FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((0, 0, 0))
    NewSurf.blit(FontImage, (0, 0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((255, 255, 255))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize + 1) * num), 0, TileSize, TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing