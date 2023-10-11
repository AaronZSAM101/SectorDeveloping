import os
path = 'E:\Flight Simulation\ATC\EuroScope Data\Sector\VATPRC Personal Sector\Data\All\ASRs'

filenames = os.listdir(path)

f = open('E:\Flight Simulation\ATC\EuroScope Data\Sector\VATPRC Personal Sector\Data\ASR.txt', 'w')
for name in filenames:
    name = name.split('.')[0]
    f.write(name + '\n')
f.close
print('done.')