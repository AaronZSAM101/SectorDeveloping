input_filename = input('icao.txt address:')
output_filename = "output.txt"

with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
    for line in input_file:
        parts = line.strip().split()
        if len(parts) == 2:
            icao = parts[0]
            coordinates = parts[1].split("-")
            if len(coordinates) == 2:
                latitude = coordinates[0]
                longitude = coordinates[1]
                output_line = f"{icao}\t{latitude}\t{longitude}\n"
                output_file.write(output_line)

print("转换完成并已保存到output.txt中")