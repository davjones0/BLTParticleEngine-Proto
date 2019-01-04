import random
import math
from bearlibterminal import terminal

class Particle(object):
    def __init__(self, x, y, z, life, angle, speed):
        self.position = {
            "x": x,
            "y": y
        }
        self.y = y
        self.z = z
        self.originalLife = self.life = life

        # angleInRadians = angle * math.pi / 180

        self.velocity = {
            "x": speed * math.cos(math.radians(angle)),
            "y": -speed * math.sin(math.radians(angle)),
        }

    def update(self, dt):
        self.life -= dt

        if self.life > 0:
            self.position["x"]+= self.velocity["x"] * dt
            self.position["y"] += self.velocity["y"] * dt

    def setVelocity(self, angle, speed):
        self.velocity = {
            "x": math.cos(angleInRadians) * speed,
            "y": -math.sin(angleInRadians) * speed
        }

class Emitter(object):
    def __init__(self):
        self._particlePool = []
        self.totalParticles
        self.deviation
        self.rate
        self.collide
        self.emissionRate
        self.pos = {
            "x": 0,
            "y": 0
        }
        self.posVar = {
            "x": 0,
            "y": 0
        }
        self.angle
        self.life
        self.lifeVar
        self.gravity = 0
        self._particleCount = 0
        self._particleIndex = 0
        self._elapsed = 0
        self._emitCounter = 0
        self.active = False

        for x in range(self.totalParticles):
            self._particlePool.append(Particle(50, 25, 0, 10, 90, 1))

    def restart(self):
        self._particlePool = []
        for x in range(len(self.totalParticles)):
            particle = Particle
            self._particlePool.append(particle)

        self._particleCount = 0
        self._particleIndex = 0
        self._elapsed = 0
        self._emitCounter = 0

    # Returns whether all the particles in pool are currently active
    def _isFull(self):
        return self._particleCount == self.totalParticles

    # Takes a dormant particle out of the pool and makes it active.
    def _addParticle(self):
        if self._isFull():
            return False

        p = self._particlePool[self._particleCount]
        self._initParticle(p)
        self._particleCount += 1
        return True

    # Initializes the particle based on the current settings
    def _initParticle(self, particles):
        posVar = {
            "x": self.posVar["x"] * random.randint(-1, 1),
            "y": self.posVar["y"] * random.randint(-1, 1)
        }

        if self.posVarTransformFn:
            posVar = self.posVarTransformFn(posVar)

        particles.position["x"] = self.pos["x"] + self.posVar["x"]
        particles.position["y"] = self.pos["y"] + self.posVar["y"]

        angle = self.angle + (self.angleVar * random.randint(-1,1))
        # speed here

        particles.setVelocity(angle, 1) # speed will always be 1 I think

        life = self.life + self.lifeVar * random.randint(-1,1) or 0
        particles.life = max(0, life)

    # Updates a particle based on time moves based on using its velocity
    def _updateParticle(self, particle, delta, i):
        if particle.life > 0:
            particle.forces = {
                "x": 0,
                "y": 0
            }

            particle.forces["x"] *= delta
            particle.forces["y"] *= delta

            particle.velocity["x"] += particle.velocity["x"]
            particle.velocity["y"] += particle.velocity["y"]
            particle.life -= delta

            self._particleIndex += 1
        else:
            # take dead particle to particlepool
            temp = self._particlePool[i]

            # move to end of active particles
            self._particlePool[i] = self._particlePool[self._particleCount - 1]
            self._particlePool[self._particleCount - 1] = temp

            # decrease the count to indicate that one less particle in the pool is active
            self._particleCount -= 1


    def update(self, delta):
        self._elapsed += delta
        self.active = self._elapsed < self.duration

        if self.active == False:
            return

        if self.emissionRate:
            # emit new particles based on how much time has passed and emissionRate
            rate = 1.0 / self.emissionRate
            self._emitCounter += delta

            while self._isFull() == False and self._emitCounter > rate:
                self._addParticle()
                self._emitCounter -= rate

        self._particleIndex = 0

        while self._particleIndex < self._particleCount:
            p = self._particlePool[self._particleIndex]
            self._updateParticle(p, delta, self._particleIndex)


def render(particle):
    print(particle.position)
    terminal.printf(int(particle.position["x"]), int(particle.position["y"]), 'J')
    terminal.refresh()


def run():
    terminal.open()
    terminal.set("window: size=100x50, cellsize=8x12, resizeable=true;")
    terminal.setf("font: Andux_cp866ish.png, size=8x12, codepage=437;")
    terminal.composition(True)

    terminal.refresh()
    # p1 = Particle(50, 25, 0, 10, 90, 1)
    # p2 = Particle(50, 25, 0, 10, 70, 1)

    pool = [p1, p2]

    while terminal.read() != terminal.TK_CLOSE:
        terminal.clear()
        #for par in pool:
        #    render(par)
        #    par.update(1)
        pass

    terminal.close()

run()
