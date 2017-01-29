from math import sqrt
import numpy as np
import time

class PSO():
    def ran(self,min,max):
        sp=max-min
        return (np.random.random_sample()*sp+min)

    class partic:
        def __init__(self, x, y):
            self.position = x
            self.velocity = y
            self.P = x    

    def __init__(self, param_boarder, func, number=10, generations=10, w=1, c1=1, c2=1):
        self.stepnr = 0 
        self.number = number
        self.generations = generations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.swarm = []
        self.func = func
        self.param_boarder = param_boarder
        # print " number of params: " ,range(len(param_boarder))
        for j in range(number):            
            arraypos = np.zeros(len(param_boarder))
            for i in range(len(param_boarder)):
                arraypos[i] = float(self.ran(param_boarder[i]["unten"],param_boarder[i]["oben"]))
            arrayvel = np.zeros(len(param_boarder))
            for i in range(len(param_boarder)):
                arrayvel[i] = float(np.random.random_sample()*(param_boarder[i]["oben"]-param_boarder[i]["unten"])/2-float(param_boarder[i]["oben"]-param_boarder[i]["unten"])/4)                
            particle = self.partic(arraypos,arrayvel)
            self.swarm.append(particle)
        self.G = self.swarm[0].position #select first particle to start serach for global best
        for i in range(self.number):
            if func(self.swarm[i].position)<func(self.G):
                self.G=self.swarm[i].position


    def run(self):
        # import matplotlib.pyplot as plt

        start_time = time.time()
        for i in range(self.generations):            
            # #here the loop for every particle
            if (i%6):
                somepartic_id = int(np.random.random_sample()*self.number)
                arraypos = []
                arrayvel = []
                for k in range(len(self.param_boarder)):
                    arraypos.append(self.ran(self.param_boarder[k]["unten"],self.param_boarder[k]["oben"]))
                for i in range(len(self.param_boarder)):
                    arrayvel.append(float(np.random.random_sample()*(self.param_boarder[i]["oben"]-self.param_boarder[i]["unten"])/2-float(self.param_boarder[i]["oben"]-self.param_boarder[i]["unten"])/4))
                self.swarm[somepartic_id].position = arraypos
                # for ko in arraypos:
                #     plt.plot([ko,0], 'ro')
                self.swarm[somepartic_id].position = arrayvel
                if self.func(self.swarm[somepartic_id].position)<self.func(self.G):
                    self.G=self.swarm[somepartic_id].position
            for j in range(len(self.swarm)):        
                # print "generation ", i, "partikel ", j
                r1=np.random.random()
                r2=np.random.random()
                
                self.swarm[j].position = self.swarm[j].position + self.swarm[j].velocity
                self.swarm[j].velocity = self.w*(self.swarm[j].velocity+self.c1*r1*(self.swarm[j].P-self.swarm[j].position)+self.c2*r2*(self.G-self.swarm[j].position))
                if self.func(self.swarm[j].position)<self.func(self.swarm[j].P):            
                    self.swarm[j].P=self.swarm[j].position
                if self.func(self.swarm[j].position)<self.func(self.G):                    
                    self.G=self.swarm[j].position
            print ("error",self.func(self.G))            
        print ('elapsed time: ' , time.time() - start_time)
        # print ("solution: ", self.G, self.func(self.G))        
        # plt.show()
        return self.G

    def step(self):
        start_time = time.time()
    
        # #here the loop for every particle
        if (self.stepnr%6):
            somepartic_id = int(np.random.random_sample()*self.number)
            arraypos = []
            for k in range(len(self.param_boarder)):
                arraypos.append(self.ran(self.param_boarder[k]["unten"],self.param_boarder[k]["oben"]))
            self.swarm[somepartic_id].position = arraypos
            if self.func(self.swarm[somepartic_id].position)<self.func(self.G):
                self.G=self.swarm[somepartic_id].position
        for j in range(len(self.swarm)):        
            # print "generation ", self.stepnr, "partikel ", j
            r1=np.random.random()
            r2=np.random.random()
            
            self.swarm[j].position = self.swarm[j].position + self.swarm[j].velocity        
            self.swarm[j].velocity = self.w*(self.swarm[j].velocity+self.c1*r1*(self.swarm[j].P-self.swarm[j].position)+self.c2*r2*(self.G-self.swarm[j].position))
            if self.func(self.swarm[j].position)<self.func(self.swarm[j].P):            
                self.swarm[j].P=self.swarm[j].position
            if self.func(self.swarm[j].position)<self.func(self.G):
                # print (self.func(self.swarm[j].position)," ist kleiner als: ",self.func(self.G))
                self.G=self.swarm[j].position
                # print ("neues G: ", self.swarm[j].position)
        # print ("error",self.func(self.G))
        self.stepnr = self.stepnr + 1
        # print ('elapsed time: ' , time.time() - start_time)              
        return self.G