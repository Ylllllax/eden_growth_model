import pygame
import random
import math
import time

background_colour = (255, 255, 255)
(width, height) = (800, 800)
mass_of_air = 0
gravity = (math.pi, 0.01)

# just loop things
counter = 0
off = 0

my_particles_frozen = []

elasticity = 0    # 0 means balls stick i.e. what percentage of speed is retained on bounce


def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None


def newParticle():
    size = random.randint(10, 20)
    density = random.randint(1, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, size+1)

    particle = Particle((x, y), size, density * size ** 2)
    particle.colour = (200 - density * 10, 200 - density * 10, 255)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)

    my_particles.append(particle)


def newParticleRow():
    size = 15
    density = 1
    y = 1
    dummy = 0

    for x in range(width):
        dummy = dummy + 1
        if dummy%30 == 0:
            particle = Particle((x, y), size, density * size ** 2)
            particle.colour = (200 - density * 10, 200 - density * 10, 255)
            particle.speed = 0
            particle.angle = 0

            my_particles.append(particle)


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


class Particle():
    def __init__(self, (x, y), size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (102, 0, 255)    # a beautiful purple
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        #self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        #self.speed *= self.drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Eden deposition off-lattice')

number_of_particles = 40
my_particles = []

for n in range(number_of_particles):
    newParticle()

selected_particle = None
running = True

while running:

    counter = counter + 1
    off = off + 1

    # if counter % 10 == 0:
        # newParticle()
    if counter == 1000:
        newParticleRow()
        off = 0
        if counter == 1500:
            for i in my_particles:
                my_particles_frozen.append(i)
                my_particles.remove(i)
                counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     (mouseX, mouseY) = pygame.mouse.get_pos()
        #     selected_particle = findParticle(my_particles, mouseX, mouseY)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     selected_particle = None

    # if selected_particle:
    #     (mouseX, mouseY) = pygame.mouse.get_pos()
    #     dx = mouseX - selected_particle.x
    #     dy = mouseY - selected_particle.y
    #     selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
    #     selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    for i, particle in enumerate(my_particles_frozen):
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    pygame.display.flip()
