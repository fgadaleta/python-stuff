import matplotlib.pyplot as plt
import scipy.signal as sps

raw = np.zeros(100)

# create some outliers 
raw[54:57] = 1
raw[23:24] = 1
raw[91] = -1
raw[76:80] = -1    # too big to be outlier



figure(1)
plt.plot(raw, 'bo', label='raw data')

# filter outliers 
filtered = sps.medfilt(raw, kernel_size=7)
plt.plot(filtered, 'r', label='Filtered profile')

axis([0, len(raw), -1.5, 1.5])
plt.legend(loc=3, ncol=2, borderaxespad=0.)
#plt.show()

savefig('plot.png')

