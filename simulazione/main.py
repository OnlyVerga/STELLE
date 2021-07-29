import numpy as np
import pygame
from astropy.time import Time
import engine as e
from astroquery.jplhorizons import Horizons
import math

scaling = 100

pygame.init()
sim_start_date = "2022-8-25"     # simulating a solar system starting from this date
consumi = 0
winsize = (1000, 600)
offset = ((winsize[0] - 200) / 2 + 200, winsize[1] / 2)
window = pygame.display.set_mode(winsize)
clock = pygame.time.Clock()


partito = False

ss = e.SolarSystem(e.Object("Sun", 28, [0, 0, 0], [0, 0, 0], "./graphics/sole.png"), offset)
ss.time = Time(sim_start_date).jd
#colors = ['gray', 'orange', 'blue', 'chocolate', 'orange', 'yellow']
sizes = [0.38, 0.95, 1., 0.53, 3, 2]
paths = ["./graphics/mercurio.png", "./graphics/venere.png", "./graphics/terra.png",
         "./graphics/marte.png", "./graphics/giove.png", "./graphics/saturno.png"]
for i, nasaid in enumerate([1, 2, 3, 4, 5, 6]):  # The 1st, 2nd, 3rd, 4th planet in solar system
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    ss.add_planet(e.Object(nasaid, 20 * sizes[i],
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']],    #pos
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']], paths[i]))  #vel

obj = Horizons(id=3, location="@sun", epochs=ss.time, id_type='id').vectors()
v = 29780
vel = v * 5.7755e-7 #m/s in AU/giorno
velocity = [-vel * (obj['y'] / math.sqrt(pow(obj['x'], 2) + pow(obj['y'], 2))), vel * (obj['x'] / math.sqrt(pow(obj['x'], 2) + pow(obj['y'], 2))), 0]
rocket = e.Razzo([np.double(obj[xi]) for xi in ['x', 'y', 'z']], velocity, offset) #lo faccio partire dalla terra e gli dò una velocità

text_color = e.white
font = e.generate_font('fonts/small_font.png', e.font_dat, 5, 8, text_color)



while True:

    sizescale = (scaling - 15) * 0.008

    if sizescale > 1:
        sizescale = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not partito:
                v = 32700
                vel = v * 5.7755e-7 #m/s in AU/giorno
                velocity = [-vel * (rocket.r[1] / math.sqrt(pow(rocket.r[0], 2) + pow(rocket.r[1], 2))),
                            vel * (rocket.r[0] / math.sqrt(pow(rocket.r[0], 2) + pow(rocket.r[1], 2))), 0]
                partito = True
                rocket.v = np.array(velocity, dtype=float)
                consumi = rocket.update_mass(np.array(velocity, dtype=float))
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4 and scaling >= 30:
                scaling -= 1
            if event.button == 5 and scaling <= 200:
                scaling += 1

    window.fill(e.black)
    pygame.draw.rect(window, e.white, pygame.Rect(0, 0, 200, 600))
    e.show_text("Dati utili:", 0, 0, window.get_width(), font, window,
                scaling=3)
    e.show_text("Distanza Sole:", 0, 30, window.get_width(), font, window,
                scaling=3)
    e.show_text(str(round(math.sqrt(pow(rocket.r[0], 2) + pow(rocket.r[1], 2)), 1)) + " AU", 0, 60, window.get_width(), font, window,
                scaling=3)
    e.show_text("Massa:", 0, 90, window.get_width(), font, window,
                scaling=3)
    e.show_text(str(round(rocket.mass,1)), 0, 120, window.get_width(), font, window,
                scaling=3)
    e.show_text("velocita':", 0, 150, window.get_width(), font, window,
                scaling=3)
    e.show_text(str(round(math.sqrt(pow(rocket.v[0], 2) + pow(rocket.v[1], 2)) / 5.7755e-4, 3)) + " km/s", 0, 180, window.get_width(), font, window,
                scaling=3)
    e.show_text("totale consumi:", 0, 210, window.get_width(), font, window,
                scaling=3)
    e.show_text(str(round(consumi,1)) + " tons", 0, 240, window.get_width(), font, window,
                scaling=3)
    e.setscale(sizescale, scaling)
    ss.evolve(window)
    rocket.update(window)
    pygame.display.update()
    clock.tick(120)