import linear_algebra
import pygame
import json

pygame.init()
monitor = pygame.display.Info()
font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}

winsize = (1000, 600)
window = pygame.display.set_mode(winsize, pygame.RESIZABLE)
surface = pygame.Surface(winsize)
pygame.display.set_caption("simulazione")


data = None

with open("data.json", "r") as write_file:
     data = json.load(write_file)

clock = pygame.time.Clock()
FPS = 60
linear_algebra.normalization = 1000000
earth_img = pygame.image.load("earth.png")
iss_img = pygame.image.load("iss.png")

sole = linear_algebra.Obj(linear_algebra.Vector(data["sole"]["orbita"] + winsize[0] * linear_algebra.normalization / 2, (winsize[1] / 2)  * linear_algebra.normalization, 0), linear_algebra.Vector(0, 0, 0), data["sole"]["massa"], 700)
sat = linear_algebra.Obj(linear_algebra.Vector(data["mercurio"]["orbita"] + winsize[0] * linear_algebra.normalization / 2, (winsize[1] / 2)  * linear_algebra.normalization, 0), linear_algebra.Vector(0, data["mercurio"]["velocita"], 0), data["mercurio"]["massa"], 700)

while True:
    clock.tick(FPS)
    surface.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    sat.update(sole)
    sole.update(sat)
    sole.draw(surface, earth_img)
    sat.draw(surface, iss_img)
    window.blit(pygame.transform.scale(surface, winsize), [0,0])
    pygame.display.update()
