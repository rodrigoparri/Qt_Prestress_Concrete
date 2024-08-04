# Import necessary libraries
from math import log
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

#from StructEng.Materials.class_Concrete import Concrete
#define the concrete instance
#concrete = Concrete(fck=40)
# Define the component functions Ud_c, Ud_s1, Ud_s2, Ud_p as functions of eps and y
fck = 35
b=500
h=1000
d_s1=60
d_s2=960
d_p=800
E_s=200E3
E_p=195E3
A_s1=500
A_s2=2000
A_p=1000
M = 5
def fctm():
    if 0 < fck <= 50:
        return 0.30 * pow(fck, 2 / 3)
    elif fck > 50:
        return 2.12 * log(1 + (fck + 8) * 0.1)
    else:
        raise ValueError

def Ecm():
    return 22 * pow((fck + 8) * 0.1, 0.3) * 1E3

def A(y):
    return b*y

def Qx(y):
    return b*pow(y,2)/2

def Ix(y):
    return b*pow(y,3)/3

def k(eps,y):
    E_cm = Ecm()
    return (fctm()-eps*E_cm)/(y*E_cm)

def Ud_c(eps, y):
    return Ecm()*(eps*Qx(y) + k(eps,y)*Ix(y))

def Ud_s1(eps, y):
    return (eps + k(eps,y)*d_s1)*E_s*A_s1*d_s1

def Ud_s2(eps,y):
    return (eps + k(eps,y)*d_s2)*E_s*A_s2*d_s2

def Ud_p(eps, y):
    return (eps + k(eps,y)*d_p)*E_p*A_p*d_p

# Define the constant M


# Define the eqM function
def eqM(eps, y):
    return Ud_c(eps, y) + Ud_s1(eps, y) + Ud_s2(eps, y) + Ud_p(eps, y) + M


if __name__ == '__main__':
    # Create a meshgrid for eps and y
    eps = np.linspace(-0.02, 0, 100)
    y = np.linspace(h*.2, h, 100)
    eps, y = np.meshgrid(eps, y)

    # Compute eqM values
    z = eqM(eps, y)

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(eps, y, z, cmap='viridis')

    # Set labels
    ax.set_xlabel('Eps')
    ax.set_ylabel('Y')
    ax.set_zlabel('eqM')

    # Show plot
    plt.show()
