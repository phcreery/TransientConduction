"""
Author: Peyton Creery

Simple script to calculate and display 1d transient conduction through a plane wall via 2 methods
"""

import math
import numpy as np
import plot

k = 0.05	# W/m*K			Thermal Conductivity of Material
p = 96		# kg/m^3		Density of Material
cp = 1130	# J/kg*K		Specific Heat of Material
h0 = 5.719	# W/m^2*K		

Tinf = 72	# F				Surrounding Temperature
Qin = 60	# W				Energy tramsitted into plane

sigma = 5.6704 * (10**(-8))	# W/m^2*K^4	Stephan Boltzman's Constant

Ai = 0.511	# m^2			Inner Wall Area
Ao = 0.712	# m^2			Outer Wall Area
Aavg = (Ai + Ao)/2
A = Aavg

L = 1			# in		Of cross-section
dx = 0.1		# in		distance between calculation points
xscale = 1/dx	# for matrix allocation

time = 440		# s			Of analysis
dt = 5			# s			interval between calculations
tscale = 1/dt	# for matrix allocation


def in2m(inches):
	return inches/39.37

def m2in(m):
	return m*39.37

def F2K(f):
	return (f - 32) * 5/9 + 273.15


def initMatrix(row,col,val):
	row = int(row)+1
	col = int(col)+1
	#matrix = [[val for x in range(col)] for y in range(row)] 
	#matrix = np.matrix(matrix)
	matrix = np.ones((row, col))
	matrix = matrix.dot(val)
	return matrix

L = in2m(L)
dx = in2m(dx)
xscale = 1/dx	# in2m(xscale)
Tinf = F2K(Tinf)


Li = int(L*xscale)		# L scale for matrix indexing
ti = int(time*tscale)	# t scaled for t indexing
y = np.arange(0,Li+1)
x = np.arange(0,ti+1)
X, Y = np.meshgrid(x, y)

print()
print("x steps: ", int(L/dx) )
print("x range (m): ", 0, dx, L)
print("x range index: ", 0, int(dx*xscale), Li)
print("x index stepsize (in): ", round(m2in(dx),2) )


print()
print("time steps: ", int(time/dt))
print("time range: ", 0, dt, time)
print("time range index: ", 0, int(dt*tscale), ti)
print("time index stepsize (s): ", round(dt,2) )
print()

diffusionNumber = (k*dt)/(cp*p*(dx**2))
print("Diffusion Number: {}".format(diffusionNumber))
if diffusionNumber > 0.5:
	print("With a diffusion number greater than 0.5, the forward euler method of estimation may be unstable.")
print()
print()


# Forward Euler
if True:

	T = initMatrix(Li,ti,Tinf)

	for t in range(0,ti):
		Qout = sigma*A* ( T[Li,t]**4-Tinf**4 ) + h0*A * ( T[Li,t]-Tinf )
		T[0,t+1] = T[0,t] + diffusionNumber * (T[1,t] - T[0,t] + Qin*(dx)/(k*Ai))
		T[Li,t+1] = T[Li,t] + diffusionNumber * (T[Li-1,t] - T[Li,t] - Qout*((dx)/(k*A)))

		for x in range(int(dx*xscale), int((L-dx)*xscale)+1, int(dx*xscale)):
			T[x,t+1] = T[x,t] + diffusionNumber * (T[x-1,t] -2*T[x,t] + T[x+1,t])


	Tlim = T



def XXinit(type, n, val):
	n = int(n-1)
	matrix = np.ones((n, n))
	if type == "BB":
		val = -val
	for i in range(n):
		for j in range(n):
			if i==j:
				matrix[i][j] = 1+val
			elif (i == j+1) or (i == j-1):
				matrix[i][j] = -0.5*val
			else:
				matrix[i][j] = 0
	#print(matrix)
	return matrix



# CrankNicholson Method
if True:
	
	T = initMatrix(Li,ti,Tinf)
	AA = XXinit("AA", Li, diffusionNumber)
	BB = XXinit("BB", Li, diffusionNumber)
	bc = np.zeros((Li-1))	# degrees K
	print("T:  ", T.shape)
	print("AA,BB: ", AA.shape, BB.shape)
	print("bc: ", bc, bc.shape)

	for t in range(0,ti):
		Qout = sigma*A* ( T[Li,t]**4-Tinf**4 ) + h0*A * ( T[Li,t]-Tinf )
		T[0,t+1] = T[0,t] + diffusionNumber * (T[1,t] - T[0,t] + Qin*(dx)/(k*Ai))
		T[Li,t+1] = T[Li,t] + diffusionNumber * (T[Li-1,t] - T[Li,t] - Qout*((dx)/(k*A)))
		
		bc[0] = T[0,t+1] * diffusionNumber
		bc[Li-2] = T[Li,t+1] * diffusionNumber

		Tsub = np.linalg.solve(AA, np.add(np.dot(BB,T[1:Li,t]), bc) )

		T[:,t+1] = np.concatenate(( np.array([T[0,t+1]]), Tsub, np.array([T[Li,t+1]]) ))

	#print(T)
	Tcn = T

plot.generate( X, Y, Tlim, Tcn, xss=dt, yss=m2in(dx) )