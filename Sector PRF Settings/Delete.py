# 批量删除
print('Delete Script')
import os

search_path = input('Please enter your Sector Path:')
# 方括号内为你要删除的内容
target_strings = [ 
'LastSession atis_url0 http://127.0.0.1:11452/atis?icao=$atisairportA&dep_rwy=$deprwy($atisairportA)&arr_rwy=$arrrwy($atisairportA)&code=$atiscodeA&apptype=IDM&arr_oprt=I&dep_oprt=I&is_auto=1',
'LastSession atis_url1 http://127.0.0.1:11452/atis?icao=$atisairportB&dep_rwy=$deprwy($atisairportB)&arr_rwy=$arrrwy($atisairportB)&code=$atiscodeB&apptype=IDM&arr_oprt=I&dep_oprt=I&is_auto=1',
'LastSession atis_url2 http://127.0.0.1:11452/atis?icao=$atisairportC&dep_rwy=$deprwy($atisairportC)&arr_rwy=$arrrwy($atisairportC)&code=$atiscodeC&apptype=IDM&arr_oprt=I&dep_oprt=I&is_auto=1',
'LastSession atis_url3 http://127.0.0.1:11452/atis?icao=$atisairportD&dep_rwy=$deprwy($atisairportD)&arr_rwy=$arrrwy($atisairportD)&code=$atiscodeD&apptype=IDM&arr_oprt=I&dep_oprt=I&is_auto=1'
] 

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith('.prf'):
            file_path = os.path.join(root, file)
            updated_lines = []
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if all(target_string not in line for target_string in target_strings):
                        updated_lines.append(line)

            with open(file_path, 'w') as f:
                f.writelines(updated_lines)
print('Mission Complete.')