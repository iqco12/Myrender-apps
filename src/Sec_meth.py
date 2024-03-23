import numpy as np

# Tair = 278.15
# Patm = 100600
# RH = 70

def sec_meth(Tair, RH, Patm):
    #Tair = Tair + 273.15

    Psair = np.exp(77.345 + 0.0057 * Tair - 7235 / Tair) / (Tair ** (8.2))
    Pw = RH / 100 * Psair
    xair = 0.62198 * Pw / (Patm - Pw)


    Ttar0 = Tair + 1
    Ttar1 = Tair + 20

    i = 0
    e = 0.00000000001
    err = 9999
    n = 2000
    Ttarn = Ttar1
    Ttarnm1 = Ttar0

    while(err > e) and (i < n):
        #Ptarn = Exp(77.345 + 0.0057 * Ttarn - 7235 / Ttarn) / (Ttarn ^ (8.2))

        Num = -0.62198 * Patm * (8.2 * Ttarn ** (7.2) - Ttarn ** (8.2) * (0.0057 + 7235 / Ttarn ** (2)))
        Den = (Patm * Ttarn ** (8.2) / np.exp(77.345 + 0.0057 * Ttarn - 7235 / Ttarn) - 1) ** (2) * np.exp(
            77.345 + 0.0057 * Ttarn - 7235 / Ttarn)
        Dern = Num / Den

        xsn = 0.62198 / (Patm * Ttarn ** (8.2) / np.exp(77.345 + 0.0057 * Ttarn - 7235 / Ttarn) - 1)

        Fxn = Dern * (Ttarn - Tair) + xair - xsn

        # ----------------------------

        #Ptarnm1 = Exp(77.345 + 0.0057 * Ttarnm1 - 7235 / Ttarnm1) / (Ttarnm1 ^ (8.2))

        Numm1 = -0.62198 * Patm * (8.2 * Ttarnm1 ** (7.2) - Ttarnm1 ** (8.2) * (0.0057 + 7235 / Ttarnm1 ** (2)))
        Denm1 = (Patm * Ttarnm1 ** (8.2) / np.exp(77.345 + 0.0057 * Ttarnm1 - 7235 / Ttarnm1) - 1) ** (2) * np.exp(
            77.345 + 0.0057 * Ttarnm1 - 7235 / Ttarnm1)
        Dernm1 = Numm1 / Denm1

        xsnm1 = 0.62198 / (Patm * Ttarnm1 ** (8.2) / np.exp(77.345 + 0.0057 * Ttarnm1 - 7235 / Ttarnm1) - 1)

        Fxnm1 = Dernm1 * (Ttarnm1 - Tair) + xair - xsnm1

        # -----------------------------

        Ttarn1 = Ttarn - Fxn * (Ttarn - Ttarnm1) / (Fxn - Fxnm1)

        err = np.abs(Ttarn1 - Ttarn)
        Ttarnm1 = Ttarn
        Ttarn = Ttarn1
        i = i + 1

    Ttar = Ttarn

    Num = -0.62198 * Patm * (8.2 * Ttar ** (7.2) - Ttar ** (8.2) * (0.0057 + 7235 / Ttar ** (2)))
    Den = ((Patm * Ttar ** (8.2) / np.exp(77.345 + 0.0057 * Ttar - 7235 / Ttar) - 1) ** (2) *
           np.exp(77.345 + 0.0057 * Ttar - 7235 / Ttar))
    Dern = Num / Den

    Der = Dern

    return Der

# result = sec_meth(Tair, Patm, RH)
# print(result)

