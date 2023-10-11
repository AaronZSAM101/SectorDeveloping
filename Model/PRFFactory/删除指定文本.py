# 批量删除
print('Delete Script')
import os

search_path = input('Please enter your Sector Path:')
# 方括号内为你要删除的内容
target_strings = [ 
'ASRFastKeys	2	\All\ASRs\FSS.asr'
] 

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith('_TWR.prf'):
            file_path = os.path.join(root, file)
            updated_lines = []
            with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
                lines = f.readlines()
                for line in lines:
                    if all(target_string not in line for target_string in target_strings):
                        updated_lines.append(line)

            with open(file_path, 'w', encoding='gbk', errors='ignore') as f:
                f.writelines(updated_lines)
print('Mission Complete.')