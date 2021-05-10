import numpy as np
import matplotlib.pyplot as plt
import math
   
Y = np.loadtxt('statistic_nomad206.0.txt')
A = Y[:,0]
B = Y[:,1]
C = Y[:,2]
D = Y[:,3]
E = Y[:,4]
F = Y[:,5]
G = Y[:,6] #mase od naprezanja J
H = Y[:,7]# mase od naprezanja I
I = Y[:,8]
J = Y[:,9]



#GOAL FUNCTION CONVERGENCE
plt.figure()
for i, ip in enumerate(H):
    if math.isnan(float(ip)):
        H[i] = H[i-1]
    H_min = [np.min(H[:i]) for i in range(np.size(H))[1:]]
    fig1 = plt.plot(H_min, 'g')
    plt.title('Goal function convergence')
    plt.ylabel('Goal function value')
    plt.xlabel('Number of iterations')
plt.grid()

#MASS CONVERGENCE FOR CASE 1
plt.figure()
fig2 = plt.plot(A, H, 'g')
plt.title('Mass convergence')
plt.grid()
plt.xlabel('Number of iterations')
plt.ylabel('Mass [Kg]')

#STRESS CONVERGENCE FOR 1
plt.figure()
fig3 = plt.plot(A, I, 'g')
plt.title('Stress convergence for case 1')
plt.grid()
plt.xlabel('Number of iterations')
plt.ylabel('Stress [MPa]')

#STRESS CONVERGENCE FOR 2
plt.figure()
fig4 = plt.plot(A, J, 'g')
plt.title('Stress convergence for case 2')
plt.grid()
plt.xlabel('Number of iterations')
plt.ylabel('Stress [MPa]')

#CRANE WIDTH CONVERGENCE ( a - varijabla)
plt.figure()
fig5 = plt.plot(A, B, 'g')
plt.title('Crane width convergence ( a - variable )')
plt.grid()
plt.xlabel('Number of iterations')
plt.ylabel('Crane width - a [m]')

#BEAM PROFILE CONVERGENCE
plt.figure()
fig6 = plt.plot(A, C, 'g', label= 'Visina I - profila') # h - varijabla
fig7 = plt.plot(A, D, color='purple', label='Širina I - profila') # b - varijabla
fig8 = plt.plot(A, E, 'r', label='Debljina I - profila gore') # t - varijabla
fig10 = plt.plot(A, F, 'b', label='Radijus kružnog presjeka') # r - varijabla
plt.title('Beam profile dimension convergence')
plt.legend()
plt.grid()
plt.xlabel('Number of iterations')
plt.ylabel('Beam profile dimensions [ m ]')



plt.show()

