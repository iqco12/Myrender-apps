import numpy as np

# Tairk = 278.15
# Tfumk = 45 + 273.15

def Psat(Tk):
    Psat = np.exp(77.345+0.0057*Tk-7235/Tk)/Tk**8.2
    return Psat




# Psat = np.exp(77.345+0.0057*Tairk-7235/Tairk)/Tairk**8.2

#print(f"the value is {Psat} Pa")