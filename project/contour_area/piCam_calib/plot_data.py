import pandas
import matplotlib.pyplot as plt

csv_file = pandas.read_csv('data.csv')
y = csv_file['distance(ft)']
x = csv_file['pixels']

plt.stem(x, y)
plt.xlabel('pixels')
plt.ylabel('feet')
plt.title('Area vs Distance')
plt.show()