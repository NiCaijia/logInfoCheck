import sys
import os

sys.path.append(os.path.dirname(__file__))

import argparse

# 获取当前工作目录
path = os.path.abspath('.')

# 创建解析器对象
parser = argparse.ArgumentParser()

# 创建互斥参数组
group = parser.add_mutually_exclusive_group()

# 添加命令行参数
group.add_argument("-f", "--file", dest="filename", default="/Users/nicaijia/ncj-develop/tools/logInfoCheck/test/phone_test",
                    help="需要检查敏感信息的日志文件路径,非压缩包。",
                    metavar="FILE")

group.add_argument("-d", "--dir", dest="directory",
                    help="需要检查敏感信息的日志文件夹路径,非日志文件。",
                    metavar="PATH")

group.add_argument("-z", "--zip", dest="zipname",
                    help="需要检查敏感信息的压缩包日志文件路径，支持.zip .rar 。",
                    metavar="FILE")

parser.add_argument("-l", "--level", dest="level",
                    help="需要检查敏感信息的扫描等级，1级仅检出当前行首条敏感信息（速度快），2级检出当前行所有敏感信息（精度高）。默认使用2级。",
                    metavar="LEVEL", default= "2")

parser.add_argument("-s", "--save", dest="savename",
                    help="日志敏感数据保存文件路径-默认脚本所在路径info_check.txt及info_check.csv",
                    metavar="PATH", default=os.path.join(path, 'info_check'))

parser.add_argument("-gz", "--extract_gz", dest="extract_gz",
                    help="提取和删除gz文件。传入含有gz文件的文件夹，可以实现遍历解压文件夹中的所有gz文件并删除源gz文件。",
                    action='store_true')

parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s version : v0.6.1', help='当前工具版本号。')

# 解析命令行参数
args = parser.parse_args()

# 验证互斥参数
if not args.filename and not args.zipname and not args.directory:
    parser.error("必须指定 -f 或 -z 或 -d 中的一个参数")

# 获取解析结果
filename = args.filename
savename = args.savename
zipname = args.zipname