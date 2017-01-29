#!/usr/bin/python

# this is a small class that implements the particle swarm optimization technique in python
# obligatoric for the initialization are a function which returns one value, which should be minimized 
# and a list containing the lower and upper limit of the search space in a dictionary with the keys "lower" and "upper" 
# e.g. limits = [{"lower":-10,"upper":10},{"lower":-300,"upper":-20}]
# further parameters:   w:              speed of the correction
#                       c1:             higher -> selfish behavior
#                       c2:             higher -> go for global optimum 
#                       c3:             generations at which a particle is thrown randomly to the seach space
#                       number:         number of particles in total
#                       generations:    number of generation the PSO lives

from math import sqrt
import numpy as np
import time

class PSO():

    def ran(self,min,max):                                                                      # get random number between lower and upper limit
        sp=max-min
        return (np.random.random_sample()*sp+min)

    class partic:                                                                               # the particle with personal best solution P
        def __init__(self, x, y):
            self.position = x
            self.velocity = y
            self.P = x    

    def __init__(self, param_boarder, func, number=10, generations=10, w=1, c1=1, c2=1,c3=5):
        self.stepnr = 0 
        self.number = number
        self.generations = generations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.swarm = []
        self.func = func
        self.param_boarder = param_boarder
        for j in range(number):                                                                 # create particles according to number

            arraypos = np.zeros(len(param_boarder))
            for i in range(len(param_boarder)):
                arraypos[i] = float(self.ran(param_boarder[i]["lower"],param_boarder[i]["upper"]))  # get random position

            arrayvel = np.zeros(len(param_boarder))
            for i in range(len(param_boarder)):
                arrayvel[i] = float(np.random.random_sample()*(param_boarder[i]["upper"]-
                param_boarder[i]["lower"])/2-float(param_boarder[i]["upper"]-param_boarder[i]["lower"])/4) #randowm speed

            particle = self.partic(arraypos,arrayvel)                                           # create particle

            self.swarm.append(particle)

        self.G = self.swarm[0].position                                                         #select first particle to start serach for global best
        for i in range(self.number):
            if func(self.swarm[i].position)<func(self.G):
                self.G=self.swarm[i].position


    def run(self):                                                                              # run with the predefined generations
        
        start_time = time.time()
        for i in range(self.generations):
            self.step()        
        print ('elapsed time: ' , time.time() - start_time)        
        return self.G                                                                           # return global best solution

    def step(self):                                                                             # do one optimization step at a time
        start_time = time.time()
        if (self.stepnr%self.c3):                                                               # throw random particle to search space every c3 generations
            somepartic_id = int(np.random.random_sample()*self.number)
            arraypos = []
            for k in range(len(self.param_boarder)):
                arraypos.append(self.ran(self.param_boarder[k]["lower"],self.param_boarder[k]["upper"]))
            self.swarm[somepartic_id].position = arraypos
            if self.func(self.swarm[somepartic_id].position)<self.func(self.G):
                self.G=self.swarm[somepartic_id].position
        for j in range(len(self.swarm)):        
            r1=np.random.random()                                                               # faktors for random variation of the speed
            r2=np.random.random()            
            self.swarm[j].position = self.swarm[j].position + self.swarm[j].velocity            #compute new position and velocity
            self.swarm[j].velocity = self.w*(self.swarm[j].velocity+self.c1*r1*(self.swarm[j].P-
                self.swarm[j].position)+self.c2*r2*(self.G-self.swarm[j].position))
            if self.func(self.swarm[j].position)<self.func(self.swarm[j].P):            
                self.swarm[j].P=self.swarm[j].position
            if self.func(self.swarm[j].position)<self.func(self.G):
                self.G=self.swarm[j].position
        self.stepnr = self.stepnr + 1
        return self.G                                                                           # return global best solution
