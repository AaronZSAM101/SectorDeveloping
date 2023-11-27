TOPSKY_MAPS = input('Topsky Maps Path:')
with open(TOPSKY_MAPS, 'r', encoding='gbk', errors='ignore') as f:
	lines = list(f)

added_asrdata = False


ground_indices = [i for i, line in enumerate(lines) if 'GROUND' in line]


for index in reversed(ground_indices):
    lines.insert(index + 1, 'ASRDATA:GROUND\n')

with open(TOPSKY_MAPS, 'w', encoding='gbk', errors='ignore') as f:
	f.writelines(lines)

input('Done.')