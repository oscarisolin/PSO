#!/usr/bin/python

# this is a small demo that visualizes the optimization steps made by the PSO module



from numpy import meshgrid, linspace
import time
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, pi, exp, sin, cos
import matplotlib.pyplot as plt
import imp
mod =  imp.load_source('mod', './PSO_classe.py')
from mod import PSO


def wert(kord):                                                                 # make up some functions to be minimized
    # return kord[0]**2+kord[1]**2
    return kord[0]**2+1000*-cos(kord[1]*2*pi/space)+1000
    # return 2+kord[1]**2/(space**2)+kord[0]**2/(space**2)-cos(2*kord[1]*2*pi/(1.2*space))-cos(2*kord[0]*2*pi/(1.2*space))



space = 50                                                                      # create plots and grid
fig, ax0 = plt.subplots(subplot_kw={'projection': '3d'})
ax0.view_init(elev=50)
ax0.set_ylim([-1.2*space,1.2*space])
ax0.set_xlim([-1.2*space,1.2*space])
xx = linspace(-1.2*space,1.2*space,100)
yy = linspace(-1.2*space,1.2*space,100)
Y, X = meshgrid(xx,yy)
Z = X+Y


for i in range(len(X)):                                                         # calculate and set values according to function
    for j in range(len(X[i])):        
        Z[i][j]=wert([X[i][j],Y[i][j]])
ax0.plot_wireframe(X, Y, Z, rstride=1, cstride=1,alpha=0.2)
fig.show()                                                                      # display function to be minimized




fak = []                                                                        # prepare upper and lower border for solution parameters
for i in range(2):
    fak.append({"lower":-space,"upper":space})

mypso=PSO(fak,wert,number=25, generations = 20,w=0.7448,c1=0.1699,c2=0.1950)    # create instance of PSO


pointplots = []                                                                 # plot solutions
for par in mypso.swarm:
    pointplots.append((ax0.scatter([par.position[0]],[par.position[1]],[wert(par.position)],marker='o',color='r',s=40,alpha=.8)))



start_time = time.time()

for i in range(50):                                                             # perfom some steps and update plot
    stepstart_time = time.time()
    mypso.step()
    steptime = time.time()-stepstart_time
    plotstart_time = time.time()
    for key,par in enumerate(mypso.swarm):
        pointplots[key]._offsets3d = ([par.position[0]],[par.position[1]],[wert(par.position)])
    fig.canvas.draw()
    # time.sleep(0.25)
    print ("global best: %.10f step time: %.6f draw time: %.3f step number: %i" % (wert(mypso.G), steptime, time.time()-plotstart_time,i))

print ('elapsed time: ' , time.time() - start_time)


ax0.scatter([mypso.G[0]],[mypso.G[1]],[wert(mypso.G)], marker='o', color='g',s=120)   # plot best global solution in greeen


plt.show()