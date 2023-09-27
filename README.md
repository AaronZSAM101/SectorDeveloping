# SectorDeveloping
开发EuroScope扇区文件时用到的一些python脚本

## Add Text
该部分的脚本主要是用于多行文本需要批量在行首/行尾添加文字的情况

例如：MVA的前缀及后缀

## Coordinate Related
该部分的脚本主要是造的一些轮子，用于转换一些坐标。目前已经实现的转换功能有：

| 坐标格式 | 原格式 | 转换后格式
| :---: | :---: | :---: |
| 度格式转度分秒格式 | `XX.XXXXXXXX` | `XX°XX′XX″` |
| 度分秒格式转度格式 | `Nxxxxxx Exxxxxxx` | `XX.XXXXXXX XX.XXXXXXX` |
| 度分秒转ES格式 | `Nxxxxxx Exxxxxxx` | `Nxx.xx.xx.xxx Exxx.xx.xx.xxx` |

**注：导出结果可顺最终结果需要而改变格式**
## Generate SCT
**注：该部分代码已向[中国版权保护中心](https://www.ccopyright.com.cn/)申请了著作权保护，使用时请遵守相关规则**

该部分的脚本主要是读取NavChina数据库，根据需要转换出ES的SCT文件所需的格式

当前已知bug：`RWY.txt`在最终处理时由于python的系统权限问题，无法将这个文件删除

## Sector PRF Settings
该部分的脚本主要用于PRF文件的编写，由于PRF文件众多，故批量写入相同内容还是有所必要的