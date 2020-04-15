import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.figure()

y = [ 1, 2, 3, 4, 5 ]
    
psd_image = plt.plot(y, color='r', linewidth=2.0)

plt.savefig('/var/www/html/obrazky/power_spectral_density.png')

# Clear figure
plt.clf()