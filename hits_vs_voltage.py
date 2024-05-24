import numpy as np 
import matplotlib.pyplot as plt

hits    = [7748525, 7188876, 1103238, 658043, 233614, 21307, 2]
voltage = [35     , 30     , 25     , 20    , 15    , 10   , 5]
time    = [10     , 10     , 2      , 2     , 2     , 2    , 2]

hits    = np.array(hits)
voltage = np.array(voltage)
time    = np.array(time)
hits_time = hits/time  

plt.plot(voltage, hits_time, 'o-')
plt.xlabel('Voltage [V]')
plt.ylabel('Hits/Time')
plt.title('Voltage vs Hits')
plt.show()