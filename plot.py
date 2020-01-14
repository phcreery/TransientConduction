import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate(X,Y,Tlim,Tcn,xss=1,yss=1):

	xlabel = "time (*"+str(round(xss,2))+"s)"
	ylabel = "length (*"+str(round(yss,2))+"m)"
	zlabel = " temp (K)"

	fig = plt.figure(1)
	ax = plt.axes(projection='3d')
	ax.invert_xaxis()
	#ax.contour3D(X, Y, T, 100, cmap='viridis')	#binary, viridis
	ax.plot_surface(X, Y, Tlim, rstride=1, cstride=1, cmap='plasma', edgecolor='none')
	#ax.plot_wireframe(X, Y, T, color='black')

	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_zlabel(zlabel)
	ax.set_title('Forward Euler')
	ax.view_init(40, 125)

	plt.savefig('imgs/ForwareEuler.png')

	fig = plt.figure(2)
	ax = plt.axes(projection='3d')
	ax.invert_xaxis()
	ax.plot_surface(X, Y, Tcn, rstride=1, cstride=1, cmap='plasma', edgecolor='none')

	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_zlabel(zlabel)
	ax.set_title('Crank Nicholson')
	ax.view_init(40, 125)

	plt.savefig('imgs/CrankNicholson.png')


	fig = plt.figure(3, figsize=plt.figaspect(0.4))

	ax = fig.add_subplot(1, 2, 1, projection='3d')
	#plt.subplot(121)
	#ax = plt.axes(projection='3d')
	ax.invert_xaxis()
	ax.plot_surface(X, Y, Tlim, rstride=1, cstride=1, cmap='plasma', edgecolor='none')
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_zlabel(zlabel)
	ax.set_title('Forward Euler')
	ax.view_init(40, 125)

	ax1 = fig.add_subplot(1, 2, 2, projection='3d')
	#plt.subplot(122)
	#ax1 = plt.axes(projection='3d')
	ax1.invert_xaxis()
	ax1.plot_surface(X, Y, Tcn, rstride=1, cstride=1, cmap='plasma', edgecolor='none')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel)
	ax1.set_zlabel(zlabel)
	ax1.set_title('Crank Nicholson')
	ax1.view_init(40, 125)

	plt.savefig('imgs/Comparison.png')