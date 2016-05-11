import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize.minpack import curve_fit
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D

# Path to the measurment images
path = 'iot_data/'
# Read data, sizes of input
sizes = ['A0.25/', 'A0.5/', 'A1/', 'A1.5/']

aggregate = True
if aggregate ==True:
    for size in sizes:    
        with open(path+size+'data.csv','w') as outfile:
            outfile.write('distance(ft),pixels\n')
            for i in range(4,14):
                with open(path+size+'{}ft.txt'.format(str(i)),'r') as infile:
                    outfile.write("{},{}\n".format(str(i),infile.readline()))
                    

# Read data
csv_file = pandas.read_csv(path+'A0.25/data.csv')
y1 = np.array(csv_file['distance(ft)'])
x1 = np.array(csv_file['pixels'])

csv_file = pandas.read_csv(path+'A0.5/data.csv')
y2 = np.array(csv_file['distance(ft)'])
x2= np.array(csv_file['pixels'])

csv_file = pandas.read_csv(path+'A1/data.csv')
y3 = np.array(csv_file['distance(ft)'])
x3= np.array(csv_file['pixels'])

csv_file = pandas.read_csv(path+'A1.5/data.csv')
y4 = np.array(csv_file['distance(ft)'])
x4= np.array(csv_file['pixels'])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
z1 = np.ones(x1.shape)




# plotting first figure
for i in range(len(x1)):
  ax.plot([x1[i], x1[i]], [z1[i]*0.25, z1[i]*0.25], [0, y1[i]], 
          '-o', linewidth=2, color='g', alpha=.5)    
  ax.plot([x2[i], x2[i]], [z1[i]*0.5, z1[i]*0.5], [0, y2[i]], 
          '-o', linewidth=2, color='y', alpha=.5)    
  ax.plot([x3[i], x3[i]], [z1[i], z1[i]], [0, y3[i]], 
          '-o', linewidth=2, color='b', alpha=.5)
  ax.plot([x4[i], x4[i]], [z1[i]*1.5, z1[i]*1.5], [0, y4[i]], 
          '-o', linewidth=2, color='r', alpha=.5)
    
# Reshaping data      
Data = np.concatenate((x1.reshape(len(x1),1),x2.reshape(len(x1),1),x3.reshape(len(x1),1),x4.reshape(len(x1),1)),axis=1)  
fig = plt.figure() 
ax = Axes3D(fig)
z2 = np.array([0.25, 0.5, 1, 1.5])

# Plotting second figure
for j in range (4,4+len(x1)):
    for i in range(0,4):
      ax.plot([j, j], [z2[i], z2[i]], [0, Data[j-4,i]],
              '-*', color='r', linewidth=2, alpha=.5)
ax.set_xlabel('Distance [ft]')
ax.set_ylabel('Real area')
ax.set_zlabel('Pixel area')

# Plotting mesh figur
fig2 = plt.figure()
X = np.ones((len(x1),4))*np.arange(4,len(x1)+4).reshape(len(x1),1)
Y = np.ones((len(x1),4))*z2.T
ax2 = Axes3D(fig2)
ax2.plot_wireframe(X,Y,Data)
ax2.set_xlabel('Distance [ft]')
ax2.set_ylabel('Real area')
ax2.set_zlabel('Pixel area')

'''
for j in range (0,1):#len(x1)):
    fig = plt.figure()
    plt.plot(Y[j,:], Data[j,:], 'o-')
'''




    

# Interpolate new points
Avg = np.sum(Data, axis=1)/3.25
w = 0.18 # arbitrary area (% of original)
x0 = w*Avg.reshape(len(x1),1)
x = x0.reshape(len(x1))
smoothx = np.linspace(x[0], x[-1], 500)
fig3 = plt.figure()



y = y1
# Predict curve
guess_a, guess_b, guess_c = 16, -0.0005, 4
guess = [guess_a, guess_b, guess_c]
#
exp_decay = lambda x, A, t, y0: A * np.exp(x * t) + y0
params, cov = curve_fit(exp_decay, x, y, p0=guess)
A, t, y0 = params
print "A = %s\nt = %s\ny0 = %s\n" % (A, t, y0)
best_fit = lambda x: A * np.exp(t * x) + y0

# Plot
plt.stem(x, y, 'b')
plt.plot(smoothx, best_fit(smoothx), 'r-')
plt.legend(('fit', 'measurement'))
plt.xlabel('Area [pixel]')
plt.ylabel('Distance [feet]')
plt.title('Area vs Distance')
plt.show()

# Save parameters of curve
np.save('params.npy', [A,t,y0])


