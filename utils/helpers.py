# General utility functions

import numpy as np

def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2*np.pi) * wid)) * np.exp(-(x-cen)**2 / (2*wid**2))

def lorentzian(x, amp, cen, wid):
    """1-d lorentzian: lorentzian(x, amp, cen, wid)"""
    # Using FWHM definition for 'wid'
    return (amp / np.pi) * (wid / 2) / ((x - cen)**2 + (wid / 2)**2)

# Add other helpers: baseline correction, unit conversions, etc.
print("Utility functions loaded (placeholder)")