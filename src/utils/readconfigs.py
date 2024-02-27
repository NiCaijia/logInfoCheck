import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.utils import logging_utils
import configparser

class Config(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None,strict=False)
 
    def optionxform(self, optionstr):
        return optionstr

logger = logging_utils.init_logger("log_logger")

def readConfigs():
    try:
        #proDir = os.path.split(os.path.realpath(__file__))[0]
        configPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "configs.ini")
        path = os.path.abspath(configPath)

        data = Config()
        regex_conf = configparser.RawConfigParser(strict=False)
        data.read(path,encoding='utf-8')
        regex_conf.read(path,encoding='utf-8')

        logger.info(f'正在读取配置文件: {configPath}')  # 记录日志：打印配置文件路径
        
        c30 = data.items("C3")
        c20= data.items("C2")
        c31 = regex_conf.items("C3")
        c21= regex_conf.items("C2")
        r30 = [] #C3类数据关键词
        r31 = [] #C3类数据正则表达式
        r20 = [] #C2类数据关键词
        r21 = [] #C2类数据正则表达式

        for c in c30:
            if c[1] == '':
                r30.append(c[0])
            else:
                r31

        for c in c20:
            if c[1] == '':
                r20.append(c[0])
            else:
                r21

        for c in c31:
            if c[1] == '':
                r30
            else:
                r31.append(c[1])

        for c in c21:
            if c[1] == '':
                r20
            else:
                r21.append(c[1])

        return(r30,r31,r20,r21) #目前正则表达式是写在程序中的，没有从配置文件获取，故只需要使用r30、r20两个参数即可。
    except configparser.ParsingError as e:
        str_print = f'【Error】configs.ini配置文件读取错误。配置文件默认会处理等号（=）或冒号（:）作为分隔符，如果你需要在键（key）或值（value）中包含特殊字符（包括等号和冒号），你需要将它们用引号包围起来。eg:"key=1" = 或":key2:" = '
        print("\033[0;31;40m" + str_print + "\033[0m")
        logger.error(f'【Error】configs.ini配置文件读取错误。', exc_info=True)