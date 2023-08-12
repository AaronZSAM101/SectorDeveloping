## 对于多跑道机场，再次进行排序
matching_lines = []
target_string= '要查找的机场'
with open('output.txt', 'w', encoding='utf-8') as file:
    for line in file:
        if target_string in line:
            matching_lines.append(line.strip())
            result_text = '\n'.join(matching_lines)
print(result_text)
