import os
import re
import shutil
# 定义扇区路径
Sector_PATH=input('请输入扇区路径：')
# 定义个人信息
realname=input('请输入登陆时显示的名字：')
cid=input('请输入你的VATSIM CID：')
password=input('请输入你的密码：')
print('等级：S1-"1" S2-"2" S3-"3" C1-"4" C3-"6" I1-"7" I3-"9" SUP-"10"')
rating=input('请输入你的等级：')
# 对扇区文件进行操作
## 写入个人信息
text_to_append = f'''
LastSession\trealname\t{realname}
LastSession\tcertificate\t{cid}
LastSession\tpassword\t{password}
LastSession\trating\t{rating}
'''
file_list = [file for file in os.listdir(Sector_PATH) if file.endswith('.prf')]
## 遍历文件夹中的PRF文件
for file_name in file_list:
    file_path = os.path.join(Sector_PATH, file_name)
    
    try:
        ### 在文件末尾追加文本内容
        with open(file_path, 'a') as file:
            file.write(text_to_append)
    ### 如失败，显示报错
    except Exception as e:
        print(f"个人信息在添加至: {file_name}时出错，报错信息: {str(e)}")

print('个人信息修改完成！')

## 修改Topsky的CPDLC Logon Code
TopskyPath=input('请输入Topsky插件的目录：')
logon_code=input('请输入你的CPDLC Logon Code：')
with open(os.path.join(TopskyPath, "TopSkyCPDLChoppieCode.txt"), 'a') as f:
    f.write(f"{logon_code}")
print("CPDLC Logon Code 修改完成！")
## 复制并自定义个人的配置文件（一般为Symbology，Tag，Alias）
print('接下来开始设置你的个人配置文件，请先确保你的Alias.txt, Symbology.txt, Tag.txt已经放到同一个文件夹中。')
Personal_Setting_Files=input('如果你没有个人配置文件，请按Ctrl+C结束设置；否则，请输入你的个人配置文件的路径：')
### 删除Telephonics
re.remove(os.path.join(Sector_PATH, 'All', 'Plugins', 'Telephonics.dll' ))
### 复制Plugins下文件
shutil.copyfile(os.path.join(Personal_Setting_Files, 'MTEPlugin.dll'),os.path.join(Sector_PATH, 'All', 'Plugins', 'MTEPlugin.dll'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Route.csv'),os.path.join(Sector_PATH, 'All', 'Plugins', 'Route.csv'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'DiscordEuroscope.dll'),os.path.join(Sector_PATH, 'All', 'Plugins', 'DiscordEuroscope.dll'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'DiscordEuroscope_RadioCallsigns.txt'),os.path.join(Sector_PATH, 'All', 'Plugins', 'DiscordEuroscope_RadioCallsigns.txt'))
### 复制Topsky下文件
shutil.copyfile(os.path.join(Personal_Setting_Files, 'TopSkySettings.txt'),os.path.join(Sector_PATH, 'All', 'Plugins', 'TopSky', 'TopSkySettings.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'TopSkyCPDLCsound.wav'),os.path.join(Sector_PATH, 'All', 'Plugins', 'TopSky', 'TopSkyCPDLCsound.wav'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'TopskySymbols.txt'),os.path.join(Sector_PATH, 'All', 'Plugins', 'TopSky', 'TopskySymbols.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'TopSkySymbolsADS-B.txt'),os.path.join(Sector_PATH, 'All', 'Plugins', 'TopSky', 'TopSkySymbolsADS-B.txt'))
### 复制Settings下文件
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Alias.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'Alias.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Symbology.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'Symbology.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Tag.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'Tag.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'General_ACC.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'General_ACC.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'General_FSS.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'General_FSS.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'General_TWR.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'General_TWR.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Lists_ACC.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'Lists_ACC.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Lists_FSS.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'Lists_FSS.txt'))
shutil.copyfile(os.path.join(Personal_Setting_Files, 'Lists_TWR.txt'),os.path.join(Sector_PATH, 'All', 'Settings', 'Lists_TWR.txt'))
input("扇区配置完成，按回车键退出！")