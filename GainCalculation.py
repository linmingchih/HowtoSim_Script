import math

Max_U=132.443e-3
Radiated_Power=949.313e-3
Accepted_Power=935.337e-3
Incidenet_Power=1
System_Power=2

directivity=10*math.log10(Max_U*4*math.pi/Radiated_Power)
print(f'directivity:{directivity:.3f}(dB)')
peak_gain=10*math.log10(Max_U*4*math.pi/Accepted_Power)
print(f'peak_gain:{peak_gain:.3f}(dB)')
realized_gain=10*math.log10(Max_U*4*math.pi/Incidenet_Power)
print(f'realized_gain:{realized_gain:.3f}(dB)')
peak_system_gain=10*math.log10(Max_U*4*math.pi/System_Power)
print(f'peak_system_gain:{peak_system_gain:.3f}(dB)')
