# Code adapted by Raven Ironwing from https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/

import pygame as pg

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

vec = pg.math.Vector2
WIDTH = 834
HEIGHT = 834
START_NUM_PARTICLES = 1000
MAX_NUM_PARTICLES = 2000
FIX_CENTER = True
DEFAULT_COMP = {'H': 0, 'He': 0, 'O': 0, 'C': 0, 'Fe': 0, 'Ne': 0, 'N': 0, 'Si': 0, 'Mg': 0, 'S': 0, 'Ot': 0} # The dictionary used to copy to set the randomized composition of each of the particles.
COMPOSITION_SEED = {'H': 0.73, 'He': 0.25, 'O': 0.008, 'C': 0.0035, 'Fe': 0.0016, 'Ne': 0.0012, 'N': 0.0009, 'Si': 0.0007, 'Mg': 0.0005, 'S': 0.0004, 'Ot': 0.0004}
ELEMENT_COLORS = {'H': (255, 255, 255), 'He': (52, 195, 235), 'O': (255, 0, 0), 'C': (148, 146, 146), 'Fe': (156, 56, 56), 'Ne': (255, 0, 0), 'N': (137, 110, 245), 'Si': (214, 198, 105), 'Mg': (149, 160, 163), 'S': (39, 194, 44), 'Ot': (150, 75, 0)}
PROBS = [0.73, 0.25, 0.008, 0.0035, 0.0016, 0.0012, 0.0009, 0.0007, 0.0005, 0.0004, 0.0004]
START_PARTICLE_MASS = 70
MAX_PARTICLE_MASS = 400
CENTER_CRIT_MASS = 10000 # The mass when a particles becomes a star and turns yellow and becomes the center of the star system.
START_NOVA_RADIUS = 45 # The initial spread of the exploding star particles.
MAX_NOVA_RADIUS = 450
START_NOVA_FORCE = 100# Initial explosive force of dying star.
MAX_NOVA_FORCE = 500
START_CYCLES = 1 # How many cycles before particles can collide. The rand collide force will be applied for these cycles.
RADIUS_SCALE = 0.4 # Sets the scale of the particles
START_COLLIDE_RATIO = 0.5 # The percentage the particles collide at.
MAX_COLLIDE_RATIO = 1
START_G = 0.8 # Value of the gravitational constant.... Not set to the real value to speed things up.
MAX_G = 5.0
KILL_BOUND = 200 # The off screen distance to kill particles that go off the screen.

