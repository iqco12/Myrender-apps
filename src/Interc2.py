import numpy as np

# (Patm, Tairk, xair, TfumK, xfum)

# Patm = 100600
# Tairk = 278.15
# xair = 0.00378781926200016
# Tfumk = 45 + 273.15
# xfum = 0.0375915157793469


def Interc2(Tairk, Patm, xair, Tfumk, xfum):

    m = (xfum - xair) / (Tfumk - Tairk)

    Ttar0 = 360
    Ttar1 = 360 + 1

    i = 0
    e = 0.00000000001
    err = 9999
    n = 2000

    Ttarn = Ttar1
    Ttarnm1 = Ttar0

    while(err > e) and(i < n):
        xsn = 0.62198 / (Patm * Ttarn ** (8.2) / np.exp(77.345 + 0.0057 * Ttarn - 7235 / Ttarn) - 1)
        Fxn = xsn - (m * (Ttarn - Tairk) + xair)

        # ----------------------------
        xsnm1 = 0.62198 / (Patm * Ttarnm1 ** (8.2) / np.exp(77.345 + 0.0057 * Ttarnm1 - 7235 / Ttarnm1) - 1)
        Fxnm1 = xsnm1 - (m * (Ttarnm1 - Tairk) + xair)

        # -----------------------------
        Ttarn1 = Ttarn - Fxn * (Ttarn - Ttarnm1) / (Fxn - Fxnm1)
        err = np.abs(Ttarn1 - Ttarn)
        Ttarnm1 = Ttarn
        Ttarn = Ttarn1
        i = i + 1

    Interc2 = Ttarn - 273.15

    return Interc2

#print(f" value is {Interc2}")