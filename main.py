import random
import math
import time
from bearlibterminal import terminal


def run():
    terminal.open()
    terminal.set("window: size=100x50, cellsize8x12, resizeable=true;")
    terminal.setf("font: Andux_cp866ish.png, size=8x12, codepage=437")
    terminal.composition(True)

    terminal.refresh()

    #p1 = Particle(50, 25, 0, 10, 90, 1)
    #p2 = Particle(50, 25, 0, 10, 70, 1)
    emitter = Emitter(25, 25, 1, 90, 2.0, 2, 4)
    emitter.restart()

    #sudo_pool = [p1, p2]
    timer1 = time.perf_counter()
    while terminal.read() != terminal.TK_CLOSE:
        terminal.clear()
        for par in emitter._particlePool:
            print(par)
            render(par)
            timer2 = time.perf_counter()
            delta = timer2 - timer1
            # print(delta)
            emitter.update(delta)
        pass

    terminal.clear()


def render(particle):
    terminal.printf(int(particle.position["x"]), int(particle.position["y"]), 'J')
    terminal.refresh()


class Particle(object):
    def __init__(self, x, y, z, life, angle, speed):
        self.position = {
            "x": x,
            "y": y
        }

        self.forces = {
            "x": 0,
            "y": 0
        }

        self.life = life
        self._startingLife = life

        self.velocity = {
            "x": speed * math.cos(math.radians(angle)),
            "y": -speed * math.sin(math.radians(angle))
        }

    # def update(self, delta):
    #     self.life -= delta
    #     print(self.life)
    #     if self.life > 0:
    #         self.position["x"] += self.velocity["x"] * delta
    #         self.position["y"] += self.velocity["y"] * delta

    def setVelocity(self, angle, speed):
        self.velocity = {
            "x": math.cos(math.radians(angle)) * speed,
            "y": -math.sin(math.radians(angle)) * speed
        }


class Emitter(object):
    def __init__(self, x, y, speed, angle, emissionRate, totalParticles, life):
        self._particlePool = []
        self._particleCount = 0
        self._particleIndex = 0
        self._elapsed = 0
        self._emitCounter = 0

        self.totalParticles = totalParticles
        self.emissionRate = emissionRate

        self.active = False
        self.duration = 1000000

        self._pos = {
            "x": x,
            "y": y
        }
        self.posVar = {
            "x": 0,
            "y": 0
        }

        self.speed = speed
        self.speedVar = 0

        self.angle = angle
        self.angleVar = 0

        self.life = life
        self.lifeVar = 0

        self.radius = 0
        self.radiusVar = 0

    def restart(self):
        self._particlePool = []

        for _ in range(0, self.totalParticles):
            self._particlePool.append(Particle(self._pos["x"], self._pos["y"], 0, 0, 0, 0))

        self._particleCount = 0
        self._particleIndex = 0
        self._elapsed = 0
        self._emitCounter = 0

    def _isFull(self):
        return self._particleCount == self.totalParticles

    def _addParticle(self):
        if self._isFull():
            return False

        p = self._particlePool[self._particleCount]
        self._initParticle(p)
        self._particleCount += 1
        return True

    def _initParticle(self, particle):
        posVar = {
            "x": self.posVar["x"] * random.randrange(-1, 1),
            "y": self.posVar["y"] * random.randrange(-1, 1)
        }

        # if this.posVarTransformFn {
        # posVar = this.posVarTransformFn(posVar, util)
        # }

        particle.position["x"] = posVar["x"] + self._pos["x"]
        particle.position["y"] = posVar["y"] + self._pos["y"]
        particle.position["z"] = 0

        angle = self.angle + self.angleVar * random.randrange(-1, 1)
        speed = self.speed + self.speedVar * random.randrange(-1, 1)

        particle.setVelocity(angle, speed)
        particle._startingLife = self.life + self.lifeVar * random.randrange(-1, 1)
        particle.life = particle._startingLife
        print("life")

    def _updateParticle(self, particle, delta, i):
        print('Life: ', particle.life)
        if particle.life > 0:
            particle.forces["x"] = 0
            particle.forces["y"] = 0

            particle.position["x"] += particle.velocity["x"] * delta
            particle.position["y"] += particle.velocity["y"] * delta
            print("position: ", particle.position)
            particle.life -= delta

            self._particleIndex += 1
        else:
            print("dead particle")
            temp = self._particlePool[i]
            self._particlePool[i] = self._particlePool[self._particleCount - 1]
            self._particlePool[self._particleCount - 1] = temp
            self._particleCount -= 1

    def update(self, delta):
        print('delta: ', delta)
        self._elapsed += delta
        print('elapsed: ', self._elapsed)
        self.active = self._elapsed < self.duration
        print('active: ', self.active)
        if not self.active:
            return

        if self.emissionRate:
            rate = 1.0 / self.emissionRate
            self._emitCounter += delta
            while not self._isFull() and self._emitCounter > rate:
                self._addParticle()
                self._emitCounter -= rate

        self._particleIndex = 0

        while self._particleIndex < self._particleCount:
            p = self._particlePool[self._particleIndex]
            self._updateParticle(p, delta, self._particleIndex)

run()
