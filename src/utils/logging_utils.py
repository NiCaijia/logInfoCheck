import sys
import os

sys.path.append(os.path.dirname(__file__))

from datetime import datetime
import logging

def init_logger(name, log_level='DEBUG', log_type='general'):
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 创建日志文件夹
    log_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', current_date))
    os.makedirs(log_dir, exist_ok=True)

    # 生成日志文件名
    log_name = f"{log_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

    # 拼接日志文件路径
    log_file = os.path.join(log_dir, log_name)

    # 设置日志输出格式
    log_format = "%(asctime)s %(levelname)s %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format)

    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器
    logger.addHandler(file_handler)

    # 创建控制台处理器，并禁用输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)
    console_handler.setFormatter(formatter)

    # 将控制台处理器添加到日志记录器
    logger.addHandler

    return logger

#  调用日志打印函数
#logger = init_logger()
#logger.error("This is an error message.")
#logger.warning("This is a warning message.")
#logger.info("This is an info message.")
#logger.debug("This is a debug message.")