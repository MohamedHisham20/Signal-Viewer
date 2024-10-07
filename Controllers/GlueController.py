import numpy as np
from scipy import interpolate
class GlueController:

    def InterPolate_signals(self,
    signal1,
    signal2,
    order,
    overlap,
    signal1_start,
    signal2_start ,
    signal1_size,
    signal2_size):
    
        signal1 = signal1[signal1_start:signal1_start+signal1_size]
        signal2 = signal2[signal2_start:signal2_start+signal2_size]

        signal1_normlized = np.linspace(0,1,signal1) 
        signal2_normlized = np.linspace(0,1,signal2)
        x_values_glued = np.empty()
        if overlap > 0:
            x_values_glued = np.linspace(signal1_normlized[-1],signal2_normlized[0],overlap)
        else: 
            x_values_glued = np.linspace(signal1_normlized[-overlap],signal2_normlized[overlap], -overlap)

        predict1 = interpolate.interp1d(signal1_normlized,signal1,kind=order)
        predict2 = interpolate.interp1d(signal2_normlized,signal2,kind=order)
        signal_glued = predict1(x_values_glued) + predict2(x_values_glued)
        concatenated_signal = np.concatenate((signal1,signal_glued,signal2))

        return concatenated_signal

        

        

        