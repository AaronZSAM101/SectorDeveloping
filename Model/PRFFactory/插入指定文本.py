# 批量写入（在行中操作）
print('Writing Script')
import os

search_path = input('Please enter the root of your sector: ')
target_string = ['Plugins\tPlugin5Display0\tGround Radar display']
new_line = ['Plugins\tPlugin6\t\Data\Stock\Plugins\DiscordEuroscope.dll',
'Plugins\tPlugin6Display0\tGround Radar display',
'Plugins\tPlugin6Display1\tStandard ES radar screen']

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith('.prf'):
            file_path = os.path.join(root, file)
            updated_lines = []
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    updated_lines.append(line)
                    if all(item in line for item in target_string):
                        updated_lines.append(''.join(new_line) + '\n')

            with open(file_path, 'w') as f:
                f.writelines(updated_lines)
print('Mission Complete.')