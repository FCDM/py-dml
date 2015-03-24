import scipy.special

airyAi = lambda t : scipy.special.airy(t)[0]
airyBi = lambda t : scipy.special.airy(t)[2]

airyAiDerivative = lambda t : scipy.special.airy(t)[1]
airyBiDerivative = lambda t : scipy.special.airy(t)[3]

airyAiExp = lambda t : scipy.special.airye(t)[0]
airyBiExp = lambda t : scipy.special.airye(t)[2]

airyAiExpDerivative = lambda t : scipy.special.airye(t)[1]
airyBiExpDerivative = lambda t : scipy.special.airye(t)[3]

ellipticComplete1 = scipy.special.ellipk
ellipticComplete2 = scipy.special.ellipe

ellipticIncomplete1 = scipy.special.ellipkinc
ellipticIncomplete2 = scipy.special.ellipeinc

besselJ = scipy.special.jn
besselY = scipy.special.yn
besselK = scipy.special.kn
besselI = scipy.special.iv

besselJExp = scipy.special.jne
besselYExp = scipy.special.yne
besselKExp = scipy.special.kne
besselIExp = scipy.special.ive