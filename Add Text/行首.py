file_path = input('File Path plz:')

output_lines = []

with open(file_path, 'r') as file:
    for line in file:
        modified_line = "ZGGG_MVA " + line.strip()
        output_lines.append(modified_line)

with open(file_path, 'w') as file:
    file.write('\n'.join(output_lines))

print("Modification complete.")
