import pygame as pg
vec = pg.math.Vector2
WIDTH = 800
HEIGHT = 800
NUM_PARTICLES = 1000
FIX_CENTER = True
RED = (255, 0, 0)
DEFAULT_COMP = {'H': 0, 'He': 0, 'O': 0, 'C': 0, 'Fe': 0, 'Ne': 0, 'N': 0, 'Si': 0, 'Mg': 0, 'S': 0, 'Ot': 0} # The dictionary used to copy to set the randomized composition of each of the particles.
COMPOSITION_SEED = {'H': 0.73, 'He': 0.25, 'O': 0.008, 'C': 0.0035, 'Fe': 0.0016, 'Ne': 0.0012, 'N': 0.0009, 'Si': 0.0007, 'Mg': 0.0005, 'S': 0.0004, 'Ot': 0.0004}
ELEMENT_COLORS = {'H': (255, 255, 255), 'He': (52, 195, 235), 'O': (255, 0, 0), 'C': (148, 146, 146), 'Fe': (156, 56, 56), 'Ne': (255, 0, 0), 'N': (137, 110, 245), 'Si': (214, 198, 105), 'Mg': (149, 160, 163), 'S': (39, 194, 44), 'Ot': (150, 75, 0)}
PROBS = [0.73, 0.25, 0.008, 0.0035, 0.0016, 0.0012, 0.0009, 0.0007, 0.0005, 0.0004, 0.0004]
MAX_MASS = 70
CENTER_CRIT_MASS = 10000 # The mass when a particles becomes a star and turns yellow and becomes the center of the star system.
STAR_RADIUS = 45 # The initial spread of the exploding star particles.
START_FORCE = 100# Initial explosive force of dying star.
START_CYCLES = 2 # How many cycles before particles can collide. The rand collide force will be applied for these cycles.
RAND_COLLIDE_FORCE = 1 # This number adds a randomized directional force to the explosion simulating particles striking each other during collisions early on in the explosion.
RADIUS_SCALE = 0.4 # Sets the scale of the particles
COLLIDE_RATIO = 0.5 # The percentage the particles collide at.
G = 0.8 # Value of the gravitational constant.... Not set to the real value to speed things up.
KILL_BOUND = 200 # The off screen distance to kill particles that go off the screen.

