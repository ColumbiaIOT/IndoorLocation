import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize.minpack import curve_fit

# Read data
csv_file = pandas.read_csv('data.csv')
y = np.array(csv_file['distance(ft)'])
x = np.array(csv_file['pixels'])

smoothx = np.linspace(x[0], x[-1], 200)

# Predict curve
guess_a, guess_b, guess_c = 16, -0.005, 4
guess = [guess_a, guess_b, guess_c]

exp_decay = lambda x, A, t, y0: A * np.exp(x * t) + y0
params, cov = curve_fit(exp_decay, x, y, p0=guess)
A, t, y0 = params
print "A = %s\nt = %s\ny0 = %s\n" % (A, t, y0)
best_fit = lambda x: A * np.exp(t * x) + y0

# Plot
plt.stem(x, y)
plt.plot(smoothx, best_fit(smoothx), 'r-')
plt.xlabel('pixels')
plt.ylabel('feet')
plt.title('Area vs Distance')
plt.show()