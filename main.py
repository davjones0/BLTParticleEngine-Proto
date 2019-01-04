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

    p1 = Particle(50, 25, 0, 10, 90, 1)
    p2 = Particle(50, 25, 0, 10, 70, 1)

    sudo_pool = [p1, p2]
    timer1 = time.perf_counter()
    while terminal.read() != terminal.TK_CLOSE:
        terminal.clear()
        for par in sudo_pool:
            render(par)
            timer2 = time.perf_counter()
            delta = timer2 - timer1
            #print(delta)
            par.update(delta)
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
        self._startingLife = self.life = life

        self.velocity = {
            "x": speed * math.cos(math.radians(angle)),
            "y": -speed * math.sin(math.radians(angle))
        }

    def update(self, delta):
        self.life -= delta
        print(self.life)
        if self.life > 0:
            self.position["x"] += self.velocity["x"] * delta
            self.position["y"] += self.velocity["y"] * delta

    def setVelocity(self, angle, speed):
        self.velocity = {
            "x": math.cos(math.radians(angle)) * speed,
            "y": -math.sin(math.radians(angle)) * speed
        }


class Emitter(object):
    def __init__(self):
        self._particlePool = []
        self._particleCount = 0
        self._particleIndex = 0
        self._elapsed = 0
        self._emitCounter = 0

        self.totalParticles = 0
        self.emissionRate = 0
        
        self.active = False
        self.duration = 0

        self.posVar = {
            "x": posVar["x"],
            "y": posVar["y"]
        }

        self.speed = 0
        self.speedVar = 0

        self.angle = 0
        self.angleVar = 0

        self.life = 0
        self.lifeVar = 0

        self.radius = 0
        self.radiusVar = 0

    def restart(self):
        self._particlePool = []

        for _ in range(0, self.totalParticles):
            self._particlePool.append(Particle())

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
            "x": self.posVar["x"] * random.randrange(-1,1),
            "y": self.posVar["y"] * random.randrange(-1,1)
        }

        

run()
