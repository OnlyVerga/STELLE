import numpy as np
import pygame
from astropy.time import Time
from astroquery.jplhorizons import Horizons
import math

scaling = 100

pygame.init()
sim_start_date = "2020-03-01"     # simulating a solar system starting from this date
m_earth = 5.9722e24 / 1.98847e30  # Mass of Earth relative to mass of the sun
m_moon = 7.3477e22 / 1.98847e30

winsize = (800, 600)
offset = (winsize[0] / 2, winsize[1] / 2)
window = pygame.display.set_mode(winsize)

dt = 0.1


class Object:  # define the objects: the Sun, Earth, Mercury, etc
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=np.float)
        self.v = np.array(v, dtype=np.float)
        self.xs = []
        self.ys = []
        self.color = color
        self.size = rad


class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None

    def add_planet(self, planet):
        self.planets.append(planet)

    def evolve(self):
        self.time += dt
        pygame.draw.circle(window, self.thesun.color, (self.thesun.r[0] + offset[0], self.thesun.r[1] + offset[1]),
                           self.thesun.size * sizescale)
        for p in self.planets:
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r ** 2) ** (3. / 2)  # in units of AU/day^2
            p.v += acc * dt
            p.r *= scaling
            pygame.draw.circle(window, p.color, (p.r[0] + offset[0], p.r[1] + offset[1]), p.size * sizescale)
            pygame.draw.circle(window, p.color, offset, math.sqrt(pow(p.r[0], 2) + pow(p.r[1], 2)), 4)
            p.r /= scaling

class Razzo:
    def __init__(self, r, v):
        self.r = np.array(r, dtype=np.float)
        self.v = np.array(v, dtype=np.float)
        self.color = (255, 255, 255)
        self.size = 10

    def update(self):
        self.r += self.v * dt
        acc = -2.959e-4 * self.r / np.sum(self.r ** 2) ** (3. / 2)  # in units of AU/day^2
        self.v += acc * dt
        self.r *= scaling
        pygame.draw.circle(window, self.color, (self.r[0] + offset[0], self.r[1] + offset[1]), self.size * sizescale)
        self.r /= scaling


ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd
colors = ['gray', 'orange', 'blue', 'chocolate']
#colors = ['gray', 'orange', 'blue', 'chocolate', 'orange', 'yellow']
#sizes = [0.38, 0.95, 1., 0.53, 3, 2]
sizes = [0.38, 0.95, 1., 0.53]
for i, nasaid in enumerate([1, 2, 3, 4]):
#for i, nasaid in enumerate([1, 2, 3, 4, 5, 6]):  # The 1st, 2nd, 3rd, 4th planet in solar system
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    ss.add_planet(Object(nasaid, 20 * sizes[i], colors[i],
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']],    #pos
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))  #vel

obj = Horizons(id=3, location="@sun", epochs=ss.time, id_type='id').vectors()
vel = 32700 * 5.7755e-7 #m/s in AU/giorno
rocket = Razzo([np.double(obj[xi]) for xi in ['x', 'y', 'z']], [vel * obj['y'] / math.sqrt(pow(obj['x'], 2) + pow(obj['y'], 2)), vel * obj['x'] / math.sqrt(pow(obj['x'], 2) + pow(obj['y'], 2)), 0]) #lo faccio partire dalla terra e gli dò una velocità
print(rocket.v)
print(obj['vx'], obj['vy'])
while True:
    sizescale = (scaling - 15) * 0.008

    if sizescale > 1:
        sizescale = 1
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
            if e.button == 4 and scaling >= 10:
                scaling -= 1
            if e.button == 5 and scaling <= 200:
                scaling += 1

    window.fill((0, 0, 0))
    ss.evolve()
    rocket.update()
    pygame.display.update()