
import numpy as np

def get_psd(I, Q, nfft):
    ## TODO
    data = []
    for i in range(len(I)):
        data.append(I[i] + 1j*Q[i])
    temp = 20*np.log10(np.abs(np.fft.fft(data, n=nfft)))
    mid = int(nfft/2)
    return np.concatenate((temp[mid:],temp[:mid]))