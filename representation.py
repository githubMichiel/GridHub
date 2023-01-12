import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 50)
y = np.arange(0, 50)

plt.scatter(x, y)
plt.xticks(np.arange(1, 51, step=1))
plt.yticks(np.arange(1, 51, step=1))
plt.grid()
plt.show()
