import math

# 中心点坐标
center_latitude = 40.0  # 以度为单位
center_longitude = 160.0  # 以度为单位

# 跑道头方向（航向）以度为单位
runway_heading = 360

# 跑道头偏移距离（以海里为单位）
runway_distance = 0.9  # 请替换为您的实际距离

# 将跑道头方向转换为弧度
runway_heading_rad = math.radians(runway_heading)

# 计算新坐标
new_latitude = center_latitude + (runway_distance / 60.0) * math.cos(runway_heading_rad)
new_longitude = center_longitude + (runway_distance / 60.0) * math.sin(runway_heading_rad)

# 将坐标转换为度分秒格式
def decimal_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = ((decimal_degrees - degrees) * 60 - minutes) * 60
    return degrees, minutes, seconds

new_latitude_dms = decimal_to_dms(new_latitude)
new_longitude_dms = decimal_to_dms(new_longitude)

# 打印跑道头坐标（度分秒格式）
print("跑道头坐标（度分秒格式）：")
print(f"N{new_latitude_dms[0]}° {new_latitude_dms[1]}' {new_latitude_dms[2]:.2f}\" E{new_longitude_dms[0]}° {new_longitude_dms[1]}' {new_longitude_dms[2]:.2f}\"")