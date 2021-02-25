import pygame
from pygame.locals import *
import sys, os, traceback
import random
from random import choice, choices, randrange, uniform
from math import *
from settings import *

if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.display.init()
pygame.font.init()

num_particles = NUM_PARTICLES
# Whether collisions are enabled
collisions = True
# Whether to contrain particles to the edges.  Not affected by the collisions enabled flag.
edge_clamp = False
# Particles' maximum (random) speed (pixels/sec)
max_initial_speed = 100.0
# Movement substeps at the given timestep
movement_substeps = 1
# Target FPS
target_fps = 60.0
# dt (should be 1.0/target_fps for realtime, but you can change it to speed up or slow down time)
dt = 1.0 / target_fps

clock = pygame.time.Clock()

#if num_particles == -1:
#    while True:
#        try:
#            num_particles = int(input("Number of particles: "))
#            break
#        except:
#            print("Could not parse number.")
num_particles_orig = num_particles
new_particles = []
dead_particles = []
start = 0
exploding = True
set_center = FIX_CENTER
biggest = None

screen_size = [WIDTH, HEIGHT]
icon = pygame.Surface((1, 1));
icon.set_alpha(0);
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Simulator")
surface = pygame.display.set_mode(screen_size)


def rndint(num): return int(round(num))


class Particle(object):
    def __init__(self, pos=None, vel=None, mass=None, composition=None):
        if mass:
            self.mass = mass
            self.composition = composition

        else:
            self.composition = DEFAULT_COMP.copy()
            base_element = choice(choices(list(COMPOSITION_SEED.keys()), PROBS, k=20)) # Randomly picks base element type weighted by composition type.
            self.composition[base_element] = randrange(30, 100)/100
            for i, el in enumerate(self.composition):
                if el != base_element:
                    perc_left = 1 - sum(self.composition.values())
                    if perc_left > 0:
                        add_perc = ceil((perc_left) * 1000)
                        self.composition[el] = randrange(0, add_perc)/1000
            perc_left = 1 - sum(self.composition.values())
            if perc_left > 0: # Adds remainder to a randomly selected element.
                el = choice(list(self.composition.keys()))
                self.composition[el] += perc_left
            if self.composition['H'] + self.composition['O'] + self.composition['N'] + self.composition['Ne']   > 0.80: #Gass based particles
                self.mass = randrange(1, int(MAX_MASS/4))
            elif self.composition['Fe'] + self.composition['C'] + self.composition['Mg'] + self.composition['Si'] + self.composition['S'] > 0.7: #Solid based particles
                self.mass = randrange(int(MAX_MASS/5), MAX_MASS)
            else:
                self.mass = randrange(1, MAX_MASS) #Other particles

        #Sets particle color based on elemental composition
        self.color = [0, 0, 0]
        for el in self.composition:
            perc = self.composition[el]
            self.color[0] += ELEMENT_COLORS[el][0] * perc
            self.color[1] += ELEMENT_COLORS[el][1] * perc
            self.color[2] += ELEMENT_COLORS[el][2] * perc
        for i, color in enumerate(self.color): #Makes sure all values are vallid colors.
            if color > 255:
                self.color[i] = 255

        self.color = tuple(self.color)
        if self.mass > CENTER_CRIT_MASS: #Turns mass yellow when it turns into a star.
            self.color = (255, 255, 0)

            #element_type = choice(choices(list(COMPOSITION_SEED.keys()), PROBS, k=20)) # Randomly picks particle type weighted by composition type.
            #temp_mass = 0
            #if element_type == 'OE':
            #    elrange = randrange(4, 10)
            #    temp_mass = randrange(4, elrange + 1)
            #    for val in ELEMENT_MASSES: # Prevents creating weighted elements
            #        if val == temp_mass:
            #            temp_mass += 1
            #    #self.mass = (2*temp_mass)**.5 # Uses a natural log function to scale the mass to something displayable.
            #    self.mass = temp_mass
            #else:
                #self.mass = (2*ELEMENT_MASSES[element_type])**.5
            #    self.mass = ELEMENT_MASSES[element_type]
            #self.composition[element_type] += 1 # adds initial particle of selected randomized type
            #self.color = ELEMENT_COLORS[element_type]

        if pos == None:
            randdisp = randrange(ceil(STAR_RADIUS/self.mass), STAR_RADIUS + 1)
            randveclength = randrange(0, randdisp)
            randvec = vec(randveclength, 0)
            randangle = randrange(0, 361)
            randvec = randvec.rotate(randangle)
            self.pos = [WIDTH / 2 + randvec.x, HEIGHT / 2 + randvec.y]
        else:
            self.pos = pos

        self.forces = [0.0, 0.0]
        if vel:
            self.vel = vel
        else:
            force = START_FORCE
            a = force / self.mass
            t = 1
            vel = a * t
            self.vel = vec(vel, 0)
            randangle = randrange(0, 361)
            self.vel = self.vel.rotate(randangle)
            self.vel = [self.vel.x, self.vel.y]
            self.dir = vec(self.vel[0], self.vel[1]).normalize()
            self.exp_force = self.dir * START_FORCE

        self.r = RADIUS_SCALE * (self.mass ** (1.0 / 3.0))
        self.collide_r = self.r * COLLIDE_RATIO

    def move(self, dt):
        self.pos[0] += dt * self.vel[0]
        self.pos[1] += dt * self.vel[1]
        a_x = dt * self.forces[0] / self.mass  # F=MA -> A=F/M
        a_y = dt * self.forces[1] / self.mass
        while abs(a_x) > 1000.0:
            a_x /= 10.0  # This can happen, especially without collisions
        while abs(a_y) > 1000.0:
            a_y /= 10.0
        self.vel[0] += a_x
        self.vel[1] += a_y
        self.forces[0] = 0.0
        self.forces[1] = 0.0

        #kills particles that go too far off screen
        if WIDTH + KILL_BOUND > self.pos[0] > -KILL_BOUND:
            pass
        elif HEIGHT + KILL_BOUND > self.pos[1] > -KILL_BOUND:
            pass
        else:
            dead_particles.append(self)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (rndint(self.pos[0]), rndint(screen_size[1] - self.pos[1])), rndint(self.r), 0)

def setup_particles():
    global particles, num_particles, new_particles, start, exploding, dead_particles, biggest
    num_particles = num_particles_orig
    new_particles = []
    dead_particles = []
    exploding = True
    biggest = None
    particles = [Particle() for i in range(num_particles)]

def get_input():
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
            elif event.key == K_r:
                new()  # reset
    return True

def add_forces(particle1, particle2, cycle = None):
    dx = particle2.pos[0] - particle1.pos[0]
    dy = particle2.pos[1] - particle1.pos[1]
    r_squared = dx * dx + dy * dy
    if r_squared == 0:
        collide(particle1, particle2)
        return
    r = r_squared ** 0.5
    if cycle: # Makes the minimum distance of particles the sum of their radii before collisions are active. This prevents unrealistically large forces during the explosion.
        min_dist = particle1.r + particle2.r
        if r < min_dist:
            r = min_dist
    force_magnitude = (G * particle1.mass * particle2.mass) / r_squared  # F=G*M1*M2/(r^2)
    dx_normalized_scaled = (dx / r) * force_magnitude
    dy_normalized_scaled = (dy / r) * force_magnitude
    particle1.forces[0] += dx_normalized_scaled
    particle1.forces[1] += dy_normalized_scaled
    particle2.forces[0] -= dx_normalized_scaled
    particle2.forces[1] -= dy_normalized_scaled

    r1 = particle1.collide_r
    r2 = particle2.collide_r
    both = r1 + r2
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if not exploding:
        if abs_dx * abs_dx + abs_dy * abs_dy <= both * both:
            collide(particle1, particle2)
    elif cycle == 0: # Only applies force to first cycle
        particle1.forces[0] += particle1.exp_force.x
        particle1.forces[1] += particle1.exp_force.y
        # applies randomized collision forces durring first cycle to simulate the particles bouncing off of one another.
    elif cycle > 0:
        if RAND_COLLIDE_FORCE > 0:
            randx = randrange(0, RAND_COLLIDE_FORCE)
            randy = randrange(0, RAND_COLLIDE_FORCE)
            xsign = choice([-1, 1])
            ysign = choice([-1, 1])
            randx = randx * xsign
            randy = randy * ysign
            particle1.forces[0] += randx
            particle1.forces[1] += randy


def move():
    global new_particles, dead_particles, num_particles, particles, biggest
    surface.fill((25, 0, 0))
    new_particles = []
    dead_particles = []
    temp = []
    for i in range(movement_substeps):
        for j, p in enumerate(particles):
            for k in range(j + 1, num_particles, 1):
                if (particles[j] not in dead_particles) and (particles[k] not in dead_particles):
                    add_forces(particles[j], particles[k])
            p.draw(surface)
            if p != biggest:
                p.move(dt / float(movement_substeps))
            if p in dead_particles:
                continue
            temp.append(p)
    pygame.display.flip()
    particles = temp
    particles += new_particles
    num_particles = len(particles)

def explode(cycle):
    surface.fill((25, 0, 0))
    for i in range(movement_substeps):
        for j, p in enumerate(particles):
            for k in range(j + 1, num_particles, 1):
                add_forces(particles[j], particles[k], cycle)
            p.draw(surface)
            p.move(dt / float(movement_substeps))
    pygame.display.flip()

def collide(p1, p2):
    global particles, num_particles, dead_particles, new_particles, biggest
    # Remove both colliding particles
    dead_particles.append(p1)
    dead_particles.append(p2)
    # Replace with a single particle with their properties
    mv_x = p1.mass * p1.vel[0] + p2.mass * p2.vel[0]
    mv_y = p1.mass * p1.vel[1] + p2.mass * p2.vel[1]
    mass = p1.mass + p2.mass
    ratp1 = p1.mass / mass
    ratp2 = p2.mass / mass
    composition = p1.composition.copy()
    for key in p2.composition: # Combines the compositions depending on the mass of each particle.
        composition[key] = (p1.composition[key] * ratp1 + p2.composition[key] * ratp2)
    biggest_hit = False
    if biggest in [p1, p2]: #Makes it so the center particle doesn't move.
        biggest_hit = True
    if biggest_hit:
        biggest = new_particle = Particle(
        [biggest.pos[0], biggest.pos[1]],  # center of mass
        [0, 0],  # momentum is conserved but not kinetic energy
        mass,
        composition)
    else:
        new_particle = Particle(
            [(p1.pos[0] * p1.mass + p2.pos[0] * p2.mass) / mass, (p1.pos[1] * p1.mass + p2.pos[1] * p2.mass) / mass],  # center of mass
            [mv_x / mass, mv_y / mass],  # momentum is conserved but not kinetic energy
            mass,
            composition)
    new_particles.append(new_particle)

def clamp_to_edges():
    for p in particles:
        r = p.r
        if p.pos[0] <= r: p.vel[0] = abs(p.vel[0])
        if p.pos[1] <= r: p.vel[1] = abs(p.vel[1])
        if p.pos[0] >= screen_size[0] - r: p.vel[0] = -abs(p.vel[0])
        if p.pos[1] >= screen_size[1] - r: p.vel[1] = -abs(p.vel[1])

def set_fixed_center():
    global biggest
    biggest = find_largest()
    offset_vel = biggest.vel
    offset_pos = [WIDTH/2 - biggest.pos[0], HEIGHT/2 - biggest.pos[1]]
    biggest.vel = [0, 0] # Stops largest particle from moving.
    biggest.pos = [WIDTH/2, HEIGHT/2] # Sets largest particle to center
    for p in particles:
        if p != biggest:
            p.pos[0] += offset_pos[0]
            p.pos[1] += offset_pos[1]

def find_largest():
    largest = particles[0]
    for p in particles:
        if p.mass > largest.mass:
            largest = p
    return largest


def new():
    global exploding, set_center, start
    setup_particles()
    for i in range(0, START_CYCLES):
        explode(i)
    exploding = False
    set_center = FIX_CENTER
    start = pygame.time.get_ticks()

def main():
    global set_center
    new()
    while True:
        if set_center and (find_largest().mass > CENTER_CRIT_MASS):
            print('center set')
            set_fixed_center()
            set_center = False
        if not get_input(): break
        move()
        if edge_clamp: clamp_to_edges()
        clock.tick(target_fps)
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()