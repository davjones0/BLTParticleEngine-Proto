import random
import math
import time
import toml
from bearlibterminal import terminal
from os import system, name 
# [U+2593] [U+00B7]


def read_config():
    f = toml.load('particleEffects.toml')
    emitter = Emitter(f)
    return emitter


def run():
    terminal.open()
    terminal.set("window: size=100x50, cellsize8x12, resizeable=true;")
    terminal.setf("font: Andux_cp866ish.png, size=8x12, codepage=437")
    terminal.composition(True)

    terminal.refresh()

    #p1 = Particle(50, 25, 0, 10, 90, 1)
    #p2 = Particle(50, 25, 0, 10, 70, 1)
    #emitter = Emitter(25, 25, 40, 90, .05, 2, 4)
    emitter = read_config()
    emitter.setColor([255, 138, 138, 255], [0, 0, 0, 0], [55, 138, 1, 255], [ 0, 0, 0, 0])
    emitter.restart()

    #sudo_pool = [p1, p2]
    emitter.start(0)
    timer1 = time.perf_counter()
    flag = True

    while flag:
        timer2 = time.perf_counter()
        delta = timer2 - timer1

        while terminal.has_input():
            key = terminal.read()
            if key == 21:
                emitter = read_config()
                emitter.setColor([255, 138, 138, 255], [0, 0, 0, 0], [55, 138, 1, 255], [ 0, 0, 0, 0])
                emitter.restart()
                emitter.start(0)
            if key == 27 or key == 224:
                flag = False


        emitter.update(delta, 1.0)
        terminal.clear()

        for p in emitter._particlePool:
            render(p, emitter._pos)
        terminal.refresh()
        system('clear')

        timer1 = time.perf_counter()
    exit
        


def render(particle, emitter_pos):
    if particle.life > 0.0:
        #print("---------Render-----------")
        # int(particle.position["x"]), int(particle.position["y"])
        offset = {
            "x": particle.position["x"] - emitter_pos["x"],
            "y": particle.position["y"] - emitter_pos["y"]
        }
        terminal.printf(int(emitter_pos["x"]), int(emitter_pos["y"]), "[offset={},{}][color={}]{}[/color]".format(int(offset["x"]), int(offset["y"]), terminal.color_from_argb(int(particle.color[0]), int(particle.color[1]), int(particle.color[2]), int(particle.color[3])), particle.glyph))
        #terminal.refresh()

def rand11(_min, _max):
    _range = _max - _min
    result = random.random() * _range + _min
    return result

def normalize(vector):
    length = math.sqrt(vector["x"] * vector["x"] + vector["y"] * vector["y"])

    vector["x"] /= length
    vector["y"] /= length


class Particle(object):
    def __init__(self, x, y, z, life, angle, speed, glyph):
        self.glyph = glyph
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
            "x": 0,
            "y": 0
        }

        self.radialAccel = 0
        self.radial = {
            "x": 0,
            "y": 0
        }

        self.tangentialAccel = 0
        self.tangential = {
            "x": 0,
            "y": 0
        }

        self.color = []
        self.deltaColor = []

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
    def __init__(self, config):
        self.ascii = config["TestEffect"]["ASCII"]
        self._particlePool = []
        self._particleCount = 0
        self._particleIndex = 0
        self._elapsed = 0
        self._emitCounter = 0

        self.totalParticles = config['TestEffect']['total_particles']
        self.emissionRate = config['TestEffect']['emissionRate']

        self.active = False
        self.duration = 1000000

        self._pos = {
            "x": config['TestEffect']['Movement']['xEmitterPos'],
            "y": config['TestEffect']['Movement']['yEmitterPos']
        }
        self.posVar = {
            "x": config['TestEffect']['Deviate']['Position']['x'],
            "y": config['TestEffect']['Deviate']['Position']['y']
        }

        self.gravity = {
            "x": config['TestEffect']['Movement']['Gravity']['x'],
            "y": config['TestEffect']['Movement']['Gravity']['y']
        }

        self.speed = config['TestEffect']['Movement']['speed']
        self.speedVar = config['TestEffect']['Deviate']['Movement']['speed']

        self.angle = config['TestEffect']['Movement']['angle']
        self.angleVar = config['TestEffect']['Deviate']['Movement']['angle']

        self.life = config['TestEffect']['life']
        self.lifeVar = config['TestEffect']['Deviate']['Life']['life']

        self.radialAccel = config['TestEffect']['Movement']['radialAccel']
        self.radialAccelVar = config['TestEffect']['Deviate']['Movement']['radialAccel']
        self.tangentialAccel = config['TestEffect']['Movement']['tangentialAccel']
        self.tangentialAccelVar = config['TestEffect']['Deviate']['Movement']['tangentialAccel']
        
        #format arbg base 255
        self.startColor = [0, 0, 0, 0]
        self.startColorVar = [0, 0, 0, 0]

        self.endColor = [0, 0, 0, 0]
        self.endColorVar = [0, 0, 0, 0]

    def setColor(self, start, startVar, end, endVar):
        self.startColor = start
        self.startColorVar = startVar
        self.endColor = end
        self.endColorVcoco2dar = endVar

    def restart(self):
        self._particlePool = []

        for _ in range(0, self.totalParticles):
            self._particlePool.append(Particle(self._pos["x"], self._pos["y"], 0, 0, 0, 0, self.ascii))

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
            "x": self.posVar["x"] * rand11(-1, 1),
            "y": self.posVar["y"] * rand11(-1, 1)
        }

        # if this.posVarTransformFn {
        # posVar = this.posVarTransformFn(posVar, util)
        # }
        particle.glyph = self.ascii
        particle.position["x"] = posVar["x"] + self._pos["x"]
        particle.position["y"] = posVar["y"] + self._pos["y"]
        particle.position["z"] = 0

        angle = self.angle + self.angleVar * rand11(-1, 1)
        speed = self.speed + self.speedVar * rand11(-1, 1)

        particle.setVelocity(angle, speed)

        particle.radialAccel = self.radialAccel + self.radialAccelVar * rand11(-1,1)
        particle.tangentialAccel = self.tangentialAccel + self.tangentialAccelVar * rand11(-1,1)

        particle._startingLife = self.life + self.lifeVar * rand11(-1, 1)
        particle.life = particle._startingLife

        # color
        # note that colors are stored as arrays => [r,g,b,a]
        if self.startColor:
            startColor = [
                self.startColor[0] + self.startColorVar[0] * random.randrange(-1,2),
                self.startColor[1] + self.startColorVar[1] * random.randrange(-1,2),
                self.startColor[2] + self.startColorVar[2] * random.randrange(-1,2),
                self.startColor[3] + self.startColorVar[3] * random.randrange(-1,2),
            ]
            
            # if no endcolor stay as startcolor
            endColor = startColor
            if self.endColor:
                endColor = [
                    self.endColor[0] + self.endColorVar[0] * random.randrange(-1,2),
                    self.endColor[1] + self.endColorVar[1] * random.randrange(-1,2),
                    self.endColor[2] + self.endColorVar[2] * random.randrange(-1,2),
                    self.endColor[3] + self.endColorVar[3] * random.randrange(-1,2),
                ]
                particle.color = startColor
                particle.deltaColor = [
                    (endColor[0] - startColor[0]) / particle.life,
                    (endColor[1] - startColor[1]) / particle.life,
                    (endColor[2] - startColor[2]) / particle.life,
                    (endColor[3] - startColor[3]) / particle.life
                ]

    def _updateParticle(self, particle, delta, i):
        #print("*****Particle[{}]*****".format(i))
        #print('Life: ', particle.life)
        #print('color: ', particle.color)
        if particle.life > 0.0:
            particle.forces["x"] = 0
            particle.forces["y"] = 0

            particle.radial["x"] = 0
            particle.radial["y"] = 0

            # dont apply radial forces until moved away from the emitter
            if particle.position["x"] != self._pos["x"] or particle.position["y"] != self._pos["y"] and particle.radialAccel or particle.tangentialAccel:
                particle.radial["x"] = particle.position["x"] - self._pos["x"]
                particle.radial["y"] = particle.position["y"] - self._pos["y"]
                
                normalize(particle.radial)
                

            particle.tangential["x"] = particle.radial["x"]
            particle.tangential["y"] = particle.radial["y"]

            particle.radial["x"] *= particle.radialAccel
            particle.radial["y"] *= particle.radialAccel

            newy = particle.tangential["x"]
            particle.tangential["x"] = -particle.tangential["y"]
            particle.tangential["y"] = newy

            particle.tangential["x"] *= particle.tangentialAccel
            particle.tangential["y"] *= particle.tangentialAccel

            # + gravity on here if needed
            particle.forces["x"] = particle.radial["x"] + particle.tangential["x"] + self.gravity["x"]
            particle.forces["y"] = particle.radial["y"] + particle.tangential["y"] + self.gravity["y"]

            particle.forces["x"] *= delta
            particle.forces["y"] *= delta

            particle.velocity["x"] += particle.forces["x"]
            particle.velocity["y"] += particle.forces["y"]
             

           
            #print("velocity: ", particle.velocity)
            particle.position["x"] += particle.velocity["x"] * delta
            particle.position["y"] += particle.velocity["y"] * delta
           
            #print("position: ", particle.position)
            particle.life -= delta

            if particle.color:
                particle.color[0] += particle.deltaColor[0] * delta
                particle.color[1] += particle.deltaColor[1] * delta
                particle.color[2] += particle.deltaColor[2] * delta
                particle.color[3] += particle.deltaColor[3] * delta

            self._particleIndex += 1
        else:
            #print("dead particle")
            temp = self._particlePool[i]
            self._particlePool[i] = self._particlePool[self._particleCount - 1]
            self._particlePool[self._particleCount - 1] = temp
            self._particleCount -= 1

    def update(self, delta, timeRate):
        delta *= timeRate

        self._elapsed += delta
        # print('elapsed: ', self._elapsed)
        self.active = self._elapsed < self.duration
        if not self.active:
            return

        # ideal emissionRate = total particles / average life of particles
        if self.emissionRate:
            rate = 1.0 / self.emissionRate
            self._emitCounter += delta
            #print('emission rate: ', rate)
            #print('emit counter: ', self._emitCounter)
            while not self._isFull() and self._emitCounter > rate:
                self._addParticle()
                self._emitCounter -= rate

        self._particleIndex = 0

        while self._particleIndex < self._particleCount:
            p = self._particlePool[self._particleIndex]
            self._updateParticle(p, delta, self._particleIndex)

    def start(self, delay):
        time.sleep(delay)
        self._addParticle()


run()
