def convert_coordinates(coord_str):
    degree = int(coord_str[:3])
    minute = int(coord_str[3:5])
    seconds = float(coord_str[5:])
    converted_seconds = round((seconds * 60), 3)
    return f"{degree:03d}.{minute:02d}.{converted_seconds:06.3f}"

input_filename = "output.txt"
output_filename = "rwy.txt"

with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []

        for part in parts:
            if part.startswith("N") or part.startswith("E"):
                converted_part = convert_coordinates(part[1:])
                converted_parts.append(part[0] + converted_part)
            else:
                converted_parts.append(part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")

print("Conversion complete. Output saved in", output_filename)