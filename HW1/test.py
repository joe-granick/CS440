import numpy as np
import matplotlib.pyplot as plt

a= np.random.normal(size= 1000)
b= a*3 + np.random.normal(size= 1000)

plt.hist2d(a, b,(50,50),cmap= plt.cm.jet)
plt.colorbar()
plt.show()