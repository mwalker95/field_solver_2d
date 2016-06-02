import numpy as np

a = np.array([1,2,3,4])

f = open('filename.txt', 'w+')	
np.savetxt('filename.txt', a)



