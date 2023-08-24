# region 定义添加方法和排序方式
def process_lines(line):
    if line:
        words = line.split()
        first_word = words[0]
        sorted_line = ' '.join(sorted(words))
        new_line = f"{sorted_line} {' '.join([first_word] * len(words))}"
        return new_line
    return ""
# endregion

# region 定义splt方法

# endregion



input_file = input("PMDG_airports.dat Location:")
output_lines = []

with open(input_file, "r") as file:
    for line in file:
        processed_line = process_lines(line.strip())
        output_lines.append(processed_line)

output_text = '\n'.join(output_lines)

with open("icao.txt", "w") as output_file:
    output_file.write(output_text)