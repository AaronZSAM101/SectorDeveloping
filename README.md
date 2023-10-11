# SectorDeveloping
开发EuroScope扇区文件时用到的一些python脚本

## Model
Model文件夹为分为以下三个部分：
- AlgorithmFactory（算法工厂）：存储了用于坐标转换的一些代码或文件
- ExistingFileFactory（现有文件处理工厂）：存储了用于批量读写现有文件的代码（例如：`.prf`,`.asr`）
- TextFactory（文字部分工厂）：存储了用于大量纯文本需要批量添加相同前缀或后缀的代码（例如：MVA）

当前，可用于开发的一些算法有：
1. 坐标转换：

| 可实现功能 | 原格式 | 转换后格式 |
| :---: | :---: | :---: |
| **度** 转 **度分秒** | `XX.XXXXXXXX` | `XX°XX′XX″` |
| **度分秒** 转 **度** | `Nxxxxxx Exxxxxxx` | `XX.XXXXXXX XX.XXXXXXX` |
| **度分秒** 转 **ES** | `Nxxxxxx Exxxxxxx` | `Nxx.xx.xx.xxx Exxx.xx.xx.xxx` |

**注：导出结果可顺最终结果需要而改变格式**

2. 航路的单双数计算（由于部分敏感内容恕不公开）


## Generate SCT
**注：该部分代码已向[中国版权保护中心](https://www.ccopyright.com.cn/)申请了著作权保护，使用时请遵守相关规则**

该部分的脚本主要是读取NavChina数据库，根据需要转换出ES的SCT文件所需的格式。

当前已知bug：`RWY.txt`在最终处理时由于python的系统权限问题，无法将这个文件删除。目前已将删除文件的代码暂时移除，待后续解决。

## Generate MTEPlugin Files
为实现[MTEPlugin-for-EuroScope](https://github.com/KingfuChan/MTEPlugin-for-EuroScope)（下称**MTEP**）的功能而开发的脚本。
### 航路检查器`Generate Route`
该部分脚本通过读取NavChina数据库，与人工维护的**城市名称-机场**对应表`CityMatching.csv`进行对应，再将转换格式后的航路写入文件`Route.csv`，从而生成能够使MTEP读取的航路文件。

`Extract City Name.py`用于读取从数据库读到的城市名称，该部分代码将合并相同的地名名称，然后打印结果以供维护。

## Sector PRF Settings
该部分的脚本主要用于新打包好的扇区进行PRF文件的设置，该部分代码将通过命令行交互的方式，批量在PRF中写入以下内容：
- 扇区包路径
- 登录信息
    - `Real Name` 登录名
    - `Certificate` 登录账号
    - `Password` 登录密码
    - `Rating` 登录等级

将在扇区包中复制自主配置文件
- Topsky
    - `Settings` 设置文件
    - `CPDLCsound` CPDLC的声音
    - `Symbols` 雷达目标样式
    - `SymbolsADS-B` ADS-B目标样式
- Settings
    - `Alias` 简语文件
    - `Symbology` 配色文件
    - `Tag` 标牌文件
    - `General_扇区类型` 设置文件
    - `Lists_扇区类型` 列表文件