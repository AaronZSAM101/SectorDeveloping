def convert_coordinates(coord_str):
    degree = int(coord_str[:3])
    minute = int(coord_str[3:5])
    seconds = float(coord_str[5:])
    converted_seconds = round((seconds * 60), 3)
    return f"{degree:03d}.{minute:02d}.{converted_seconds:06.3f}"

