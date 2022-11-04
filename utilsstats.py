import numpy as np

def autocorr(npa, shift):
    if shift == 0: return 1
    return np.corrcoef(npa[:-shift], npa[shift:])[0, 1]
    
def full_autocorr(npa, shiftmax=10):
    return np.array([autocorr(npa, shift) for shift in range(1, shiftmax)]) #start with 1
    #because autocorr for zero shift is always 1