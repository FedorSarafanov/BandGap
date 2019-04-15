import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.backends.backend_pdf import PdfPages
plt.rc('text', usetex = True)
plt.rc('font', size=13, family = 'serif')
# plt.rc('text.latex',unicode=True)
plt.rc('legend', fontsize=14)
plt.rc('text.latex', preamble=r'\usepackage[russian]{babel}')

data = np.loadtxt('data.tsv')
size = data.shape
Et, T, Iob, Ik1, Ik2 = [],[],[],[],[]
# Re = 10 #Ohm
# a = 20  #width
# d = 4  #thickness
# l = 7  #len between 1&2

Re = 10 #Ohm
a = 4  #width
d = 1.4  #thickness
l = 7  #len between 1&2

room_t = 28
k_b = 8.62 *10**(-5) ## eV/K
d_T = 5 # temp error
#Note, that the temperature is added with room temp of 28 degs C!
# print('Shape:',size)
for i in range(0,size[0]):
    Et.append(data[i][0])
    T.append(data[i][1])
    Iob.append(data[i][2])
    Ik1.append(data[i][3])
    Ik2.append(data[i][4])


T = np.array(T) - room_t
weights = np.ones(T.shape)
weights[0:6] = 0
print(weights)
Iob = np.array(Iob)
Ik1 = np.array(Ik1)
Ik2 = np.array(Ik2)
#calcs
T = T + 255 #to kelvin 
Ik = (Ik1+Ik2)/2
Rob =  Ik*Re / Iob 
ro = (a*d / l) * Rob
sigma = 1/ro
k_T = 1000/T 
ln_sigma = np.log(sigma)

err_10 = [2.5,2.5,2.5,2.5,2.5,0.1,0.1,0.1,0.1,0.1,]
err_Iob = 0.1 / Iob # err,%
err_Ik = err_10 / Ik
print(err_Iob) 
print(err_Ik)

#approx
pp = np.polyfit(k_T,ln_sigma,1, w = weights)
print('tan(theta) = ',pp[0])
print('ln(sigma)(0) = ',pp[1])
Wg = -pp[0]*2*k_b*1000
print('Wg = ', Wg,' эВ')
pf = np.poly1d(pp)

plt.plot(k_T,ln_sigma,'-o',color = 'magenta')
plt.grid(which = 'both')
plt.xlabel('$1000 \cdot T^{-1},1000 K^{-1}$')
plt.ylabel('$ln ~\sigma$')

plt.plot(k_T[weights>0],pf(k_T[weights>0]),'k-')
# plt.savefig('graphs/lns.png',dpi=500)

plt.show()